#ifndef OPTIMIZATIONPATH3D_H
#define OPTIMIZATIONPATH3D_H

#include <QWidget>
#include <QtDataVisualization/Q3DSurface>
#include <QtDataVisualization/QCustom3DItem>
#include <QPushButton>
#include <QComboBox>
#include <QSpinBox>
#include <QDoubleSpinBox>
#include <QTimer>
#include <functional>

namespace QtDataVisualization {
    class Q3DSurface;
    class QCustom3DItem;
}

class OptimizationPath3D : public QWidget
{
    Q_OBJECT

public:
    using LossFunction = std::function<double(double, double)>;
    
    enum OptimizerType {
        SGD,
        Momentum,
        Adam,
        RMSprop
    };
    
    explicit OptimizationPath3D(QWidget *parent = nullptr);
    
    void setSurface(QtDataVisualization::Q3DSurface* surface);
    void setLossFunction(LossFunction func);
    void setStartPoint(double x, double y);
    void setOptimizer(OptimizerType type);
    void setLearningRate(double lr);
    void setMaxIterations(int maxIter);
    
    void start();
    void pause();
    void reset();
    void step();

signals:
    void iterationCompleted(int iteration, double x, double y, double loss);
    void optimizationFinished();
    void optimizerInfo(const QString& info);

private slots:
    void onAnimationStep();
    void onStartClicked();
    void onPauseClicked();
    void onResetClicked();
    void onStepClicked();
    void onOptimizerChanged(int index);

private:
    void setupUI();
    void performOptimizationStep();
    void updateVisualization();
    void addPathPoint(double x, double y);
    void clearPath();
    
    QPointF computeGradient(double x, double y) const;
    double evaluateFunction(double x, double y) const;
    
    QString getOptimizerName() const;
    QString getOptimizerDescription() const;
    
    QtDataVisualization::Q3DSurface* m_surface = nullptr;
    LossFunction m_function;
    
    // Optimization state
    OptimizerType m_optimizerType = SGD;
    double m_currentX = 0.0;
    double m_currentY = 0.0;
    double m_startX = 0.0;
    double m_startY = 0.0;
    double m_learningRate = 0.01;
    int m_maxIterations = 1000;
    int m_currentIteration = 0;
    
    // Optimizer-specific state
    double m_velocityX = 0.0;
    double m_velocityY = 0.0;
    double m_momentum = 0.9;
    
    // Adam parameters
    double m_beta1 = 0.9;
    double m_beta2 = 0.999;
    double m_epsilon = 1e-8;
    double m_m_x = 0.0, m_m_y = 0.0; // First moment
    double m_v_x = 0.0, m_v_y = 0.0; // Second moment
    
    // RMSprop parameters
    double m_rho = 0.9;
    double m_cache_x = 0.0;
    double m_cache_y = 0.0;
    
    // Visualization
    struct PathPoint {
        double x, y, z;
    };
    QVector<PathPoint> m_path;
    QVector<QtDataVisualization::QCustom3DItem*> m_pathItems;
    
    // Animation
    QTimer* m_animationTimer;
    bool m_isRunning = false;
    int m_animationSpeed = 50; // ms per step
    
    // UI Components
    QPushButton* m_startButton;
    QPushButton* m_pauseButton;
    QPushButton* m_resetButton;
    QPushButton* m_stepButton;
    
    QComboBox* m_optimizerCombo;
    QDoubleSpinBox* m_learningRateSpin;
    QSpinBox* m_maxIterSpin;
    QSpinBox* m_speedSpin;
    
    QLabel* m_statusLabel;
    QLabel* m_infoLabel;
};

#endif // OPTIMIZATIONPATH3D_H
