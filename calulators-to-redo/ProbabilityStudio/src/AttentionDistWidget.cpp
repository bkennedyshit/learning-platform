#include "AttentionDistWidget.h"
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QFormLayout>
#include <QGridLayout>
#include <QHeaderView>
#include <QFileDialog>
#include <QTextStream>
#include <cmath>
#include <numeric>
#include <algorithm>

AttentionDistWidget::AttentionDistWidget(QWidget *parent)
    : QWidget(parent)
    , chart(new QChart())
    , chartView(new QChartView(chart))
    , temperature(1.0)
{
    setupUI();
    loadExample(1); // Load first example
}

AttentionDistWidget::~AttentionDistWidget()
{
}

void AttentionDistWidget::setupUI()
{
    QVBoxLayout *mainLayout = new QVBoxLayout(this);
    
    // Header
    QHBoxLayout *headerLayout = new QHBoxLayout();
    QLabel *titleLabel = new QLabel("<h2>Attention Weight Distribution Visualizer</h2>");
    
    exampleSelector = new QComboBox();
    exampleSelector->addItem("Custom");
    for (const auto& ex : getExamples()) {
        exampleSelector->addItem(ex.name);
    }
    connect(exampleSelector, QOverload<int>::of(&QComboBox::currentIndexChanged),
            this, &AttentionDistWidget::loadExample);
    
    modeSelector = new QComboBox();
    modeSelector->addItem("Bar Chart");
    modeSelector->addItem("Pie Chart");
    modeSelector->addItem("Heatmap");
    modeSelector->addItem("Entropy vs Temperature");
    connect(modeSelector, QOverload<int>::of(&QComboBox::currentIndexChanged),
            this, &AttentionDistWidget::onModeChanged);
    
    headerLayout->addWidget(titleLabel);
    headerLayout->addStretch();
    headerLayout->addWidget(new QLabel("Examples:"));
    headerLayout->addWidget(exampleSelector);
    headerLayout->addWidget(new QLabel("View:"));
    headerLayout->addWidget(modeSelector);
    mainLayout->addLayout(headerLayout);
    
    // Main content
    QHBoxLayout *contentLayout = new QHBoxLayout();
    
    // Left side: Controls
    QVBoxLayout *leftLayout = new QVBoxLayout();
    
    // Token scores table
    QGroupBox *tokensGroup = new QGroupBox("Attention Scores");
    QVBoxLayout *tokensLayout = new QVBoxLayout(tokensGroup);
    
    setupTokenTable();
    tokensLayout->addWidget(tokenTable);
    
    QHBoxLayout *tokenButtonsLayout = new QHBoxLayout();
    addTokenButton = new QPushButton("+ Add Token");
    connect(addTokenButton, &QPushButton::clicked, this, &AttentionDistWidget::addToken);
    tokenButtonsLayout->addWidget(addTokenButton);
    
    removeTokenButton = new QPushButton("- Remove Token");
    connect(removeTokenButton, &QPushButton::clicked, this, &AttentionDistWidget::removeToken);
    tokenButtonsLayout->addWidget(removeTokenButton);
    tokensLayout->addLayout(tokenButtonsLayout);
    
    leftLayout->addWidget(tokensGroup);
    
    // Attention parameters
    QGroupBox *paramsGroup = new QGroupBox("Attention Parameters");
    QFormLayout *paramsLayout = new QFormLayout(paramsGroup);
    
    QHBoxLayout *tempLayout = new QHBoxLayout();
    temperatureSlider = new QSlider(Qt::Horizontal);
    temperatureSlider->setRange(1, 200); // 0.01 to 2.0
    temperatureSlider->setValue(100);
    temperatureLabel = new QLabel("1.00");
    tempLayout->addWidget(temperatureSlider);
    tempLayout->addWidget(temperatureLabel);
    paramsLayout->addRow("Temperature (τ):", tempLayout);
    connect(temperatureSlider, &QSlider::valueChanged, this, &AttentionDistWidget::updateTemperature);
    
    scalingSpin = new QDoubleSpinBox();
    scalingSpin->setRange(0.1, 10.0);
    scalingSpin->setValue(1.0);
    scalingSpin->setSingleStep(0.1);
    connect(scalingSpin, QOverload<double>::of(&QDoubleSpinBox::valueChanged),
            this, &AttentionDistWidget::updateVisualization);
    paramsLayout->addRow("Score Scaling (√d_k):", scalingSpin);
    
    leftLayout->addWidget(paramsGroup);
    
    // Statistics
    QGroupBox *statsGroup = new QGroupBox("Distribution Statistics");
    QFormLayout *statsLayout = new QFormLayout(statsGroup);
    
    entropyLabel = new QLabel("0.000");
    QFont boldFont = entropyLabel->font();
    boldFont.setBold(true);
    entropyLabel->setFont(boldFont);
    statsLayout->addRow("Entropy (bits):", entropyLabel);
    
    maxAttentionLabel = new QLabel("0.000");
    statsLayout->addRow("Max Weight:", maxAttentionLabel);
    
    effectiveTokensLabel = new QLabel("0");
    statsLayout->addRow("Effective Tokens:", effectiveTokensLabel);
    
    sparsityLabel = new QLabel("0.000");
    statsLayout->addRow("Sparsity:", sparsityLabel);
    
    leftLayout->addWidget(statsGroup);
    
    // Export button
    exportButton = new QPushButton("Export Weights");
    connect(exportButton, &QPushButton::clicked, this, &AttentionDistWidget::exportData);
    leftLayout->addWidget(exportButton);
    
    leftLayout->addStretch();
    contentLayout->addLayout(leftLayout, 1);
    
    // Right side: Visualization
    chartView->setRenderHint(QPainter::Antialiasing);
    chartView->setMinimumHeight(400);
    contentLayout->addWidget(chartView, 2);
    
    mainLayout->addLayout(contentLayout);
    
    // Explanation
    explanationText = new QTextEdit();
    explanationText->setReadOnly(true);
    explanationText->setMaximumHeight(150);
    mainLayout->addWidget(explanationText);
    
    updateExplanation();
}

void AttentionDistWidget::setupTokenTable()
{
    tokenTable = new QTableWidget(5, 2);
    tokenTable->setHorizontalHeaderLabels(QStringList() << "Token" << "Score");
    tokenTable->horizontalHeader()->setSectionResizeMode(0, QHeaderView::Stretch);
    tokenTable->horizontalHeader()->setSectionResizeMode(1, QHeaderView::Fixed);
    tokenTable->setColumnWidth(1, 80);
    tokenTable->setMaximumHeight(200);
    
    connect(tokenTable, &QTableWidget::cellChanged, this, &AttentionDistWidget::updateVisualization);
}

void AttentionDistWidget::rebuildTokenTable()
{
    tokenTable->setRowCount(tokens.size());
    
    // Disconnect temporarily to avoid triggering updates
    disconnect(tokenTable, &QTableWidget::cellChanged, this, &AttentionDistWidget::updateVisualization);
    
    for (size_t i = 0; i < tokens.size(); ++i) {
        QTableWidgetItem *tokenItem = new QTableWidgetItem(QString::fromStdString(tokens[i]));
        tokenTable->setItem(i, 0, tokenItem);
        
        QTableWidgetItem *scoreItem = new QTableWidgetItem(QString::number(scores[i], 'f', 2));
        tokenTable->setItem(i, 1, scoreItem);
    }
    
    // Reconnect
    connect(tokenTable, &QTableWidget::cellChanged, this, &AttentionDistWidget::updateVisualization);
    
    updateVisualization();
}

std::vector<double> AttentionDistWidget::softmax(const std::vector<double>& scores, double temp)
{
    std::vector<double> weights;
    
    if (scores.empty()) return weights;
    
    // Apply temperature scaling
    std::vector<double> scaledScores;
    for (double s : scores) {
        scaledScores.push_back(s / temp);
    }
    
    // Find max for numerical stability
    double maxScore = *std::max_element(scaledScores.begin(), scaledScores.end());
    
    // Compute exponentials
    std::vector<double> exps;
    double sumExp = 0.0;
    for (double s : scaledScores) {
        double e = std::exp(s - maxScore);
        exps.push_back(e);
        sumExp += e;
    }
    
    // Normalize
    for (double e : exps) {
        weights.push_back(e / sumExp);
    }
    
    return weights;
}

double AttentionDistWidget::calculateEntropy(const std::vector<double>& probs)
{
    double entropy = 0.0;
    const double epsilon = 1e-10;
    
    for (double p : probs) {
        if (p > epsilon) {
            entropy -= p * std::log2(p);
        }
    }
    
    return entropy;
}

int AttentionDistWidget::calculateEffectiveTokens(const std::vector<double>& weights)
{
    // Count tokens with weight > 5%
    int count = 0;
    for (double w : weights) {
        if (w > 0.05) count++;
    }
    return count;
}

std::vector<double> AttentionDistWidget::calculateAttentionWeights()
{
    // Read scores from table
    scores.clear();
    tokens.clear();
    
    for (int i = 0; i < tokenTable->rowCount(); ++i) {
        QTableWidgetItem *tokenItem = tokenTable->item(i, 0);
        QTableWidgetItem *scoreItem = tokenTable->item(i, 1);
        
        if (tokenItem && scoreItem) {
            tokens.push_back(tokenItem->text().toStdString());
            scores.push_back(scoreItem->text().toDouble() / scalingSpin->value());
        }
    }
    
    return softmax(scores, temperature);
}

void AttentionDistWidget::updateVisualization()
{
    attentionWeights = calculateAttentionWeights();
    
    updateStatistics();
    
    VisualizationMode mode = static_cast<VisualizationMode>(modeSelector->currentIndex());
    
    switch (mode) {
        case WEIGHTS_BAR:
            updateBarChart();
            break;
        case WEIGHTS_PIE:
            updatePieChart();
            break;
        case HEATMAP_MODE:
            updateHeatmap();
            break;
        case ENTROPY_MODE:
            updateEntropyPlot();
            break;
    }
}

void AttentionDistWidget::updateStatistics()
{
    if (attentionWeights.empty()) return;
    
    double entropy = calculateEntropy(attentionWeights);
    double maxWeight = *std::max_element(attentionWeights.begin(), attentionWeights.end());
    int effectiveTokens = calculateEffectiveTokens(attentionWeights);
    
    // Sparsity: how concentrated is the distribution?
    // Use Gini coefficient or simply ratio of max to uniform
    double uniform = 1.0 / attentionWeights.size();
    double sparsity = maxWeight / uniform;
    
    entropyLabel->setText(QString::number(entropy, 'f', 3));
    maxAttentionLabel->setText(QString::number(maxWeight, 'f', 4));
    effectiveTokensLabel->setText(QString::number(effectiveTokens));
    sparsityLabel->setText(QString::number(sparsity, 'f', 2) + "x uniform");
}

void AttentionDistWidget::updateBarChart()
{
    chart->removeAllSeries();
    
    QBarSet *weightsSet = new QBarSet("Attention Weight");
    QStringList categories;
    
    for (size_t i = 0; i < attentionWeights.size(); ++i) {
        *weightsSet << attentionWeights[i];
        categories << QString::fromStdString(tokens[i]);
    }
    
    QBarSeries *series = new QBarSeries();
    series->append(weightsSet);
    
    chart->addSeries(series);
    
    QBarCategoryAxis *axisX = new QBarCategoryAxis();
    axisX->append(categories);
    chart->addAxis(axisX, Qt::AlignBottom);
    series->attachAxis(axisX);
    
    QValueAxis *axisY = new QValueAxis();
    axisY->setTitleText("Attention Weight (Probability)");
    axisY->setRange(0, std::min(1.0, *std::max_element(attentionWeights.begin(), attentionWeights.end()) * 1.1));
    chart->addAxis(axisY, Qt::AlignLeft);
    series->attachAxis(axisY);
    
    chart->setTitle(QString("Attention Distribution (τ=%.2f)").arg(temperature));
    chart->legend()->setVisible(false);
}

void AttentionDistWidget::updatePieChart()
{
    chart->removeAllSeries();
    
    QPieSeries *series = new QPieSeries();
    
    for (size_t i = 0; i < attentionWeights.size(); ++i) {
        QPieSlice *slice = series->append(
            QString::fromStdString(tokens[i]), 
            attentionWeights[i]
        );
        
        // Highlight largest attention
        if (attentionWeights[i] == *std::max_element(attentionWeights.begin(), attentionWeights.end())) {
            slice->setExploded(true);
            slice->setLabelVisible(true);
        }
        
        slice->setLabel(QString("%1: %2%")
                       .arg(QString::fromStdString(tokens[i]))
                       .arg(attentionWeights[i] * 100, 0, 'f', 1));
    }
    
    series->setLabelsVisible(true);
    series->setLabelsPosition(QPieSlice::LabelOutside);
    
    chart->addSeries(series);
    chart->setTitle("Attention Weight Distribution");
    chart->legend()->setAlignment(Qt::AlignRight);
}

void AttentionDistWidget::updateHeatmap()
{
    chart->removeAllSeries();
    
    // Create a visual heatmap representation using bars
    QBarSet *heatSet = new QBarSet("Attention");
    QStringList categories;
    
    for (size_t i = 0; i < attentionWeights.size(); ++i) {
        *heatSet << attentionWeights[i] * 100; // As percentage
        categories << QString::fromStdString(tokens[i]);
    }
    
    QBarSeries *series = new QBarSeries();
    series->append(heatSet);
    
    chart->addSeries(series);
    
    QBarCategoryAxis *axisX = new QBarCategoryAxis();
    axisX->append(categories);
    axisX->setTitleText("Tokens (Sequence)");
    chart->addAxis(axisX, Qt::AlignBottom);
    series->attachAxis(axisX);
    
    QValueAxis *axisY = new QValueAxis();
    axisY->setTitleText("Attention (%)");
    axisY->setRange(0, 100);
    chart->addAxis(axisY, Qt::AlignLeft);
    series->attachAxis(axisY);
    
    chart->setTitle("Attention Heatmap");
    chart->legend()->setVisible(false);
}

void AttentionDistWidget::updateEntropyPlot()
{
    chart->removeAllSeries();
    
    // Plot entropy vs temperature
    QLineSeries *entropySeries = new QLineSeries();
    entropySeries->setName("Entropy");
    
    double maxEntropy = std::log2(static_cast<double>(scores.size()));
    
    for (int t = 1; t <= 200; t += 2) {
        double temp = t / 100.0;
        auto weights = softmax(scores, temp);
        double entropy = calculateEntropy(weights);
        entropySeries->append(temp, entropy);
    }
    
    // Mark current temperature
    QScatterSeries *currentPoint = new QScatterSeries();
    currentPoint->setName("Current");
    currentPoint->setMarkerSize(15);
    currentPoint->append(temperature, calculateEntropy(attentionWeights));
    
    chart->addSeries(entropySeries);
    chart->addSeries(currentPoint);
    
    chart->createDefaultAxes();
    QValueAxis *axisX = qobject_cast<QValueAxis*>(chart->axes(Qt::Horizontal).first());
    QValueAxis *axisY = qobject_cast<QValueAxis*>(chart->axes(Qt::Vertical).first());
    
    if (axisX && axisY) {
        axisX->setTitleText("Temperature (τ)");
        axisX->setRange(0, 2.0);
        axisY->setTitleText("Entropy (bits)");
        axisY->setRange(0, maxEntropy);
        
        // Add max entropy line
        QLineSeries *maxLine = new QLineSeries();
        maxLine->setName("Max Entropy (Uniform)");
        maxLine->append(0, maxEntropy);
        maxLine->append(2, maxEntropy);
        chart->addSeries(maxLine);
        maxLine->attachAxis(axisX);
        maxLine->attachAxis(axisY);
    }
    
    chart->setTitle("Entropy vs Temperature: Distribution Sharpness");
    chart->legend()->setVisible(true);
}

void AttentionDistWidget::updateTemperature(int value)
{
    temperature = value / 100.0;
    temperatureLabel->setText(QString::number(temperature, 'f', 2));
    updateVisualization();
}

void AttentionDistWidget::addToken()
{
    int row = tokenTable->rowCount();
    tokenTable->insertRow(row);
    
    QTableWidgetItem *tokenItem = new QTableWidgetItem(QString("Token%1").arg(row + 1));
    tokenTable->setItem(row, 0, tokenItem);
    
    QTableWidgetItem *scoreItem = new QTableWidgetItem("0.0");
    tokenTable->setItem(row, 1, scoreItem);
}

void AttentionDistWidget::removeToken()
{
    int row = tokenTable->currentRow();
    if (row >= 0 && tokenTable->rowCount() > 1) {
        tokenTable->removeRow(row);
        updateVisualization();
    }
}

std::vector<AttentionDistWidget::Example> AttentionDistWidget::getExamples()
{
    return {
        {"Translation: 'The cat sat on the mat'",
         {"The", "cat", "sat", "on", "the", "mat"},
         {0.5, 3.2, 1.0, 0.8, 0.3, 2.5},
         "Self-attention focusing on content words"},
        
        {"Question Answering",
         {"What", "is", "AI", "?", "[Answer]"},
         {0.2, 0.1, 4.5, 0.1, 1.0},
         "Cross-attention to 'AI' when generating answer"},
        
        {"Uniform Attention",
         {"Token1", "Token2", "Token3", "Token4"},
         {1.0, 1.0, 1.0, 1.0},
         "Equal attention - high entropy"},
        
        {"Sparse Attention",
         {"A", "B", "C", "D", "E"},
         {8.0, 0.5, 0.3, 0.2, 0.1},
         "Focused attention - low entropy"},
        
        {"Multi-Modal: Image Regions",
         {"Background", "Person", "Car", "Tree", "Sky"},
         {0.5, 5.0, 3.5, 1.0, 0.8},
         "Attention to salient objects"}
    };
}

void AttentionDistWidget::loadExample(int index)
{
    if (index == 0) return; // Custom
    
    auto examples = getExamples();
    if (index - 1 >= 0 && index - 1 < static_cast<int>(examples.size())) {
        const Example& ex = examples[index - 1];
        
        tokens = ex.tokens;
        scores = ex.scores;
        
        rebuildTokenTable();
        
        updateExplanation();
        explanationText->append(QString("<p><b>Example:</b> %1<br><i>%2</i></p>")
                               .arg(ex.name)
                               .arg(ex.description));
    }
}

void AttentionDistWidget::onModeChanged(int index)
{
    updateVisualization();
}

void AttentionDistWidget::updateExplanation()
{
    explanationText->setHtml(
        "<h3>Attention as Probability Distribution</h3>"
        "<p><b>Key Formula:</b> α<sub>i</sub> = softmax(score<sub>i</sub>/τ) = exp(s<sub>i</sub>/τ) / Σ exp(s<sub>j</sub>/τ)</p>"
        "<p><b>Temperature (τ) Effect:</b></p>"
        "<ul>"
        "<li><b>τ → 0:</b> Sharp distribution (argmax, one-hot). Low entropy.</li>"
        "<li><b>τ = 1:</b> Standard softmax</li>"
        "<li><b>τ → ∞:</b> Uniform distribution. Maximum entropy.</li>"
        "</ul>"
        "<p><b>Why Softmax?</b> Makes attention differentiable (vs hard selection), ensures weights sum to 1 (probability)</p>"
        "<p><b>Entropy:</b> Measures distribution spread. High = diffuse attention. Low = focused attention.</p>"
    );
}

void AttentionDistWidget::exportData()
{
    QString fileName = QFileDialog::getSaveFileName(this, "Export Attention Weights", "", "CSV Files (*.csv)");
    if (fileName.isEmpty()) return;
    
    QFile file(fileName);
    if (!file.open(QIODevice::WriteOnly | QIODevice::Text)) return;
    
    QTextStream out(&file);
    
    out << "Token,Score,Attention Weight,Percentage\n";
    
    for (size_t i = 0; i < tokens.size(); ++i) {
        out << QString::fromStdString(tokens[i]) << ","
            << scores[i] << ","
            << attentionWeights[i] << ","
            << (attentionWeights[i] * 100) << "%\n";
    }
    
    out << "\nStatistics:\n";
    out << "Temperature," << temperature << "\n";
    out << "Entropy," << calculateEntropy(attentionWeights) << " bits\n";
    out << "Max Weight," << *std::max_element(attentionWeights.begin(), attentionWeights.end()) << "\n";
    out << "Effective Tokens," << calculateEffectiveTokens(attentionWeights) << "\n";
    
    file.close();
}
