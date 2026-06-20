#ifndef CONTOURWIDGET_H
#define CONTOURWIDGET_H

#include <QWidget>
#include <QPainter>
#include <QMouseEvent>
#include <QWheelEvent>
#include <QVector>
#include <QPointF>
#include <functional>

class ContourWidget : public QWidget
{
    Q_OBJECT

public:
    using LossFunction = std::function<double(double, double)>;
    
    explicit ContourWidget(QWidget *parent = nullptr);
    
    void setLossFunction(LossFunction func);
    void setBounds(double minX, double maxX, double minY, double maxY);
    void setShowGradient(bool show);
    void setShowCriticalPoints(bool show);
    void setContourLevels(int levels);
    
    void addPath(const QVector<QPointF>& path, const QColor& color);
    void clearPaths();
    
    QPointF screenToWorld(const QPoint& screen) const;
    QPoint worldToScreen(const QPointF& world) const;

signals:
    void pointClicked(double x, double y);

protected:
    void paintEvent(QPaintEvent* event) override;
    void mousePressEvent(QMouseEvent* event) override;
    void mouseMoveEvent(QMouseEvent* event) override;
    void mouseReleaseEvent(QMouseEvent* event) override;
    void wheelEvent(QWheelEvent* event) override;
    void resizeEvent(QResizeEvent* event) override;

private:
    void computeContours();
    void computeGradient();
    void findCriticalPoints();
    
    double evaluateFunction(double x, double y) const;
    QPointF computeGradientAt(double x, double y) const;
    
    void drawContours(QPainter& painter);
    void drawGradientField(QPainter& painter);
    void drawCriticalPoints(QPainter& painter);
    void drawPaths(QPainter& painter);
    void drawAxes(QPainter& painter);
    
    LossFunction m_function;
    
    // View bounds (world coordinates)
    double m_minX = -5.0;
    double m_maxX = 5.0;
    double m_minY = -5.0;
    double m_maxY = 5.0;
    
    // Display options
    bool m_showGradient = true;
    bool m_showCriticalPoints = true;
    int m_contourLevels = 20;
    
    // Computed data
    struct ContourLevel {
        double value;
        QVector<QVector<QPointF>> lines;
    };
    QVector<ContourLevel> m_contours;
    
    struct GradientArrow {
        QPointF position;
        QPointF direction;
        double magnitude;
    };
    QVector<GradientArrow> m_gradientField;
    
    struct CriticalPoint {
        QPointF position;
        QString type; // "minimum", "maximum", "saddle"
        double value;
    };
    QVector<CriticalPoint> m_criticalPoints;
    
    // Optimization paths
    struct PathData {
        QVector<QPointF> points;
        QColor color;
    };
    QVector<PathData> m_paths;
    
    // Mouse interaction
    bool m_dragging = false;
    QPoint m_lastMousePos;
    QPointF m_panOffset;
    double m_zoom = 1.0;
    
    // Resolution for computation
    int m_resolution = 100;
    int m_gradientResolution = 20;
};

#endif // CONTOURWIDGET_H
