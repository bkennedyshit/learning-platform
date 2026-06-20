#include "ConfusionMatrixWidget.h"
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QFormLayout>
#include <QGridLayout>
#include <QFileDialog>
#include <QTextStream>
#include <QComboBox>
#include <QRandomGenerator>
#include <cmath>
#include <algorithm>

ConfusionMatrixWidget::ConfusionMatrixWidget(QWidget *parent)
    : QWidget(parent)
    , metricsChart(new QChart())
    , metricsChartView(new QChartView(metricsChart))
{
    setupUI();
    updateMetrics();
}

ConfusionMatrixWidget::~ConfusionMatrixWidget()
{
}

void ConfusionMatrixWidget::setupUI()
{
    QVBoxLayout *mainLayout = new QVBoxLayout(this);
    
    // Header
    QHBoxLayout *headerLayout = new QHBoxLayout();
    QLabel *titleLabel = new QLabel("<h2>Confusion Matrix & Classification Metrics</h2>");
    headerLayout->addWidget(titleLabel);
    headerLayout->addStretch();
    
    // Example scenarios dropdown
    QComboBox *scenarioSelector = new QComboBox();
    scenarioSelector->addItem("Custom");
    for (const auto& scenario : getExampleScenarios()) {
        scenarioSelector->addItem(scenario.name);
    }
    connect(scenarioSelector, QOverload<int>::of(&QComboBox::currentIndexChanged),
            this, &ConfusionMatrixWidget::loadExampleScenario);
    headerLayout->addWidget(new QLabel("Examples:"));
    headerLayout->addWidget(scenarioSelector);
    
    mainLayout->addLayout(headerLayout);
    
    // Main content layout
    QHBoxLayout *contentLayout = new QHBoxLayout();
    
    // Left side: Confusion matrix input
    QVBoxLayout *leftLayout = new QVBoxLayout();
    
    QGroupBox *matrixGroup = new QGroupBox("Confusion Matrix Input");
    QVBoxLayout *matrixLayout = new QVBoxLayout(matrixGroup);
    
    // Create confusion matrix table
    confusionTable = new QTableWidget(2, 2);
    confusionTable->setHorizontalHeaderLabels(QStringList() << "Predicted: Positive" << "Predicted: Negative");
    confusionTable->setVerticalHeaderLabels(QStringList() << "Actual: Positive" << "Actual: Negative");
    confusionTable->horizontalHeader()->setSectionResizeMode(QHeaderView::Stretch);
    confusionTable->verticalHeader()->setSectionResizeMode(QHeaderView::Stretch);
    confusionTable->setMaximumHeight(200);
    
    // Create spinboxes for each cell
    tpSpin = new QSpinBox();
    tpSpin->setRange(0, 1000000);
    tpSpin->setValue(85);
    tpSpin->setAlignment(Qt::AlignCenter);
    connect(tpSpin, QOverload<int>::of(&QSpinBox::valueChanged),
            this, &ConfusionMatrixWidget::updateMetrics);
    confusionTable->setCellWidget(0, 0, tpSpin);
    
    fnSpin = new QSpinBox();
    fnSpin->setRange(0, 1000000);
    fnSpin->setValue(15);
    fnSpin->setAlignment(Qt::AlignCenter);
    connect(fnSpin, QOverload<int>::of(&QSpinBox::valueChanged),
            this, &ConfusionMatrixWidget::updateMetrics);
    confusionTable->setCellWidget(0, 1, fnSpin);
    
    fpSpin = new QSpinBox();
    fpSpin->setRange(0, 1000000);
    fpSpin->setValue(10);
    fpSpin->setAlignment(Qt::AlignCenter);
    connect(fpSpin, QOverload<int>::of(&QSpinBox::valueChanged),
            this, &ConfusionMatrixWidget::updateMetrics);
    confusionTable->setCellWidget(1, 0, fpSpin);
    
    tnSpin = new QSpinBox();
    tnSpin->setRange(0, 1000000);
    tnSpin->setValue(90);
    tnSpin->setAlignment(Qt::AlignCenter);
    connect(tnSpin, QOverload<int>::of(&QSpinBox::valueChanged),
            this, &ConfusionMatrixWidget::updateMetrics);
    confusionTable->setCellWidget(1, 1, tnSpin);
    
    matrixLayout->addWidget(confusionTable);
    
    // Legend
    QLabel *legendLabel = new QLabel(
        "<b>TP</b>=True Positives  <b>FP</b>=False Positives<br>"
        "<b>FN</b>=False Negatives  <b>TN</b>=True Negatives"
    );
    legendLabel->setAlignment(Qt::AlignCenter);
    matrixLayout->addWidget(legendLabel);
    
    leftLayout->addWidget(matrixGroup);
    
    // Metrics display
    setupMetricsDisplay();
    
    // Buttons
    randomButton = new QPushButton("Generate Random");
    connect(randomButton, &QPushButton::clicked, this, &ConfusionMatrixWidget::generateRandomMatrix);
    leftLayout->addWidget(randomButton);
    
    exportButton = new QPushButton("Export Metrics");
    connect(exportButton, &QPushButton::clicked, this, &ConfusionMatrixWidget::exportData);
    leftLayout->addWidget(exportButton);
    
    leftLayout->addStretch();
    contentLayout->addLayout(leftLayout, 1);
    
    // Right side: Metrics visualization
    QVBoxLayout *rightLayout = new QVBoxLayout();
    
    QLabel *chartLabel = new QLabel("<b>Metrics Visualization</b>");
    rightLayout->addWidget(chartLabel);
    
    metricsChartView->setRenderHint(QPainter::Antialiasing);
    metricsChartView->setMinimumHeight(300);
    rightLayout->addWidget(metricsChartView);
    
    // ROC point display
    rocPointLabel = new QLabel();
    rocPointLabel->setAlignment(Qt::AlignCenter);
    QFont rocFont = rocPointLabel->font();
    rocFont.setPointSize(10);
    rocPointLabel->setFont(rocFont);
    rightLayout->addWidget(rocPointLabel);
    
    contentLayout->addLayout(rightLayout, 1);
    
    mainLayout->addLayout(contentLayout);
    
    // Bottom: Explanation
    explanationText = new QTextEdit();
    explanationText->setReadOnly(true);
    explanationText->setMaximumHeight(150);
    mainLayout->addWidget(explanationText);
    
    updateExplanation();
}

void ConfusionMatrixWidget::setupMetricsDisplay()
{
    QGroupBox *metricsGroup = new QGroupBox("Classification Metrics");
    QFormLayout *metricsLayout = new QFormLayout(metricsGroup);
    
    QFont boldFont;
    boldFont.setBold(true);
    boldFont.setPointSize(10);
    
    totalLabel = new QLabel("200");
    metricsLayout->addRow("Total Samples:", totalLabel);
    
    accuracyLabel = new QLabel("0.000");
    accuracyLabel->setFont(boldFont);
    metricsLayout->addRow("Accuracy:", accuracyLabel);
    
    precisionLabel = new QLabel("0.000");
    precisionLabel->setFont(boldFont);
    metricsLayout->addRow("Precision:", precisionLabel);
    
    recallLabel = new QLabel("0.000");
    recallLabel->setFont(boldFont);
    metricsLayout->addRow("Recall (Sensitivity):", recallLabel);
    
    f1Label = new QLabel("0.000");
    f1Label->setFont(boldFont);
    metricsLayout->addRow("F1-Score:", f1Label);
    
    specificityLabel = new QLabel("0.000");
    metricsLayout->addRow("Specificity:", specificityLabel);
    
    fprLabel = new QLabel("0.000");
    metricsLayout->addRow("False Positive Rate:", fprLabel);
    
    fnrLabel = new QLabel("0.000");
    metricsLayout->addRow("False Negative Rate:", fnrLabel);
    
    mccLabel = new QLabel("0.000");
    metricsLayout->addRow("Matthews Corr Coef:", mccLabel);
    
    QVBoxLayout* leftLayout = qobject_cast<QVBoxLayout*>(
        qobject_cast<QHBoxLayout*>(parentWidget()->layout()->itemAt(1))->itemAt(0));
    if (leftLayout) {
        leftLayout->insertWidget(1, metricsGroup);
    }
}

ConfusionMatrixWidget::Metrics ConfusionMatrixWidget::calculateMetrics(int tp, int fp, int fn, int tn)
{
    Metrics m;
    
    double total = tp + fp + fn + tn;
    if (total == 0) {
        m.accuracy = m.precision = m.recall = m.f1Score = 0;
        m.specificity = m.falsePositiveRate = m.falseNegativeRate = 0;
        m.matthewsCC = 0;
        return m;
    }
    
    // Accuracy
    m.accuracy = (tp + tn) / total;
    
    // Precision
    m.precision = (tp + fp > 0) ? static_cast<double>(tp) / (tp + fp) : 0;
    
    // Recall (Sensitivity, True Positive Rate)
    m.recall = (tp + fn > 0) ? static_cast<double>(tp) / (tp + fn) : 0;
    
    // F1-Score
    m.f1Score = (m.precision + m.recall > 0) ? 
                2 * (m.precision * m.recall) / (m.precision + m.recall) : 0;
    
    // Specificity (True Negative Rate)
    m.specificity = (tn + fp > 0) ? static_cast<double>(tn) / (tn + fp) : 0;
    
    // False Positive Rate
    m.falsePositiveRate = 1.0 - m.specificity;
    
    // False Negative Rate
    m.falseNegativeRate = 1.0 - m.recall;
    
    // Matthews Correlation Coefficient
    double numerator = static_cast<double>(tp * tn - fp * fn);
    double denominator = std::sqrt(static_cast<double>(tp + fp) * (tp + fn) * (tn + fp) * (tn + fn));
    m.matthewsCC = (denominator > 0) ? numerator / denominator : 0;
    
    return m;
}

void ConfusionMatrixWidget::updateMetrics()
{
    int tp = tpSpin->value();
    int fp = fpSpin->value();
    int fn = fnSpin->value();
    int tn = tnSpin->value();
    
    Metrics m = calculateMetrics(tp, fp, fn, tn);
    
    // Update labels
    totalLabel->setText(QString::number(tp + fp + fn + tn));
    accuracyLabel->setText(QString::number(m.accuracy, 'f', 4));
    precisionLabel->setText(QString::number(m.precision, 'f', 4));
    recallLabel->setText(QString::number(m.recall, 'f', 4));
    f1Label->setText(QString::number(m.f1Score, 'f', 4));
    specificityLabel->setText(QString::number(m.specificity, 'f', 4));
    fprLabel->setText(QString::number(m.falsePositiveRate, 'f', 4));
    fnrLabel->setText(QString::number(m.falseNegativeRate, 'f', 4));
    mccLabel->setText(QString::number(m.matthewsCC, 'f', 4));
    
    // Update ROC point
    rocPointLabel->setText(QString("ROC Point: (FPR=%.3f, TPR=%.3f)")
                          .arg(m.falsePositiveRate)
                          .arg(m.recall));
    
    updateMetricsChart();
    highlightBestMetric();
}

void ConfusionMatrixWidget::updateMetricsChart()
{
    metricsChart->removeAllSeries();
    
    int tp = tpSpin->value();
    int fp = fpSpin->value();
    int fn = fnSpin->value();
    int tn = tnSpin->value();
    
    Metrics m = calculateMetrics(tp, fp, fn, tn);
    
    // Create bar chart for metrics
    QBarSet *metricsSet = new QBarSet("Metrics");
    *metricsSet << m.accuracy << m.precision << m.recall << m.f1Score 
                << m.specificity << std::abs(m.matthewsCC);
    
    QBarSeries *series = new QBarSeries();
    series->append(metricsSet);
    
    QStringList categories;
    categories << "Accuracy" << "Precision" << "Recall" << "F1-Score" 
               << "Specificity" << "|MCC|";
    
    metricsChart->addSeries(series);
    
    QBarCategoryAxis *axisX = new QBarCategoryAxis();
    axisX->append(categories);
    metricsChart->addAxis(axisX, Qt::AlignBottom);
    series->attachAxis(axisX);
    
    QValueAxis *axisY = new QValueAxis();
    axisY->setTitleText("Score");
    axisY->setRange(0, 1.0);
    metricsChart->addAxis(axisY, Qt::AlignLeft);
    series->attachAxis(axisY);
    
    metricsChart->setTitle("Classification Metrics Comparison");
    metricsChart->legend()->setVisible(false);
}

void ConfusionMatrixWidget::highlightBestMetric()
{
    // Reset colors
    accuracyLabel->setStyleSheet("");
    precisionLabel->setStyleSheet("");
    recallLabel->setStyleSheet("");
    f1Label->setStyleSheet("");
    
    // Highlight the best metric (F1 usually most balanced)
    double f1 = f1Label->text().toDouble();
    if (f1 >= 0.9) {
        f1Label->setStyleSheet("color: green;");
    } else if (f1 >= 0.7) {
        f1Label->setStyleSheet("color: orange;");
    } else {
        f1Label->setStyleSheet("color: red;");
    }
}

void ConfusionMatrixWidget::generateRandomMatrix()
{
    int total = QRandomGenerator::global()->bounded(100, 1000);
    
    // Generate with some reasonable distribution
    int positives = QRandomGenerator::global()->bounded(total / 4, 3 * total / 4);
    int negatives = total - positives;
    
    double accuracy = 0.6 + QRandomGenerator::global()->generateDouble() * 0.35; // 60-95% accuracy
    
    int tp = static_cast<int>(positives * (accuracy + QRandomGenerator::global()->generateDouble() * 0.1));
    tp = std::min(tp, positives);
    int fn = positives - tp;
    
    int tn = static_cast<int>(negatives * (accuracy + QRandomGenerator::global()->generateDouble() * 0.1));
    tn = std::min(tn, negatives);
    int fp = negatives - tn;
    
    tpSpin->setValue(tp);
    fpSpin->setValue(fp);
    fnSpin->setValue(fn);
    tnSpin->setValue(tn);
}

std::vector<ConfusionMatrixWidget::Scenario> ConfusionMatrixWidget::getExampleScenarios()
{
    return {
        {"Perfect Classifier", 100, 0, 0, 100, 
         "All predictions correct - ideal scenario"},
        {"High Precision, Low Recall", 40, 5, 60, 95,
         "Few false positives, many false negatives - conservative classifier"},
        {"High Recall, Low Precision", 90, 50, 10, 50,
         "Few false negatives, many false positives - aggressive classifier"},
        {"Balanced (Good F1)", 85, 15, 15, 85,
         "Good balance between precision and recall"},
        {"Imbalanced Dataset", 5, 10, 5, 980,
         "Rare positive class - accuracy is misleading!"},
        {"Random Classifier", 50, 50, 50, 50,
         "No better than random guessing"},
        {"Medical Screening", 95, 200, 5, 700,
         "High recall critical - don't miss diseases"},
        {"Spam Filter", 180, 5, 20, 795,
         "High precision critical - don't flag real emails"}
    };
}

void ConfusionMatrixWidget::loadExampleScenario(int index)
{
    if (index == 0) return; // "Custom" option
    
    auto scenarios = getExampleScenarios();
    if (index - 1 >= 0 && index - 1 < static_cast<int>(scenarios.size())) {
        const Scenario& s = scenarios[index - 1];
        
        tpSpin->setValue(s.tp);
        fpSpin->setValue(s.fp);
        fnSpin->setValue(s.fn);
        tnSpin->setValue(s.tn);
        
        // Update explanation with scenario context
        updateExplanation();
        explanationText->append(QString("<p><b>Scenario:</b> %1<br><i>%2</i></p>")
                               .arg(s.name)
                               .arg(s.description));
    }
}

void ConfusionMatrixWidget::updateExplanation()
{
    explanationText->setHtml(
        "<h3>Understanding Classification Metrics</h3>"
        "<p><b>Which metric to optimize?</b></p>"
        "<ul>"
        "<li><b>Accuracy:</b> Overall correct, but <span style='color:red;'>MISLEADING with imbalanced data!</span></li>"
        "<li><b>Precision:</b> Minimize false positives (spam detection, recommender systems)</li>"
        "<li><b>Recall:</b> Minimize false negatives (disease detection, fraud detection)</li>"
        "<li><b>F1-Score:</b> Balanced metric when you care about both precision and recall</li>"
        "<li><b>MCC:</b> Best for imbalanced datasets, ranges from -1 (worst) to +1 (perfect)</li>"
        "</ul>"
        "<p><b>Trade-off:</b> Precision ↑ usually means Recall ↓ (adjust threshold to balance)</p>"
    );
}

void ConfusionMatrixWidget::exportData()
{
    QString fileName = QFileDialog::getSaveFileName(this, "Export Confusion Matrix", "", "CSV Files (*.csv)");
    if (fileName.isEmpty()) return;
    
    QFile file(fileName);
    if (!file.open(QIODevice::WriteOnly | QIODevice::Text)) return;
    
    QTextStream out(&file);
    
    int tp = tpSpin->value();
    int fp = fpSpin->value();
    int fn = fnSpin->value();
    int tn = tnSpin->value();
    
    Metrics m = calculateMetrics(tp, fp, fn, tn);
    
    out << "=== Confusion Matrix ===\n";
    out << ",Predicted Positive,Predicted Negative\n";
    out << "Actual Positive," << tp << "," << fn << "\n";
    out << "Actual Negative," << fp << "," << tn << "\n\n";
    
    out << "=== Metrics ===\n";
    out << "Total Samples," << (tp + fp + fn + tn) << "\n";
    out << "Accuracy," << m.accuracy << "\n";
    out << "Precision," << m.precision << "\n";
    out << "Recall," << m.recall << "\n";
    out << "F1-Score," << m.f1Score << "\n";
    out << "Specificity," << m.specificity << "\n";
    out << "False Positive Rate," << m.falsePositiveRate << "\n";
    out << "False Negative Rate," << m.falseNegativeRate << "\n";
    out << "Matthews Correlation Coefficient," << m.matthewsCC << "\n";
    
    file.close();
}
