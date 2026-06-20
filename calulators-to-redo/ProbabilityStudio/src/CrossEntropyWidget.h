#ifndef CROSSENTROPYWIDGET_H
#define CROSSENTROPYWIDGET_H

#include <QWidget>
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QSlider>
#include <QLabel>
#include <QPushButton>
#include <QComboBox>
#include <QTextEdit>
#include <QGroupBox>
#include <QtCharts/QChartView>
#include <QtCharts/QLineSeries>
#include <QtCharts/QValueAxis>
#include <QtCharts/QBarSeries>
#include <QtCharts/QBarSet>
#include <QtCharts/QBarCategoryAxis>
#include <QSpinBox>
#include <vector>

QT_CHARTS_USE_NAMESPACE

/**
 * CrossEntropyWidget - Interactive visualization of cross-entropy loss
 * 
 * WHAT IS CROSS-ENTROPY?
 * Cross-entropy measures the difference between two probability distributions.
 * In ML, it quantifies how well predicted probabilities match true labels.
 * 
 * Binary Cross-Entropy: H(p,q) = -[p*log(q) + (1-p)*log(1-q)]
 * Categorical Cross-Entropy: H(p,q) = -Σ p_i * log(q_i)
 * 
 * WHY USE IT AS A LOSS FUNCTION?
 * 1. Penalizes confident wrong predictions heavily
 * 2. Gradient-friendly for neural networks
 * 3. Directly optimizes probability calibration
 * 4. Equivalent to maximum likelihood estimation
 */
class CrossEntropyWidget : public QWidget
{
    Q_OBJECT

public:
    explicit CrossEntropyWidget(QWidget *parent = nullptr);
    ~CrossEntropyWidget();

private slots:
    void updateBinaryVisualization();
    void updateCategoricalVisualization();
    void onModeChanged(int index);
    void exportData();
    void addCategory();
    void removeCategory();

private:
    // UI Components
    QComboBox *modeSelector;
    QChartView *chartView;
    QChart *chart;
    QTextEdit *explanationText;
    QPushButton *exportButton;
    
    // Binary mode widgets
    QGroupBox *binaryGroup;
    QSlider *trueLabelSlider;
    QSlider *predictedProbSlider;
    QLabel *trueLabelValue;
    QLabel *predictedProbValue;
    QLabel *binaryLossValue;
    
    // Categorical mode widgets
    QGroupBox *categoricalGroup;
    QSpinBox *numClassesSpinBox;
    std::vector<QSlider*> trueProbSliders;
    std::vector<QSlider*> predictedProbSliders;
    std::vector<QLabel*> trueProbLabels;
    std::vector<QLabel*> predictedProbLabels;
    QLabel *categoricalLossValue;
    QWidget *classesContainer;
    QVBoxLayout *classesLayout;
    
    // Calculation methods
    double calculateBinaryCrossEntropy(double trueLabel, double predicted);
    double calculateCategoricalCrossEntropy(const std::vector<double>& trueProbs, 
                                           const std::vector<double>& predProbs);
    
    // Visualization methods
    void setupBinaryChart();
    void setupCategoricalChart();
    void updateBinaryChart();
    void updateCategoricalChart();
    
    // UI setup methods
    void setupUI();
    void setupBinaryControls();
    void setupCategoricalControls();
    void updateExplanation();
    void rebuildCategorySliders();
};

#endif // CROSSENTROPYWIDGET_H
