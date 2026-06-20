#ifndef EIGENVISUALIZER_H
#define EIGENVISUALIZER_H

#include <QWidget>
#include <QPainter>
#include <QMouseEvent>
#include <QWheelEvent>
#include <QPointF>
#include <QVector>
#include <QPushButton>
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QLabel>
#include <QSlider>
#include <QCheckBox>
#include <QComboBox>
#include <complex>
#include "MatrixEngineAdapter.h"

/**
 * EigenVisualizer - Educational Eigenvalue/Eigenvector Visualizer
 * 
 * Visualizes the special properties of eigenvectors:
 * - Eigenvectors are directions that only get scaled (not rotated) by a transformation
 * - Eigenvalues tell you the scaling factor
 * - Shows the eigenspace (span of eigenvector)
 * - Demonstrates why eigenvectors are fundamental to understanding transformations
 * 
 * Features:
 * - Color-coded eigenvectors by eigenvalue magnitude
 * - Eigenspaces (lines through origin)
 * - Comparison with non-eigenvectors to show the difference
 * - Support for real and complex eigenvalues
 * - Interactive zoom/pan
 * - Export to PNG
 */
class EigenVisualizer : public QWidget
{
    Q_OBJECT

public:
    explicit EigenVisualizer(QWidget *parent = nullptr);
    
    // Matrix and eigenvalue management
    void setMatrix(const Matrix &matrix);
    void clearMatrix();
    
    // Manually set eigenvalues/eigenvectors (e.g., from external computation)
    void setEigenData(const QVector<std::complex<double>> &eigenvalues,
                      const QVector<QPointF> &eigenvectors);
    
    // Add comparison vectors (to show how they transform differently)
    void addComparisonVector(double x, double y);
    void clearComparisonVectors();
    
    // View control
    void resetView();
    void setZoom(double zoom);
    
    // Export
    bool exportToPNG(const QString &filePath, int width = 800, int height = 800);
    
    // Display options
    void setShowGrid(bool show);
    void setShowEigenspaces(bool show);
    void setShowComparisonVectors(bool show);
    void setShowScalingFactors(bool show);

signals:
    void eigenDataCalculated(int numRealEigenvalues);
    void matrixChanged();

protected:
    void paintEvent(QPaintEvent *event) override;
    void mousePressEvent(QMouseEvent *event) override;
    void mouseMoveEvent(QMouseEvent *event) override;
    void mouseReleaseEvent(QMouseEvent *event) override;
    void wheelEvent(QWheelEvent *event) override;
    void resizeEvent(QResizeEvent *event) override;

private slots:
    void onResetViewClicked();
    void onExportClicked();
    void onCalculateEigenClicked();
    void onVisualizationModeChanged(int index);

private:
    // Drawing functions
    void drawGrid(QPainter &painter);
    void drawAxes(QPainter &painter);
    void drawEigenspace(QPainter &painter, const QPointF &eigenvector, 
                       const QColor &color, double eigenvalue);
    void drawEigenvector(QPainter &painter, const QPointF &eigenvector, 
                        const std::complex<double> &eigenvalue, const QColor &color);
    void drawVector(QPainter &painter, const QPointF &vec, const QColor &color, 
                   double width = 2.0, bool dashed = false);
    void drawVectorLabel(QPainter &painter, const QPointF &vec, const QString &label,
                        const QColor &color = Qt::black);
    void drawEigenvalueInfo(QPainter &painter);
    void drawTransformationComparison(QPainter &painter);
    
    // Coordinate transformations
    QPointF worldToScreen(const QPointF &worldPos) const;
    QPointF screenToWorld(const QPointF &screenPos) const;
    
    // Helper functions
    void setupUI();
    void applyTheme();
    void calculateEigenvalues();
    QColor getColorForEigenvalue(const std::complex<double> &eigenvalue) const;
    QPointF transformVector(const QPointF &vec) const;
    double getEigenvalueMagnitude(const std::complex<double> &eigenvalue) const;
    
    // Simplified 2x2 eigenvalue calculation
    void calculateEigen2x2();
    
    // Eigenvalue/eigenvector data
    struct EigenData {
        std::complex<double> eigenvalue;
        QPointF eigenvector;  // Only for real eigenvalues in 2D
        QColor color;
        bool isReal;
    };
    
    QVector<EigenData> eigenData;
    Matrix transformMatrix;
    bool hasMatrix;
    bool hasEigenData;
    
    // Comparison vectors (to show difference from eigenvectors)
    struct ComparisonVector {
        QPointF original;
        QPointF transformed;
        QColor color;
    };
    QVector<ComparisonVector> comparisonVectors;
    
    // View state
    double zoom;
    QPointF panOffset;
    QPointF lastMousePos;
    bool isPanning;
    
    // Display options
    bool showGrid;
    bool showEigenspaces;
    bool showComparisonVectors;
    bool showScalingFactors;
    bool showTransformation;
    
    // Visualization mode: 0 = eigenvectors only, 1 = with transformation, 2 = comparison
    int visualizationMode;
    
    // UI Controls
    QPushButton *resetViewButton;
    QPushButton *exportButton;
    QPushButton *calculateEigenButton;
    QComboBox *visualizationModeCombo;
    QCheckBox *showGridCheckbox;
    QCheckBox *showEigenspacesCheckbox;
    QCheckBox *showComparisonCheckbox;
    QCheckBox *showScalingCheckbox;
    QLabel *infoLabel;
    QLabel *eigenInfoLabel;
    
    // Colors
    QColor gridColor;
    QColor axisColor;
    QColor eigenspaceColor;
    QColor backgroundColor;
    QColor comparisonColor;
};

#endif // EIGENVISUALIZER_H
