#ifndef GRAPHWIDGET_H
#define GRAPHWIDGET_H

#include <QWidget>
#include <QPointF>
#include <QVector>
#include <QString>
#include <QPainter>
#include <QMouseEvent>
#include <QWheelEvent>

class GraphWidget : public QWidget {
    Q_OBJECT

public:
    explicit GraphWidget(QWidget *parent = nullptr);
    ~GraphWidget() override;

    void setFunction(const QString &function);
    void resetView();
    void setGridVisible(bool visible);

signals:
    void pointSelected(double x, double y);
    void derivativeCalculated(const QString &derivative);

protected:
    void paintEvent(QPaintEvent *event) override;
    void mousePressEvent(QMouseEvent *event) override;
    void mouseMoveEvent(QMouseEvent *event) override;
    void mouseReleaseEvent(QMouseEvent *event) override;
    void wheelEvent(QWheelEvent *event) override;
    void resizeEvent(QResizeEvent *event) override;

private:
    struct FunctionData {
        QString expression;
        QVector<QPointF> points;
        QColor color;
        QString label;
    };

    void calculatePoints();
    void calculateDerivativePoints();
    double evaluateFunction(const QString &expr, double x);
    QString calculateSymbolicDerivative(const QString &expr);
    
    void drawGrid(QPainter &painter);
    void drawAxes(QPainter &painter);
    void drawFunction(QPainter &painter, const FunctionData &func);
    void drawLegend(QPainter &painter);
    void drawCrosshair(QPainter &painter);
    void drawTracePoint(QPainter &painter);
    
    QPointF worldToScreen(const QPointF &worldPoint) const;
    QPointF screenToWorld(const QPointF &screenPoint) const;
    
    // Function data
    FunctionData m_functionData;
    FunctionData m_derivativeData;
    QString m_currentFunction;
    QString m_currentDerivative;
    
    // View transform
    double m_xMin, m_xMax;
    double m_yMin, m_yMax;
    double m_defaultXMin, m_defaultXMax;
    double m_defaultYMin, m_defaultYMax;
    
    // Interaction state
    bool m_isPanning;
    QPoint m_lastMousePos;
    QPointF m_tracePoint;
    bool m_showTrace;
    bool m_showGrid;
    
    // Colors (Desmos-inspired)
    QColor m_bgColor;
    QColor m_gridColor;
    QColor m_axisColor;
    QColor m_functionColor;
    QColor m_derivativeColor;
    QColor m_textColor;
};

#endif // GRAPHWIDGET_H
