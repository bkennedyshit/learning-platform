#include "CrossEntropyWidget.h"
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QFormLayout>
#include <QFileDialog>
#include <QTextStream>
#include <cmath>
#include <numeric>
#include <algorithm>

CrossEntropyWidget::CrossEntropyWidget(QWidget *parent)
    : QWidget(parent)
    , chart(new QChart())
    , chartView(new QChartView(chart))
{
    setupUI();
    updateBinaryVisualization();
}

CrossEntropyWidget::~CrossEntropyWidget()
{
}

void CrossEntropyWidget::setupUI()
{
    QVBoxLayout *mainLayout = new QVBoxLayout(this);
    
    // Title and mode selector
    QHBoxLayout *headerLayout = new QHBoxLayout();
    QLabel *titleLabel = new QLabel("<h2>Cross-Entropy Loss Visualization</h2>");
    modeSelector = new QComboBox();
    modeSelector->addItem("Binary Classification");
    modeSelector->addItem("Categorical Classification");
    connect(modeSelector, QOverload<int>::of(&QComboBox::currentIndexChanged),
            this, &CrossEntropyWidget::onModeChanged);
    
    headerLayout->addWidget(titleLabel);
    headerLayout->addStretch();
    headerLayout->addWidget(new QLabel("Mode:"));
    headerLayout->addWidget(modeSelector);
    mainLayout->addLayout(headerLayout);
    
    // Controls and chart layout
    QHBoxLayout *contentLayout = new QHBoxLayout();
    
    // Left side: Controls
    QVBoxLayout *controlsLayout = new QVBoxLayout();
    
    setupBinaryControls();
    setupCategoricalControls();
    
    controlsLayout->addWidget(binaryGroup);
    controlsLayout->addWidget(categoricalGroup);
    controlsLayout->addStretch();
    
    // Export button
    exportButton = new QPushButton("Export Data");
    connect(exportButton, &QPushButton::clicked, this, &CrossEntropyWidget::exportData);
    controlsLayout->addWidget(exportButton);
    
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
    
    categoricalGroup->hide();
    updateExplanation();
}

void CrossEntropyWidget::setupBinaryControls()
{
    binaryGroup = new QGroupBox("Binary Cross-Entropy Controls");
    QFormLayout *layout = new QFormLayout(binaryGroup);
    
    // True label slider (0 or 1)
    QHBoxLayout *trueLabelLayout = new QHBoxLayout();
    trueLabelSlider = new QSlider(Qt::Horizontal);
    trueLabelSlider->setRange(0, 100);
    trueLabelSlider->setValue(100);
    trueLabelValue = new QLabel("1.00");
    trueLabelLayout->addWidget(trueLabelSlider);
    trueLabelLayout->addWidget(trueLabelValue);
    layout->addRow("True Label:", trueLabelLayout);
    
    // Predicted probability slider
    QHBoxLayout *predLayout = new QHBoxLayout();
    predictedProbSlider = new QSlider(Qt::Horizontal);
    predictedProbSlider->setRange(1, 99); // Avoid log(0)
    predictedProbSlider->setValue(80);
    predictedProbValue = new QLabel("0.80");
    predLayout->addWidget(predictedProbSlider);
    predLayout->addWidget(predictedProbValue);
    layout->addRow("Predicted Prob:", predLayout);
    
    // Loss display
    binaryLossValue = new QLabel("0.000");
    QFont boldFont = binaryLossValue->font();
    boldFont.setPointSize(14);
    boldFont.setBold(true);
    binaryLossValue->setFont(boldFont);
    layout->addRow("Cross-Entropy Loss:", binaryLossValue);
    
    connect(trueLabelSlider, &QSlider::valueChanged, this, &CrossEntropyWidget::updateBinaryVisualization);
    connect(predictedProbSlider, &QSlider::valueChanged, this, &CrossEntropyWidget::updateBinaryVisualization);
}

void CrossEntropyWidget::setupCategoricalControls()
{
    categoricalGroup = new QGroupBox("Categorical Cross-Entropy Controls");
    QVBoxLayout *layout = new QVBoxLayout(categoricalGroup);
    
    // Number of classes
    QHBoxLayout *classLayout = new QHBoxLayout();
    classLayout->addWidget(new QLabel("Number of Classes:"));
    numClassesSpinBox = new QSpinBox();
    numClassesSpinBox->setRange(2, 10);
    numClassesSpinBox->setValue(3);
    classLayout->addWidget(numClassesSpinBox);
    classLayout->addStretch();
    layout->addLayout(classLayout);
    
    connect(numClassesSpinBox, QOverload<int>::of(&QSpinBox::valueChanged),
            this, &CrossEntropyWidget::rebuildCategorySliders);
    
    // Container for class sliders
    classesContainer = new QWidget();
    classesLayout = new QVBoxLayout(classesContainer);
    layout->addWidget(classesContainer);
    
    // Loss display
    QHBoxLayout *lossLayout = new QHBoxLayout();
    lossLayout->addWidget(new QLabel("Cross-Entropy Loss:"));
    categoricalLossValue = new QLabel("0.000");
    QFont boldFont = categoricalLossValue->font();
    boldFont.setPointSize(14);
    boldFont.setBold(true);
    categoricalLossValue->setFont(boldFont);
    lossLayout->addWidget(categoricalLossValue);
    lossLayout->addStretch();
    layout->addLayout(lossLayout);
    
    rebuildCategorySliders();
}

void CrossEntropyWidget::rebuildCategorySliders()
{
    // Clear existing sliders
    QLayoutItem *item;
    while ((item = classesLayout->takeAt(0)) != nullptr) {
        delete item->widget();
        delete item;
    }
    trueProbSliders.clear();
    predictedProbSliders.clear();
    trueProbLabels.clear();
    predictedProbLabels.clear();
    
    int numClasses = numClassesSpinBox->value();
    
    for (int i = 0; i < numClasses; ++i) {
        QGroupBox *classBox = new QGroupBox(QString("Class %1").arg(i));
        QFormLayout *classForm = new QFormLayout(classBox);
        
        // True probability
        QHBoxLayout *trueLayout = new QHBoxLayout();
        QSlider *trueSlider = new QSlider(Qt::Horizontal);
        trueSlider->setRange(0, 100);
        trueSlider->setValue(i == 0 ? 100 : 0);
        QLabel *trueLabel = new QLabel("0.00");
        trueLayout->addWidget(trueSlider);
        trueLayout->addWidget(trueLabel);
        classForm->addRow("True Prob:", trueLayout);
        
        // Predicted probability
        QHBoxLayout *predLayout = new QHBoxLayout();
        QSlider *predSlider = new QSlider(Qt::Horizontal);
        predSlider->setRange(1, 99); // Avoid log(0)
        predSlider->setValue(i == 0 ? 80 : 20);
        QLabel *predLabel = new QLabel("0.00");
        predLayout->addWidget(predSlider);
        predLayout->addWidget(predLabel);
        classForm->addRow("Predicted Prob:", predLayout);
        
        classesLayout->addWidget(classBox);
        
        trueProbSliders.push_back(trueSlider);
        predictedProbSliders.push_back(predSlider);
        trueProbLabels.push_back(trueLabel);
        predictedProbLabels.push_back(predLabel);
        
        connect(trueSlider, &QSlider::valueChanged, this, &CrossEntropyWidget::updateCategoricalVisualization);
        connect(predSlider, &QSlider::valueChanged, this, &CrossEntropyWidget::updateCategoricalVisualization);
    }
    
    updateCategoricalVisualization();
}

double CrossEntropyWidget::calculateBinaryCrossEntropy(double trueLabel, double predicted)
{
    // Binary cross-entropy: H(p,q) = -[p*log(q) + (1-p)*log(1-q)]
    const double epsilon = 1e-7;
    predicted = std::max(epsilon, std::min(1.0 - epsilon, predicted));
    
    return -(trueLabel * std::log(predicted) + (1.0 - trueLabel) * std::log(1.0 - predicted));
}

double CrossEntropyWidget::calculateCategoricalCrossEntropy(
    const std::vector<double>& trueProbs, 
    const std::vector<double>& predProbs)
{
    // Categorical cross-entropy: H(p,q) = -Σ p_i * log(q_i)
    double loss = 0.0;
    const double epsilon = 1e-7;
    
    for (size_t i = 0; i < trueProbs.size(); ++i) {
        double pred = std::max(epsilon, std::min(1.0 - epsilon, predProbs[i]));
        loss -= trueProbs[i] * std::log(pred);
    }
    
    return loss;
}

void CrossEntropyWidget::updateBinaryVisualization()
{
    double trueLabel = trueLabelSlider->value() / 100.0;
    double predicted = predictedProbSlider->value() / 100.0;
    
    trueLabelValue->setText(QString::number(trueLabel, 'f', 2));
    predictedProbValue->setText(QString::number(predicted, 'f', 2));
    
    double loss = calculateBinaryCrossEntropy(trueLabel, predicted);
    binaryLossValue->setText(QString::number(loss, 'f', 4));
    
    updateBinaryChart();
}

void CrossEntropyWidget::updateCategoricalVisualization()
{
    std::vector<double> trueProbs, predProbs;
    
    for (size_t i = 0; i < trueProbSliders.size(); ++i) {
        double trueP = trueProbSliders[i]->value() / 100.0;
        double predP = predictedProbSliders[i]->value() / 100.0;
        
        trueProbs.push_back(trueP);
        predProbs.push_back(predP);
        
        trueProbLabels[i]->setText(QString::number(trueP, 'f', 2));
        predictedProbLabels[i]->setText(QString::number(predP, 'f', 2));
    }
    
    double loss = calculateCategoricalCrossEntropy(trueProbs, predProbs);
    categoricalLossValue->setText(QString::number(loss, 'f', 4));
    
    updateCategoricalChart();
}

void CrossEntropyWidget::updateBinaryChart()
{
    chart->removeAllSeries();
    
    // Create loss surface for different predicted probabilities
    QLineSeries *lossSeries = new QLineSeries();
    lossSeries->setName("Cross-Entropy Loss");
    
    double trueLabel = trueLabelSlider->value() / 100.0;
    
    for (int p = 1; p < 100; ++p) {
        double predicted = p / 100.0;
        double loss = calculateBinaryCrossEntropy(trueLabel, predicted);
        lossSeries->append(predicted, loss);
    }
    
    // Current point
    QLineSeries *currentPoint = new QLineSeries();
    currentPoint->setName("Current Point");
    double currentPred = predictedProbSlider->value() / 100.0;
    double currentLoss = calculateBinaryCrossEntropy(trueLabel, currentPred);
    currentPoint->append(currentPred, currentLoss);
    
    chart->addSeries(lossSeries);
    chart->addSeries(currentPoint);
    
    // Setup axes
    chart->createDefaultAxes();
    QValueAxis *axisX = qobject_cast<QValueAxis*>(chart->axes(Qt::Horizontal).first());
    QValueAxis *axisY = qobject_cast<QValueAxis*>(chart->axes(Qt::Vertical).first());
    
    if (axisX && axisY) {
        axisX->setTitleText("Predicted Probability");
        axisX->setRange(0, 1);
        axisY->setTitleText("Loss");
        axisY->setRange(0, 10);
    }
    
    chart->setTitle(QString("Binary Cross-Entropy (True Label = %1)").arg(trueLabel, 0, 'f', 2));
    chart->legend()->setVisible(true);
}

void CrossEntropyWidget::updateCategoricalChart()
{
    chart->removeAllSeries();
    
    QBarSet *trueSet = new QBarSet("True Distribution");
    QBarSet *predSet = new QBarSet("Predicted Distribution");
    
    QStringList categories;
    
    for (size_t i = 0; i < trueProbSliders.size(); ++i) {
        double trueP = trueProbSliders[i]->value() / 100.0;
        double predP = predictedProbSliders[i]->value() / 100.0;
        
        *trueSet << trueP;
        *predSet << predP;
        categories << QString("Class %1").arg(i);
    }
    
    QBarSeries *series = new QBarSeries();
    series->append(trueSet);
    series->append(predSet);
    
    chart->addSeries(series);
    
    QBarCategoryAxis *axisX = new QBarCategoryAxis();
    axisX->append(categories);
    chart->addAxis(axisX, Qt::AlignBottom);
    series->attachAxis(axisX);
    
    QValueAxis *axisY = new QValueAxis();
    axisY->setTitleText("Probability");
    axisY->setRange(0, 1);
    chart->addAxis(axisY, Qt::AlignLeft);
    series->attachAxis(axisY);
    
    chart->setTitle("Categorical Cross-Entropy: True vs Predicted");
    chart->legend()->setVisible(true);
}

void CrossEntropyWidget::onModeChanged(int index)
{
    if (index == 0) {
        binaryGroup->show();
        categoricalGroup->hide();
        updateBinaryVisualization();
    } else {
        binaryGroup->hide();
        categoricalGroup->show();
        updateCategoricalVisualization();
    }
    updateExplanation();
}

void CrossEntropyWidget::updateExplanation()
{
    if (modeSelector->currentIndex() == 0) {
        explanationText->setHtml(
            "<h3>Binary Cross-Entropy Loss</h3>"
            "<p><b>Formula:</b> H(p,q) = -[p·log(q) + (1-p)·log(1-q)]</p>"
            "<p><b>Why use it?</b></p>"
            "<ul>"
            "<li><b>Penalizes confidence:</b> Wrong predictions with high confidence receive heavy penalties</li>"
            "<li><b>Gradient behavior:</b> Provides strong gradients when predictions are wrong, weak when right</li>"
            "<li><b>Probabilistic interpretation:</b> Equivalent to negative log-likelihood</li>"
            "<li><b>Convex:</b> Guaranteed to find global minimum during optimization</li>"
            "</ul>"
            "<p><b>Key insight:</b> When p=1, loss is -log(q). As q→0, loss→∞. This heavily penalizes "
            "confident wrong predictions!</p>"
        );
    } else {
        explanationText->setHtml(
            "<h3>Categorical Cross-Entropy Loss</h3>"
            "<p><b>Formula:</b> H(p,q) = -Σ p<sub>i</sub> · log(q<sub>i</sub>)</p>"
            "<p><b>Why use it?</b></p>"
            "<ul>"
            "<li><b>Multi-class generalization:</b> Extends binary cross-entropy to multiple classes</li>"
            "<li><b>Information theory:</b> Measures information 'surprise' between distributions</li>"
            "<li><b>Softmax pairing:</b> Works perfectly with softmax activation for probability outputs</li>"
            "<li><b>Maximum likelihood:</b> Minimizing cross-entropy = maximizing likelihood of correct class</li>"
            "</ul>"
            "<p><b>Key insight:</b> Only the true class contributes to loss. If true class has p=1 and "
            "predicted q=0.1, loss = -log(0.1) ≈ 2.3 (very high penalty).</p>"
        );
    }
}

void CrossEntropyWidget::exportData()
{
    QString fileName = QFileDialog::getSaveFileName(this, "Export Cross-Entropy Data", "", "CSV Files (*.csv)");
    if (fileName.isEmpty()) return;
    
    QFile file(fileName);
    if (!file.open(QIODevice::WriteOnly | QIODevice::Text)) return;
    
    QTextStream out(&file);
    
    if (modeSelector->currentIndex() == 0) {
        out << "Predicted Probability,Loss\n";
        double trueLabel = trueLabelSlider->value() / 100.0;
        
        for (int p = 1; p < 100; ++p) {
            double predicted = p / 100.0;
            double loss = calculateBinaryCrossEntropy(trueLabel, predicted);
            out << predicted << "," << loss << "\n";
        }
    } else {
        out << "Class,True Probability,Predicted Probability\n";
        for (size_t i = 0; i < trueProbSliders.size(); ++i) {
            out << i << ","
                << trueProbSliders[i]->value() / 100.0 << ","
                << predictedProbSliders[i]->value() / 100.0 << "\n";
        }
    }
    
    file.close();
}

void CrossEntropyWidget::addCategory() {}
void CrossEntropyWidget::removeCategory() {}
