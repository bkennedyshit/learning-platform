#include "SamplingVisualizer.h"
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QFormLayout>
#include <QFileDialog>
#include <QTextStream>
#include <cmath>
#include <numeric>
#include <algorithm>

SamplingVisualizer::SamplingVisualizer(QWidget *parent)
    : QWidget(parent)
    , sourceChart(new QChart())
    , resultChart(new QChart())
    , sourceChartView(new QChartView(sourceChart))
    , resultChartView(new QChartView(resultChart))
    , animationTimer(new QTimer(this))
    , currentSampleCount(0)
    , rng(std::random_device{}())
{
    setupUI();
    resetSimulation();
}

SamplingVisualizer::~SamplingVisualizer()
{
}

void SamplingVisualizer::setupUI()
{
    QVBoxLayout *mainLayout = new QVBoxLayout(this);
    
    // Header
    QHBoxLayout *headerLayout = new QHBoxLayout();
    QLabel *titleLabel = new QLabel("<h2>Sampling Theory Visualizer</h2>");
    
    modeSelector = new QComboBox();
    modeSelector->addItem("Central Limit Theorem");
    modeSelector->addItem("Law of Large Numbers");
    connect(modeSelector, QOverload<int>::of(&QComboBox::currentIndexChanged),
            this, &SamplingVisualizer::onModeChanged);
    
    headerLayout->addWidget(titleLabel);
    headerLayout->addStretch();
    headerLayout->addWidget(new QLabel("Mode:"));
    headerLayout->addWidget(modeSelector);
    mainLayout->addLayout(headerLayout);
    
    // Controls
    QGroupBox *controlsGroup = new QGroupBox("Sampling Parameters");
    QHBoxLayout *controlsLayout = new QHBoxLayout(controlsGroup);
    
    QFormLayout *paramsLayout = new QFormLayout();
    
    distributionSelector = new QComboBox();
    distributionSelector->addItem("Uniform [0,1]");
    distributionSelector->addItem("Exponential (λ=1)");
    distributionSelector->addItem("Bimodal");
    distributionSelector->addItem("Discrete (Die Roll)");
    connect(distributionSelector, QOverload<int>::of(&QComboBox::currentIndexChanged),
            this, &SamplingVisualizer::onDistributionChanged);
    paramsLayout->addRow("Source Distribution:", distributionSelector);
    
    sampleSizeSpinBox = new QSpinBox();
    sampleSizeSpinBox->setRange(1, 1000);
    sampleSizeSpinBox->setValue(30);
    connect(sampleSizeSpinBox, QOverload<int>::of(&QSpinBox::valueChanged),
            this, &SamplingVisualizer::updateVisualization);
    paramsLayout->addRow("Sample Size (n):", sampleSizeSpinBox);
    
    numSamplesSpinBox = new QSpinBox();
    numSamplesSpinBox->setRange(10, 10000);
    numSamplesSpinBox->setValue(1000);
    numSamplesSpinBox->setSingleStep(100);
    paramsLayout->addRow("Number of Samples:", numSamplesSpinBox);
    
    controlsLayout->addLayout(paramsLayout);
    
    // Statistics display
    QGroupBox *statsGroup = new QGroupBox("Statistics");
    QFormLayout *statsLayout = new QFormLayout(statsGroup);
    
    theoreticalMeanLabel = new QLabel("0.500");
    statsLayout->addRow("Population Mean (μ):", theoreticalMeanLabel);
    
    currentMeanLabel = new QLabel("0.000");
    QFont boldFont = currentMeanLabel->font();
    boldFont.setBold(true);
    currentMeanLabel->setFont(boldFont);
    statsLayout->addRow("Sample Mean (X̄):", currentMeanLabel);
    
    theoreticalStdLabel = new QLabel("0.289");
    statsLayout->addRow("Expected Std:", theoreticalStdLabel);
    
    currentStdLabel = new QLabel("0.000");
    currentStdLabel->setFont(boldFont);
    statsLayout->addRow("Observed Std:", currentStdLabel);
    
    controlsLayout->addWidget(statsGroup);
    
    // Animation controls
    QVBoxLayout *animationLayout = new QVBoxLayout();
    animateButton = new QPushButton("▶ Start Animation");
    connect(animateButton, &QPushButton::clicked, this, &SamplingVisualizer::startAnimation);
    animationLayout->addWidget(animateButton);
    
    stopButton = new QPushButton("⏸ Pause");
    stopButton->setEnabled(false);
    connect(stopButton, &QPushButton::clicked, this, &SamplingVisualizer::stopAnimation);
    animationLayout->addWidget(stopButton);
    
    resetButton = new QPushButton("↻ Reset");
    connect(resetButton, &QPushButton::clicked, this, &SamplingVisualizer::resetSimulation);
    animationLayout->addWidget(resetButton);
    
    exportButton = new QPushButton("Export Data");
    connect(exportButton, &QPushButton::clicked, this, &SamplingVisualizer::exportData);
    animationLayout->addWidget(exportButton);
    
    animationLayout->addStretch();
    controlsLayout->addLayout(animationLayout);
    
    mainLayout->addWidget(controlsGroup);
    
    // Charts
    QHBoxLayout *chartsLayout = new QHBoxLayout();
    
    QVBoxLayout *sourceLayout = new QVBoxLayout();
    sourceLayout->addWidget(new QLabel("<b>Source Distribution</b>"));
    sourceChartView->setRenderHint(QPainter::Antialiasing);
    sourceChartView->setMinimumHeight(250);
    sourceLayout->addWidget(sourceChartView);
    chartsLayout->addLayout(sourceLayout);
    
    QVBoxLayout *resultLayout = new QVBoxLayout();
    resultLayout->addWidget(new QLabel("<b>Sample Means Distribution</b>"));
    resultChartView->setRenderHint(QPainter::Antialiasing);
    resultChartView->setMinimumHeight(250);
    resultLayout->addWidget(resultChartView);
    chartsLayout->addLayout(resultLayout);
    
    mainLayout->addLayout(chartsLayout);
    
    // Explanation
    explanationText = new QTextEdit();
    explanationText->setReadOnly(true);
    explanationText->setMaximumHeight(120);
    mainLayout->addWidget(explanationText);
    
    // Animation timer
    connect(animationTimer, &QTimer::timeout, this, &SamplingVisualizer::animationStep);
    
    updateExplanation();
    updateSourceDistribution();
}

double SamplingVisualizer::sampleFromDistribution(SourceDist dist)
{
    switch (dist) {
        case UNIFORM_DIST: {
            std::uniform_real_distribution<> d(0.0, 1.0);
            return d(rng);
        }
        case EXPONENTIAL_DIST: {
            std::exponential_distribution<> d(1.0);
            return d(rng);
        }
        case BIMODAL_DIST: {
            std::uniform_real_distribution<> coin(0.0, 1.0);
            if (coin(rng) < 0.5) {
                std::normal_distribution<> d(0.3, 0.1);
                return std::max(0.0, std::min(1.0, d(rng)));
            } else {
                std::normal_distribution<> d(0.7, 0.1);
                return std::max(0.0, std::min(1.0, d(rng)));
            }
        }
        case DISCRETE_DIST: {
            std::uniform_int_distribution<> d(1, 6);
            return static_cast<double>(d(rng));
        }
    }
    return 0.0;
}

std::vector<double> SamplingVisualizer::generateSourceSamples(int n)
{
    std::vector<double> samples;
    SourceDist dist = static_cast<SourceDist>(distributionSelector->currentIndex());
    
    for (int i = 0; i < n; ++i) {
        samples.push_back(sampleFromDistribution(dist));
    }
    
    return samples;
}

double SamplingVisualizer::calculateSampleMean(const std::vector<double>& samples)
{
    return std::accumulate(samples.begin(), samples.end(), 0.0) / samples.size();
}

double SamplingVisualizer::calculateStdDev(const std::vector<double>& samples, double mean)
{
    double variance = 0.0;
    for (double x : samples) {
        variance += (x - mean) * (x - mean);
    }
    variance /= samples.size();
    return std::sqrt(variance);
}

void SamplingVisualizer::updateSourceDistribution()
{
    sourceChart->removeAllSeries();
    
    SourceDist dist = static_cast<SourceDist>(distributionSelector->currentIndex());
    
    // Update population parameters
    switch (dist) {
        case UNIFORM_DIST:
            populationMean = 0.5;
            populationStd = std::sqrt(1.0 / 12.0);
            break;
        case EXPONENTIAL_DIST:
            populationMean = 1.0;
            populationStd = 1.0;
            break;
        case BIMODAL_DIST:
            populationMean = 0.5;
            populationStd = 0.25;
            break;
        case DISCRETE_DIST:
            populationMean = 3.5;
            populationStd = std::sqrt(35.0 / 12.0);
            break;
    }
    
    theoreticalMeanLabel->setText(QString::number(populationMean, 'f', 3));
    
    // Generate distribution visualization
    auto samples = generateSourceSamples(10000);
    
    // Create histogram
    QBarSet *histSet = new QBarSet("Frequency");
    QStringList categories;
    
    int numBins = 20;
    double minVal = *std::min_element(samples.begin(), samples.end());
    double maxVal = *std::max_element(samples.begin(), samples.end());
    double binWidth = (maxVal - minVal) / numBins;
    
    std::vector<int> histogram(numBins, 0);
    for (double s : samples) {
        int bin = std::min(static_cast<int>((s - minVal) / binWidth), numBins - 1);
        histogram[bin]++;
    }
    
    for (int i = 0; i < numBins; ++i) {
        *histSet << histogram[i];
        categories << QString::number(minVal + i * binWidth, 'f', 2);
    }
    
    QBarSeries *series = new QBarSeries();
    series->append(histSet);
    
    sourceChart->addSeries(series);
    
    QBarCategoryAxis *axisX = new QBarCategoryAxis();
    axisX->append(categories);
    sourceChart->addAxis(axisX, Qt::AlignBottom);
    series->attachAxis(axisX);
    
    QValueAxis *axisY = new QValueAxis();
    axisY->setTitleText("Frequency");
    sourceChart->addAxis(axisY, Qt::AlignLeft);
    series->attachAxis(axisY);
    
    sourceChart->setTitle("Source Distribution");
    sourceChart->legend()->setVisible(false);
}

void SamplingVisualizer::updateCLTVisualization()
{
    resultChart->removeAllSeries();
    
    if (sampleMeans.empty()) {
        resultChart->setTitle("Sample Means Distribution (CLT)");
        return;
    }
    
    // Create histogram of sample means
    QBarSet *histSet = new QBarSet("Sample Means");
    QStringList categories;
    
    int numBins = 30;
    double minVal = *std::min_element(sampleMeans.begin(), sampleMeans.end());
    double maxVal = *std::max_element(sampleMeans.begin(), sampleMeans.end());
    double binWidth = (maxVal - minVal) / numBins;
    
    if (binWidth == 0) binWidth = 0.1;
    
    std::vector<int> histogram(numBins, 0);
    for (double mean : sampleMeans) {
        int bin = std::min(static_cast<int>((mean - minVal) / binWidth), numBins - 1);
        histogram[bin]++;
    }
    
    for (int i = 0; i < numBins; ++i) {
        *histSet << histogram[i];
        if (i % 5 == 0) {
            categories << QString::number(minVal + i * binWidth, 'f', 2);
        } else {
            categories << "";
        }
    }
    
    QBarSeries *series = new QBarSeries();
    series->append(histSet);
    
    resultChart->addSeries(series);
    
    QBarCategoryAxis *axisX = new QBarCategoryAxis();
    axisX->append(categories);
    resultChart->addAxis(axisX, Qt::AlignBottom);
    series->attachAxis(axisX);
    
    QValueAxis *axisY = new QValueAxis();
    axisY->setTitleText("Frequency");
    resultChart->addAxis(axisY, Qt::AlignLeft);
    series->attachAxis(axisY);
    
    resultChart->setTitle(QString("CLT: n=%1, samples=%2")
                         .arg(sampleSizeSpinBox->value())
                         .arg(sampleMeans.size()));
    resultChart->legend()->setVisible(false);
}

void SamplingVisualizer::updateLLNVisualization()
{
    resultChart->removeAllSeries();
    
    if (runningMeans.empty()) {
        resultChart->setTitle("Running Mean Convergence (LLN)");
        return;
    }
    
    QLineSeries *meanSeries = new QLineSeries();
    meanSeries->setName("Running Mean");
    
    for (size_t i = 0; i < runningMeans.size(); ++i) {
        meanSeries->append(i + 1, runningMeans[i]);
    }
    
    // Add theoretical mean line
    QLineSeries *theoreticalSeries = new QLineSeries();
    theoreticalSeries->setName("True Mean");
    theoreticalSeries->append(1, populationMean);
    theoreticalSeries->append(runningMeans.size(), populationMean);
    
    resultChart->addSeries(meanSeries);
    resultChart->addSeries(theoreticalSeries);
    
    resultChart->createDefaultAxes();
    QValueAxis *axisX = qobject_cast<QValueAxis*>(resultChart->axes(Qt::Horizontal).first());
    QValueAxis *axisY = qobject_cast<QValueAxis*>(resultChart->axes(Qt::Vertical).first());
    
    if (axisX && axisY) {
        axisX->setTitleText("Sample Number");
        axisY->setTitleText("Mean Value");
    }
    
    resultChart->setTitle(QString("LLN: Convergence to μ=%1").arg(populationMean, 0, 'f', 3));
    resultChart->legend()->setVisible(true);
}

void SamplingVisualizer::updateVisualization()
{
    Mode mode = static_cast<Mode>(modeSelector->currentIndex());
    
    if (mode == CLT_MODE) {
        updateCLTVisualization();
        
        // Update expected std for CLT
        int n = sampleSizeSpinBox->value();
        double expectedStd = populationStd / std::sqrt(n);
        theoreticalStdLabel->setText(QString::number(expectedStd, 'f', 4));
    } else {
        updateLLNVisualization();
        theoreticalStdLabel->setText(QString::number(populationStd, 'f', 4));
    }
    
    updateStatistics();
}

void SamplingVisualizer::updateStatistics()
{
    Mode mode = static_cast<Mode>(modeSelector->currentIndex());
    
    if (mode == CLT_MODE && !sampleMeans.empty()) {
        double mean = calculateSampleMean(sampleMeans);
        double std = calculateStdDev(sampleMeans, mean);
        
        currentMeanLabel->setText(QString::number(mean, 'f', 4));
        currentStdLabel->setText(QString::number(std, 'f', 4));
    } else if (mode == LLN_MODE && !runningMeans.empty()) {
        double currentMean = runningMeans.back();
        currentMeanLabel->setText(QString::number(currentMean, 'f', 4));
        currentStdLabel->setText("N/A");
    }
}

void SamplingVisualizer::startAnimation()
{
    animateButton->setEnabled(false);
    stopButton->setEnabled(true);
    animationTimer->start(50); // 50ms interval
}

void SamplingVisualizer::stopAnimation()
{
    animationTimer->stop();
    animateButton->setEnabled(true);
    stopButton->setEnabled(false);
}

void SamplingVisualizer::resetSimulation()
{
    stopAnimation();
    currentSampleCount = 0;
    sampleMeans.clear();
    runningMeans.clear();
    
    updateSourceDistribution();
    updateVisualization();
}

void SamplingVisualizer::animationStep()
{
    Mode mode = static_cast<Mode>(modeSelector->currentIndex());
    int sampleSize = sampleSizeSpinBox->value();
    int maxSamples = numSamplesSpinBox->value();
    
    if (mode == CLT_MODE) {
        // Generate one sample and calculate its mean
        auto samples = generateSourceSamples(sampleSize);
        double mean = calculateSampleMean(samples);
        sampleMeans.push_back(mean);
        
        currentSampleCount++;
        
        if (currentSampleCount >= maxSamples) {
            stopAnimation();
        }
        
        if (currentSampleCount % 10 == 0) {
            updateCLTVisualization();
            updateStatistics();
        }
    } else {
        // LLN: accumulate samples and update running mean
        double sample = sampleFromDistribution(
            static_cast<SourceDist>(distributionSelector->currentIndex()));
        
        if (runningMeans.empty()) {
            runningMeans.push_back(sample);
        } else {
            int n = runningMeans.size() + 1;
            double newMean = (runningMeans.back() * (n - 1) + sample) / n;
            runningMeans.push_back(newMean);
        }
        
        currentSampleCount++;
        
        if (currentSampleCount >= maxSamples) {
            stopAnimation();
        }
        
        if (currentSampleCount % 20 == 0) {
            updateLLNVisualization();
            updateStatistics();
        }
    }
}

void SamplingVisualizer::onModeChanged(int index)
{
    resetSimulation();
    updateExplanation();
}

void SamplingVisualizer::onDistributionChanged(int index)
{
    resetSimulation();
}

void SamplingVisualizer::updateExplanation()
{
    Mode mode = static_cast<Mode>(modeSelector->currentIndex());
    
    if (mode == CLT_MODE) {
        explanationText->setHtml(
            "<h3>Central Limit Theorem</h3>"
            "<p><b>Key Insight:</b> Sample means form a normal distribution, <b>regardless of source distribution!</b></p>"
            "<p><b>Formula:</b> X̄ ~ N(μ, σ²/n) as n→∞</p>"
            "<p><b>Applications:</b> Hypothesis testing, confidence intervals, bootstrapping, normality assumption in ML</p>"
        );
    } else {
        explanationText->setHtml(
            "<h3>Law of Large Numbers</h3>"
            "<p><b>Key Insight:</b> Sample mean converges to population mean as sample size increases.</p>"
            "<p><b>Formula:</b> lim (n→∞) X̄ₙ = μ</p>"
            "<p><b>Applications:</b> Monte Carlo methods, empirical risk minimization, why more data helps</p>"
        );
    }
}

void SamplingVisualizer::exportData()
{
    QString fileName = QFileDialog::getSaveFileName(this, "Export Sampling Data", "", "CSV Files (*.csv)");
    if (fileName.isEmpty()) return;
    
    QFile file(fileName);
    if (!file.open(QIODevice::WriteOnly | QIODevice::Text)) return;
    
    QTextStream out(&file);
    
    Mode mode = static_cast<Mode>(modeSelector->currentIndex());
    
    if (mode == CLT_MODE) {
        out << "Sample Number,Sample Mean\n";
        for (size_t i = 0; i < sampleMeans.size(); ++i) {
            out << i + 1 << "," << sampleMeans[i] << "\n";
        }
    } else {
        out << "Sample Number,Running Mean\n";
        for (size_t i = 0; i < runningMeans.size(); ++i) {
            out << i + 1 << "," << runningMeans[i] << "\n";
        }
    }
    
    file.close();
}
