#ifndef MULTIOPTIMIZER_H
#define MULTIOPTIMIZER_H

#include <QWidget>
#include <QTableWidget>
#include <QPushButton>
#include <QSpinBox>
#include <QDoubleSpinBox>
#include <QTimer>
#include <QCheckBox>
#include <functional>

class MultiOptimizer : public QWidget
{
    Q_OBJECT

public:
    using LossFunction = std::function<double(double, double)>;
    
    enum OptimizerType {
        SGD,
        Momentum,
        Adam,
        RMSprop,
        Adagrad,
        Adadelta
    };
    
    struct OptimizerConfig {
        QString name;
        OptimizerType type;
        QColor color;
        double learningRate;
        bool enabled;
        
        // Starting position
        double startX;
        double startY;
        
        // Current state
        double currentX;
        double currentY;
        double currentLoss;
        int iterations;
        bool converged;
        
        // Algorithm-specific state
        double velocityX = 0.0;
        double velocityY = 0.0;
        double m_x = 0.0, m_y = 0.0;  // First moment (Adam/Momentum)
        double v_x = 0.0, v_y = 0.0;  // Second moment (Adam/RMSprop)
        double cache_x = 0.0, cache_y = 0.0; // Accumulated gradients
        
        // Per-optimizer tuning
        double momentum = 0.9;
        double beta1 = 0.9;
        double beta2 = 0.999;
        double rho = 0.9;
        double epsilon = 1e-8;
        
        QVector<QPointF> path;
    };
    
    explicit MultiOptimizer(QWidget *parent = nullptr);
    
    void setLossFunction(LossFunction func);
    void setBounds(double minX, double maxX, double minY, double maxY);
    void addOptimizer(const OptimizerConfig& config);
    void setRandomStartPoints(int count = 6);
    void clearAll();
    
    QVector<OptimizerConfig>& getOptimizers() { return m_optimizers; }
    
public slots:
    void startRace();
    void pause();
    void reset();
    void stepAll();

signals:
    void iterationCompleted(int optimizerIndex);
    void raceFinished(const QString& winner);
    void statusUpdate(const QString& status);

protected:
    void paintEvent(QPaintEvent* event) override;

private slots:
    void onAnimationStep();
    void onStartClicked();
    void onPauseClicked();
    void onResetClicked();
    void onStepClicked();
    void onOptimizerToggled(int row, int column);

private:
    void setupUI();
    void setupDefaultOptimizers();
    void performOptimizationStep(OptimizerConfig& opt);
    void updateTable();
    void drawPaths(QPainter& painter);
    void drawStartPoints(QPainter& painter);
    
    QPointF computeGradient(double x, double y) const;
    double evaluateFunction(double x, double y) const;
    
    QPoint worldToScreen(double x, double y) const;
    QPointF screenToWorld(const QPoint& screen) const;
    
    QString getOptimizerStats(const OptimizerConfig& opt) const;
    
    LossFunction m_function;
    QVector<OptimizerConfig> m_optimizers;
    
    double m_minX = -5.0;
    double m_maxX = 5.0;
    double m_minY = -5.0;
    double m_maxY = 5.0;
    
    int m_maxIterations = 1000;
    double m_convergenceThreshold = 1e-6;
    
    QTimer* m_animationTimer;
    bool m_isRunning = false;
    int m_animationSpeed = 100;
    
    // UI Components
    QWidget* m_canvas;
    QTableWidget* m_table;
    QPushButton* m_startButton;
    QPushButton* m_pauseButton;
    QPushButton* m_resetButton;
    QPushButton* m_stepButton;
    QPushButton* m_randomStartsButton;
    
    QSpinBox* m_maxIterSpin;
    QSpinBox* m_speedSpin;
    QCheckBox* m_showPathsCheck;
    
    bool m_showPaths = true;
};

#endif // MULTIOPTIMIZER_H
