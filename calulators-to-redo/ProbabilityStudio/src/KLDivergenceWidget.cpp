#include "KLDivergenceWidget.h"
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QFormLayout>
#include <QFileDialog>
#include <QTextStream>
#include <cmath>
#include <numeric>
#include <algorithm>

KLDivergenceWidget::KLDivergenceWidget(QWidget *parent)
    : QWidget(parent)
    , chart(new QChart())
    , chartView(new QChartView(chart))
{
    setupUI();
    updateVisualization();
}

KLDivergenceWidget::~KLDivergenceWidget()
{
}

void KLDivergenceWidget::setupUI()
{
    QVBoxLayout *mainLayout = new QVBoxLayout(this);
    
    // Title
    QLabel *titleLabel = new QLabel("<h2>Kullback-Leibler Divergence Visualizer</h2>");
    mainLayout->addWidget(titleLabel);
    
    // Controls and chart layout
    QHBoxLayout *contentLayout = new QHBoxLayout();
    
    // Left side: Controls
    QVBoxLayout *controlsLayout = new QVBoxLayout();
    
    // Distribution P controls
    distPGroup = new QGroupBox("Distribution P (Reference)");
    QFormLayout *pLayout = new QFormLayout(distPGroup);
    
    distPSelector = new QComboBox();
    distPSelector->addItem("Normal (Gaussian)");
    distPSelector->addItem("Exponential");
    distPSelector->addItem("Uniform");
    distPSelector->addItem("Beta");
    connect(distPSelector, QOverload<int>::of(&QComboBox::currentIndexChanged),
            this, &KLDivergenceWidget::onDistributionTypeChanged);
    pLayout->addRow("Type:", distPSelector);
    
    pParam1Label = new QLabel("Mean (μ):");
    pParam1Spin = new QDoubleSpinBox();
    pParam1Spin->setRange(-10, 10);
    pParam1Spin->setValue(0);
    pParam1Spin->setSingleStep(0.1);
    pLayout->addRow(pParam1Label, pParam1Spin);
    
    pParam2Label = new QLabel("Std Dev (σ):");
    pParam2Spin = new QDoubleSpinBox();
    pParam2Spin->setRange(0.1, 10);
    pParam2Spin->setValue(1.0);
    pParam2Spin->setSingleStep(0.1);
    pLayout->addRow(pParam2Label, pParam2Spin);
    
    connect(pParam1Spin, QOverload<double>::of(&QDoubleSpinBox::valueChanged),
            this, &KLDivergenceWidget::updateVisualization);
    connect(pParam2Spin, QOverload<double>::of(&QDoubleSpinBox::valueChanged),
            this, &KLDivergenceWidget::updateVisualization);
    
    controlsLayout->addWidget(distPGroup);
    
    // Distribution Q controls
    distQGroup = new QGroupBox("Distribution Q (Approximation)");
    QFormLayout *qLayout = new QFormLayout(distQGroup);
    
    distQSelector = new QComboBox();
    distQSelector->addItem("Normal (Gaussian)");
    distQSelector->addItem("Exponential");
    distQSelector->addItem("Uniform");
    distQSelector->addItem("Beta");
    connect(distQSelector, QOverload<int>::of(&QComboBox::currentIndexChanged),
            this, &KLDivergenceWidget::onDistributionTypeChanged);
    qLayout->addRow("Type:", distQSelector);
    
    qParam1Label = new QLabel("Mean (μ):");
    qParam1Spin = new QDoubleSpinBox();
    qParam1Spin->setRange(-10, 10);
    qParam1Spin->setValue(0.5);
    qParam1Spin->setSingleStep(0.1);
    qLayout->addRow(qParam1Label, qParam1Spin);
    
    qParam2Label = new QLabel("Std Dev (σ):");
    qParam2Spin = new QDoubleSpinBox();
    qParam2Spin->setRange(0.1, 10);
    qParam2Spin->setValue(1.5);
    qParam2Spin->setSingleStep(0.1);
    qLayout->addRow(qParam2Label, qParam2Spin);
    
    connect(qParam1Spin, QOverload<double>::of(&QDoubleSpinBox::valueChanged),
            this, &KLDivergenceWidget::updateVisualization);
    connect(qParam2Spin, QOverload<double>::of(&QDoubleSpinBox::valueChanged),
            this, &KLDivergenceWidget::updateVisualization);
    
    controlsLayout->addWidget(distQGroup);
    
    // KL Divergence results
    QGroupBox *resultsGroup = new QGroupBox("KL Divergence Results");
    QFormLayout *resultsLayout = new QFormLayout(resultsGroup);
    
    klPQValue = new QLabel("0.000");
    QFont boldFont = klPQValue->font();
    boldFont.setPointSize(12);
    boldFont.setBold(true);
    klPQValue->setFont(boldFont);
    resultsLayout->addRow("D<sub>KL</sub>(P||Q):", klPQValue);
    
    klQPValue = new QLabel("0.000");
    klQPValue->setFont(boldFont);
    resultsLayout->addRow("D<sub>KL</sub>(Q||P):", klQPValue);
    
    asymmetryValue = new QLabel("0.000");
    resultsLayout->addRow("Asymmetry:", asymmetryValue);
    
    controlsLayout->addWidget(resultsGroup);
    
    // Action buttons
    swapButton = new QPushButton("⇄ Swap P ↔ Q");
    connect(swapButton, &QPushButton::clicked, this, &KLDivergenceWidget::swapDistributions);
    controlsLayout->addWidget(swapButton);
    
    exportButton = new QPushButton("Export Data");
    connect(exportButton, &QPushButton::clicked, this, &KLDivergenceWidget::exportData);
    controlsLayout->addWidget(exportButton);
    
    controlsLayout->addStretch();
    contentLayout->addLayout(controlsLayout, 1);
    
    // Right side: Chart
    chartView->setRenderHint(QPainter::Antialiasing);
    chartView->setMinimumHeight(400);
    contentLayout->addWidget(chartView, 2);
    
    mainLayout->addLayout(contentLayout);
    
    // Bottom: Explanation
    explanationText = new QTextEdit();
    explanationText->setReadOnly(true);
    explanationText->setMaximumHeight(150);
    mainLayout->addWidget(explanationText);
    
    updateExplanation();
}

double KLDivergenceWidget::normalPDF(double x, double mu, double sigma)
{
    const double pi = 3.14159265358979323846;
    return (1.0 / (sigma * std::sqrt(2 * pi))) * 
           std::exp(-0.5 * std::pow((x - mu) / sigma, 2));
}

double KLDivergenceWidget::exponentialPDF(double x, double lambda)
{
    if (x < 0) return 0;
    return lambda * std::exp(-lambda * x);
}

double KLDivergenceWidget::uniformPDF(double x, double a, double b)
{
    if (x >= a && x <= b) return 1.0 / (b - a);
    return 0;
}

double KLDivergenceWidget::betaPDF(double x, double alpha, double beta)
{
    if (x <= 0 || x >= 1) return 0;
    
    // Simplified beta function approximation
    double logBeta = std::lgamma(alpha) + std::lgamma(beta) - std::lgamma(alpha + beta);
    return std::exp((alpha - 1) * std::log(x) + (beta - 1) * std::log(1 - x) - logBeta);
}

std::vector<double> KLDivergenceWidget::generateDistribution(
    DistType type, const std::vector<double>& params, const std::vector<double>& xValues)
{
    std::vector<double> pdf;
    
    for (double x : xValues) {
        double value = 0;
        switch (type) {
            case NORMAL:
                value = normalPDF(x, params[0], params[1]);
                break;
            case EXPONENTIAL:
                value = exponentialPDF(x, params[0]);
                break;
            case UNIFORM:
                value = uniformPDF(x, params[0], params[1]);
                break;
            case BETA:
                value = betaPDF(x, params[0], params[1]);
                break;
        }
        pdf.push_back(value);
    }
    
    return pdf;
}

double KLDivergenceWidget::klNormalNormal(double mu1, double sigma1, double mu2, double sigma2)
{
    // Analytical KL divergence for two normal distributions
    // D_KL(N(μ1,σ1²) || N(μ2,σ2²)) = log(σ2/σ1) + (σ1² + (μ1-μ2)²)/(2σ2²) - 1/2
    return std::log(sigma2 / sigma1) + 
           (sigma1 * sigma1 + (mu1 - mu2) * (mu1 - mu2)) / (2 * sigma2 * sigma2) - 0.5;
}

double KLDivergenceWidget::klExponentialExponential(double lambda1, double lambda2)
{
    // Analytical KL divergence for two exponential distributions
    // D_KL(Exp(λ1) || Exp(λ2)) = log(λ2/λ1) + λ1/λ2 - 1
    return std::log(lambda2 / lambda1) + lambda1 / lambda2 - 1;
}

double KLDivergenceWidget::calculateKLNumerical(const std::vector<double>& P, const std::vector<double>& Q)
{
    const double epsilon = 1e-10;
    double kl = 0;
    
    for (size_t i = 0; i < P.size(); ++i) {
        if (P[i] > epsilon) {
            double q = std::max(epsilon, Q[i]);
            kl += P[i] * std::log(P[i] / q);
        }
    }
    
    return kl;
}

double KLDivergenceWidget::calculateKLDivergence(
    DistType distP, const std::vector<double>& paramsP,
    DistType distQ, const std::vector<double>& paramsQ)
{
    // Use analytical formula when available
    if (distP == NORMAL && distQ == NORMAL) {
        return klNormalNormal(paramsP[0], paramsP[1], paramsQ[0], paramsQ[1]);
    }
    if (distP == EXPONENTIAL && distQ == EXPONENTIAL) {
        return klExponentialExponential(paramsP[0], paramsQ[0]);
    }
    
    // Otherwise use numerical integration
    std::vector<double> xValues;
    double xMin = -10, xMax = 10;
    int numPoints = 1000;
    
    if (distP == EXPONENTIAL || distQ == EXPONENTIAL || 
        distP == BETA || distQ == BETA) {
        xMin = 0;
        xMax = distP == BETA || distQ == BETA ? 1 : 10;
    }
    
    double dx = (xMax - xMin) / numPoints;
    for (int i = 0; i < numPoints; ++i) {
        xValues.push_back(xMin + i * dx);
    }
    
    auto P = generateDistribution(distP, paramsP, xValues);
    auto Q = generateDistribution(distQ, paramsQ, xValues);
    
    // Normalize
    double sumP = std::accumulate(P.begin(), P.end(), 0.0) * dx;
    double sumQ = std::accumulate(Q.begin(), Q.end(), 0.0) * dx;
    
    for (auto& p : P) p /= sumP;
    for (auto& q : Q) q /= sumQ;
    
    return calculateKLNumerical(P, Q) * dx;
}

void KLDivergenceWidget::updateVisualization()
{
    DistType distP = static_cast<DistType>(distPSelector->currentIndex());
    DistType distQ = static_cast<DistType>(distQSelector->currentIndex());
    
    std::vector<double> paramsP = {pParam1Spin->value(), pParam2Spin->value()};
    std::vector<double> paramsQ = {qParam1Spin->value(), qParam2Spin->value()};
    
    // Calculate KL divergences
    double klPQ = calculateKLDivergence(distP, paramsP, distQ, paramsQ);
    double klQP = calculateKLDivergence(distQ, paramsQ, distP, paramsP);
    double asymmetry = std::abs(klPQ - klQP);
    
    klPQValue->setText(QString::number(klPQ, 'f', 4));
    klQPValue->setText(QString::number(klQP, 'f', 4));
    asymmetryValue->setText(QString::number(asymmetry, 'f', 4));
    
    updateChart();
}

void KLDivergenceWidget::updateChart()
{
    chart->removeAllSeries();
    
    DistType distP = static_cast<DistType>(distPSelector->currentIndex());
    DistType distQ = static_cast<DistType>(distQSelector->currentIndex());
    
    std::vector<double> paramsP = {pParam1Spin->value(), pParam2Spin->value()};
    std::vector<double> paramsQ = {qParam1Spin->value(), qParam2Spin->value()};
    
    // Generate x values
    std::vector<double> xValues;
    double xMin = -10, xMax = 10;
    
    if (distP == EXPONENTIAL || distQ == EXPONENTIAL || 
        distP == BETA || distQ == BETA) {
        xMin = 0;
        xMax = distP == BETA || distQ == BETA ? 1 : 10;
    }
    
    int numPoints = 500;
    double dx = (xMax - xMin) / numPoints;
    for (int i = 0; i < numPoints; ++i) {
        xValues.push_back(xMin + i * dx);
    }
    
    auto P = generateDistribution(distP, paramsP, xValues);
    auto Q = generateDistribution(distQ, paramsQ, xValues);
    
    // Create series
    QLineSeries *seriesP = new QLineSeries();
    seriesP->setName("P (Reference)");
    
    QLineSeries *seriesQ = new QLineSeries();
    seriesQ->setName("Q (Approximation)");
    
    for (size_t i = 0; i < xValues.size(); ++i) {
        seriesP->append(xValues[i], P[i]);
        seriesQ->append(xValues[i], Q[i]);
    }
    
    chart->addSeries(seriesP);
    chart->addSeries(seriesQ);
    
    chart->createDefaultAxes();
    QValueAxis *axisX = qobject_cast<QValueAxis*>(chart->axes(Qt::Horizontal).first());
    QValueAxis *axisY = qobject_cast<QValueAxis*>(chart->axes(Qt::Vertical).first());
    
    if (axisX && axisY) {
        axisX->setTitleText("x");
        axisX->setRange(xMin, xMax);
        axisY->setTitleText("Probability Density");
    }
    
    chart->setTitle("KL Divergence: Distribution Comparison");
    chart->legend()->setVisible(true);
}

void KLDivergenceWidget::onDistributionTypeChanged(int index)
{
    updateParameterLabels();
    updateVisualization();
}

void KLDivergenceWidget::updateParameterLabels()
{
    DistType distP = static_cast<DistType>(distPSelector->currentIndex());
    DistType distQ = static_cast<DistType>(distQSelector->currentIndex());
    
    // Update P parameters
    switch (distP) {
        case NORMAL:
            pParam1Label->setText("Mean (μ):");
            pParam2Label->setText("Std Dev (σ):");
            pParam1Spin->setRange(-10, 10);
            pParam2Spin->setRange(0.1, 10);
            break;
        case EXPONENTIAL:
            pParam1Label->setText("Rate (λ):");
            pParam2Label->setText("(unused):");
            pParam1Spin->setRange(0.1, 10);
            pParam2Spin->setEnabled(false);
            break;
        case UNIFORM:
            pParam1Label->setText("Min (a):");
            pParam2Label->setText("Max (b):");
            pParam1Spin->setRange(-10, 10);
            pParam2Spin->setRange(-10, 10);
            pParam2Spin->setEnabled(true);
            break;
        case BETA:
            pParam1Label->setText("Alpha (α):");
            pParam2Label->setText("Beta (β):");
            pParam1Spin->setRange(0.1, 10);
            pParam2Spin->setRange(0.1, 10);
            pParam2Spin->setEnabled(true);
            break;
    }
    
    // Update Q parameters
    switch (distQ) {
        case NORMAL:
            qParam1Label->setText("Mean (μ):");
            qParam2Label->setText("Std Dev (σ):");
            qParam1Spin->setRange(-10, 10);
            qParam2Spin->setRange(0.1, 10);
            break;
        case EXPONENTIAL:
            qParam1Label->setText("Rate (λ):");
            qParam2Label->setText("(unused):");
            qParam1Spin->setRange(0.1, 10);
            qParam2Spin->setEnabled(false);
            break;
        case UNIFORM:
            qParam1Label->setText("Min (a):");
            qParam2Label->setText("Max (b):");
            qParam1Spin->setRange(-10, 10);
            qParam2Spin->setRange(-10, 10);
            qParam2Spin->setEnabled(true);
            break;
        case BETA:
            qParam1Label->setText("Alpha (α):");
            qParam2Label->setText("Beta (β):");
            qParam1Spin->setRange(0.1, 10);
            qParam2Spin->setRange(0.1, 10);
            qParam2Spin->setEnabled(true);
            break;
    }
}

void KLDivergenceWidget::swapDistributions()
{
    int tempType = distPSelector->currentIndex();
    distPSelector->setCurrentIndex(distQSelector->currentIndex());
    distQSelector->setCurrentIndex(tempType);
    
    double tempParam1 = pParam1Spin->value();
    double tempParam2 = pParam2Spin->value();
    
    pParam1Spin->setValue(qParam1Spin->value());
    pParam2Spin->setValue(qParam2Spin->value());
    qParam1Spin->setValue(tempParam1);
    qParam2Spin->setValue(tempParam2);
}

void KLDivergenceWidget::updateExplanation()
{
    explanationText->setHtml(
        "<h3>Kullback-Leibler Divergence</h3>"
        "<p><b>Formula:</b> D<sub>KL</sub>(P||Q) = Σ P(x) · log(P(x)/Q(x))</p>"
        "<p><b>What does it measure?</b></p>"
        "<ul>"
        "<li><b>Information loss:</b> Extra bits needed to encode P using Q's code</li>"
        "<li><b>Surprise:</b> How 'surprised' we are seeing P when expecting Q</li>"
        "<li><b>NOT symmetric:</b> D<sub>KL</sub>(P||Q) ≠ D<sub>KL</sub>(Q||P) - Try swapping!</li>"
        "<li><b>Always ≥ 0:</b> Equals 0 only when P = Q everywhere</li>"
        "</ul>"
        "<p><b>ML Applications:</b></p>"
        "<ul>"
        "<li><b>VAEs:</b> KL(q(z|x)||p(z)) regularizes latent space</li>"
        "<li><b>Distillation:</b> Match teacher and student distributions</li>"
        "<li><b>RL:</b> Trust region policy optimization (TRPO, PPO)</li>"
        "</ul>"
    );
}

void KLDivergenceWidget::exportData()
{
    QString fileName = QFileDialog::getSaveFileName(this, "Export KL Divergence Data", "", "CSV Files (*.csv)");
    if (fileName.isEmpty()) return;
    
    QFile file(fileName);
    if (!file.open(QIODevice::WriteOnly | QIODevice::Text)) return;
    
    QTextStream out(&file);
    out << "x,P(x),Q(x)\n";
    
    DistType distP = static_cast<DistType>(distPSelector->currentIndex());
    DistType distQ = static_cast<DistType>(distQSelector->currentIndex());
    
    std::vector<double> paramsP = {pParam1Spin->value(), pParam2Spin->value()};
    std::vector<double> paramsQ = {qParam1Spin->value(), qParam2Spin->value()};
    
    std::vector<double> xValues;
    double xMin = -10, xMax = 10;
    if (distP == EXPONENTIAL || distQ == EXPONENTIAL || distP == BETA || distQ == BETA) {
        xMin = 0;
        xMax = distP == BETA || distQ == BETA ? 1 : 10;
    }
    
    int numPoints = 500;
    double dx = (xMax - xMin) / numPoints;
    for (int i = 0; i < numPoints; ++i) {
        xValues.push_back(xMin + i * dx);
    }
    
    auto P = generateDistribution(distP, paramsP, xValues);
    auto Q = generateDistribution(distQ, paramsQ, xValues);
    
    for (size_t i = 0; i < xValues.size(); ++i) {
        out << xValues[i] << "," << P[i] << "," << Q[i] << "\n";
    }
    
    file.close();
}
