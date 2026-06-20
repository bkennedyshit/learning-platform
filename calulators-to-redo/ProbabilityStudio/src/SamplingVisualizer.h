#ifndef SAMPLINGVISUALIZER_H
#define SAMPLINGVISUALIZER_H

#include <QWidget>
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QSlider>
#include <QLabel>
#include <QPushButton>
#include <QComboBox>
#include <QTextEdit>
#include <QGroupBox>
#include <QSpinBox>
#include <QTimer>
#include <QtCharts/QChartView>
#include <QtCharts/QLineSeries>
#include <QtCharts/QScatterSeries>
#include <QtCharts/QBarSeries>
#include <QtCharts/QBarSet>
#include <QtCharts/QValueAxis>
#include <QtCharts/QBarCategoryAxis>
#include <vector>
#include <random>

QT_CHARTS_USE_NAMESPACE

/**
 * SamplingVisualizer - Central Limit Theorem and Law of Large Numbers
 * 
 * CENTRAL LIMIT THEOREM (CLT):
 * Given n i.i.d. random variables X₁, X₂, ..., Xₙ with mean μ and variance σ²,
 * the distribution of (X̄ₙ - μ)/(σ/√n) approaches N(0,1) as n→∞
 * 
 * KEY INSIGHT: Sample means become normally distributed regardless of 
 * the original distribution! This is WHY normal distributions are everywhere.
 * 
 * LAW OF LARGE NUMBERS (LLN):
 * As sample size n→∞, sample mean X̄ₙ converges to population mean μ
 * 
 * PRACTICAL IMPLICATIONS:
 * - Why bootstrapping works
 * - Foundation of hypothesis testing
 * - Justifies normal approximations
 * - Monte Carlo simulation validity
 * - Confidence interval construction
 */
class SamplingVisualizer : public QWidget
{
    Q_OBJECT

public:
    explicit SamplingVisualizer(QWidget *parent = nullptr);
    ~SamplingVisualizer();

private slots:
    void updateVisualization();
    void onModeChanged(int index);
    void onDistributionChanged(int index);
    void startAnimation();
    void stopAnimation();
    void resetSimulation();
    void animationStep();
    void exportData();

private:
    enum Mode {
        CLT_MODE,
        LLN_MODE
    };
    
    enum SourceDist {
        UNIFORM_DIST,
        EXPONENTIAL_DIST,
        BIMODAL_DIST,
        DISCRETE_DIST
    };
    
    // UI Components
    QComboBox *modeSelector;
    QComboBox *distributionSelector;
    QChartView *sourceChartView;
    QChartView *resultChartView;
    QChart *sourceChart;
    QChart *resultChart;
    QTextEdit *explanationText;
    
    // Controls
    QSpinBox *sampleSizeSpinBox;
    QSpinBox *numSamplesSpinBox;
    QLabel *currentMeanLabel;
    QLabel *theoreticalMeanLabel;
    QLabel *currentStdLabel;
    QLabel *theoreticalStdLabel;
    QPushButton *animateButton;
    QPushButton *stopButton;
    QPushButton *resetButton;
    QPushButton *exportButton;
    
    // Animation
    QTimer *animationTimer;
    int currentSampleCount;
    std::vector<double> sampleMeans;
    std::vector<double> runningMeans;
    
    // Random number generation
    std::mt19937 rng;
    
    // Statistics
    double populationMean;
    double populationStd;
    
    // Methods
    void setupUI();
    void setupSourceChart();
    void setupResultChart();
    void updateSourceDistribution();
    void updateCLTVisualization();
    void updateLLNVisualization();
    void updateExplanation();
    void updateStatistics();
    
    // Sampling methods
    double sampleFromDistribution(SourceDist dist);
    std::vector<double> generateSourceSamples(int n);
    double calculateSampleMean(const std::vector<double>& samples);
    double calculateStdDev(const std::vector<double>& samples, double mean);
    
    // Distribution generation
    std::vector<double> generateDistributionPDF(SourceDist dist, int numPoints = 100);
};

#endif // SAMPLINGVISUALIZER_H
