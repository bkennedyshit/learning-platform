#ifndef HYPOTHESISTESTWIDGET_H
#define HYPOTHESISTESTWIDGET_H

#include <QWidget>
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QSlider>
#include <QLabel>
#include <QPushButton>
#include <QComboBox>
#include <QTextEdit>
#include <QGroupBox>
#include <QDoubleSpinBox>
#include <QSpinBox>
#include <QLineEdit>
#include <QtCharts/QChartView>
#include <QtCharts/QLineSeries>
#include <QtCharts/QAreaSeries>
#include <QtCharts/QValueAxis>
#include <vector>

QT_CHARTS_USE_NAMESPACE

/**
 * HypothesisTestWidget - Statistical Hypothesis Testing Calculator
 * 
 * WHAT IS HYPOTHESIS TESTING?
 * A framework for making decisions about population parameters using sample data.
 * 
 * NULL HYPOTHESIS (H₀): The "status quo" or "no effect" claim
 * ALTERNATIVE HYPOTHESIS (H₁): What we're trying to prove
 * 
 * P-VALUE: Probability of observing data this extreme if H₀ is true
 * - p < 0.05: "Statistically significant" (reject H₀)
 * - p ≥ 0.05: "Not significant" (fail to reject H₀)
 * 
 * TEST TYPES:
 * - t-test: Compare means with unknown population variance
 * - z-test: Compare means with known population variance (large n)
 * 
 * CONFIDENCE INTERVALS:
 * Range of plausible values for population parameter
 * 95% CI: We're 95% confident true value lies within this range
 * 
 * WHY IT MATTERS IN ML:
 * - A/B testing: Is new model significantly better?
 * - Feature selection: Is correlation real or random?
 * - Model comparison: Statistical significance of performance difference
 * - Hyperparameter tuning: Are results meaningful or noise?
 */
class HypothesisTestWidget : public QWidget
{
    Q_OBJECT

public:
    explicit HypothesisTestWidget(QWidget *parent = nullptr);
    ~HypothesisTestWidget();

private slots:
    void updateVisualization();
    void onTestTypeChanged(int index);
    void exportData();
    void calculateTest();

private:
    enum TestType {
        ONE_SAMPLE_T,
        TWO_SAMPLE_T,
        Z_TEST,
        PAIRED_T
    };
    
    enum TailType {
        TWO_TAILED,
        LEFT_TAILED,
        RIGHT_TAILED
    };
    
    // UI Components
    QComboBox *testTypeSelector;
    QComboBox *tailTypeSelector;
    QChartView *chartView;
    QChart *chart;
    QTextEdit *explanationText;
    QPushButton *exportButton;
    QPushButton *calculateButton;
    
    // Test parameters
    QGroupBox *parametersGroup;
    QDoubleSpinBox *sampleMeanSpin;
    QDoubleSpinBox *sampleStdSpin;
    QSpinBox *sampleSizeSpin;
    QDoubleSpinBox *nullMeanSpin;
    QDoubleSpinBox *alpha Spin;
    
    // Two-sample specific
    QDoubleSpinBox *sampleMean2Spin;
    QDoubleSpinBox *sampleStd2Spin;
    QSpinBox *sampleSize2Spin;
    QLabel *sampleMean2Label;
    QLabel *sampleStd2Label;
    QLabel *sampleSize2Label;
    
    // Z-test specific
    QDoubleSpinBox *popStdSpin;
    QLabel *popStdLabel;
    
    // Results display
    QGroupBox *resultsGroup;
    QLabel *testStatisticValue;
    QLabel *pValueLabel;
    QLabel *criticalValueLabel;
    QLabel *confidenceIntervalLabel;
    QLabel *decisionLabel;
    
    // Calculation methods
    double calculateOneSampleT(double sampleMean, double sampleStd, int n, double nullMean);
    double calculateTwoSampleT(double mean1, double std1, int n1, 
                              double mean2, double std2, int n2);
    double calculateZTest(double sampleMean, double popStd, int n, double nullMean);
    double calculatePValue(double testStat, int df, TailType tail, bool useTDist);
    double calculateCriticalValue(double alpha, int df, TailType tail, bool useTDist);
    std::pair<double, double> calculateConfidenceInterval(double mean, double std, int n, 
                                                          double alpha, bool useTDist);
    
    // Statistical functions
    double tCDF(double x, int df);
    double normalCDF(double x);
    double tQuantile(double p, int df);
    double normalQuantile(double p);
    
    // Visualization methods
    void updateChart();
    void plotDistribution(double testStat, double criticalValue, int df, bool useTDist);
    
    // UI setup methods
    void setupUI();
    void setupParameterControls();
    void updateParameterVisibility();
    void updateExplanation();
    void displayResults();
};

#endif // HYPOTHESISTESTWIDGET_H
