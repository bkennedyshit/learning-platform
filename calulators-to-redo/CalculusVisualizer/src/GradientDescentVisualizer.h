/**
 * GradientDescentVisualizer.h - Interactive gradient descent animation
 * Demonstrates how optimization works for understanding backpropagation
 */

#ifndef GRADIENTDESCENTVISUALIZER_H
#define GRADIENTDESCENTVISUALIZER_H

#include <QWidget>
#include <QTimer>
#include <QLineEdit>
#include <QPushButton>
#include <QSlider>
#include <QLabel>
#include <QSpinBox>
#include <QDoubleSpinBox>
#include <vector>

class GraphWidget;

class GradientDescentVisualizer : public QWidget
{
    Q_OBJECT

public:
    explicit GradientDescentVisualizer(QWidget *parent = nullptr);
    ~GradientDescentVisualizer() override;

private slots:
    void onStartAnimation();
    void onStopAnimation();
    void onResetAnimation();
    void onStepAnimation();
    void onLearningRateChanged(double value);
    void onFunctionChanged();
    void updateAnimation();

private:
    void setupUI();
    void setupConnections();
    void initializeOptimization();
    double evaluateFunction(double x);
    double computeGradient(double x);
    void performGradientStep();
    void updateVisualization();
    
    // UI Components
    GraphWidget *graphWidget;
    QLineEdit *functionInput;
    QPushButton *startBtn;
    QPushButton *stopBtn;
    QPushButton *resetBtn;
    QPushButton *stepBtn;
    QDoubleSpinBox *learningRateSpinBox;
    QSpinBox *maxIterationsSpinBox;
    QLabel *statusLabel;
    QLabel *currentValueLabel;
    QLabel *iterationLabel;
    QSlider *animationSpeedSlider;
    
    // Animation
    QTimer *animationTimer;
    
    // Optimization state
    QString currentFunction;
    double currentX;
    double currentY;
    double learningRate;
    int maxIterations;
    int currentIteration;
    std::vector<std::pair<double, double>> trajectory;
    
    bool isAnimating;
};

#endif // GRADIENTDESCENTVISUALIZER_H
