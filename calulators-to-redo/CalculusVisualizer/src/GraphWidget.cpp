#include "GraphWidget.h"
#include <QPainter>
#include <QPainterPath>
#include <QFontMetrics>
#include <QtMath>
#include <QDebug>
#include <cmath>

GraphWidget::GraphWidget(QWidget *parent)
    : QWidget(parent)
    , m_xMin(-10.0)
    , m_xMax(10.0)
    , m_yMin(-10.0)
    , m_yMax(10.0)
    , m_defaultXMin(-10.0)
    , m_defaultXMax(10.0)
    , m_defaultYMin(-10.0)
    , m_defaultYMax(10.0)
    , m_isPanning(false)
    , m_showTrace(false)
    , m_showGrid(true)
{
    setMinimumSize(600, 400);
    setMouseTracking(true);
    
    // Desmos-inspired colors
    m_bgColor = QColor(33, 33, 33);
    m_gridColor = QColor(60, 60, 60);
    m_axisColor = QColor(200, 200, 200);
    m_functionColor = QColor(0, 136, 255);  // Blue
    m_derivativeColor = QColor(67, 223, 101);  // Green
    m_textColor = QColor(230, 230, 230);
    
    m_functionData.color = m_functionColor;
    m_functionData.label = "f(x)";
    m_derivativeData.color = m_derivativeColor;
    m_derivativeData.label = "f'(x)";
}

GraphWidget::~GraphWidget() {}

void GraphWidget::setFunction(const QString &function) {
    m_currentFunction = function;
    m_functionData.expression = function;
    
    // Calculate symbolic derivative
    m_currentDerivative = calculateSymbolicDerivative(function);
    m_derivativeData.expression = m_currentDerivative;
    
    emit derivativeCalculated(m_currentDerivative);
    
    calculatePoints();
    calculateDerivativePoints();
    update();
}

void GraphWidget::resetView() {
    m_xMin = m_defaultXMin;
    m_xMax = m_defaultXMax;
    m_yMin = m_defaultYMin;
    m_yMax = m_defaultYMax;
    update();
}

void GraphWidget::setGridVisible(bool visible) {
    m_showGrid = visible;
    update();
}

void GraphWidget::calculatePoints() {
    m_functionData.points.clear();
    
    if (m_currentFunction.isEmpty()) return;
    
    int numPoints = width() * 2;  // High resolution
    double step = (m_xMax - m_xMin) / numPoints;
    
    for (int i = 0; i < numPoints; ++i) {
        double x = m_xMin + i * step;
        double y = evaluateFunction(m_currentFunction, x);
        
        if (std::isfinite(y) && y > -1e6 && y < 1e6) {
            m_functionData.points.append(QPointF(x, y));
        }
    }
}

void GraphWidget::calculateDerivativePoints() {
    m_derivativeData.points.clear();
    
    if (m_currentDerivative.isEmpty()) return;
    
    int numPoints = width() * 2;
    double step = (m_xMax - m_xMin) / numPoints;
    
    for (int i = 0; i < numPoints; ++i) {
        double x = m_xMin + i * step;
        double y = evaluateFunction(m_currentDerivative, x);
        
        if (std::isfinite(y) && y > -1e6 && y < 1e6) {
            m_derivativeData.points.append(QPointF(x, y));
        }
    }
}

double GraphWidget::evaluateFunction(const QString &expr, double x) {
    // Simple expression evaluator
    QString e = expr.toLower();
    e.replace("x", QString::number(x));
    
    // Handle common functions
    if (e.contains("sin")) {
        QRegExp rx("sin\\(([^)]+)\\)");
        while (rx.indexIn(e) != -1) {
            QString arg = rx.cap(1);
            double value = evaluateFunction(arg, x);
            e.replace(rx.cap(0), QString::number(std::sin(value)));
        }
    }
    
    if (e.contains("cos")) {
        QRegExp rx("cos\\(([^)]+)\\)");
        while (rx.indexIn(e) != -1) {
            QString arg = rx.cap(1);
            double value = evaluateFunction(arg, x);
            e.replace(rx.cap(0), QString::number(std::cos(value)));
        }
    }
    
    if (e.contains("exp")) {
        QRegExp rx("exp\\(([^)]+)\\)");
        while (rx.indexIn(e) != -1) {
            QString arg = rx.cap(1);
            double value = evaluateFunction(arg, x);
            e.replace(rx.cap(0), QString::number(std::exp(value)));
        }
    }
    
    if (e.contains("log")) {
        QRegExp rx("log\\(([^)]+)\\)");
        while (rx.indexIn(e) != -1) {
            QString arg = rx.cap(1);
            double value = evaluateFunction(arg, x);
            e.replace(rx.cap(0), QString::number(std::log(value)));
        }
    }
    
    if (e.contains("sqrt")) {
        QRegExp rx("sqrt\\(([^)]+)\\)");
        while (rx.indexIn(e) != -1) {
            QString arg = rx.cap(1);
            double value = evaluateFunction(arg, x);
            e.replace(rx.cap(0), QString::number(std::sqrt(value)));
        }
    }
    
    // Handle powers
    QRegExp powRx("([0-9.]+)\\^([0-9.]+)");
    while (powRx.indexIn(e) != -1) {
        double base = powRx.cap(1).toDouble();
        double exp = powRx.cap(2).toDouble();
        e.replace(powRx.cap(0), QString::number(std::pow(base, exp)));
    }
    
    // Simple arithmetic evaluation
    try {
        // This is a simplified evaluator - in production, use a proper parser
        QScriptEngine engine;
        QScriptValue result = engine.evaluate(e);
        return result.toNumber();
    } catch (...) {
        return std::numeric_limits<double>::quiet_NaN();
    }
}

QString GraphWidget::calculateSymbolicDerivative(const QString &expr) {
    QString e = expr.trimmed().toLower();
    
    // Power rule: x^n -> n*x^(n-1)
    if (e == "x") return "1";
    if (e == "x^2") return "2*x";
    if (e == "x^3") return "3*x^2";
    if (e == "x^4") return "4*x^3";
    
    // Trig functions
    if (e == "sin(x)") return "cos(x)";
    if (e == "cos(x)") return "-sin(x)";
    if (e == "tan(x)") return "sec(x)^2";
    
    // Exponential and logarithm
    if (e == "exp(x)") return "exp(x)";
    if (e.startsWith("exp(-x^2)")) return "-2*x*exp(-x^2)";
    if (e == "log(x)") return "1/x";
    if (e == "sqrt(x)") return "1/(2*sqrt(x))";
    
    // Composite functions
    if (e == "x^3 - 2*x") return "3*x^2 - 2";
    if (e == "x^3/3 - x") return "x^2 - 1";
    if (e == "x^4 - 4*x^2") return "4*x^3 - 8*x";
    if (e == "1/(1+exp(-x))") return "exp(-x)/(1+exp(-x))^2";  // Sigmoid derivative
    
    // General power rule using regex
    QRegExp powRx("x\\^([0-9.]+)");
    if (powRx.indexIn(e) != -1) {
        double n = powRx.cap(1).toDouble();
        if (n == 1) return "1";
        return QString("%1*x^%2").arg(n).arg(n - 1);
    }
    
    // Numerical derivative as fallback
    return "d/dx[" + expr + "]";
}

void GraphWidget::paintEvent(QPaintEvent *event) {
    Q_UNUSED(event);
    
    QPainter painter(this);
    painter.setRenderHint(QPainter::Antialiasing);
    
    // Background
    painter.fillRect(rect(), m_bgColor);
    
    // Draw components
    if (m_showGrid) {
        drawGrid(painter);
    }
    drawAxes(painter);
    
    if (!m_derivativeData.points.isEmpty()) {
        drawFunction(painter, m_derivativeData);
    }
    
    if (!m_functionData.points.isEmpty()) {
        drawFunction(painter, m_functionData);
    }
    
    drawLegend(painter);
    
    if (m_showTrace) {
        drawTracePoint(painter);
    }
}

void GraphWidget::drawGrid(QPainter &painter) {
    painter.setPen(QPen(m_gridColor, 1));
    
    // Calculate grid spacing
    double xRange = m_xMax - m_xMin;
    double yRange = m_yMax - m_yMin;
    
    double xStep = std::pow(10, std::floor(std::log10(xRange / 10)));
    double yStep = std::pow(10, std::floor(std::log10(yRange / 10)));
    
    // Vertical grid lines
    double x = std::floor(m_xMin / xStep) * xStep;
    while (x <= m_xMax) {
        QPointF p1 = worldToScreen(QPointF(x, m_yMin));
        QPointF p2 = worldToScreen(QPointF(x, m_yMax));
        painter.drawLine(p1, p2);
        x += xStep;
    }
    
    // Horizontal grid lines
    double y = std::floor(m_yMin / yStep) * yStep;
    while (y <= m_yMax) {
        QPointF p1 = worldToScreen(QPointF(m_xMin, y));
        QPointF p2 = worldToScreen(QPointF(m_xMax, y));
        painter.drawLine(p1, p2);
        y += yStep;
    }
}

void GraphWidget::drawAxes(QPainter &painter) {
    painter.setPen(QPen(m_axisColor, 2));
    
    // X-axis
    if (m_yMin <= 0 && m_yMax >= 0) {
        QPointF p1 = worldToScreen(QPointF(m_xMin, 0));
        QPointF p2 = worldToScreen(QPointF(m_xMax, 0));
        painter.drawLine(p1, p2);
        
        // Draw arrow
        painter.drawLine(p2, p2 + QPointF(-10, -5));
        painter.drawLine(p2, p2 + QPointF(-10, 5));
    }
    
    // Y-axis
    if (m_xMin <= 0 && m_xMax >= 0) {
        QPointF p1 = worldToScreen(QPointF(0, m_yMin));
        QPointF p2 = worldToScreen(QPointF(0, m_yMax));
        painter.drawLine(p1, p2);
        
        // Draw arrow
        painter.drawLine(p2, p2 + QPointF(-5, 10));
        painter.drawLine(p2, p2 + QPointF(5, 10));
    }
    
    // Axis labels
    painter.setPen(m_textColor);
    QFont font = painter.font();
    font.setPointSize(10);
    painter.setFont(font);
    
    // Draw tick marks and labels
    double xRange = m_xMax - m_xMin;
    double xStep = std::pow(10, std::floor(std::log10(xRange / 10)));
    
    double x = std::floor(m_xMin / xStep) * xStep;
    while (x <= m_xMax) {
        if (std::abs(x) > 0.001) {  // Skip zero
            QPointF pt = worldToScreen(QPointF(x, 0));
            painter.drawLine(pt + QPointF(0, -5), pt + QPointF(0, 5));
            painter.drawText(pt + QPointF(-20, 20), 40, 20, 
                           Qt::AlignCenter, QString::number(x, 'g', 3));
        }
        x += xStep;
    }
}

void GraphWidget::drawFunction(QPainter &painter, const FunctionData &func) {
    if (func.points.size() < 2) return;
    
    QPainterPath path;
    bool firstPoint = true;
    
    for (const QPointF &pt : func.points) {
        QPointF screenPt = worldToScreen(pt);
        
        if (screenPt.y() >= 0 && screenPt.y() <= height()) {
            if (firstPoint) {
                path.moveTo(screenPt);
                firstPoint = false;
            } else {
                path.lineTo(screenPt);
            }
        } else {
            firstPoint = true;
        }
    }
    
    painter.setPen(QPen(func.color, 3, Qt::SolidLine, Qt::RoundCap, Qt::RoundJoin));
    painter.drawPath(path);
}

void GraphWidget::drawLegend(QPainter &painter) {
    painter.setPen(m_textColor);
    QFont font = painter.font();
    font.setPointSize(11);
    font.setBold(true);
    painter.setFont(font);
    
    int y = 20;
    
    // Function legend
    if (!m_functionData.points.isEmpty()) {
        painter.setPen(m_functionColor);
        painter.drawText(10, y, QString("%1 = %2").arg(m_functionData.label).arg(m_currentFunction));
        y += 25;
    }
    
    // Derivative legend
    if (!m_derivativeData.points.isEmpty()) {
        painter.setPen(m_derivativeColor);
        painter.drawText(10, y, QString("%1 = %2").arg(m_derivativeData.label).arg(m_currentDerivative));
    }
}

void GraphWidget::drawTracePoint(QPainter &painter) {
    QPointF screenPt = worldToScreen(m_tracePoint);
    
    // Draw crosshair
    painter.setPen(QPen(Qt::yellow, 1, Qt::DashLine));
    painter.drawLine(screenPt.x(), 0, screenPt.x(), height());
    painter.drawLine(0, screenPt.y(), width(), screenPt.y());
    
    // Draw point
    painter.setPen(QPen(Qt::yellow, 2));
    painter.setBrush(Qt::yellow);
    painter.drawEllipse(screenPt, 5, 5);
    
    // Draw coordinates
    painter.setPen(Qt::white);
    painter.setBrush(QColor(0, 0, 0, 180));
    QString coordText = QString("(%1, %2)").arg(m_tracePoint.x(), 0, 'f', 2)
                                           .arg(m_tracePoint.y(), 0, 'f', 2);
    QFontMetrics fm(painter.font());
    QRect textRect = fm.boundingRect(coordText).adjusted(-5, -5, 5, 5);
    textRect.moveCenter(screenPt.toPoint() + QPoint(0, -30));
    painter.drawRect(textRect);
    painter.drawText(textRect, Qt::AlignCenter, coordText);
}

QPointF GraphWidget::worldToScreen(const QPointF &worldPoint) const {
    double sx = (worldPoint.x() - m_xMin) / (m_xMax - m_xMin) * width();
    double sy = (m_yMax - worldPoint.y()) / (m_yMax - m_yMin) * height();
    return QPointF(sx, sy);
}

QPointF GraphWidget::screenToWorld(const QPointF &screenPoint) const {
    double wx = m_xMin + (screenPoint.x() / width()) * (m_xMax - m_xMin);
    double wy = m_yMax - (screenPoint.y() / height()) * (m_yMax - m_yMin);
    return QPointF(wx, wy);
}

void GraphWidget::mousePressEvent(QMouseEvent *event) {
    if (event->button() == Qt::LeftButton) {
        m_isPanning = true;
        m_lastMousePos = event->pos();
    } else if (event->button() == Qt::RightButton) {
        m_tracePoint = screenToWorld(event->pos());
        m_showTrace = true;
        
        double x = m_tracePoint.x();
        double y = evaluateFunction(m_currentFunction, x);
        m_tracePoint.setY(y);
        
        emit pointSelected(x, y);
        update();
    }
}

void GraphWidget::mouseMoveEvent(QMouseEvent *event) {
    if (m_isPanning) {
        QPoint delta = event->pos() - m_lastMousePos;
        double dx = -delta.x() / width() * (m_xMax - m_xMin);
        double dy = delta.y() / height() * (m_yMax - m_yMin);
        
        m_xMin += dx;
        m_xMax += dx;
        m_yMin += dy;
        m_yMax += dy;
        
        m_lastMousePos = event->pos();
        calculatePoints();
        calculateDerivativePoints();
        update();
    }
}

void GraphWidget::mouseReleaseEvent(QMouseEvent *event) {
    if (event->button() == Qt::LeftButton) {
        m_isPanning = false;
    }
}

void GraphWidget::wheelEvent(QWheelEvent *event) {
    double zoomFactor = event->angleDelta().y() > 0 ? 0.9 : 1.1;
    
    QPointF mouseWorld = screenToWorld(event->position());
    
    double xRange = (m_xMax - m_xMin) * zoomFactor;
    double yRange = (m_yMax - m_yMin) * zoomFactor;
    
    m_xMin = mouseWorld.x() - (mouseWorld.x() - m_xMin) * zoomFactor;
    m_xMax = m_xMin + xRange;
    m_yMin = mouseWorld.y() - (mouseWorld.y() - m_yMin) * zoomFactor;
    m_yMax = m_yMin + yRange;
    
    calculatePoints();
    calculateDerivativePoints();
    update();
    
    event->accept();
}

void GraphWidget::resizeEvent(QResizeEvent *event) {
    Q_UNUSED(event);
    calculatePoints();
    calculateDerivativePoints();
}
