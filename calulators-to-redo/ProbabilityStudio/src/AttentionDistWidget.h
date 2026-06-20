#ifndef ATTENTIONDISTWIDGET_H
#define ATTENTIONDISTWIDGET_H

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
#include <QDoubleSpinBox>
#include <QLineEdit>
#include <QTableWidget>
#include <QtCharts/QChartView>
#include <QtCharts/QLineSeries>
#include <QtCharts/QScatterSeries>
#include <QtCharts/QBarSeries>
#include <QtCharts/QBarSet>
#include <QtCharts/QPieSeries>
#include <QtCharts/QValueAxis>
#include <QtCharts/QBarCategoryAxis>
#include <vector>
#include <string>

QT_CHARTS_USE_NAMESPACE

/**
 * AttentionDistWidget - Attention Mechanism Visualizer
 * 
 * WHAT IS ATTENTION?
 * A mechanism that allows models to focus on relevant parts of input 
 * by computing weighted combinations using probability distributions.
 * 
 * ATTENTION FORMULA:
 * 1. Scores: e_i = f(query, key_i)  [similarity/relevance scores]
 * 2. Weights: α_i = softmax(e_i) = exp(e_i) / Σ exp(e_j)  [probabilities!]
 * 3. Output: context = Σ α_i * value_i  [weighted combination]
 * 
 * KEY INSIGHT: Attention weights form a PROBABILITY DISTRIBUTION!
 * - Each weight α_i ∈ [0, 1]
 * - Σ α_i = 1
 * - Interpret as "where the model is looking"
 * 
 * TYPES:
 * - Self-Attention: Query, Key, Value all from same sequence
 * - Cross-Attention: Query from one sequence, K/V from another
 * - Multi-Head: Multiple attention mechanisms in parallel
 * - Scaled Dot-Product: Attention(Q,K,V) = softmax(QK^T/√d_k)V
 * 
 * WHY IT REVOLUTIONIZED ML:
 * - Transformers (GPT, BERT, etc.) rely entirely on attention
 * - Replaces recurrence with parallelizable operations
 * - Long-range dependencies without sequential processing
 * - Interpretable: visualize what model attends to
 * 
 * PROBABILISTIC PERSPECTIVE:
 * Attention is soft/weighted selection using probability distributions,
 * unlike hard selection (argmax). This makes it differentiable!
 */
class AttentionDistWidget : public QWidget
{
    Q_OBJECT

public:
    explicit AttentionDistWidget(QWidget *parent = nullptr);
    ~AttentionDistWidget();

private slots:
    void updateVisualization();
    void onModeChanged(int index);
    void exportData();
    void addToken();
    void removeToken();
    void loadExample(int index);
    void updateTemperature(int value);

private:
    enum VisualizationMode {
        WEIGHTS_BAR,
        WEIGHTS_PIE,
        HEATMAP_MODE,
        ENTROPY_MODE
    };
    
    // UI Components
    QComboBox *modeSelector;
    QComboBox *exampleSelector;
    QChartView *chartView;
    QChart *chart;
    QTextEdit *explanationText;
    QPushButton *exportButton;
    QPushButton *addTokenButton;
    QPushButton *removeTokenButton;
    
    // Token/sequence input
    QTableWidget *tokenTable;
    QSpinBox *numTokensSpin;
    QSlider *temperatureSlider;
    QLabel *temperatureLabel;
    QDoubleSpinBox *scalingSpin;
    
    // Statistics display
    QLabel *entropyLabel;
    QLabel *maxAttentionLabel;
    QLabel *effectiveTokensLabel;
    QLabel *sparsityLabel;
    
    // Data
    std::vector<std::string> tokens;
    std::vector<double> scores;
    std::vector<double> attentionWeights;
    double temperature;
    
    // Methods
    void setupUI();
    void setupTokenTable();
    std::vector<double> calculateAttentionWeights();
    std::vector<double> softmax(const std::vector<double>& scores, double temp = 1.0);
    double calculateEntropy(const std::vector<double>& probs);
    int calculateEffectiveTokens(const std::vector<double>& weights);
    
    // Visualization methods
    void updateBarChart();
    void updatePieChart();
    void updateHeatmap();
    void updateEntropyPlot();
    
    // UI updates
    void updateStatistics();
    void updateExplanation();
    void rebuildTokenTable();
    
    // Example scenarios
    struct Example {
        QString name;
        std::vector<std::string> tokens;
        std::vector<double> scores;
        QString description;
    };
    std::vector<Example> getExamples();
};

#endif // ATTENTIONDISTWIDGET_H
