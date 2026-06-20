#ifndef TANGENTLINEWIDGET_H
#define TANGENTLINEWIDGET_H

#include <QWidget>
#include <QPointF>
#include <QVector>
#include <QString>
#include <QPushButton>
#include <QSlider>
#include <QLabel>

class TangentLineWidget : public QWidget {
    Q_OBJECT

public:
    explicit TangentLineWidget(QWidget *parent = nullptr);
    ~TangentLineWidget() override;

    void setFunction(const QString &function);
    void resetView();
    void setGridVisible(bool visible);

protected:
    void paintEvent(QPaintEvent *event) override;
    void mousePressEvent(QMouseEvent *event) override;
    void mouseMoveEvent(QMouseEvent *event) override;
    void wheelEvent(QWheelEvent *event) override;

private slots:
    void onXSliderChanged(int value);
    void onAnimationToggled(bool checked);
    void updateAnimation();

private:
    void setupUI();
    void calculateFunctionPoints();
    void drawFunction(QPainter &painter);
    void drawTangentLine(QPainter &painter);
    void drawNormalLine(QPainter &painter);
    void drawSecantLine(QPainter &painter);
    void drawGrid(QPainter &painter);
    void drawAxes(QPainter &painter);
    void drawInfo(QPainter &painter);
    void drawTangentInfo(QPainter &painter);
    
    double evaluateFunction(double x);
    double evaluateDerivative(double x);
    QPointF worldToScreen(const QPointF &worldPoint) const;
    QPointF screenToWorld(const QPointF &screenPoint) const;
    
    // UI Components
    QSlider *m_xSlider;
    QLabel *m_xLabel;
    QLabel *m_slopeLabel;
    QLabel *m_equationLabel;
    QPushButton *m_animateButton;
    QTimer *m_animationTimer;
    
    // Function data
    QString m_currentFunction;
    QVector<QPointF> m_functionPoints;
    double m_tangentX;
    double m_tangentY;
    double m_slope;
    bool m_showNormal;
    bool m_showSecant;
    bool m_showGrid;
    bool m_isAnimating;
    
    // View bounds
    double m_xMin, m_xMax;
    double m_yMin, m_yMax;
    
    // Secant line second point
    double m_secantX2;
    
    // Colors
    QColor m_bgColor;
    QColor m_gridColor;
    QColor m_axisColor;
    QColor m_functionColor;
    QColor m_tangentColor;
    QColor m_normalColor;
    QColor m_secantColor;
    QColor m_pointColor;
};

#endif // TANGENTLINEWIDGET_H
