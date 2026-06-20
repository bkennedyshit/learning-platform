#ifndef VECTORVISUALIZER_H
#define VECTORVISUALIZER_H

#include <QWidget>
#include <QPainter>
#include <QMouseEvent>
#include <QWheelEvent>
#include <QTimer>
#include <QPointF>
#include <QVector>
#include <QPushButton>
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QLabel>
#include <QSlider>
#include <QCheckBox>
#include "MatrixEngineAdapter.h"

/**
 * VectorVisualizer - Interactive 2D Vector and Matrix Transformation Visualizer
 * 
 * Educational tool for visualizing:
 * - 2D vectors as arrows on a coordinate grid
 * - Matrix transformations (before/after)
 * - Basis vector transformations
 * - Animated transitions between states
 * 
 * Features:
 * - Zoom/Pan with mouse
 * - Color-coded vectors (original vs transformed)
 * - Grid with axis labels
 * - Export to PNG
 * - Animation of transformations
 */
class VectorVisualizer : public QWidget
{
    Q_OBJECT

public:
    explicit VectorVisualizer(QWidget *parent = nullptr);
    
    // Vector management
    void addVector(double x, double y, const QColor &color = Qt::blue);
    void clearVectors();
    void setVectors(const QVector<QPointF> &vectors);
    
    // Transformation
    void setTransformationMatrix(const Matrix &matrix);
    void applyTransformation();
    void resetTransformation();
    void animateTransformation(int durationMs = 1000);
    
    // View control
    void resetView();
    void setZoom(double zoom);
    void centerView();
    
    // Export
    bool exportToPNG(const QString &filePath, int width = 800, int height = 800);
    
    // Display options
    void setShowGrid(bool show);
    void setShowBasisVectors(bool show);
    void setShowTransformed(bool show);
    void setShowOriginal(bool show);

signals:
    void vectorClicked(int index, QPointF position);
    void transformationComplete();

protected:
    void paintEvent(QPaintEvent *event) override;
    void mousePressEvent(QMouseEvent *event) override;
    void mouseMoveEvent(QMouseEvent *event) override;
    void mouseReleaseEvent(QMouseEvent *event) override;
    void wheelEvent(QWheelEvent *event) override;
    void resizeEvent(QResizeEvent *event) override;

private slots:
    void onAnimationTick();
    void onPlayPauseClicked();
    void onResetViewClicked();
    void onExportClicked();
    void onAnimationSpeedChanged(int value);

private:
    // Drawing functions
    void drawGrid(QPainter &painter);
    void drawAxes(QPainter &painter);
    void drawVector(QPainter &painter, const QPointF &vec, const QColor &color, 
                   double width = 2.0, bool dashed = false);
    void drawBasisVectors(QPainter &painter);
    void drawVectorLabel(QPainter &painter, const QPointF &vec, const QString &label);
    
    // Coordinate transformations
    QPointF worldToScreen(const QPointF &worldPos) const;
    QPointF screenToWorld(const QPointF &screenPos) const;
    
    // Helper functions
    void setupUI();
    void applyTheme();
    Matrix getIdentityMatrix2D() const;
    QPointF transformVector(const QPointF &vec, const Matrix &matrix) const;
    
    // Vectors and transformations
    struct VectorData {
        QPointF original;
        QPointF transformed;
        QColor color;
        QString label;
    };
    
    QVector<VectorData> vectors;
    Matrix transformMatrix;
    bool hasTransformation;
    
    // Basis vectors (i-hat, j-hat)
    QPointF basisI;      // (1, 0)
    QPointF basisJ;      // (0, 1)
    QPointF transformedBasisI;
    QPointF transformedBasisJ;
    
    // View state
    double zoom;
    QPointF panOffset;
    QPointF lastMousePos;
    bool isPanning;
    bool isDragging;
    
    // Display options
    bool showGrid;
    bool showBasisVectors;
    bool showTransformed;
    bool showOriginal;
    bool showLabels;
    
    // Animation
    QTimer *animationTimer;
    double animationProgress;  // 0.0 to 1.0
    bool isAnimating;
    int animationSpeed;  // milliseconds for full animation
    
    // UI Controls
    QPushButton *playPauseButton;
    QPushButton *resetViewButton;
    QPushButton *exportButton;
    QSlider *animationSpeedSlider;
    QCheckBox *showGridCheckbox;
    QCheckBox *showBasisCheckbox;
    QCheckBox *showOriginalCheckbox;
    QCheckBox *showTransformedCheckbox;
    QLabel *infoLabel;
    
    // Colors
    QColor gridColor;
    QColor axisColor;
    QColor originalVectorColor;
    QColor transformedVectorColor;
    QColor basisIColor;
    QColor basisJColor;
    QColor backgroundColor;
};

#endif // VECTORVISUALIZER_H
