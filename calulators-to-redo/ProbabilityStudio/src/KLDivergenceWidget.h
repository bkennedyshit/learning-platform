#ifndef KLDIVERGENCEWIDGET_H
#define KLDIVERGENCEWIDGET_H

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
#include <QtCharts/QChartView>
#include <QtCharts/QLineSeries>
#include <QtCharts/QAreaSeries>
#include <QtCharts/QValueAxis>
#include <vector>

QT_CHARTS_USE_NAMESPACE

/**
 * KLDivergenceWidget - Kullback-Leibler Divergence Visualization
 * 
 * WHAT IS KL DIVERGENCE?
 * KL divergence D_KL(P||Q) measures how much probability distribution Q 
 * diverges from reference distribution P. It's the "extra bits" needed to encode
 * samples from P when using a code optimized for Q.
 * 
 * Formula: D_KL(P||Q) = Σ P(x) * log(P(x)/Q(x))
 * 
 * KEY PROPERTIES:
 * 1. NOT symmetric: D_KL(P||Q) ≠ D_KL(Q||P)
 * 2. Always ≥ 0, equals 0 only when P = Q
 * 3. Not a true distance metric (no triangle inequality)
 * 
 * WHY IT MATTERS IN ML:
 * - Variational inference (ELBO optimization)
 * - Model comparison and selection
 * - Regularization (e.g., KL penalty in VAEs)
 * - Measuring distribution shift
 * - Policy optimization in RL (trust region methods)
 */
class KLDivergenceWidget : public QWidget
{
    Q_OBJECT

public:
    explicit KLDivergenceWidget(QWidget *parent = nullptr);
    ~KLDivergenceWidget();

private slots:
    void updateVisualization();
    void onDistributionTypeChanged(int index);
    void exportData();
    void swapDistributions();

private:
    // Distribution types
    enum DistType {
        NORMAL,
        EXPONENTIAL,
        UNIFORM,
        BETA
    };
    
    // UI Components
    QComboBox *distPSelector;
    QComboBox *distQSelector;
    QChartView *chartView;
    QChart *chart;
    QTextEdit *explanationText;
    QPushButton *exportButton;
    QPushButton *swapButton;
    
    // Distribution P parameters
    QGroupBox *distPGroup;
    QDoubleSpinBox *pParam1Spin;
    QDoubleSpinBox *pParam2Spin;
    QLabel *pParam1Label;
    QLabel *pParam2Label;
    
    // Distribution Q parameters
    QGroupBox *distQGroup;
    QDoubleSpinBox *qParam1Spin;
    QDoubleSpinBox *qParam2Spin;
    QLabel *qParam1Label;
    QLabel *qParam2Label;
    
    // KL divergence displays
    QLabel *klPQValue;  // D_KL(P||Q)
    QLabel *klQPValue;  // D_KL(Q||P)
    QLabel *asymmetryValue;
    
    // Calculation methods
    double calculateKLDivergence(DistType distP, const std::vector<double>& paramsP,
                                 DistType distQ, const std::vector<double>& paramsQ);
    double calculateKLNumerical(const std::vector<double>& P, const std::vector<double>& Q);
    
    // Distribution generation
    std::vector<double> generateDistribution(DistType type, const std::vector<double>& params,
                                             const std::vector<double>& xValues);
    double normalPDF(double x, double mu, double sigma);
    double exponentialPDF(double x, double lambda);
    double uniformPDF(double x, double a, double b);
    double betaPDF(double x, double alpha, double beta);
    
    // Analytical KL calculations
    double klNormalNormal(double mu1, double sigma1, double mu2, double sigma2);
    double klExponentialExponential(double lambda1, double lambda2);
    
    // Visualization methods
    void updateChart();
    
    // UI setup methods
    void setupUI();
    void setupDistributionControls();
    void updateParameterLabels();
    void updateExplanation();
};

#endif // KLDIVERGENCEWIDGET_H
