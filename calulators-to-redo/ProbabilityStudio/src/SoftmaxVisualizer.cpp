#include "SoftmaxVisualizer.h"
#include <QtCharts/QChart>
#include <QtCharts/QChartView>
#include <QtCharts/QBarSeries>
#include <QtCharts/QBarSet>
#include <QtCharts/QBarCategoryAxis>
#include <QtCharts/QValueAxis>
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QGridLayout>
#include <QGroupBox>
#include <QRandomGenerator>
#include <cmath>
#include <algorithm>

using namespace QtCharts;

SoftmaxVisualizer::SoftmaxVisualizer(QWidget *parent)
    : QWidget(parent)
    , temperature(1.0)
{
    setupUI();
    updateVisualization();
}

SoftmaxVisualizer::~SoftmaxVisualizer()
{
}

void SoftmaxVisualizer::setupUI()
{
    QVBoxLayout *mainLayout = new QVBoxLayout(this);
    
    // Title
    QLabel *title = new QLabel("<h2>Softmax Temperature Visualizer</h2>");
    title->setAlignment(Qt::AlignCenter);
    mainLayout->addWidget(title);
    
    // Info
    infoLabel = new QLabel(
        "🔥 <b>Critical for LLM Sampling!</b> Temperature controls randomness in text generation:<br>"
        "• T = 0.1: Deterministic, picks highest probability (greedy)<br>"
        "• T = 1.0: Standard probabilities<br>"
        "• T = 2.0: More random, creative outputs<br>"
        "Lower temp = focused, higher temp = diverse"
    );
    infoLabel->setWordWrap(true);
    infoLabel->setStyleSheet("QLabel { background-color: #fff3e0; padding: 10px; border-radius: 5px; }");
    mainLayout->addWidget(infoLabel);
    
    QHBoxLayout *topLayout = new QHBoxLayout();
    
    // Left: Controls
    QGroupBox *controlGroup = new QGroupBox("Logits (Pre-Softmax Scores)");
    QVBoxLayout *controlLayout = new QVBoxLayout(controlGroup);
    
    QGridLayout *inputGrid = new QGridLayout();
    QStringList classNames = {"Class A", "Class B", "Class C", "Class D", "Class E"};
    
    for (int i = 0; i < NUM_CLASSES; ++i) {
        inputGrid->addWidget(new QLabel(classNames[i] + ":"), i, 0);
        QLineEdit *input = new QLineEdit("0.0");
        input->setMaximumWidth(80);
        connect(input, &QLineEdit::textChanged, this, &SoftmaxVisualizer::onInputChanged);
        logitInputs.append(input);
        inputGrid->addWidget(input, i, 1);
        
        QLabel *probLabel = new QLabel("→ 0.200");
        probLabel->setMinimumWidth(100);
        probLabel->setStyleSheet("QLabel { font-weight: bold; color: #1976d2; }");
        probabilityLabels.append(probLabel);
        inputGrid->addWidget(probLabel, i, 2);
    }
    
    controlLayout->addLayout(inputGrid);
    
    randomizeButton = new QPushButton("🎲 Randomize Logits");
    connect(randomizeButton, &QPushButton::clicked, this, &SoftmaxVisualizer::randomizeInputs);
    controlLayout->addWidget(randomizeButton);
    
    topLayout->addWidget(controlGroup);
    
    // Right: Temperature control
    QGroupBox *tempGroup = new QGroupBox("Temperature Control");
    QVBoxLayout *tempLayout = new QVBoxLayout(tempGroup);
    
    QHBoxLayout *tempSliderLayout = new QHBoxLayout();
    temperatureLabel = new QLabel("<b>Temperature (T):</b>");
    tempSliderLayout->addWidget(temperatureLabel);
    tempSliderLayout->addStretch();
    temperatureValue = new QLabel("1.00");
    temperatureValue->setStyleSheet("QLabel { font-size: 16pt; font-weight: bold; color: #d32f2f; }");
    tempSliderLayout->addWidget(temperatureValue);
    tempLayout->addLayout(tempSliderLayout);
    
    temperatureSlider = new QSlider(Qt::Horizontal);
    temperatureSlider->setRange(1, 300);  // 0.01 to 3.0
    temperatureSlider->setValue(100);
    connect(temperatureSlider, &QSlider::valueChanged, this, &SoftmaxVisualizer::onTemperatureChanged);
    tempLayout->addWidget(temperatureSlider);
    
    // Tick marks
    QHBoxLayout *tickLayout = new QHBoxLayout();
    tickLayout->addWidget(new QLabel("0.01<br>(Sharp)"));
    tickLayout->addStretch();
    tickLayout->addWidget(new QLabel("1.0<br>(Normal)"));
    tickLayout->addStretch();
    tickLayout->addWidget(new QLabel("3.0<br>(Smooth)"));
    tempLayout->addLayout(tickLayout);
    
    entropyLabel = new QLabel("<b>Entropy:</b> 0.0 (bits)");
    entropyLabel->setStyleSheet("QLabel { padding: 10px; background-color: #e8f5e9; border-radius: 5px; }");
    tempLayout->addWidget(entropyLabel);
    
    tempLayout->addStretch();
    topLayout->addWidget(tempGroup);
    
    mainLayout->addLayout(topLayout);
    
    // Chart
    chart = new QChart();
    chart->setTitle("Softmax Output Probabilities");
    chart->setAnimationOptions(QChart::SeriesAnimations);
    
    chartView = new QChartView(chart);
    chartView->setRenderHint(QPainter::Antialiasing);
    mainLayout->addWidget(chartView, 1);
    
    // Set initial logit values for demonstration
    logitInputs[0]->setText("2.5");
    logitInputs[1]->setText("1.0");
    logitInputs[2]->setText("0.5");
    logitInputs[3]->setText("-1.0");
    logitInputs[4]->setText("0.2");
}

void SoftmaxVisualizer::onTemperatureChanged(int value)
{
    temperature = value / 100.0;
    temperatureValue->setText(QString::number(temperature, 'f', 2));
    updateVisualization();
}

void SoftmaxVisualizer::onInputChanged()
{
    updateVisualization();
}

void SoftmaxVisualizer::randomizeInputs()
{
    for (int i = 0; i < NUM_CLASSES; ++i) {
        double value = (QRandomGenerator::global()->bounded(1000) - 500) / 100.0;  // -5.0 to 5.0
        logitInputs[i]->setText(QString::number(value, 'f', 1));
    }
}

void SoftmaxVisualizer::updateVisualization()
{
    // Parse logits
    QVector<double> logits;
    for (int i = 0; i < NUM_CLASSES; ++i) {
        bool ok;
        double value = logitInputs[i]->text().toDouble(&ok);
        logits.append(ok ? value : 0.0);
    }
    
    // Compute softmax
    QVector<double> probs = computeSoftmax(logits, temperature);
    
    // Update probability labels
    for (int i = 0; i < NUM_CLASSES; ++i) {
        probabilityLabels[i]->setText(QString("→ %1").arg(probs[i], 0, 'f', 3));
    }
    
    // Calculate entropy
    double entropy = 0.0;
    for (double p : probs) {
        if (p > 1e-10) {  // Avoid log(0)
            entropy -= p * std::log2(p);
        }
    }
    entropyLabel->setText(QString("<b>Entropy:</b> %1 bits<br>"
                                 "<i>%2</i>")
                         .arg(entropy, 0, 'f', 3)
                         .arg(entropy < 0.5 ? "Very certain" : 
                              entropy < 1.5 ? "Moderate uncertainty" : "High uncertainty"));
    
    // Update chart
    chart->removeAllSeries();
    
    QBarSet *barSet = new QBarSet("Probability");
    barSet->setColor(QColor("#1976d2"));
    
    for (double prob : probs) {
        *barSet << prob;
    }
    
    QBarSeries *series = new QBarSeries();
    series->append(barSet);
    chart->addSeries(series);
    
    // Setup axes
    QStringList categories;
    categories << "A" << "B" << "C" << "D" << "E";
    QBarCategoryAxis *axisX = new QBarCategoryAxis();
    axisX->append(categories);
    chart->addAxis(axisX, Qt::AlignBottom);
    series->attachAxis(axisX);
    
    QValueAxis *axisY = new QValueAxis();
    axisY->setRange(0, 1.0);
    axisY->setTitleText("Probability");
    axisY->setLabelFormat("%.2f");
    chart->addAxis(axisY, Qt::AlignLeft);
    series->attachAxis(axisY);
    
    chart->legend()->setVisible(false);
}

QVector<double> SoftmaxVisualizer::computeSoftmax(const QVector<double> &logits, double temp)
{
    QVector<double> probs(logits.size());
    
    // Find max for numerical stability
    double maxLogit = *std::max_element(logits.begin(), logits.end());
    
    // Compute exp(logit/T) for each element
    double sum = 0.0;
    for (int i = 0; i < logits.size(); ++i) {
        probs[i] = std::exp((logits[i] - maxLogit) / temp);
        sum += probs[i];
    }
    
    // Normalize
    for (int i = 0; i < probs.size(); ++i) {
        probs[i] /= sum;
    }
    
    return probs;
}
