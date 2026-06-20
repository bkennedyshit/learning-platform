#include "GradientFieldWidget.h"
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QGroupBox>
#include <QLabel>
#include <cmath>
#include <algorithm>

// Canvas widget for drawing
class GradientCanvas : public QWidget
{
public:
    GradientCanvas(GradientFieldWidget* parent) : QWidget(parent), m_parent(parent) {
        setMinimumSize(400, 400);
    }

protected:
    void paintEvent(QPaintEvent* event) override {
        m_parent->QWidget::paintEvent(event);
    }
    
    void mousePressEvent(QMouseEvent* event) override {
        m_parent->mousePressEvent(event);
    }

private:
    GradientFieldWidget* m_parent;
};

GradientFieldWidget::GradientFieldWidget(QWidget *parent)
    : QWidget(parent)
{
    setupUI();
}

void GradientFieldWidget::setupUI()
{
    QVBoxLayout* mainLayout = new QVBoxLayout(this);
    
    // Canvas will be the main widget
    m_canvas = new QWidget(this);
    m_canvas->setMinimumSize(400, 400);
    mainLayout->addWidget(m_canvas, 1);
    
    // Control panel
    QGroupBox* controlBox = new QGroupBox("Gradient Field Controls");
    QVBoxLayout* controlLayout = new QVBoxLayout(controlBox);
    
    // Arrow density
    QHBoxLayout* densityLayout = new QHBoxLayout();
    densityLayout->addWidget(new QLabel("Arrow Density:"));
    m_densitySlider = new QSlider(Qt::Horizontal);
    m_densitySlider->setRange(10, 50);
    m_densitySlider->setValue(25);
    densityLayout->addWidget(m_densitySlider);
    QLabel* densityLabel = new QLabel("25");
    densityLayout->addWidget(densityLabel);
    controlLayout->addLayout(densityLayout);
    
    // Arrow size
    QHBoxLayout* sizeLayout = new QHBoxLayout();
    sizeLayout->addWidget(new QLabel("Arrow Size:"));
    m_arrowSizeSlider = new QSlider(Qt::Horizontal);
    m_arrowSizeSlider->setRange(50, 200);
    m_arrowSizeSlider->setValue(100);
    sizeLayout->addWidget(m_arrowSizeSlider);
    QLabel* sizeLabel = new QLabel("1.0x");
    sizeLayout->addWidget(sizeLabel);
    controlLayout->addLayout(sizeLayout);
    
    // Color mode
    QHBoxLayout* colorLayout = new QHBoxLayout();
    colorLayout->addWidget(new QLabel("Color Mode:"));
    m_colorModeCombo = new QComboBox();
    m_colorModeCombo->addItem("Uniform");
    m_colorModeCombo->addItem("By Magnitude");
    m_colorModeCombo->addItem("By Direction");
    m_colorModeCombo->setCurrentIndex(1);
    colorLayout->addWidget(m_colorModeCombo);
    controlLayout->addLayout(colorLayout);
    
    // Options
    m_heatmapCheck = new QCheckBox("Show Magnitude Heatmap");
    m_heatmapCheck->setChecked(false);
    controlLayout->addWidget(m_heatmapCheck);
    
    m_normalizeCheck = new QCheckBox("Normalize Arrow Lengths");
    m_normalizeCheck->setChecked(false);
    controlLayout->addWidget(m_normalizeCheck);
    
    mainLayout->addWidget(controlBox);
    
    // Connect signals
    connect(m_densitySlider, &QSlider::valueChanged, [this, densityLabel](int value) {
        densityLabel->setText(QString::number(value));
        onDensityChanged(value);
    });
    
    connect(m_arrowSizeSlider, &QSlider::valueChanged, [this, sizeLabel](int value) {
        double size = value / 100.0;
        sizeLabel->setText(QString::number(size, 'f', 1) + "x");
        onArrowSizeChanged(value);
    });
    
    connect(m_colorModeCombo, QOverload<int>::of(&QComboBox::currentIndexChanged),
            this, &GradientFieldWidget::onColorModeChanged);
    
    connect(m_heatmapCheck, &QCheckBox::toggled, [this](bool checked) {
        m_showHeatmap = checked;
        update();
    });
    
    connect(m_normalizeCheck, &QCheckBox::toggled, [this](bool checked) {
        m_normalizeArrows = checked;
        update();
    });
}

void GradientFieldWidget::setLossFunction(LossFunction func)
{
    m_function = func;
    computeGradientField();
    update();
}

void GradientFieldWidget::setBounds(double minX, double maxX, double minY, double maxY)
{
    m_minX = minX;
    m_maxX = maxX;
    m_minY = minY;
    m_maxY = maxY;
    
    if (m_function) {
        computeGradientField();
        update();
    }
}

void GradientFieldWidget::setArrowDensity(int density)
{
    m_arrowDensity = density;
    computeGradientField();
    update();
}

void GradientFieldWidget::setColorByMagnitude(bool enable)
{
    m_colorByMagnitude = enable;
    update();
}

void GradientFieldWidget::setShowHeatmap(bool show)
{
    m_showHeatmap = show;
    update();
}

void GradientFieldWidget::computeGradientField()
{
    if (!m_function) return;
    
    m_arrows.clear();
    m_maxMagnitude = 0.0;
    
    double stepX = (m_maxX - m_minX) / m_arrowDensity;
    double stepY = (m_maxY - m_minY) / m_arrowDensity;
    
    for (int i = 0; i <= m_arrowDensity; ++i) {
        for (int j = 0; j <= m_arrowDensity; ++j) {
            double x = m_minX + stepX * i;
            double y = m_minY + stepY * j;
            
            QPointF grad = computeGradient(x, y);
            double mag = std::sqrt(grad.x() * grad.x() + grad.y() * grad.y());
            
            Arrow arrow;
            arrow.position = QPointF(x, y);
            arrow.gradient = grad;
            arrow.magnitude = mag;
            
            m_arrows.append(arrow);
            m_maxMagnitude = std::max(m_maxMagnitude, mag);
        }
    }
}

QPointF GradientFieldWidget::computeGradient(double x, double y) const
{
    if (!m_function) return QPointF(0, 0);
    
    double h = 0.01;
    
    double fx1 = m_function(x + h, y);
    double fx0 = m_function(x - h, y);
    double fy1 = m_function(x, y + h);
    double fy0 = m_function(x, y - h);
    
    double dx = (fx1 - fx0) / (2 * h);
    double dy = (fy1 - fy0) / (2 * h);
    
    // Clamp extreme gradients
    if (!std::isfinite(dx)) dx = 0;
    if (!std::isfinite(dy)) dy = 0;
    dx = std::max(-100.0, std::min(100.0, dx));
    dy = std::max(-100.0, std::min(100.0, dy));
    
    return QPointF(dx, dy);
}

QColor GradientFieldWidget::magnitudeToColor(double magnitude, double maxMag) const
{
    if (maxMag < 1e-8) return Qt::blue;
    
    double t = std::min(magnitude / maxMag, 1.0);
    
    // Color gradient: Blue (low) -> Cyan -> Green -> Yellow -> Red (high)
    if (t < 0.25) {
        return QColor::fromHsvF(0.67, 1.0, 0.5 + t * 2);
    } else if (t < 0.5) {
        return QColor::fromHsvF(0.5, 1.0, 0.8);
    } else if (t < 0.75) {
        return QColor::fromHsvF(0.33, 1.0, 0.9);
    } else {
        double s = (t - 0.75) * 4;
        return QColor::fromHsvF(0.17 - s * 0.17, 1.0, 1.0);
    }
}

QPoint GradientFieldWidget::worldToScreen(double x, double y) const
{
    int canvasWidth = m_canvas->width();
    int canvasHeight = m_canvas->height();
    
    double worldWidth = m_maxX - m_minX;
    double worldHeight = m_maxY - m_minY;
    
    int screenX = ((x - m_minX) / worldWidth) * canvasWidth;
    int screenY = ((m_maxY - y) / worldHeight) * canvasHeight;
    
    return QPoint(screenX, screenY);
}

QPointF GradientFieldWidget::screenToWorld(const QPoint& screen) const
{
    int canvasWidth = m_canvas->width();
    int canvasHeight = m_canvas->height();
    
    double worldWidth = m_maxX - m_minX;
    double worldHeight = m_maxY - m_minY;
    
    double x = m_minX + (screen.x() / (double)canvasWidth) * worldWidth;
    double y = m_maxY - (screen.y() / (double)canvasHeight) * worldHeight;
    
    return QPointF(x, y);
}

void GradientFieldWidget::paintEvent(QPaintEvent* event)
{
    QPainter painter(m_canvas);
    painter.setRenderHint(QPainter::Antialiasing);
    
    // Background
    painter.fillRect(m_canvas->rect(), Qt::white);
    
    if (m_showHeatmap) {
        drawHeatmap(painter);
    }
    
    drawQuiverPlot(painter);
    drawColorLegend(painter);
    
    // Draw border
    painter.setPen(Qt::black);
    painter.drawRect(m_canvas->rect().adjusted(0, 0, -1, -1));
}

void GradientFieldWidget::drawHeatmap(QPainter& painter)
{
    int width = m_canvas->width();
    int height = m_canvas->height();
    
    QImage heatmap(width, height, QImage::Format_RGB32);
    
    for (int y = 0; y < height; ++y) {
        for (int x = 0; x < width; ++x) {
            QPointF world = screenToWorld(QPoint(x, y));
            QPointF grad = computeGradient(world.x(), world.y());
            double mag = std::sqrt(grad.x() * grad.x() + grad.y() * grad.y());
            
            QColor color = magnitudeToColor(mag, m_maxMagnitude);
            color.setAlpha(100); // Semi-transparent
            heatmap.setPixelColor(x, y, color);
        }
    }
    
    painter.setOpacity(0.3);
    painter.drawImage(0, 0, heatmap);
    painter.setOpacity(1.0);
}

void GradientFieldWidget::drawQuiverPlot(QPainter& painter)
{
    for (const auto& arrow : m_arrows) {
        QPoint start = worldToScreen(arrow.position.x(), arrow.position.y());
        
        // Determine arrow color
        QColor color;
        switch (m_colorMode) {
            case Uniform:
                color = Qt::darkBlue;
                break;
            
            case Magnitude:
                color = magnitudeToColor(arrow.magnitude, m_maxMagnitude);
                break;
            
            case Direction: {
                double angle = std::atan2(arrow.gradient.y(), arrow.gradient.x());
                double hue = (angle + M_PI) / (2 * M_PI); // Map [-π, π] to [0, 1]
                color = QColor::fromHsvF(hue, 0.8, 0.8);
                break;
            }
        }
        
        painter.setPen(QPen(color, 1.5));
        painter.setBrush(color);
        
        // Calculate arrow end point
        QPointF direction = arrow.gradient;
        double mag = arrow.magnitude;
        
        if (mag < 1e-8) continue;
        
        if (m_normalizeArrows) {
            direction /= mag; // Normalize
            mag = 1.0;
        }
        
        // Scale arrow length
        double worldWidth = m_maxX - m_minX;
        double arrowLength = (worldWidth / m_arrowDensity) * 0.4 * m_arrowSize;
        
        if (!m_normalizeArrows) {
            arrowLength *= std::min(mag / m_maxMagnitude, 1.0);
        }
        
        QPointF endWorld = arrow.position + (direction / mag) * arrowLength;
        QPoint end = worldToScreen(endWorld.x(), endWorld.y());
        
        // Draw arrow line
        painter.drawLine(start, end);
        
        // Draw arrowhead
        double angle = std::atan2(arrow.gradient.y(), arrow.gradient.x());
        double headSize = 6;
        
        QPointF p1(
            end.x() - headSize * std::cos(angle - 0.4),
            end.y() - headSize * std::sin(angle - 0.4)
        );
        QPointF p2(
            end.x() - headSize * std::cos(angle + 0.4),
            end.y() - headSize * std::sin(angle + 0.4)
        );
        
        QPainterPath arrowHead;
        arrowHead.moveTo(end);
        arrowHead.lineTo(p1);
        arrowHead.lineTo(p2);
        arrowHead.closeSubpath();
        
        painter.drawPath(arrowHead);
    }
}

void GradientFieldWidget::drawColorLegend(QPainter& painter)
{
    if (m_colorMode == Uniform) return;
    
    int legendWidth = 20;
    int legendHeight = 200;
    int legendX = m_canvas->width() - legendWidth - 20;
    int legendY = 20;
    
    // Draw gradient bar
    for (int i = 0; i < legendHeight; ++i) {
        double t = 1.0 - (i / (double)legendHeight);
        
        QColor color;
        if (m_colorMode == Magnitude) {
            color = magnitudeToColor(t * m_maxMagnitude, m_maxMagnitude);
        } else { // Direction
            color = QColor::fromHsvF(t, 0.8, 0.8);
        }
        
        painter.fillRect(legendX, legendY + i, legendWidth, 1, color);
    }
    
    // Draw border
    painter.setPen(Qt::black);
    painter.drawRect(legendX, legendY, legendWidth, legendHeight);
    
    // Draw labels
    painter.setFont(QFont("Arial", 8));
    
    if (m_colorMode == Magnitude) {
        QString maxLabel = QString::number(m_maxMagnitude, 'f', 2);
        painter.drawText(legendX + legendWidth + 5, legendY + 10, maxLabel);
        painter.drawText(legendX + legendWidth + 5, legendY + legendHeight, "0.0");
    } else {
        painter.drawText(legendX + legendWidth + 5, legendY + 10, "0°");
        painter.drawText(legendX + legendWidth + 5, legendY + legendHeight, "360°");
    }
}

void GradientFieldWidget::mousePressEvent(QMouseEvent* event)
{
    if (!m_canvas->rect().contains(event->pos())) return;
    
    QPointF world = screenToWorld(event->pos());
    QPointF grad = computeGradient(world.x(), world.y());
    
    emit gradientClicked(world.x(), world.y(), grad.x(), grad.y());
}

void GradientFieldWidget::resizeEvent(QResizeEvent* event)
{
    QWidget::resizeEvent(event);
    update();
}

void GradientFieldWidget::onDensityChanged(int value)
{
    m_arrowDensity = value;
    computeGradientField();
    update();
}

void GradientFieldWidget::onArrowSizeChanged(int value)
{
    m_arrowSize = value / 100.0;
    update();
}

void GradientFieldWidget::onColorModeChanged(int index)
{
    m_colorMode = static_cast<ColorMode>(index);
    update();
}
