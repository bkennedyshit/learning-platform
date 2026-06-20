#include "EigenVisualizer.h"
#include <QPainter>
#include <QMouseEvent>
#include <QWheelEvent>
#include <QPainterPath>
#include <QFileDialog>
#include <QMessageBox>
#include <QGroupBox>
#include <cmath>
#include <complex>

EigenVisualizer::EigenVisualizer(QWidget *parent)
    : QWidget(parent),
      transformMatrix(2, 2),
      hasMatrix(false),
      hasEigenData(false),
      zoom(50.0),
      panOffset(0, 0),
      isPanning(false),
      showGrid(true),
      showEigenspaces(true),
      showComparisonVectors(false),
      showScalingFactors(true),
      showTransformation(false),
      visualizationMode(0)
{
    // Initialize identity matrix
    transformMatrix.setValue(0, 0, 1.0);
    transformMatrix.setValue(0, 1, 0.0);
    transformMatrix.setValue(1, 0, 0.0);
    transformMatrix.setValue(1, 1, 1.0);
    
    setupUI();
    applyTheme();
    
    setMinimumSize(600, 600);
    setMouseTracking(true);
}

void EigenVisualizer::setupUI()
{
    QVBoxLayout *mainLayout = new QVBoxLayout(this);
    
    // Control panel
    QGroupBox *controlGroup = new QGroupBox("Eigenvalue Visualization Controls");
    QHBoxLayout *controlLayout = new QHBoxLayout(controlGroup);
    
    calculateEigenButton = new QPushButton("Calculate Eigenvalues");
    connect(calculateEigenButton, &QPushButton::clicked, this, &EigenVisualizer::onCalculateEigenClicked);
    controlLayout->addWidget(calculateEigenButton);
    
    QLabel *modeLabel = new QLabel("Mode:");
    controlLayout->addWidget(modeLabel);
    
    visualizationModeCombo = new QComboBox();
    visualizationModeCombo->addItem("Eigenvectors Only");
    visualizationModeCombo->addItem("With Transformation");
    visualizationModeCombo->addItem("Comparison View");
    connect(visualizationModeCombo, QOverload<int>::of(&QComboBox::currentIndexChanged),
            this, &EigenVisualizer::onVisualizationModeChanged);
    controlLayout->addWidget(visualizationModeCombo);
    
    resetViewButton = new QPushButton("Reset View");
    connect(resetViewButton, &QPushButton::clicked, this, &EigenVisualizer::onResetViewClicked);
    controlLayout->addWidget(resetViewButton);
    
    exportButton = new QPushButton("Export PNG");
    connect(exportButton, &QPushButton::clicked, this, &EigenVisualizer::onExportClicked);
    controlLayout->addWidget(exportButton);
    
    controlLayout->addStretch();
    
    // Display options
    QGroupBox *displayGroup = new QGroupBox("Display Options");
    QHBoxLayout *displayLayout = new QHBoxLayout(displayGroup);
    
    showGridCheckbox = new QCheckBox("Show Grid");
    showGridCheckbox->setChecked(true);
    connect(showGridCheckbox, &QCheckBox::toggled, this, &EigenVisualizer::setShowGrid);
    displayLayout->addWidget(showGridCheckbox);
    
    showEigenspacesCheckbox = new QCheckBox("Show Eigenspaces");
    showEigenspacesCheckbox->setChecked(true);
    connect(showEigenspacesCheckbox, &QCheckBox::toggled, this, &EigenVisualizer::setShowEigenspaces);
    displayLayout->addWidget(showEigenspacesCheckbox);
    
    showComparisonCheckbox = new QCheckBox("Show Comparison Vectors");
    showComparisonCheckbox->setChecked(false);
    connect(showComparisonCheckbox, &QCheckBox::toggled, this, &EigenVisualizer::setShowComparisonVectors);
    displayLayout->addWidget(showComparisonCheckbox);
    
    showScalingCheckbox = new QCheckBox("Show Scaling Factors");
    showScalingCheckbox->setChecked(true);
    connect(showScalingCheckbox, &QCheckBox::toggled, this, &EigenVisualizer::setShowScalingFactors);
    displayLayout->addWidget(showScalingCheckbox);
    
    displayLayout->addStretch();
    
    // Info labels
    infoLabel = new QLabel("Use mouse wheel to zoom, drag to pan. Set a matrix to calculate eigenvalues.");
    eigenInfoLabel = new QLabel("No eigenvalue data computed yet.");
    
    mainLayout->addWidget(controlGroup);
    mainLayout->addWidget(displayGroup);
    mainLayout->addWidget(eigenInfoLabel);
    mainLayout->addWidget(infoLabel);
    mainLayout->addStretch();
}

void EigenVisualizer::applyTheme()
{
    backgroundColor = QColor(250, 250, 250);
    gridColor = QColor(220, 220, 220);
    axisColor = QColor(100, 100, 100);
    eigenspaceColor = QColor(200, 200, 255, 100);
    comparisonColor = QColor(150, 150, 150);
}

void EigenVisualizer::setMatrix(const Matrix &matrix)
{
    if (matrix.getRows() != 2 || matrix.getCols() != 2) {
        QMessageBox::warning(this, "Invalid Matrix", 
            "Eigenvalue visualization currently supports only 2x2 matrices.");
        return;
    }
    
    transformMatrix = matrix;
    hasMatrix = true;
    
    // Auto-calculate eigenvalues
    calculateEigenvalues();
    update();
}

void EigenVisualizer::clearMatrix()
{
    hasMatrix = false;
    hasEigenData = false;
    eigenData.clear();
    comparisonVectors.clear();
    eigenInfoLabel->setText("No eigenvalue data computed yet.");
    update();
}

void EigenVisualizer::setEigenData(const QVector<std::complex<double>> &eigenvalues,
                                   const QVector<QPointF> &eigenvectors)
{
    eigenData.clear();
    
    for (int i = 0; i < eigenvalues.size() && i < eigenvectors.size(); ++i) {
        EigenData data;
        data.eigenvalue = eigenvalues[i];
        data.eigenvector = eigenvectors[i];
        data.isReal = (std::abs(eigenvalues[i].imag()) < 1e-10);
        data.color = getColorForEigenvalue(eigenvalues[i]);
        eigenData.append(data);
    }
    
    hasEigenData = true;
    update();
}

void EigenVisualizer::addComparisonVector(double x, double y)
{
    ComparisonVector vec;
    vec.original = QPointF(x, y);
    vec.transformed = hasMatrix ? transformVector(vec.original) : vec.original;
    vec.color = comparisonColor;
    comparisonVectors.append(vec);
    update();
}

void EigenVisualizer::clearComparisonVectors()
{
    comparisonVectors.clear();
    update();
}

void EigenVisualizer::calculateEigenvalues()
{
    if (!hasMatrix) {
        QMessageBox::information(this, "No Matrix", 
            "Please set a matrix before calculating eigenvalues.");
        return;
    }
    
    calculateEigen2x2();
}

void EigenVisualizer::calculateEigen2x2()
{
    // For a 2x2 matrix [[a, b], [c, d]], eigenvalues solve:
    // det(A - λI) = 0
    // (a-λ)(d-λ) - bc = 0
    // λ² - (a+d)λ + (ad-bc) = 0
    // Using quadratic formula
    
    double a = transformMatrix.getValue(0, 0);
    double b = transformMatrix.getValue(0, 1);
    double c = transformMatrix.getValue(1, 0);
    double d = transformMatrix.getValue(1, 1);
    
    double trace = a + d;
    double det = a * d - b * c;
    
    // Quadratic formula: λ = (trace ± √(trace² - 4*det)) / 2
    double discriminant = trace * trace - 4 * det;
    
    eigenData.clear();
    
    if (discriminant >= 0) {
        // Real eigenvalues
        double sqrtDisc = std::sqrt(discriminant);
        double lambda1 = (trace + sqrtDisc) / 2.0;
        double lambda2 = (trace - sqrtDisc) / 2.0;
        
        // Calculate eigenvectors
        // For eigenvalue λ, solve (A - λI)v = 0
        
        // Eigenvector 1
        QPointF v1;
        if (std::abs(b) > 1e-10) {
            v1 = QPointF(b, lambda1 - a);
        } else if (std::abs(c) > 1e-10) {
            v1 = QPointF(lambda1 - d, c);
        } else {
            v1 = QPointF(1, 0);  // Diagonal matrix
        }
        
        // Normalize
        double len1 = std::sqrt(v1.x() * v1.x() + v1.y() * v1.y());
        if (len1 > 1e-10) {
            v1 = QPointF(v1.x() / len1 * 2, v1.y() / len1 * 2);  // Scale to length 2 for visibility
        }
        
        EigenData data1;
        data1.eigenvalue = std::complex<double>(lambda1, 0);
        data1.eigenvector = v1;
        data1.isReal = true;
        data1.color = getColorForEigenvalue(data1.eigenvalue);
        eigenData.append(data1);
        
        // Eigenvector 2 (if different eigenvalue)
        if (std::abs(lambda1 - lambda2) > 1e-10) {
            QPointF v2;
            if (std::abs(b) > 1e-10) {
                v2 = QPointF(b, lambda2 - a);
            } else if (std::abs(c) > 1e-10) {
                v2 = QPointF(lambda2 - d, c);
            } else {
                v2 = QPointF(0, 1);  // Diagonal matrix
            }
            
            // Normalize
            double len2 = std::sqrt(v2.x() * v2.x() + v2.y() * v2.y());
            if (len2 > 1e-10) {
                v2 = QPointF(v2.x() / len2 * 2, v2.y() / len2 * 2);
            }
            
            EigenData data2;
            data2.eigenvalue = std::complex<double>(lambda2, 0);
            data2.eigenvector = v2;
            data2.isReal = true;
            data2.color = getColorForEigenvalue(data2.eigenvalue);
            eigenData.append(data2);
        }
        
        hasEigenData = true;
        
        QString info = QString("Eigenvalues: λ₁ = %1, λ₂ = %2 (both real)")
            .arg(lambda1, 0, 'f', 3)
            .arg(lambda2, 0, 'f', 3);
        eigenInfoLabel->setText(info);
        
        emit eigenDataCalculated(2);
    } else {
        // Complex eigenvalues
        double realPart = trace / 2.0;
        double imagPart = std::sqrt(-discriminant) / 2.0;
        
        std::complex<double> lambda1(realPart, imagPart);
        std::complex<double> lambda2(realPart, -imagPart);
        
        QString info = QString("Eigenvalues: λ = %1 ± %2i (complex conjugates)\n"
                              "No real eigenvectors in 2D - rotation component present!")
            .arg(realPart, 0, 'f', 3)
            .arg(imagPart, 0, 'f', 3);
        eigenInfoLabel->setText(info);
        
        hasEigenData = false;  // Can't visualize complex eigenvectors in 2D easily
        
        emit eigenDataCalculated(0);
    }
    
    // Update comparison vectors if they exist
    for (ComparisonVector &vec : comparisonVectors) {
        vec.transformed = transformVector(vec.original);
    }
    
    update();
}

QColor EigenVisualizer::getColorForEigenvalue(const std::complex<double> &eigenvalue) const
{
    double magnitude = getEigenvalueMagnitude(eigenvalue);
    
    if (magnitude > 1.0) {
        // Expanding: red spectrum
        double t = qBound(0.0, (magnitude - 1.0) / 2.0, 1.0);
        return QColor(int(255), int(100 * (1 - t)), int(100 * (1 - t)));
    } else if (magnitude < 1.0 && magnitude > 1e-6) {
        // Contracting: blue spectrum
        double t = qBound(0.0, 1.0 - magnitude, 1.0);
        return QColor(int(100 * (1 - t)), int(100 * (1 - t)), int(255));
    } else {
        // Near zero: dark gray
        return QColor(50, 50, 50);
    }
}

double EigenVisualizer::getEigenvalueMagnitude(const std::complex<double> &eigenvalue) const
{
    return std::abs(eigenvalue);
}

void EigenVisualizer::onResetViewClicked()
{
    resetView();
}

void EigenVisualizer::onExportClicked()
{
    QString fileName = QFileDialog::getSaveFileName(this, "Export to PNG", 
        "eigen_visualization.png", "PNG Images (*.png)");
    
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

void EigenVisualizer::onCalculateEigenClicked()
{
    calculateEigenvalues();
}

void EigenVisualizer::onVisualizationModeChanged(int index)
{
    visualizationMode = index;
    
    if (index == 2) {  // Comparison mode
        // Add some default comparison vectors if none exist
        if (comparisonVectors.isEmpty()) {
            addComparisonVector(1.5, 0.5);
            addComparisonVector(0.5, 1.5);
            addComparisonVector(-1.0, 1.0);
        }
        showComparisonVectors = true;
        showComparisonCheckbox->setChecked(true);
    }
    
    showTransformation = (index == 1 || index == 2);
    update();
}

void EigenVisualizer::paintEvent(QPaintEvent *event)
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
    
    // Draw eigenspaces (lines through eigenvectors)
    if (showEigenspaces && hasEigenData) {
        for (const EigenData &data : eigenData) {
            if (data.isReal) {
                drawEigenspace(painter, data.eigenvector, data.color.lighter(160), 
                             data.eigenvalue.real());
            }
        }
    }
    
    // Draw comparison vectors (non-eigenvectors)
    if (showComparisonVectors && !comparisonVectors.isEmpty()) {
        for (const ComparisonVector &vec : comparisonVectors) {
            drawVector(painter, vec.original, comparisonColor.lighter(140), 2.0, true);
            if (showTransformation) {
                drawVector(painter, vec.transformed, comparisonColor, 3.0);
                drawVectorLabel(painter, vec.transformed, "v'", comparisonColor.darker(120));
            }
        }
    }
    
    // Draw eigenvectors
    if (hasEigenData) {
        for (int i = 0; i < eigenData.size(); ++i) {
            const EigenData &data = eigenData[i];
            if (data.isReal) {
                drawEigenvector(painter, data.eigenvector, data.eigenvalue, data.color);
                
                QString label = QString("v%1").arg(i + 1);
                drawVectorLabel(painter, data.eigenvector, label, data.color.darker(120));
                
                // Draw transformed eigenvector if in transformation mode
                if (showTransformation) {
                    QPointF transformed = transformVector(data.eigenvector);
                    drawVector(painter, transformed, data.color.darker(140), 3.0);
                    drawVectorLabel(painter, transformed, label + "'", data.color.darker(140));
                }
            }
        }
    }
    
    // Draw eigenvalue information overlay
    if (hasEigenData && showScalingFactors) {
        drawEigenvalueInfo(painter);
    }
    
    // Draw explanation text for comparison mode
    if (visualizationMode == 2 && hasEigenData) {
        drawTransformationComparison(painter);
    }
    
    // Draw status info
    painter.setPen(Qt::black);
    QFont font = painter.font();
    font.setPointSize(9);
    painter.setFont(font);
    
    QString info = QString("Zoom: %1x | Eigenvectors: %2")
        .arg(zoom / 50.0, 0, 'f', 2)
        .arg(hasEigenData ? eigenData.size() : 0);
    
    painter.drawText(10, height() - 10, info);
}

void EigenVisualizer::drawGrid(QPainter &painter)
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

void EigenVisualizer::drawAxes(QPainter &painter)
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
    
    // Draw tick marks
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
    
    // Y-axis ticks
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

void EigenVisualizer::drawEigenspace(QPainter &painter, const QPointF &eigenvector, 
                                    const QColor &color, double eigenvalue)
{
    // Draw a line through the origin in the direction of the eigenvector
    // This represents the eigenspace (span of the eigenvector)
    
    QPointF origin = worldToScreen(QPointF(0, 0));
    
    // Extend the line across the entire widget
    double angle = std::atan2(eigenvector.y(), eigenvector.x());
    double maxDist = std::max(width(), height()) * 2;
    
    QPointF end1 = worldToScreen(QPointF(std::cos(angle) * maxDist / zoom, 
                                         std::sin(angle) * maxDist / zoom));
    QPointF end2 = worldToScreen(QPointF(-std::cos(angle) * maxDist / zoom, 
                                         -std::sin(angle) * maxDist / zoom));
    
    QPen pen(color, 2, Qt::DashLine);
    painter.setPen(pen);
    painter.drawLine(end1, end2);
    
    // Draw label for eigenspace
    QPointF labelPos = worldToScreen(eigenvector * 1.3);
    painter.setPen(color.darker(130));
    QFont font = painter.font();
    font.setPointSize(8);
    painter.setFont(font);
    painter.drawText(labelPos, QString("λ = %1").arg(eigenvalue, 0, 'f', 2));
}

void EigenVisualizer::drawEigenvector(QPainter &painter, const QPointF &eigenvector, 
                                     const std::complex<double> &eigenvalue, const QColor &color)
{
    drawVector(painter, eigenvector, color, 3.5);
    
    // Also draw the negative direction (eigenspaces go both ways)
    drawVector(painter, -eigenvector, color.lighter(130), 2.0, true);
}

void EigenVisualizer::drawVector(QPainter &painter, const QPointF &vec, const QColor &color, 
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

void EigenVisualizer::drawVectorLabel(QPainter &painter, const QPointF &vec, 
                                     const QString &label, const QColor &color)
{
    QPointF screenPos = worldToScreen(vec);
    
    painter.setPen(color);
    QFont font = painter.font();
    font.setPointSize(10);
    font.setBold(true);
    painter.setFont(font);
    
    screenPos += QPointF(10, -10);
    painter.drawText(screenPos, label);
}

void EigenVisualizer::drawEigenvalueInfo(QPainter &painter)
{
    if (!hasEigenData) return;
    
    painter.setPen(Qt::black);
    QFont font = painter.font();
    font.setPointSize(10);
    painter.setFont(font);
    
    int yPos = 30;
    painter.drawText(10, yPos, "Eigenvalue Scaling Factors:");
    yPos += 20;
    
    for (int i = 0; i < eigenData.size(); ++i) {
        const EigenData &data = eigenData[i];
        painter.setPen(data.color.darker(120));
        
        QString text = QString("λ%1 = %2 → ")
            .arg(i + 1)
            .arg(data.eigenvalue.real(), 0, 'f', 3);
        
        if (std::abs(data.eigenvalue.real()) > 1.0) {
            text += "EXPANDING";
        } else if (std::abs(data.eigenvalue.real()) < 1.0 && std::abs(data.eigenvalue.real()) > 0.01) {
            text += "CONTRACTING";
        } else {
            text += "COLLAPSING";
        }
        
        painter.drawText(10, yPos, text);
        yPos += 18;
    }
}

void EigenVisualizer::drawTransformationComparison(QPainter &painter)
{
    painter.setPen(Qt::black);
    QFont font = painter.font();
    font.setPointSize(9);
    painter.setFont(font);
    
    int yPos = height() - 80;
    painter.fillRect(5, yPos - 15, 400, 75, QColor(255, 255, 220, 200));
    
    painter.drawText(10, yPos, "KEY INSIGHT:");
    yPos += 15;
    
    painter.setPen(Qt::blue);
    painter.drawText(10, yPos, "• Eigenvectors (colored) only SCALE - stay on same line");
    yPos += 15;
    
    painter.setPen(QColor(100, 100, 100));
    painter.drawText(10, yPos, "• Regular vectors (gray) both ROTATE and SCALE");
    yPos += 15;
    
    painter.setPen(Qt::black);
    painter.drawText(10, yPos, "This is why eigenvectors are special!");
}

QPointF EigenVisualizer::worldToScreen(const QPointF &worldPos) const
{
    QPointF center(width() / 2.0 + panOffset.x(), height() / 2.0 + panOffset.y());
    return QPointF(center.x() + worldPos.x() * zoom,
                   center.y() - worldPos.y() * zoom);
}

QPointF EigenVisualizer::screenToWorld(const QPointF &screenPos) const
{
    QPointF center(width() / 2.0 + panOffset.x(), height() / 2.0 + panOffset.y());
    return QPointF((screenPos.x() - center.x()) / zoom,
                   -(screenPos.y() - center.y()) / zoom);
}

QPointF EigenVisualizer::transformVector(const QPointF &vec) const
{
    if (!hasMatrix) return vec;
    
    double x = transformMatrix.getValue(0, 0) * vec.x() + transformMatrix.getValue(0, 1) * vec.y();
    double y = transformMatrix.getValue(1, 0) * vec.x() + transformMatrix.getValue(1, 1) * vec.y();
    return QPointF(x, y);
}

void EigenVisualizer::mousePressEvent(QMouseEvent *event)
{
    if (event->button() == Qt::LeftButton) {
        lastMousePos = event->pos();
        isPanning = true;
    }
}

void EigenVisualizer::mouseMoveEvent(QMouseEvent *event)
{
    if (isPanning) {
        QPointF delta = event->pos() - lastMousePos;
        panOffset += delta;
        lastMousePos = event->pos();
        update();
    }
}

void EigenVisualizer::mouseReleaseEvent(QMouseEvent *event)
{
    if (event->button() == Qt::LeftButton) {
        isPanning = false;
    }
}

void EigenVisualizer::wheelEvent(QWheelEvent *event)
{
    double zoomFactor = 1.1;
    
    if (event->angleDelta().y() > 0) {
        zoom *= zoomFactor;
    } else {
        zoom /= zoomFactor;
    }
    
    zoom = qBound(10.0, zoom, 200.0);
    update();
}

void EigenVisualizer::resizeEvent(QResizeEvent *event)
{
    Q_UNUSED(event);
    update();
}

void EigenVisualizer::resetView()
{
    zoom = 50.0;
    panOffset = QPointF(0, 0);
    update();
}

void EigenVisualizer::setZoom(double z)
{
    zoom = qBound(10.0, z, 200.0);
    update();
}

bool EigenVisualizer::exportToPNG(const QString &filePath, int width, int height)
{
    QImage image(width, height, QImage::Format_ARGB32);
    image.fill(backgroundColor);
    
    QPainter painter(&image);
    painter.setRenderHint(QPainter::Antialiasing);
    
    // Save current size
    int oldWidth = this->width();
    int oldHeight = this->height();
    
    // Temporarily resize
    resize(width, height);
    
    // Render
    if (showGrid) drawGrid(painter);
    drawAxes(painter);
    
    if (showEigenspaces && hasEigenData) {
        for (const EigenData &data : eigenData) {
            if (data.isReal) {
                drawEigenspace(painter, data.eigenvector, data.color.lighter(160), 
                             data.eigenvalue.real());
            }
        }
    }
    
    if (hasEigenData) {
        for (const EigenData &data : eigenData) {
            if (data.isReal) {
                drawEigenvector(painter, data.eigenvector, data.eigenvalue, data.color);
            }
        }
    }
    
    // Restore size
    resize(oldWidth, oldHeight);
    
    return image.save(filePath);
}

void EigenVisualizer::setShowGrid(bool show)
{
    showGrid = show;
    update();
}

void EigenVisualizer::setShowEigenspaces(bool show)
{
    showEigenspaces = show;
    update();
}

void EigenVisualizer::setShowComparisonVectors(bool show)
{
    showComparisonVectors = show;
    update();
}

void EigenVisualizer::setShowScalingFactors(bool show)
{
    showScalingFactors = show;
    update();
}
