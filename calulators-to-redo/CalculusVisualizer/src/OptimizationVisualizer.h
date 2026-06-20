#ifndef OPTIMIZATIONVISUALIZER_H
#define OPTIMIZATIONVISUALIZER_H

#include <QWidget>
#include <QPushButton>
#include <QSlider>
#include <QLabel>
#include <QTimer>
#include <QVector>
#include <QPointF>
#include <QComboBox>

class OptimizationVisualizer : public QWidget {
    Q_OBJECT

public:
    explicit OptimizationVisualizer(QWidget *parent = nullptr);
    ~OptimizationVisualizer() override;

    void setFunction(const QString &function);

protected:
    void paintEvent(QPaintEvent *event) override;
    void mousePressEvent(QMouseEvent *event) override;

private slots:
    void startOptimization();
    void stopOptimization();
    void resetOptimization();
    void updateStep();
    void onLearningRateChanged(int value);
    void onAlgorithmChanged(int index);
    void onFunctionPresetChanged(int index);

private:
    void setupUI();
    void drawSurface(QPainter &painter);
    void drawGradientPath(QPainter &painter);
    void drawCurrentPoint(QPainter &painter);
    void drawContours(QPainter &painter);
    void drawInfo(QPainter &painter);
    
    double evaluateFunction(double x);
    double evaluateDerivative(double x);
    QPointF worldToScreen(const QPointF &worldPoint) const;
    QPointF screenToWorld(const QPointF &screenPoint) const;
    
    void performGradientDescentStep();
    void performMomentumStep();
    void performAdamStep();
    
    // UI Components
    QPushButton *m_startButton;
    QPushButton *m_stopButton;
    QPushButton *m_resetButton;
    QSlider *m_learningRateSlider;
    QLabel *m_learningRateLabel;
    QLabel *m_iterationLabel;
    QLabel *m_valueLabel;
    QComboBox *m_algorithmSelector;
    QComboBox *m_functionPreset;
    QTimer *m_animationTimer;
    
    // Optimization state
    QString m_currentFunction;
    double m_currentX;
    double m_currentY;
    double m_learningRate;
    int m_iteration;
    bool m_isRunning;
    
    // Path tracking
    QVector<QPointF> m_path;
    QVector<double> m_losses;
    
    // Momentum/Adam parameters
    double m_velocity;
    double m_momentum;
    double m_m;  // First moment
    double m_v;  // Second moment
    int m_t;     // Time step
    
    // View bounds
    double m_xMin, m_xMax;
    double m_yMin, m_yMax;
    
    // Colors
    QColor m_bgColor;
    QColor m_surfaceColor;
    QColor m_pathColor;
    QColor m_pointColor;
    QColor m_contourColor;
    
    enum Algorithm {
        GradientDescent,
        Momentum,
        Adam
    };
    
    Algorithm m_algorithm;
};

#endif // OPTIMIZATIONVISUALIZER_H
