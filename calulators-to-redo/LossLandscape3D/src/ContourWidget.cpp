#include "ContourWidget.h"
#include <QPainterPath>
#include <cmath>
#include <algorithm>

ContourWidget::ContourWidget(QWidget *parent)
    : QWidget(parent)
{
    setMinimumSize(400, 400);
    setMouseTracking(true);
}

void ContourWidget::setLossFunction(LossFunction func)
{
    m_function = func;
    computeContours();
    computeGradient();
    findCriticalPoints();
    update();
}

void ContourWidget::setBounds(double minX, double maxX, double minY, double maxY)
{
    m_minX = minX;
    m_maxX = maxX;
    m_minY = minY;
    m_maxY = maxY;
    
    if (m_function) {
        computeContours();
        computeGradient();
        findCriticalPoints();
        update();
    }
}

void ContourWidget::setShowGradient(bool show)
{
    m_showGradient = show;
    update();
}

void ContourWidget::setShowCriticalPoints(bool show)
{
    m_showCriticalPoints = show;
    update();
}

void ContourWidget::setContourLevels(int levels)
{
    m_contourLevels = levels;
    if (m_function) {
        computeContours();
        update();
    }
}

void ContourWidget::addPath(const QVector<QPointF>& path, const QColor& color)
{
    m_paths.append({path, color});
    update();
}

void ContourWidget::clearPaths()
{
    m_paths.clear();
    update();
}

QPointF ContourWidget::screenToWorld(const QPoint& screen) const
{
    double worldWidth = m_maxX - m_minX;
    double worldHeight = m_maxY - m_minY;
    
    double x = m_minX + (screen.x() / (double)width()) * worldWidth / m_zoom + m_panOffset.x();
    double y = m_maxY - (screen.y() / (double)height()) * worldHeight / m_zoom + m_panOffset.y();
    
    return QPointF(x, y);
}

QPoint ContourWidget::worldToScreen(const QPointF& world) const
{
    double worldWidth = m_maxX - m_minX;
    double worldHeight = m_maxY - m_minY;
    
    int x = ((world.x() - m_minX - m_panOffset.x()) * m_zoom / worldWidth) * width();
    int y = ((m_maxY - world.y() - m_panOffset.y()) * m_zoom / worldHeight) * height();
    
    return QPoint(x, y);
}

void ContourWidget::computeContours()
{
    if (!m_function) return;
    
    m_contours.clear();
    
    // First, find min and max values
    double minVal = std::numeric_limits<double>::max();
    double maxVal = std::numeric_limits<double>::lowest();
    
    for (int i = 0; i <= m_resolution; ++i) {
        for (int j = 0; j <= m_resolution; ++j) {
            double x = m_minX + (m_maxX - m_minX) * i / m_resolution;
            double y = m_minY + (m_maxY - m_minY) * j / m_resolution;
            double val = evaluateFunction(x, y);
            
            if (std::isfinite(val)) {
                minVal = std::min(minVal, val);
                maxVal = std::max(maxVal, val);
            }
        }
    }
    
    // Create contour levels using logarithmic spacing for better visualization
    for (int i = 0; i < m_contourLevels; ++i) {
        double t = i / (double)(m_contourLevels - 1);
        
        // Use exponential spacing to emphasize lower values
        double level = minVal + (maxVal - minVal) * (std::exp(t * 2) - 1) / (std::exp(2.0) - 1);
        
        ContourLevel contour;
        contour.value = level;
        
        // Simplified marching squares algorithm
        for (int row = 0; row < m_resolution; ++row) {
            for (int col = 0; col < m_resolution; ++col) {
                double x0 = m_minX + (m_maxX - m_minX) * col / m_resolution;
                double x1 = m_minX + (m_maxX - m_minX) * (col + 1) / m_resolution;
                double y0 = m_minY + (m_maxY - m_minY) * row / m_resolution;
                double y1 = m_minY + (m_maxY - m_minY) * (row + 1) / m_resolution;
                
                double v00 = evaluateFunction(x0, y0);
                double v10 = evaluateFunction(x1, y0);
                double v11 = evaluateFunction(x1, y1);
                double v01 = evaluateFunction(x0, y1);
                
                // Check if contour passes through this cell
                double vmin = std::min({v00, v10, v11, v01});
                double vmax = std::max({v00, v10, v11, v01});
                
                if (vmin <= level && level <= vmax) {
                    // Linear interpolation to find contour crossing points
                    QVector<QPointF> cellLine;
                    
                    // Check all four edges
                    if ((v00 <= level && level <= v10) || (v10 <= level && level <= v00)) {
                        double t = (level - v00) / (v10 - v00);
                        cellLine.append(QPointF(x0 + t * (x1 - x0), y0));
                    }
                    if ((v10 <= level && level <= v11) || (v11 <= level && level <= v10)) {
                        double t = (level - v10) / (v11 - v10);
                        cellLine.append(QPointF(x1, y0 + t * (y1 - y0)));
                    }
                    if ((v11 <= level && level <= v01) || (v01 <= level && level <= v11)) {
                        double t = (level - v01) / (v11 - v01);
                        cellLine.append(QPointF(x0 + t * (x1 - x0), y1));
                    }
                    if ((v01 <= level && level <= v00) || (v00 <= level && level <= v01)) {
                        double t = (level - v00) / (v01 - v00);
                        cellLine.append(QPointF(x0, y0 + t * (y1 - y0)));
                    }
                    
                    if (cellLine.size() >= 2) {
                        contour.lines.append(cellLine);
                    }
                }
            }
        }
        
        if (!contour.lines.isEmpty()) {
            m_contours.append(contour);
        }
    }
}

void ContourWidget::computeGradient()
{
    if (!m_function) return;
    
    m_gradientField.clear();
    
    double stepX = (m_maxX - m_minX) / m_gradientResolution;
    double stepY = (m_maxY - m_minY) / m_gradientResolution;
    
    for (int i = 0; i <= m_gradientResolution; ++i) {
        for (int j = 0; j <= m_gradientResolution; ++j) {
            double x = m_minX + stepX * i;
            double y = m_minY + stepY * j;
            
            QPointF grad = computeGradientAt(x, y);
            double mag = std::sqrt(grad.x() * grad.x() + grad.y() * grad.y());
            
            if (mag > 1e-8) {
                GradientArrow arrow;
                arrow.position = QPointF(x, y);
                arrow.direction = grad / mag; // Normalize
                arrow.magnitude = mag;
                m_gradientField.append(arrow);
            }
        }
    }
}

void ContourWidget::findCriticalPoints()
{
    if (!m_function) return;
    
    m_criticalPoints.clear();
    
    // Simple critical point detection using gradient magnitude
    double stepX = (m_maxX - m_minX) / 50;
    double stepY = (m_maxY - m_minY) / 50;
    
    for (int i = 1; i < 50; ++i) {
        for (int j = 1; j < 50; ++j) {
            double x = m_minX + stepX * i;
            double y = m_minY + stepY * j;
            
            QPointF grad = computeGradientAt(x, y);
            double mag = std::sqrt(grad.x() * grad.x() + grad.y() * grad.y());
            
            if (mag < 0.1) { // Potential critical point
                // Use Hessian to classify (simplified)
                double h = 0.01;
                QPointF gx1 = computeGradientAt(x + h, y);
                QPointF gx0 = computeGradientAt(x - h, y);
                QPointF gy1 = computeGradientAt(x, y + h);
                QPointF gy0 = computeGradientAt(x, y - h);
                
                double fxx = (gx1.x() - gx0.x()) / (2 * h);
                double fyy = (gy1.y() - gy0.y()) / (2 * h);
                double fxy = (gx1.y() - gx0.y()) / (2 * h);
                
                double det = fxx * fyy - fxy * fxy;
                
                CriticalPoint cp;
                cp.position = QPointF(x, y);
                cp.value = evaluateFunction(x, y);
                
                if (det > 0.01) {
                    cp.type = (fxx > 0) ? "minimum" : "maximum";
                } else if (det < -0.01) {
                    cp.type = "saddle";
                } else {
                    continue; // Skip degenerate cases
                }
                
                // Check if this point is too close to existing criticalpoints
                bool tooClose = false;
                for (const auto& existing : m_criticalPoints) {
                    double dx = cp.position.x() - existing.position.x();
                    double dy = cp.position.y() - existing.position.y();
                    if (dx * dx + dy * dy < stepX * stepX) {
                        tooClose = true;
                        break;
                    }
                }
                
                if (!tooClose) {
                    m_criticalPoints.append(cp);
                }
            }
        }
    }
}

double ContourWidget::evaluateFunction(double x, double y) const
{
    if (!m_function) return 0.0;
    
    double val = m_function(x, y);
    
    // Clamp extreme values
    if (!std::isfinite(val) || std::abs(val) > 10000.0) {
        return (val > 0) ? 10000.0 : -10000.0;
    }
    
    return val;
}

QPointF ContourWidget::computeGradientAt(double x, double y) const
{
    double h = 0.01;
    
    double fx1 = evaluateFunction(x + h, y);
    double fx0 = evaluateFunction(x - h, y);
    double fy1 = evaluateFunction(x, y + h);
    double fy0 = evaluateFunction(x, y - h);
    
    double dx = (fx1 - fx0) / (2 * h);
    double dy = (fy1 - fy0) / (2 * h);
    
    return QPointF(dx, dy);
}

void ContourWidget::paintEvent(QPaintEvent* event)
{
    QPainter painter(this);
    painter.setRenderHint(QPainter::Antialiasing);
    
    // Background
    painter.fillRect(rect(), Qt::white);
    
    drawAxes(painter);
    drawContours(painter);
    
    if (m_showGradient) {
        drawGradientField(painter);
    }
    
    if (m_showCriticalPoints) {
        drawCriticalPoints(painter);
    }
    
    drawPaths(painter);
}

void ContourWidget::drawContours(QPainter& painter)
{
    for (int i = 0; i < m_contours.size(); ++i) {
        const auto& contour = m_contours[i];
        
        // Color based on level
        double t = i / (double)m_contours.size();
        QColor color;
        color.setHsvF(0.6 - t * 0.6, 0.7, 0.9); // Blue to red
        
        painter.setPen(QPen(color, 1.5));
        
        for (const auto& line : contour.lines) {
            if (line.size() >= 2) {
                QPainterPath path;
                QPoint start = worldToScreen(line[0]);
                path.moveTo(start);
                
                for (int j = 1; j < line.size(); ++j) {
                    QPoint pt = worldToScreen(line[j]);
                    path.lineTo(pt);
                }
                
                painter.drawPath(path);
            }
        }
    }
}

void ContourWidget::drawGradientField(QPainter& painter)
{
    for (const auto& arrow : m_gradientField) {
        // Color by magnitude
        double t = std::min(arrow.magnitude / 10.0, 1.0);
        QColor color = QColor::fromHsvF(0.0, t, 0.8);
        
        painter.setPen(QPen(color, 1.5));
        painter.setBrush(color);
        
        QPoint start = worldToScreen(arrow.position);
        double arrowLength = 20.0;
        QPointF end = arrow.position + arrow.direction * (m_maxX - m_minX) * 0.03;
        QPoint endScreen = worldToScreen(end);
        
        // Draw arrow line
        painter.drawLine(start, endScreen);
        
        // Draw arrowhead
        QPointF dir = arrow.direction;
        double angle = std::atan2(dir.y(), dir.x());
        
        QPointF arrowHead1(
            endScreen.x() - 8 * std::cos(angle - 0.4),
            endScreen.y() + 8 * std::sin(angle - 0.4)
        );
        QPointF arrowHead2(
            endScreen.x() - 8 * std::cos(angle + 0.4),
            endScreen.y() + 8 * std::sin(angle + 0.4)
        );
        
        QPainterPath arrowPath;
        arrowPath.moveTo(endScreen);
        arrowPath.lineTo(arrowHead1);
        arrowPath.lineTo(arrowHead2);
        arrowPath.closeSubpath();
        
        painter.drawPath(arrowPath);
    }
}

void ContourWidget::drawCriticalPoints(QPainter& painter)
{
    for (const auto& cp : m_criticalPoints) {
        QPoint screen = worldToScreen(cp.position);
        
        QColor color;
        QString symbol;
        
        if (cp.type == "minimum") {
            color = Qt::darkGreen;
            symbol = "MIN";
        } else if (cp.type == "maximum") {
            color = Qt::darkRed;
            symbol = "MAX";
        } else { // saddle
            color = Qt::darkMagenta;
            symbol = "SADDLE";
        }
        
        painter.setPen(QPen(color, 2));
        painter.setBrush(color);
        
        // Draw marker
        painter.drawEllipse(screen, 6, 6);
        
        // Draw label
        painter.setPen(color);
        QFont font = painter.font();
        font.setPointSize(8);
        font.setBold(true);
        painter.setFont(font);
        painter.drawText(screen.x() + 10, screen.y() - 5, symbol);
    }
}

void ContourWidget::drawPaths(QPainter& painter)
{
    for (const auto& pathData : m_paths) {
        if (pathData.points.isEmpty()) continue;
        
        painter.setPen(QPen(pathData.color, 2));
        
        QPainterPath path;
        QPoint start = worldToScreen(pathData.points[0]);
        path.moveTo(start);
        
        for (int i = 1; i < pathData.points.size(); ++i) {
            QPoint pt = worldToScreen(pathData.points[i]);
            path.lineTo(pt);
        }
        
        painter.drawPath(path);
        
        // Draw start point
        painter.setBrush(pathData.color);
        painter.drawEllipse(start, 5, 5);
        
        // Draw end point
        if (pathData.points.size() > 1) {
            QPoint end = worldToScreen(pathData.points.last());
            painter.drawEllipse(end, 4, 4);
        }
    }
}

void ContourWidget::drawAxes(QPainter& painter)
{
    painter.setPen(QPen(Qt::black, 1));
    
    // Draw border
    painter.drawRect(rect().adjusted(0, 0, -1, -1));
    
    // Draw grid
    painter.setPen(QPen(QColor(200, 200, 200), 0.5));
    
    for (int i = 0; i <= 10; ++i) {
        double t = i / 10.0;
        double x = m_minX + (m_maxX - m_minX) * t;
        double y = m_minY + (m_maxY - m_minY) * t;
        
        QPoint top = worldToScreen(QPointF(x, m_maxY));
        QPoint bottom = worldToScreen(QPointF(x, m_minY));
        painter.drawLine(top, bottom);
        
        QPoint left = worldToScreen(QPointF(m_minX, y));
        QPoint right = worldToScreen(QPointF(m_maxX, y));
        painter.drawLine(left, right);
    }
}

void ContourWidget::mousePressEvent(QMouseEvent* event)
{
    if (event->button() == Qt::LeftButton) {
        QPointF world = screenToWorld(event->pos());
        emit pointClicked(world.x(), world.y());
    } else if (event->button() == Qt::RightButton) {
        m_dragging = true;
        m_lastMousePos = event->pos();
    }
}

void ContourWidget::mouseMoveEvent(QMouseEvent* event)
{
    if (m_dragging) {
        QPoint delta = event->pos() - m_lastMousePos;
        double worldWidth = m_maxX - m_minX;
        double worldHeight = m_maxY - m_minY;
        
        m_panOffset.setX(m_panOffset.x() - delta.x() * worldWidth / width() / m_zoom);
        m_panOffset.setY(m_panOffset.y() + delta.y() * worldHeight / height() / m_zoom);
        
        m_lastMousePos = event->pos();
        update();
    }
}

void ContourWidget::mouseReleaseEvent(QMouseEvent* event)
{
    if (event->button() == Qt::RightButton) {
        m_dragging = false;
    }
}

void ContourWidget::wheelEvent(QWheelEvent* event)
{
    double zoomFactor = event->angleDelta().y() > 0 ? 1.1 : 0.9;
    m_zoom *= zoomFactor;
    m_zoom = std::max(0.1, std::min(m_zoom, 10.0));
    update();
}

void ContourWidget::resizeEvent(QResizeEvent* event)
{
    QWidget::resizeEvent(event);
}
