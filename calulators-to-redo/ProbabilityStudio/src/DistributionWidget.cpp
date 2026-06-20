#include "DistributionWidget.h"
#include <QtCharts/QChart>
#include <QtCharts/QChartView>
#include <QtCharts/QLineSeries>
#include <QtCharts/QValueAxis>
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QGridLayout>
#include <QGroupBox>
#include <cmath>
#include <algorithm>

using namespace QtCharts;

DistributionWidget::DistributionWidget(QWidget *parent)
    : QWidget(parent)
    , currentDist(Normal)
    , param1(0.0)
    , param2(1.0)
{
    setupUI();
    updateParameterControls();
    updatePlot();
}

DistributionWidget::~DistributionWidget()
{
}

void DistributionWidget::setupUI()
{
    QVBoxLayout *mainLayout = new QVBoxLayout(this);
    
    // Title
    QLabel *title = new QLabel("<h2>Probability Distribution Explorer</h2>");
    title->setAlignment(Qt::AlignCenter);
    mainLayout->addWidget(title);
    
    // Info label
    infoLabel = new QLabel("Explore common probability distributions used in ML and statistics");
    infoLabel->setWordWrap(true);
    infoLabel->setStyleSheet("QLabel { background-color: #e3f2fd; padding: 10px; border-radius: 5px; }");
    mainLayout->addWidget(infoLabel);
    
    // Controls
    QGroupBox *controlGroup = new QGroupBox("Distribution Parameters");
    QGridLayout *controlLayout = new QGridLayout(controlGroup);
    
    // Distribution selector
    controlLayout->addWidget(new QLabel("<b>Distribution:</b>"), 0, 0);
    distributionCombo = new QComboBox();
    distributionCombo->addItem("Normal (Gaussian)");
    distributionCombo->addItem("Binomial");
    distributionCombo->addItem("Poisson");
    distributionCombo->addItem("Exponential");
    distributionCombo->addItem("Uniform");
    connect(distributionCombo, QOverload<int>::of(&QComboBox::currentIndexChanged),
            this, &DistributionWidget::onDistributionChanged);
    controlLayout->addWidget(distributionCombo, 0, 1, 1, 2);
    
    // Parameter 1
    param1Label = new QLabel("μ (Mean):");
    controlLayout->addWidget(param1Label, 1, 0);
    param1Slider = new QSlider(Qt::Horizontal);
    param1Slider->setRange(-100, 100);
    param1Slider->setValue(0);
    connect(param1Slider, &QSlider::valueChanged, this, &DistributionWidget::onParam1Changed);
    controlLayout->addWidget(param1Slider, 1, 1);
    param1Value = new QLabel("0.0");
    param1Value->setMinimumWidth(60);
    controlLayout->addWidget(param1Value, 1, 2);
    
    // Parameter 2
    param2Label = new QLabel("σ (Std Dev):");
    controlLayout->addWidget(param2Label, 2, 0);
    param2Slider = new QSlider(Qt::Horizontal);
    param2Slider->setRange(10, 100);
    param2Slider->setValue(50);
    connect(param2Slider, &QSlider::valueChanged, this, &DistributionWidget::onParam2Changed);
    controlLayout->addWidget(param2Slider, 2, 1);
    param2Value = new QLabel("1.0");
    param2Value->setMinimumWidth(60);
    controlLayout->addWidget(param2Value, 2, 2);
    
    // Statistics
    meanLabel = new QLabel("<b>Mean:</b> 0.0");
    varianceLabel = new QLabel("<b>Variance:</b> 1.0");
    controlLayout->addWidget(meanLabel, 3, 0, 1, 2);
    controlLayout->addWidget(varianceLabel, 3, 2);
    
    mainLayout->addWidget(controlGroup);
    
    // Charts - PDF and CDF in tabs
    tabWidget = new QTabWidget();
    
    // PDF Chart
    pdfChart = new QChart();
    pdfChart->setTitle("Probability Density/Mass Function (PDF/PMF)");
    pdfChart->setAnimationOptions(QChart::SeriesAnimations);
    pdfChartView = new QChartView(pdfChart);
    pdfChartView->setRenderHint(QPainter::Antialiasing);
    tabWidget->addTab(pdfChartView, "PDF/PMF");
    
    // CDF Chart
    cdfChart = new QChart();
    cdfChart->setTitle("Cumulative Distribution Function (CDF)");
    cdfChart->setAnimationOptions(QChart::SeriesAnimations);
    cdfChartView = new QChartView(cdfChart);
    cdfChartView->setRenderHint(QPainter::Antialiasing);
    tabWidget->addTab(cdfChartView, "CDF");
    
    mainLayout->addWidget(tabWidget, 1);
}

void DistributionWidget::onDistributionChanged(int index)
{
    currentDist = static_cast<Distribution>(index);
    updateParameterControls();
    updatePlot();
}

void DistributionWidget::onParam1Changed(int value)
{
    switch (currentDist) {
        case Normal:
            param1 = value / 10.0;  // -10.0 to 10.0
            param1Value->setText(QString::number(param1, 'f', 1));
            break;
        case Binomial:
            param1 = value;  // n: 1 to 100
            param1Value->setText(QString::number(static_cast<int>(param1)));
            break;
        case Poisson:
            param1 = value / 10.0;  // λ: 0.1 to 10.0
            param1Value->setText(QString::number(param1, 'f', 1));
            break;
        case Exponential:
            param1 = value / 100.0;  // λ: 0.01 to 1.0
            param1Value->setText(QString::number(param1, 'f', 2));
            break;
        case Uniform:
            param1 = value / 10.0;  // a: -10.0 to 10.0
            param1Value->setText(QString::number(param1, 'f', 1));
            break;
    }
    updatePlot();
}

void DistributionWidget::onParam2Changed(int value)
{
    switch (currentDist) {
        case Normal:
            param2 = value / 50.0;  // σ: 0.2 to 2.0
            param2Value->setText(QString::number(param2, 'f', 2));
            break;
        case Binomial:
            param2 = value / 100.0;  // p: 0.1 to 1.0
            param2Value->setText(QString::number(param2, 'f', 2));
            break;
        case Uniform:
            param2 = value / 10.0;  // b: -10.0 to 10.0
            param2Value->setText(QString::number(param2, 'f', 1));
            break;
        default:
            break;
    }
    updatePlot();
}

void DistributionWidget::updateParameterControls()
{
    switch (currentDist) {
        case Normal:
            infoLabel->setText("📊 <b>Normal Distribution:</b> Bell-shaped, symmetric around mean. "
                             "Used in CNNs for weight initialization, central limit theorem.");
            param1Label->setText("μ (Mean):");
            param2Label->setText("σ (Std Dev):");
            param1Slider->setRange(-100, 100);
            param1Slider->setValue(0);
            param2Slider->setRange(10, 100);
            param2Slider->setValue(50);
            param2Slider->setEnabled(true);
            param2Label->setEnabled(true);
            param1 = 0.0;
            param2 = 1.0;
            param1Value->setText("0.0");
            param2Value->setText("1.0");
            break;
            
        case Binomial:
            infoLabel->setText("🎲 <b>Binomial Distribution:</b> Number of successes in n independent trials. "
                             "Models classification accuracy, dropout masks.");
            param1Label->setText("n (Trials):");
            param2Label->setText("p (Success):");
            param1Slider->setRange(1, 100);
            param1Slider->setValue(20);
            param2Slider->setRange(10, 100);
            param2Slider->setValue(50);
            param2Slider->setEnabled(true);
            param2Label->setEnabled(true);
            param1 = 20;
            param2 = 0.5;
            param1Value->setText("20");
            param2Value->setText("0.50");
            break;
            
        case Poisson:
            infoLabel->setText("⚡ <b>Poisson Distribution:</b> Count of events in fixed interval. "
                             "Models rare events, word counts in NLP.");
            param1Label->setText("λ (Rate):");
            param2Label->setText("(unused)");
            param1Slider->setRange(1, 100);
            param1Slider->setValue(30);
            param2Slider->setEnabled(false);
            param2Label->setEnabled(false);
            param1 = 3.0;
            param2 = 0;
            param1Value->setText("3.0");
            param2Value->setText("—");
            break;
            
        case Exponential:
            infoLabel->setText("⏱️ <b>Exponential Distribution:</b> Time between events. "
                             "Models waiting times, decay rates in physics simulations.");
            param1Label->setText("λ (Rate):");
            param2Label->setText("(unused)");
            param1Slider->setRange(1, 100);
            param1Slider->setValue(50);
            param2Slider->setEnabled(false);
            param2Label->setEnabled(false);
            param1 = 0.5;
            param2 = 0;
            param1Value->setText("0.50");
            param2Value->setText("—");
            break;
            
        case Uniform:
            infoLabel->setText("📏 <b>Uniform Distribution:</b> Equal probability over interval [a,b]. "
                             "Used for random weight initialization, data augmentation.");
            param1Label->setText("a (Min):");
            param2Label->setText("b (Max):");
            param1Slider->setRange(-100, 100);
            param1Slider->setValue(-20);
            param2Slider->setRange(-100, 100);
            param2Slider->setValue(20);
            param2Slider->setEnabled(true);
            param2Label->setEnabled(true);
            param1 = -2.0;
            param2 = 2.0;
            param1Value->setText("-2.0");
            param2Value->setText("2.0");
            break;
    }
}

void DistributionWidget::updatePlot()
{
    // Clear previous series
    pdfChart->removeAllSeries();
    cdfChart->removeAllSeries();
    
    QLineSeries *pdfSeries = new QLineSeries();
    QLineSeries *cdfSeries = new QLineSeries();
    
    double mean = 0, variance = 0;
    
    switch (currentDist) {
        case Normal: {
            mean = param1;
            variance = param2 * param2;
            double xMin = param1 - 4 * param2;
            double xMax = param1 + 4 * param2;
            int nPoints = 200;
            double dx = (xMax - xMin) / nPoints;
            
            for (int i = 0; i <= nPoints; ++i) {
                double x = xMin + i * dx;
                pdfSeries->append(x, normalPDF(x, param1, param2));
                cdfSeries->append(x, normalCDF(x, param1, param2));
            }
            break;
        }
        
        case Binomial: {
            int n = static_cast<int>(param1);
            double p = param2;
            mean = n * p;
            variance = n * p * (1 - p);
            
            for (int k = 0; k <= n; ++k) {
                double pmf = binomialPMF(k, n, p);
                double cdf = binomialCDF(k, n, p);
                pdfSeries->append(k, pmf);
                cdfSeries->append(k, cdf);
            }
            pdfChart->setTitle("Probability Mass Function (PMF)");
            break;
        }
        
        case Poisson: {
            double lambda = param1;
            mean = lambda;
            variance = lambda;
            int maxK = std::min(50, static_cast<int>(lambda * 3 + 20));
            
            for (int k = 0; k <= maxK; ++k) {
                double pmf = poissonPMF(k, lambda);
                double cdf = poissonCDF(k, lambda);
                pdfSeries->append(k, pmf);
                cdfSeries->append(k, cdf);
            }
            pdfChart->setTitle("Probability Mass Function (PMF)");
            break;
        }
        
        case Exponential: {
            double lambda = param1;
            mean = 1.0 / lambda;
            variance = 1.0 / (lambda * lambda);
            double xMax = 10.0 / lambda;
            int nPoints = 200;
            double dx = xMax / nPoints;
            
            for (int i = 0; i <= nPoints; ++i) {
                double x = i * dx;
                pdfSeries->append(x, exponentialPDF(x, lambda));
                cdfSeries->append(x, exponentialCDF(x, lambda));
            }
            break;
        }
        
        case Uniform: {
            double a = std::min(param1, param2);
            double b = std::max(param1, param2);
            mean = (a + b) / 2.0;
            variance = (b - a) * (b - a) / 12.0;
            
            double margin = (b - a) * 0.2;
            pdfSeries->append(a - margin, 0);
            pdfSeries->append(a, 0);
            pdfSeries->append(a, uniformPDF(a, a, b));
            pdfSeries->append(b, uniformPDF(b, a, b));
            pdfSeries->append(b, 0);
            pdfSeries->append(b + margin, 0);
            
            int nPoints = 100;
            double dx = (b + margin - (a - margin)) / nPoints;
            for (int i = 0; i <= nPoints; ++i) {
                double x = a - margin + i * dx;
                cdfSeries->append(x, uniformCDF(x, a, b));
            }
            break;
        }
    }
    
    // Update statistics labels
    meanLabel->setText(QString("<b>Mean:</b> %1").arg(mean, 0, 'f', 2));
    varianceLabel->setText(QString("<b>Variance:</b> %1").arg(variance, 0, 'f', 2));
    
    // Add series to charts
    pdfChart->addSeries(pdfSeries);
    cdfChart->addSeries(cdfSeries);
    
    // Create axes
    pdfChart->createDefaultAxes();
    cdfChart->createDefaultAxes();
    
    // Customize axes
    QValueAxis *pdfAxisY = qobject_cast<QValueAxis*>(pdfChart->axes(Qt::Vertical).first());
    if (pdfAxisY) {
        pdfAxisY->setTitleText("Probability");
    }
    
    QValueAxis *cdfAxisY = qobject_cast<QValueAxis*>(cdfChart->axes(Qt::Vertical).first());
    if (cdfAxisY) {
        cdfAxisY->setTitleText("Cumulative Probability");
        cdfAxisY->setRange(0, 1.05);
    }
    
    pdfChart->legend()->hide();
    cdfChart->legend()->hide();
}

double DistributionWidget::normalPDF(double x, double mu, double sigma)
{
    double z = (x - mu) / sigma;
    return (1.0 / (sigma * std::sqrt(2 * M_PI))) * std::exp(-0.5 * z * z);
}

double DistributionWidget::normalCDF(double x, double mu, double sigma)
{
    return 0.5 * (1.0 + erf((x - mu) / (sigma * std::sqrt(2.0))));
}

double DistributionWidget::binomialPMF(int k, int n, double p)
{
    if (k < 0 || k > n) return 0.0;
    return binomialCoeff(n, k) * std::pow(p, k) * std::pow(1 - p, n - k);
}

double DistributionWidget::binomialCDF(int k, int n, double p)
{
    double sum = 0.0;
    for (int i = 0; i <= k; ++i) {
        sum += binomialPMF(i, n, p);
    }
    return sum;
}

double DistributionWidget::poissonPMF(int k, double lambda)
{
    if (k < 0) return 0.0;
    return std::exp(-lambda + k * std::log(lambda) - std::lgamma(k + 1));
}

double DistributionWidget::poissonCDF(int k, double lambda)
{
    double sum = 0.0;
    for (int i = 0; i <= k; ++i) {
        sum += poissonPMF(i, lambda);
    }
    return sum;
}

double DistributionWidget::exponentialPDF(double x, double lambda)
{
    if (x < 0) return 0.0;
    return lambda * std::exp(-lambda * x);
}

double DistributionWidget::exponentialCDF(double x, double lambda)
{
    if (x < 0) return 0.0;
    return 1.0 - std::exp(-lambda * x);
}

double DistributionWidget::uniformPDF(double x, double a, double b)
{
    if (x < a || x > b) return 0.0;
    return 1.0 / (b - a);
}

double DistributionWidget::uniformCDF(double x, double a, double b)
{
    if (x < a) return 0.0;
    if (x > b) return 1.0;
    return (x - a) / (b - a);
}

double DistributionWidget::erf(double x)
{
    // Abramowitz and Stegun approximation
    double a1 =  0.254829592;
    double a2 = -0.284496736;
    double a3 =  1.421413741;
    double a4 = -1.453152027;
    double a5 =  1.061405429;
    double p  =  0.3275911;

    int sign = (x < 0) ? -1 : 1;
    x = std::abs(x);

    double t = 1.0 / (1.0 + p * x);
    double y = 1.0 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * std::exp(-x * x);

    return sign * y;
}

long long DistributionWidget::factorial(int n)
{
    if (n <= 1) return 1;
    long long result = 1;
    for (int i = 2; i <= n; ++i) {
        result *= i;
    }
    return result;
}

long long DistributionWidget::binomialCoeff(int n, int k)
{
    if (k > n - k) k = n - k;
    long long result = 1;
    for (int i = 0; i < k; ++i) {
        result *= (n - i);
        result /= (i + 1);
    }
    return result;
}
