#ifndef DISTRIBUTIONWIDGET_H
#define DISTRIBUTIONWIDGET_H

#include <QWidget>
#include <QComboBox>
#include <QSlider>
#include <QLabel>
#include <QTabWidget>
#include <QVBoxLayout>

namespace QtCharts {
    class QChart;
    class QChartView;
    class QLineSeries;
}

class DistributionWidget : public QWidget
{
    Q_OBJECT

public:
    explicit DistributionWidget(QWidget *parent = nullptr);
    ~DistributionWidget();

private slots:
    void onDistributionChanged(int index);
    void onParam1Changed(int value);
    void onParam2Changed(int value);
    void updatePlot();

private:
    void setupUI();
    void updateParameterControls();
    double normalPDF(double x, double mu, double sigma);
    double normalCDF(double x, double mu, double sigma);
    double binomialPMF(int k, int n, double p);
    double binomialCDF(int k, int n, double p);
    double poissonPMF(int k, double lambda);
    double poissonCDF(int k, double lambda);
    double exponentialPDF(double x, double lambda);
    double exponentialCDF(double x, double lambda);
    double uniformPDF(double x, double a, double b);
    double uniformCDF(double x, double a, double b);
    double erf(double x);  // Error function for normal CDF
    long long factorial(int n);
    long long binomialCoeff(int n, int k);

    QComboBox *distributionCombo;
    QSlider *param1Slider;
    QSlider *param2Slider;
    QLabel *param1Label;
    QLabel *param2Label;
    QLabel *param1Value;
    QLabel *param2Value;
    QLabel *meanLabel;
    QLabel *varianceLabel;
    QLabel *infoLabel;
    
    QTabWidget *tabWidget;
    QtCharts::QChartView *pdfChartView;
    QtCharts::QChartView *cdfChartView;
    QtCharts::QChart *pdfChart;
    QtCharts::QChart *cdfChart;
    
    enum Distribution {
        Normal,
        Binomial,
        Poisson,
        Exponential,
        Uniform
    };
    
    Distribution currentDist;
    double param1;  // μ for Normal, n for Binomial, λ for Poisson, λ for Exponential, a for Uniform
    double param2;  // σ for Normal, p for Binomial, unused for Poisson, unused for Exponential, b for Uniform
};

#endif // DISTRIBUTIONWIDGET_H
