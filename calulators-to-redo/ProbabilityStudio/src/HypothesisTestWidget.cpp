#include "HypothesisTestWidget.h"
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QFormLayout>
#include <QFileDialog>
#include <QTextStream>
#include <cmath>
#include <algorithm>

HypothesisTestWidget::HypothesisTestWidget(QWidget *parent)
    : QWidget(parent)
    , chart(new QChart())
    , chartView(new QChartView(chart))
{
    setupUI();
    updateVisualization();
}

HypothesisTestWidget::~HypothesisTestWidget()
{
}

void HypothesisTestWidget::setupUI()
{
    QVBoxLayout *mainLayout = new QVBoxLayout(this);
    
    // Header
    QHBoxLayout *headerLayout = new QHBoxLayout();
    QLabel *titleLabel = new QLabel("<h2>Hypothesis Testing Calculator</h2>");
    
    testTypeSelector = new QComboBox();
    testTypeSelector->addItem("One-Sample t-test");
    testTypeSelector->addItem("Two-Sample t-test");
    testTypeSelector->addItem("Z-test");
    testTypeSelector->addItem("Paired t-test");
    connect(testTypeSelector, QOverload<int>::of(&QComboBox::currentIndexChanged),
            this, &HypothesisTestWidget::onTestTypeChanged);
    
    tailTypeSelector = new QComboBox();
    tailTypeSelector->addItem("Two-Tailed");
    tailTypeSelector->addItem("Left-Tailed");
    tailTypeSelector->addItem("Right-Tailed");
    connect(tailTypeSelector, QOverload<int>::of(&QComboBox::currentIndexChanged),
            this, &HypothesisTestWidget::updateVisualization);
    
    headerLayout->addWidget(titleLabel);
    headerLayout->addStretch();
    headerLayout->addWidget(new QLabel("Test Type:"));
    headerLayout->addWidget(testTypeSelector);
    headerLayout->addWidget(new QLabel("Tail:"));
    headerLayout->addWidget(tailTypeSelector);
    mainLayout->addLayout(headerLayout);
    
    // Content layout
    QHBoxLayout *contentLayout = new QHBoxLayout();
    
    // Left side: Parameters
    QVBoxLayout *leftLayout = new QVBoxLayout();
    
    parametersGroup = new QGroupBox("Test Parameters");
    QFormLayout *paramsLayout = new QFormLayout(parametersGroup);
    
    // Sample 1 parameters
    sampleMeanSpin = new QDoubleSpinBox();
    sampleMeanSpin->setRange(-1000, 1000);
    sampleMeanSpin->setValue(10.5);
    sampleMeanSpin->setDecimals(3);
    connect(sampleMeanSpin, QOverload<double>::of(&QDoubleSpinBox::valueChanged),
            this, &HypothesisTestWidget::updateVisualization);
    paramsLayout->addRow("Sample Mean (x̄):", sampleMeanSpin);
    
    sampleStdSpin = new QDoubleSpinBox();
    sampleStdSpin->setRange(0.01, 1000);
    sampleStdSpin->setValue(2.5);
    sampleStdSpin->setDecimals(3);
    connect(sampleStdSpin, QOverload<double>::of(&QDoubleSpinBox::valueChanged),
            this, &HypothesisTestWidget::updateVisualization);
    paramsLayout->addRow("Sample Std Dev (s):", sampleStdSpin);
    
    sampleSizeSpin = new QSpinBox();
    sampleSizeSpin->setRange(2, 10000);
    sampleSizeSpin->setValue(30);
    connect(sampleSizeSpin, QOverload<int>::of(&QSpinBox::valueChanged),
            this, &HypothesisTestWidget::updateVisualization);
    paramsLayout->addRow("Sample Size (n):", sampleSizeSpin);
    
    // Sample 2 parameters (for two-sample tests)
    sampleMean2Label = new QLabel("Sample 2 Mean (x̄₂):");
    sampleMean2Spin = new QDoubleSpinBox();
    sampleMean2Spin->setRange(-1000, 1000);
    sampleMean2Spin->setValue(9.0);
    sampleMean2Spin->setDecimals(3);
    connect(sampleMean2Spin, QOverload<double>::of(&QDoubleSpinBox::valueChanged),
            this, &HypothesisTestWidget::updateVisualization);
    paramsLayout->addRow(sampleMean2Label, sampleMean2Spin);
    
    sampleStd2Label = new QLabel("Sample 2 Std Dev (s₂):");
    sampleStd2Spin = new QDoubleSpinBox();
    sampleStd2Spin->setRange(0.01, 1000);
    sampleStd2Spin->setValue(2.0);
    sampleStd2Spin->setDecimals(3);
    connect(sampleStd2Spin, QOverload<double>::of(&QDoubleSpinBox::valueChanged),
            this, &HypothesisTestWidget::updateVisualization);
    paramsLayout->addRow(sampleStd2Label, sampleStd2Spin);
    
    sampleSize2Label = new QLabel("Sample 2 Size (n₂):");
    sampleSize2Spin = new QSpinBox();
    sampleSize2Spin->setRange(2, 10000);
    sampleSize2Spin->setValue(25);
    connect(sampleSize2Spin, QOverload<int>::of(&QSpinBox::valueChanged),
            this, &HypothesisTestWidget::updateVisualization);
    paramsLayout->addRow(sampleSize2Label, sampleSize2Spin);
    
    // Population parameters
    popStdLabel = new QLabel("Population Std (σ):");
    popStdSpin = new QDoubleSpinBox();
    popStdSpin->setRange(0.01, 1000);
    popStdSpin->setValue(2.0);
    popStdSpin->setDecimals(3);
    connect(popStdSpin, QOverload<double>::of(&QDoubleSpinBox::valueChanged),
            this, &HypothesisTestWidget::updateVisualization);
    paramsLayout->addRow(popStdLabel, popStdSpin);
    
    nullMeanSpin = new QDoubleSpinBox();
    nullMeanSpin->setRange(-1000, 1000);
    nullMeanSpin->setValue(10.0);
    nullMeanSpin->setDecimals(3);
    connect(nullMeanSpin, QOverload<double>::of(&QDoubleSpinBox::valueChanged),
            this, &HypothesisTestWidget::updateVisualization);
    paramsLayout->addRow("Null Hypothesis (μ₀):", nullMeanSpin);
    
    alphaSpin = new QDoubleSpinBox();
    alphaSpin->setRange(0.001, 0.5);
    alphaSpin->setValue(0.05);
    alphaSpin->setDecimals(3);
    alphaSpin->setSingleStep(0.01);
    connect(alphaSpin, QOverload<double>::of(&QDoubleSpinBox::valueChanged),
            this, &HypothesisTestWidget::updateVisualization);
    paramsLayout->addRow("Significance Level (α):", alphaSpin);
    
    leftLayout->addWidget(parametersGroup);
    
    // Results group
    resultsGroup = new QGroupBox("Test Results");
    QFormLayout *resultsLayout = new QFormLayout(resultsGroup);
    
    testStatisticValue = new QLabel("0.000");
    QFont boldFont = testStatisticValue->font();
    boldFont.setPointSize(11);
    boldFont.setBold(true);
    testStatisticValue->setFont(boldFont);
    resultsLayout->addRow("Test Statistic:", testStatisticValue);
    
    pValueLabel = new QLabel("0.000");
    pValueLabel->setFont(boldFont);
    resultsLayout->addRow("p-value:", pValueLabel);
    
    criticalValueLabel = new QLabel("0.000");
    resultsLayout->addRow("Critical Value:", criticalValueLabel);
    
    confidenceIntervalLabel = new QLabel("[0.000, 0.000]");
    resultsLayout->addRow("95% CI:", confidenceIntervalLabel);
    
    decisionLabel = new QLabel("Fail to reject H₀");
    QFont decisionFont = decisionLabel->font();
    decisionFont.setPointSize(12);
    decisionFont.setBold(true);
    decisionLabel->setFont(decisionFont);
    resultsLayout->addRow("Decision:", decisionLabel);
    
    leftLayout->addWidget(resultsGroup);
    
    // Action buttons
    calculateButton = new QPushButton("Calculate Test");
    connect(calculateButton, &QPushButton::clicked, this, &HypothesisTestWidget::calculateTest);
    leftLayout->addWidget(calculateButton);
    
    exportButton = new QPushButton("Export Results");
    connect(exportButton, &QPushButton::clicked, this, &HypothesisTestWidget::exportData);
    leftLayout->addWidget(exportButton);
    
    leftLayout->addStretch();
    contentLayout->addLayout(leftLayout, 1);
    
    // Right side: Chart
    chartView->setRenderHint(QPainter::Antialiasing);
    chartView->setMinimumHeight(400);
    contentLayout->addWidget(chartView, 2);
    
    mainLayout->addLayout(contentLayout);
    
    // Explanation
    explanationText = new QTextEdit();
    explanationText->setReadOnly(true);
    explanationText->setMaximumHeight(150);
    mainLayout->addWidget(explanationText);
    
    updateParameterVisibility();
    updateExplanation();
}

void HypothesisTestWidget::updateParameterVisibility()
{
    TestType test = static_cast<TestType>(testTypeSelector->currentIndex());
    
    // Show/hide sample 2 parameters
    bool showSample2 = (test == TWO_SAMPLE_T);
    sampleMean2Label->setVisible(showSample2);
    sampleMean2Spin->setVisible(showSample2);
    sampleStd2Label->setVisible(showSample2);
    sampleStd2Spin->setVisible(showSample2);
    sampleSize2Label->setVisible(showSample2);
    sampleSize2Spin->setVisible(showSample2);
    
    // Show/hide population std (for z-test)
    bool showPopStd = (test == Z_TEST);
    popStdLabel->setVisible(showPopStd);
    popStdSpin->setVisible(showPopStd);
}

double HypothesisTestWidget::normalCDF(double x)
{
    // Approximation of standard normal CDF
    return 0.5 * (1.0 + std::erf(x / std::sqrt(2.0)));
}

double HypothesisTestWidget::normalQuantile(double p)
{
    // Approximation of normal quantile (inverse CDF)
    // Using rational approximation for simplicity
    if (p <= 0 || p >= 1) return 0;
    
    double q = p - 0.5;
    double r;
    
    if (std::abs(q) <= 0.425) {
        r = 0.180625 - q * q;
        return q * (((((((2.5090809287301226727e3 * r + 3.3430575583588128105e4) * r +
                       4.2313330701600911252e4) * r + 2.3782041382114385731e4) * r +
                      6.9642345112854059278e3) * r + 5.5504934605709632494e2) * r +
                    1.5762013422895488472e1) * r + 1.0) /
               (((((((5.2264952788528545610e3 * r + 2.8729085735721942674e4) * r +
                    3.9307895800092710610e4) * r + 2.1213794301586595867e4) * r +
                   5.3941960214247511077e3) * r + 6.8718700749205790830e2) * r +
                 4.2313330701600911252e1) * r + 1.0);
    }
    
    r = (q < 0) ? p : 1 - p;
    r = std::sqrt(-std::log(r));
    return (q < 0 ? -1 : 1) * r;
}

double HypothesisTestWidget::tCDF(double x, int df)
{
    // Simplified t-distribution CDF approximation
    // For large df, approximate with normal
    if (df > 30) {
        return normalCDF(x);
    }
    
    // Otherwise use a numerical approximation
    // This is simplified - in production use boost or GSL
    double a = df / (df + x * x);
    return 1.0 - 0.5 * std::pow(a, df / 2.0);
}

double HypothesisTestWidget::tQuantile(double p, int df)
{
    // Simplified quantile function
    if (df > 30) {
        return normalQuantile(p);
    }
    
    // Simple approximation for t-quantile
    double z = normalQuantile(p);
    double g1 = (z*z*z + z) / 4.0;
    double g2 = (5*z*z*z*z*z + 16*z*z*z + 3*z) / 96.0;
    
    return z + g1 / df + g2 / (df * df);
}

double HypothesisTestWidget::calculateOneSampleT(double sampleMean, double sampleStd, int n, double nullMean)
{
    double se = sampleStd / std::sqrt(n);
    return (sampleMean - nullMean) / se;
}

double HypothesisTestWidget::calculateTwoSampleT(double mean1, double std1, int n1,
                                                 double mean2, double std2, int n2)
{
    // Welch's t-test (unequal variances)
    double se = std::sqrt((std1 * std1 / n1) + (std2 * std2 / n2));
    return (mean1 - mean2) / se;
}

double HypothesisTestWidget::calculateZTest(double sampleMean, double popStd, int n, double nullMean)
{
    double se = popStd / std::sqrt(n);
    return (sampleMean - nullMean) / se;
}

double HypothesisTestWidget::calculatePValue(double testStat, int df, TailType tail, bool useTDist)
{
    double p;
    
    if (useTDist) {
        p = 1.0 - tCDF(std::abs(testStat), df);
    } else {
        p = 1.0 - normalCDF(std::abs(testStat));
    }
    
    switch (tail) {
        case TWO_TAILED:
            return 2.0 * p;
        case LEFT_TAILED:
            return (testStat < 0) ? p : 1.0 - p;
        case RIGHT_TAILED:
            return (testStat > 0) ? p : 1.0 - p;
    }
    
    return p;
}

double HypothesisTestWidget::calculateCriticalValue(double alpha, int df, TailType tail, bool useTDist)
{
    double p = (tail == TWO_TAILED) ? 1.0 - alpha / 2.0 : 1.0 - alpha;
    
    if (useTDist) {
        return tQuantile(p, df);
    } else {
        return normalQuantile(p);
    }
}

std::pair<double, double> HypothesisTestWidget::calculateConfidenceInterval(
    double mean, double std, int n, double alpha, bool useTDist)
{
    double se = std / std::sqrt(n);
    double critical = calculateCriticalValue(alpha, n - 1, TWO_TAILED, useTDist);
    
    double margin = critical * se;
    return {mean - margin, mean + margin};
}

void HypothesisTestWidget::calculateTest()
{
    updateVisualization();
}

void HypothesisTestWidget::updateVisualization()
{
    TestType test = static_cast<TestType>(testTypeSelector->currentIndex());
    TailType tail = static_cast<TailType>(tailTypeSelector->currentIndex());
    
    double testStat = 0;
    int df = sampleSizeSpin->value() - 1;
    bool useTDist = true;
    
    // Calculate test statistic
    switch (test) {
        case ONE_SAMPLE_T:
            testStat = calculateOneSampleT(sampleMeanSpin->value(), sampleStdSpin->value(),
                                          sampleSizeSpin->value(), nullMeanSpin->value());
            df = sampleSizeSpin->value() - 1;
            useTDist = true;
            break;
            
        case TWO_SAMPLE_T:
            testStat = calculateTwoSampleT(sampleMeanSpin->value(), sampleStdSpin->value(), sampleSizeSpin->value(),
                                          sampleMean2Spin->value(), sampleStd2Spin->value(), sampleSize2Spin->value());
            // Welch-Satterthwaite degrees of freedom (simplified)
            df = sampleSizeSpin->value() + sampleSize2Spin->value() - 2;
            useTDist = true;
            break;
            
        case Z_TEST:
            testStat = calculateZTest(sampleMeanSpin->value(), popStdSpin->value(),
                                     sampleSizeSpin->value(), nullMeanSpin->value());
            useTDist = false;
            break;
            
        case PAIRED_T:
            testStat = calculateOneSampleT(sampleMeanSpin->value(), sampleStdSpin->value(),
                                          sampleSizeSpin->value(), 0.0);
            df = sampleSizeSpin->value() - 1;
            useTDist = true;
            break;
    }
    
    // Calculate p-value
    double pValue = calculatePValue(testStat, df, tail, useTDist);
    
    // Calculate critical value
    double alpha = alphaSpin->value();
    double criticalValue = calculateCriticalValue(alpha, df, tail, useTDist);
    
    // Calculate confidence interval
    auto ci = calculateConfidenceInterval(sampleMeanSpin->value(), sampleStdSpin->value(),
                                         sampleSizeSpin->value(), alpha, useTDist);
    
    // Update display
    testStatisticValue->setText(QString::number(testStat, 'f', 4));
    pValueLabel->setText(QString::number(pValue, 'f', 4));
    
    if (tail == TWO_TAILED) {
        criticalValueLabel->setText(QString("±%1").arg(criticalValue, 0, 'f', 3));
    } else {
        criticalValueLabel->setText(QString::number(criticalValue, 'f', 3));
    }
    
    confidenceIntervalLabel->setText(QString("[%1, %2]")
                                    .arg(ci.first, 0, 'f', 3)
                                    .arg(ci.second, 0, 'f', 3));
    
    // Decision
    bool reject = pValue < alpha;
    if (reject) {
        decisionLabel->setText("<span style='color: red;'><b>REJECT H₀</b></span>");
        decisionLabel->setToolTip("The result is statistically significant");
    } else {
        decisionLabel->setText("<span style='color: green;'><b>FAIL TO REJECT H₀</b></span>");
        decisionLabel->setToolTip("The result is not statistically significant");
    }
    
    updateChart();
}

void HypothesisTestWidget::updateChart()
{
    chart->removeAllSeries();
    
    TestType test = static_cast<TestType>(testTypeSelector->currentIndex());
    TailType tail = static_cast<TailType>(tailTypeSelector->currentIndex());
    
    bool useTDist = (test != Z_TEST);
    int df = sampleSizeSpin->value() - 1;
    if (test == TWO_SAMPLE_T) {
        df = sampleSizeSpin->value() + sampleSize2Spin->value() - 2;
    }
    
    double testStat = std::stod(testStatisticValue->text().toStdString());
    double alpha = alphaSpin->value();
    double criticalValue = calculateCriticalValue(alpha, df, tail, useTDist);
    
    // Generate distribution curve
    QLineSeries *distSeries = new QLineSeries();
    distSeries->setName(useTDist ? "t-distribution" : "Normal distribution");
    
    double xMin = -5, xMax = 5;
    int numPoints = 200;
    double dx = (xMax - xMin) / numPoints;
    
    for (int i = 0; i <= numPoints; ++i) {
        double x = xMin + i * dx;
        double y;
        
        if (useTDist) {
            // Simplified t-distribution PDF
            double factor = std::tgamma((df + 1) / 2.0) / (std::sqrt(df * M_PI) * std::tgamma(df / 2.0));
            y = factor * std::pow(1 + x * x / df, -(df + 1) / 2.0);
        } else {
            // Normal PDF
            y = (1.0 / std::sqrt(2 * M_PI)) * std::exp(-0.5 * x * x);
        }
        
        distSeries->append(x, y);
    }
    
    chart->addSeries(distSeries);
    
    // Mark test statistic
    QLineSeries *testStatLine = new QLineSeries();
    testStatLine->setName("Test Statistic");
    testStatLine->append(testStat, 0);
    testStatLine->append(testStat, 0.4);
    chart->addSeries(testStatLine);
    
    // Mark critical region(s)
    if (tail == TWO_TAILED) {
        QLineSeries *critLeft = new QLineSeries();
        critLeft->setName("Critical Region");
        critLeft->append(-criticalValue, 0);
        critLeft->append(-criticalValue, 0.4);
        chart->addSeries(critLeft);
        
        QLineSeries *critRight = new QLineSeries();
        critRight->setName("");
        critRight->append(criticalValue, 0);
        critRight->append(criticalValue, 0.4);
        chart->addSeries(critRight);
    } else {
        QLineSeries *critLine = new QLineSeries();
        critLine->setName("Critical Value");
        critLine->append(criticalValue, 0);
        critLine->append(criticalValue, 0.4);
        chart->addSeries(critLine);
    }
    
    chart->createDefaultAxes();
    QValueAxis *axisX = qobject_cast<QValueAxis*>(chart->axes(Qt::Horizontal).first());
    QValueAxis *axisY = qobject_cast<QValueAxis*>(chart->axes(Qt::Vertical).first());
    
    if (axisX && axisY) {
        axisX->setTitleText("Test Statistic Value");
        axisX->setRange(xMin, xMax);
        axisY->setTitleText("Probability Density");
    }
    
    chart->setTitle(QString("Hypothesis Test: %1")
                   .arg(testTypeSelector->currentText()));
    chart->legend()->setVisible(true);
}

void HypothesisTestWidget::onTestTypeChanged(int index)
{
    updateParameterVisibility();
    updateExplanation();
    updateVisualization();
}

void HypothesisTestWidget::updateExplanation()
{
    TestType test = static_cast<TestType>(testTypeSelector->currentIndex());
    
    QString explanation;
    
    switch (test) {
        case ONE_SAMPLE_T:
            explanation = 
                "<h3>One-Sample t-test</h3>"
                "<p><b>H₀:</b> μ = μ₀ (population mean equals null hypothesis value)</p>"
                "<p><b>When to use:</b> Compare sample mean to known value, unknown population variance</p>"
                "<p><b>Formula:</b> t = (x̄ - μ₀) / (s/√n)</p>"
                "<p><b>ML Example:</b> Is model accuracy significantly different from 70%?</p>";
            break;
            
        case TWO_SAMPLE_T:
            explanation = 
                "<h3>Two-Sample t-test (Welch's)</h3>"
                "<p><b>H₀:</b> μ₁ = μ₂ (two population means are equal)</p>"
                "<p><b>When to use:</b> Compare means from two independent groups</p>"
                "<p><b>Formula:</b> t = (x̄₁ - x̄₂) / √(s₁²/n₁ + s₂²/n₂)</p>"
                "<p><b>ML Example:</b> Is new model significantly better than baseline?</p>";
            break;
            
        case Z_TEST:
            explanation = 
                "<h3>Z-test</h3>"
                "<p><b>H₀:</b> μ = μ₀ (population mean equals null hypothesis value)</p>"
                "<p><b>When to use:</b> Large sample (n > 30) OR known population variance</p>"
                "<p><b>Formula:</b> z = (x̄ - μ₀) / (σ/√n)</p>"
                "<p><b>ML Example:</b> Is average prediction error significantly different from 0?</p>";
            break;
            
        case PAIRED_T:
            explanation = 
                "<h3>Paired t-test</h3>"
                "<p><b>H₀:</b> μ_diff = 0 (mean of paired differences is zero)</p>"
                "<p><b>When to use:</b> Before/after measurements on same subjects</p>"
                "<p><b>Formula:</b> t = (x̄_diff - 0) / (s_diff/√n)</p>"
                "<p><b>ML Example:</b> Does fine-tuning improve performance on same test set?</p>";
            break;
    }
    
    explanationText->setHtml(explanation);
}

void HypothesisTestWidget::exportData()
{
    QString fileName = QFileDialog::getSaveFileName(this, "Export Test Results", "", "Text Files (*.txt)");
    if (fileName.isEmpty()) return;
    
    QFile file(fileName);
    if (!file.open(QIODevice::WriteOnly | QIODevice::Text)) return;
    
    QTextStream out(&file);
    
    out << "=== Hypothesis Test Results ===\n\n";
    out << "Test Type: " << testTypeSelector->currentText() << "\n";
    out << "Tail Type: " << tailTypeSelector->currentText() << "\n\n";
    
    out << "Parameters:\n";
    out << "  Sample Mean: " << sampleMeanSpin->value() << "\n";
    out << "  Sample Std Dev: " << sampleStdSpin->value() << "\n";
    out << "  Sample Size: " << sampleSizeSpin->value() << "\n";
    out << "  Null Hypothesis: " << nullMeanSpin->value() << "\n";
    out << "  Significance Level: " << alphaSpin->value() << "\n\n";
    
    out << "Results:\n";
    out << "  Test Statistic: " << testStatisticValue->text() << "\n";
    out << "  p-value: " << pValueLabel->text() << "\n";
    out << "  Critical Value: " << criticalValueLabel->text() << "\n";
    out << "  Confidence Interval: " << confidenceIntervalLabel->text() << "\n\n";
    
    out << "Decision: " << decisionLabel->text().remove(QRegExp("<[^>]*>")) << "\n";
    
    file.close();
}
