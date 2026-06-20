#ifndef CONFUSIONMATRIXWIDGET_H
#define CONFUSIONMATRIXWIDGET_H

#include <QWidget>
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QLabel>
#include <QPushButton>
#include <QTextEdit>
#include <QGroupBox>
#include <QSpinBox>
#include <QTableWidget>
#include <QHeaderView>
#include <QtCharts/QChartView>
#include <QtCharts/QBarSeries>
#include <QtCharts/QBarSet>
#include <QtCharts/QBarCategoryAxis>
#include <QtCharts/QValueAxis>
#include <vector>

QT_CHARTS_USE_NAMESPACE

/**
 * ConfusionMatrixWidget - Classification Metrics Visualizer
 * 
 * WHAT IS A CONFUSION MATRIX?
 * A table showing predicted vs actual classifications:
 * 
 *                  Predicted
 *              Positive | Negative
 * Actual  Pos     TP    |    FN
 *         Neg     FP    |    TN
 * 
 * KEY METRICS:
 * 
 * ACCURACY = (TP + TN) / Total
 * - Overall correctness, but misleading with imbalanced classes!
 * 
 * PRECISION = TP / (TP + FP)
 * - "Of predicted positives, how many were correct?"
 * - Important when false positives are costly (spam detection)
 * 
 * RECALL (Sensitivity) = TP / (TP + FN)
 * - "Of actual positives, how many did we catch?"
 * - Important when false negatives are costly (disease detection)
 * 
 * F1-SCORE = 2 × (Precision × Recall) / (Precision + Recall)
 * - Harmonic mean, balances precision and recall
 * 
 * SPECIFICITY = TN / (TN + FP)
 * - True negative rate
 * 
 * WHY IT MATTERS:
 * - Accuracy alone is insufficient (99% accuracy with 1% positive class is trivial!)
 * - Different metrics for different problems
 * - Medical: High recall (catch all diseases)
 * - Spam: High precision (don't mark real emails as spam)
 */
class ConfusionMatrixWidget : public QWidget
{
    Q_OBJECT

public:
    explicit ConfusionMatrixWidget(QWidget *parent = nullptr);
    ~ConfusionMatrixWidget();

private slots:
    void updateMetrics();
    void exportData();
    void generateRandomMatrix();
    void loadExampleScenario(int index);

private:
    struct Metrics {
        double accuracy;
        double precision;
        double recall;
        double f1Score;
        double specificity;
        double falsePositiveRate;
        double falseNegativeRate;
        double matthewsCC;  // Matthews Correlation Coefficient
    };
    
    // UI Components
    QTableWidget *confusionTable;
    QChartView *metricsChartView;
    QChart *metricsChart;
    QTextEdit *explanationText;
    QPushButton *exportButton;
    QPushButton *randomButton;
    
    // Input spinboxes
    QSpinBox *tpSpin;
    QSpinBox *fpSpin;
    QSpinBox *fnSpin;
    QSpinBox *tnSpin;
    
    // Metric labels
    QLabel *accuracyLabel;
    QLabel *precisionLabel;
    QLabel *recallLabel;
    QLabel *f1Label;
    QLabel *specificityLabel;
    QLabel *fprLabel;
    QLabel *fnrLabel;
    QLabel *mccLabel;
    QLabel *totalLabel;
    
    // ROC curve info
    QLabel *rocPointLabel;
    
    // Methods
    void setupUI();
    void setupConfusionTable();
    void setupMetricsDisplay();
    Metrics calculateMetrics(int tp, int fp, int fn, int tn);
    void updateMetricsChart();
    void updateConfusionMatrixDisplay();
    void updateExplanation();
    void highlightBestMetric();
    
    // Example scenarios
    struct Scenario {
        QString name;
        int tp, fp, fn, tn;
        QString description;
    };
    std::vector<Scenario> getExampleScenarios();
};

#endif // CONFUSIONMATRIXWIDGET_H
