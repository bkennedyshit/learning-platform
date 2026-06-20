#include "VectorVisualizer.h"
#include <QPainter>
#include <QMouseEvent>
#include <QWheelEvent>
#include <QPainterPath>
#include <QFileDialog>
#include <QMessageBox>
#include <QGroupBox>
#include <cmath>

VectorVisualizer::VectorVisualizer(QWidget *parent)
    : QWidget(parent),
      transformMatrix(2, 2),
      hasTransformation(false),
      zoom(50.0),  // 50 pixels per unit
      panOffset(0, 0),
      isPanning(false),
      isDragging(false),
      showGrid(true),
      showBasisVectors(true),
      showTransformed(true),
      showOriginal(true),
      showLabels(true),
      animationProgress(0.0),
      isAnimating(false),
      animationSpeed(1000)
{
    // Initialize basis vectors
    basisI = QPointF(1, 0);
    basisJ = QPointF(0, 1);
    transformedBasisI = basisI;
    transformedBasisJ = basisJ;
    
    // Initialize identity transformation
    transformMatrix.setValue(0, 0, 1.0);
    transformMatrix.setValue(0, 1, 0.0);
    transformMatrix.setValue(1, 0, 0.0);
    transformMatrix.setValue(1, 1, 1.0);
    
    // Setup animation timer
    animationTimer = new QTimer(this);
    connect(animationTimer, &QTimer::timeout, this, &VectorVisualizer::onAnimationTick);
    
    setupUI();
    applyTheme();
    
    setMinimumSize(600, 600);
    setMouseTracking(true);
}

void VectorVisualizer::setupUI()
{
    QVBoxLayout *mainLayout = new QVBoxLayout(this);
    
    // Control panel
    QGroupBox *controlGroup = new QGroupBox("Vector Visualization Controls");
    QHBoxLayout *controlLayout = new QHBoxLayout(controlGroup);
    
    // Animation controls
    playPauseButton = new QPushButton("▶ Play Animation");
    connect(playPauseButton, &QPushButton::clicked, this, &VectorVisualizer::onPlayPauseClicked);
    controlLayout->addWidget(playPauseButton);
    
    QLabel *speedLabel = new QLabel("Speed:");
    controlLayout->addWidget(speedLabel);
    
    animationSpeedSlider = new QSlider(Qt::Horizontal);
    animationSpeedSlider->setRange(100, 3000);
    animationSpeedSlider->setValue(1000);
    animationSpeedSlider->setMaximumWidth(150);
    connect(animationSpeedSlider, &QSlider::valueChanged, this, &VectorVisualizer::onAnimationSpeedChanged);
    controlLayout->addWidget(animationSpeedSlider);
    
    // View controls
    resetViewButton = new QPushButton("Reset View");
    connect(resetViewButton, &QPushButton::clicked, this, &VectorVisualizer::onResetViewClicked);
    controlLayout->addWidget(resetViewButton);
    
    exportButton = new QPushButton("Export PNG");
    connect(exportButton, &QPushButton::clicked, this, &VectorVisualizer::onExportClicked);
    controlLayout->addWidget(exportButton);
    
    controlLayout->addStretch();
    
    // Display options
    QGroupBox *displayGroup = new QGroupBox("Display Options");
    QHBoxLayout *displayLayout = new QHBoxLayout(displayGroup);
    
    showGridCheckbox = new QCheckBox("Show Grid");
    showGridCheckbox->setChecked(true);
    connect(showGridCheckbox, &QCheckBox::toggled, this, &VectorVisualizer::setShowGrid);
    displayLayout->addWidget(showGridCheckbox);
    
    showBasisCheckbox = new QCheckBox("Show Basis Vectors");
    showBasisCheckbox->setChecked(true);
    connect(showBasisCheckbox, &QCheckBox::toggled, this, &VectorVisualizer::setShowBasisVectors);
    displayLayout->addWidget(showBasisCheckbox);
    
    showOriginalCheckbox = new QCheckBox("Show Original");
    showOriginalCheckbox->setChecked(true);
    connect(showOriginalCheckbox, &QCheckBox::toggled, this, &VectorVisualizer::setShowOriginal);
    displayLayout->addWidget(showOriginalCheckbox);
    
    showTransformedCheckbox = new QCheckBox("Show Transformed");
    showTransformedCheckbox->setChecked(true);
    connect(showTransformedCheckbox, &QCheckBox::toggled, this, &VectorVisualizer::setShowTransformed);
    displayLayout->addWidget(showTransformedCheckbox);
    
    displayLayout->addStretch();
    
    // Info label
    infoLabel = new QLabel("Use mouse wheel to zoom, drag to pan. Add vectors via code.");
    
    mainLayout->addWidget(controlGroup);
    mainLayout->addWidget(displayGroup);
    mainLayout->addWidget(infoLabel);
    mainLayout->addStretch();
}

void VectorVisualizer::applyTheme()
{
    backgroundColor = QColor(250, 250, 250);
    gridColor = QColor(220, 220, 220);
    axisColor = QColor(100, 100, 100);
    originalVectorColor = QColor(70, 130, 220);     // Blue
    transformedVectorColor = QColor(220, 70, 100);   // Red
    basisIColor = QColor(0, 180, 0);                 // Green
    basisJColor = QColor(180, 100, 0);               // Orange
}

void VectorVisualizer::addVector(double x, double y, const QColor &color)
{
    VectorData vec;
    vec.original = QPointF(x, y);
    vec.transformed = hasTransformation ? transformVector(vec.original, transformMatrix) : vec.original;
    vec.color = color;
    vec.label = QString("v%1").arg(vectors.size());
    vectors.append(vec);
    update();
}

void VectorVisualizer::clearVectors()
{
    vectors.clear();
    update();
}

void VectorVisualizer::setVectors(const QVector<QPointF> &vecs)
{
    clearVectors();
    for (const QPointF &v : vecs) {
        addVector(v.x(), v.y());
    }
}

void VectorVisualizer::setTransformationMatrix(const Matrix &matrix)
{
    if (matrix.getRows() != 2 || matrix.getCols() != 2) {
        qWarning("Transformation matrix must be 2x2");
        return;
    }
    
    transformMatrix = matrix;
    hasTransformation = true;
    
    // Update transformed basis vectors
    transformedBasisI = transformVector(basisI, transformMatrix);
    transformedBasisJ = transformVector(basisJ, transformMatrix);
    
    // Update all vector transformations
    for (VectorData &vec : vectors) {
        vec.transformed = transformVector(vec.original, transformMatrix);
    }
    
    update();
}

void VectorVisualizer::applyTransformation()
{
    if (!hasTransformation) return;
    
    for (VectorData &vec : vectors) {
        vec.original = vec.transformed;
    }
    
    basisI = transformedBasisI;
    basisJ = transformedBasisJ;
    
    hasTransformation = false;
    transformMatrix = getIdentityMatrix2D();
    update();
}

void VectorVisualizer::resetTransformation()
{
    transformMatrix = getIdentityMatrix2D();
    hasTransformation = false;
    transformedBasisI = basisI;
    transformedBasisJ = basisJ;
    
    for (VectorData &vec : vectors) {
        vec.transformed = vec.original;
    }
    
    animationProgress = 0.0;
    isAnimating = false;
    animationTimer->stop();
    playPauseButton->setText("▶ Play Animation");
    
    update();
}

void VectorVisualizer::animateTransformation(int durationMs)
{
    if (!hasTransformation) return;
    
    animationSpeed = durationMs;
    animationProgress = 0.0;
    isAnimating = true;
    animationTimer->start(16);  // ~60 FPS
    playPauseButton->setText("⏸ Pause");
}

void VectorVisualizer::onAnimationTick()
{
    if (!isAnimating) return;
    
    animationProgress += 16.0 / animationSpeed;  // Increment based on frame time
    
    if (animationProgress >= 1.0) {
        animationProgress = 1.0;
        isAnimating = false;
        animationTimer->stop();
        playPauseButton->setText("▶ Replay");
    }
    
    update();
}

void VectorVisualizer::onPlayPauseClicked()
{
    if (!hasTransformation) {
        QMessageBox::information(this, "No Transformation", 
            "Please set a transformation matrix first.");
        return;
    }
    
    if (isAnimating) {
        // Pause
        isAnimating = false;
        animationTimer->stop();
        playPauseButton->setText("▶ Continue");
    } else {
        // Play or replay
        if (animationProgress >= 1.0) {
            animationProgress = 0.0;
        }
        isAnimating = true;
        animationTimer->start(16);
        playPauseButton->setText("⏸ Pause");
    }
}

void VectorVisualizer::onResetViewClicked()
{
    resetView();
}

void VectorVisualizer::onExportClicked()
{
    QString fileName = QFileDialog::getSaveFileName(this, "Export to PNG", 
        "vector_visualization.png", "PNG Images (*.png)");
    
    if (!fileName.isEmpty()) {
        if (exportToPNG(fileName)) {
            QMessageBox::information(this, "Export Successful", 
                "Visualization exported to " + fileName);
        } else {
            QMessageBox::warning(this, "Export Failed", 
                "Failed to export visualization.");
        }
    }
}

void VectorVisualizer::onAnimationSpeedChanged(int value)
{
    animationSpeed = value;
}

void VectorVisualizer::paintEvent(QPaintEvent *event)
{
    Q_UNUSED(event);
    
    QPainter painter(this);
    painter.setRenderHint(QPainter::Antialiasing);
    
    // Background
    painter.fillRect(rect(), backgroundColor);
    
    // Draw grid
    if (showGrid) {
        drawGrid(painter);
    }
    
    // Draw axes
    drawAxes(painter);
    
    // Calculate interpolation factor for animation
    double t = animationProgress;
    
    // Ease in-out function for smooth animation
    if (t < 0.5) {
        t = 2 * t * t;
    } else {
        t = -1 + (4 - 2 * t) * t;
    }
    
    // Draw basis vectors
    if (showBasisVectors) {
        if (showOriginal && animationProgress < 1.0) {
            drawVector(painter, basisI, basisIColor.lighter(150), 1.5, true);
            drawVector(painter, basisJ, basisJColor.lighter(150), 1.5, true);
            drawVectorLabel(painter, basisI, "î");
            drawVectorLabel(painter, basisJ, "ĵ");
        }
        
        if (showTransformed && hasTransformation) {
            // Interpolate basis vectors for animation
            QPointF animBasisI = basisI + (transformedBasisI - basisI) * t;
            QPointF animBasisJ = basisJ + (transformedBasisJ - basisJ) * t;
            
            drawVector(painter, animBasisI, basisIColor, 2.5);
            drawVector(painter, animBasisJ, basisJColor, 2.5);
            drawVectorLabel(painter, animBasisI, "î'");
            drawVectorLabel(painter, animBasisJ, "ĵ'");
        }
    }
    
    // Draw vectors
    for (const VectorData &vec : vectors) {
        if (showOriginal && animationProgress < 1.0) {
            drawVector(painter, vec.original, vec.color.lighter(130), 2.0, true);
        }
        
        if (showTransformed && hasTransformation) {
            // Interpolate for animation
            QPointF animVec = vec.original + (vec.transformed - vec.original) * t;
            drawVector(painter, animVec, vec.color, 3.0);
            if (showLabels) {
                drawVectorLabel(painter, animVec, vec.label);
            }
        } else if (!hasTransformation) {
            drawVector(painter, vec.original, vec.color, 3.0);
            if (showLabels) {
                drawVectorLabel(painter, vec.original, vec.label);
            }
        }
    }
    
    // Draw info overlay
    painter.setPen(Qt::black);
    QFont font = painter.font();
    font.setPointSize(9);
    painter.setFont(font);
    
    QString info = QString("Zoom: %1x | Vectors: %2")
        .arg(zoom / 50.0, 0, 'f', 2)
        .arg(vectors.size());
    
    if (hasTransformation) {
        info += QString(" | Animation: %1%").arg(int(animationProgress * 100));
    }
    
    painter.drawText(10, height() - 10, info);
}

void VectorVisualizer::drawGrid(QPainter &painter)
{
    painter.setPen(QPen(gridColor, 1));
    
    QPointF center(width() / 2.0 + panOffset.x(), height() / 2.0 + panOffset.y());
    
    // Vertical lines
    double gridSpacing = zoom;
    for (double x = fmod(center.x(), gridSpacing); x < width(); x += gridSpacing) {
        painter.drawLine(QPointF(x, 0), QPointF(x, height()));
    }
    
    // Horizontal lines
    for (double y = fmod(center.y(), gridSpacing); y < height(); y += gridSpacing) {
        painter.drawLine(QPointF(0, y), QPointF(width(), y));
    }
}

void VectorVisualizer::drawAxes(QPainter &painter)
{
    painter.setPen(QPen(axisColor, 2));
    
    QPointF center(width() / 2.0 + panOffset.x(), height() / 2.0 + panOffset.y());
    
    // X-axis
    painter.drawLine(QPointF(0, center.y()), QPointF(width(), center.y()));
    // Y-axis
    painter.drawLine(QPointF(center.x(), 0), QPointF(center.x(), height()));
    
    // Draw axis labels
    painter.setPen(Qt::black);
    QFont font = painter.font();
    font.setPointSize(10);
    font.setBold(true);
    painter.setFont(font);
    
    painter.drawText(width() - 20, center.y() - 5, "x");
    painter.drawText(center.x() + 5, 15, "y");
    
    // Draw tick marks and numbers
    font.setPointSize(8);
    font.setBold(false);
    painter.setFont(font);
    
    double tickSpacing = zoom;
    int tickSize = 5;
    
    // X-axis ticks
    for (double x = center.x(); x < width(); x += tickSpacing) {
        double worldX = (x - center.x()) / zoom;
        if (std::abs(worldX) > 0.01) {
            painter.drawLine(QPointF(x, center.y() - tickSize), QPointF(x, center.y() + tickSize));
            painter.drawText(x - 10, center.y() + 20, QString::number(worldX, 'f', 0));
        }
    }
    for (double x = center.x() - tickSpacing; x > 0; x -= tickSpacing) {
        double worldX = (x - center.x()) / zoom;
        if (std::abs(worldX) > 0.01) {
            painter.drawLine(QPointF(x, center.y() - tickSize), QPointF(x, center.y() + tickSize));
            painter.drawText(x - 10, center.y() + 20, QString::number(worldX, 'f', 0));
        }
    }
    
    // Y-axis ticks (note: screen Y is inverted)
    for (double y = center.y(); y < height(); y += tickSpacing) {
        double worldY = -(y - center.y()) / zoom;
        if (std::abs(worldY) > 0.01) {
            painter.drawLine(QPointF(center.x() - tickSize, y), QPointF(center.x() + tickSize, y));
            painter.drawText(center.x() + 10, y + 5, QString::number(worldY, 'f', 0));
        }
    }
    for (double y = center.y() - tickSpacing; y > 0; y -= tickSpacing) {
        double worldY = -(y - center.y()) / zoom;
        if (std::abs(worldY) > 0.01) {
            painter.drawLine(QPointF(center.x() - tickSize, y), QPointF(center.x() + tickSize, y));
            painter.drawText(center.x() + 10, y + 5, QString::number(worldY, 'f', 0));
        }
    }
}

void VectorVisualizer::drawVector(QPainter &painter, const QPointF &vec, const QColor &color, 
                                  double width, bool dashed)
{
    QPointF origin = worldToScreen(QPointF(0, 0));
    QPointF end = worldToScreen(vec);
    
    QPen pen(color, width);
    if (dashed) {
        pen.setStyle(Qt::DashLine);
    }
    painter.setPen(pen);
    
    // Draw vector line
    painter.drawLine(origin, end);
    
    // Draw arrowhead
    double arrowSize = 10.0;
    double angle = std::atan2(end.y() - origin.y(), end.x() - origin.x());
    
    QPointF arrowP1 = end - QPointF(arrowSize * std::cos(angle - M_PI / 6),
                                     arrowSize * std::sin(angle - M_PI / 6));
    QPointF arrowP2 = end - QPointF(arrowSize * std::cos(angle + M_PI / 6),
                                     arrowSize * std::sin(angle + M_PI / 6));
    
    painter.setBrush(color);
    QPainterPath arrowHead;
    arrowHead.moveTo(end);
    arrowHead.lineTo(arrowP1);
    arrowHead.lineTo(arrowP2);
    arrowHead.closeSubpath();
    painter.drawPath(arrowHead);
}

void VectorVisualizer::drawBasisVectors(QPainter &painter)
{
    drawVector(painter, basisI, basisIColor, 2.5);
    drawVector(painter, basisJ, basisJColor, 2.5);
}

void VectorVisualizer::drawVectorLabel(QPainter &painter, const QPointF &vec, const QString &label)
{
    QPointF screenPos = worldToScreen(vec);
    
    painter.setPen(Qt::black);
    QFont font = painter.font();
    font.setPointSize(10);
    font.setBold(true);
    painter.setFont(font);
    
    // Offset label from vector end
    screenPos += QPointF(10, -10);
    painter.drawText(screenPos, label);
}

QPointF VectorVisualizer::worldToScreen(const QPointF &worldPos) const
{
    QPointF center(width() / 2.0 + panOffset.x(), height() / 2.0 + panOffset.y());
    return QPointF(center.x() + worldPos.x() * zoom,
                   center.y() - worldPos.y() * zoom);  // Invert Y for screen coords
}

QPointF VectorVisualizer::screenToWorld(const QPointF &screenPos) const
{
    QPointF center(width() / 2.0 + panOffset.x(), height() / 2.0 + panOffset.y());
    return QPointF((screenPos.x() - center.x()) / zoom,
                   -(screenPos.y() - center.y()) / zoom);  // Invert Y
}

void VectorVisualizer::mousePressEvent(QMouseEvent *event)
{
    if (event->button() == Qt::LeftButton) {
        lastMousePos = event->pos();
        isPanning = true;
    }
}

void VectorVisualizer::mouseMoveEvent(QMouseEvent *event)
{
    if (isPanning) {
        QPointF delta = event->pos() - lastMousePos;
        panOffset += delta;
        lastMousePos = event->pos();
        update();
    }
}

void VectorVisualizer::mouseReleaseEvent(QMouseEvent *event)
{
    if (event->button() == Qt::LeftButton) {
        isPanning = false;
    }
}

void VectorVisualizer::wheelEvent(QWheelEvent *event)
{
    double zoomFactor = 1.1;
    
    if (event->angleDelta().y() > 0) {
        zoom *= zoomFactor;
    } else {
        zoom /= zoomFactor;
    }
    
    zoom = qBound(10.0, zoom, 200.0);  // Limit zoom range
    update();
}

void VectorVisualizer::resizeEvent(QResizeEvent *event)
{
    Q_UNUSED(event);
    update();
}

void VectorVisualizer::resetView()
{
    zoom = 50.0;
    panOffset = QPointF(0, 0);
    update();
}

void VectorVisualizer::setZoom(double z)
{
    zoom = qBound(10.0, z, 200.0);
    update();
}

void VectorVisualizer::centerView()
{
    panOffset = QPointF(0, 0);
    update();
}

bool VectorVisualizer::exportToPNG(const QString &filePath, int width, int height)
{
    QImage image(width, height, QImage::Format_ARGB32);
    image.fill(backgroundColor);
    
    QPainter painter(&image);
    painter.setRenderHint(QPainter::Antialiasing);
    
    // Save current size
    int oldWidth = this->width();
    int oldHeight = this->height();
    
    // Temporarily resize for export (this affects world-to-screen calculations)
    resize(width, height);
    
    // Render
    if (showGrid) drawGrid(painter);
    drawAxes(painter);
    
    if (showBasisVectors) {
        drawBasisVectors(painter);
    }
    
    for (const VectorData &vec : vectors) {
        if (showOriginal) {
            drawVector(painter, vec.original, vec.color.lighter(130), 2.0, true);
        }
        if (showTransformed && hasTransformation) {
            drawVector(painter, vec.transformed, vec.color, 3.0);
        }
    }
    
    // Restore size
    resize(oldWidth, oldHeight);
    
    return image.save(filePath);
}

void VectorVisualizer::setShowGrid(bool show)
{
    showGrid = show;
    update();
}

void VectorVisualizer::setShowBasisVectors(bool show)
{
    showBasisVectors = show;
    update();
}

void VectorVisualizer::setShowTransformed(bool show)
{
    showTransformed = show;
    update();
}

void VectorVisualizer::setShowOriginal(bool show)
{
    showOriginal = show;
    update();
}

Matrix VectorVisualizer::getIdentityMatrix2D() const
{
    Matrix identity(2, 2);
    identity.setValue(0, 0, 1.0);
    identity.setValue(0, 1, 0.0);
    identity.setValue(1, 0, 0.0);
    identity.setValue(1, 1, 1.0);
    return identity;
}

QPointF VectorVisualizer::transformVector(const QPointF &vec, const Matrix &matrix) const
{
    double x = matrix.getValue(0, 0) * vec.x() + matrix.getValue(0, 1) * vec.y();
    double y = matrix.getValue(1, 0) * vec.x() + matrix.getValue(1, 1) * vec.y();
    return QPointF(x, y);
}
