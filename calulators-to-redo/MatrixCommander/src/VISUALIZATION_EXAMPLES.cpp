/**
 * VISUALIZATION SYSTEM USAGE EXAMPLES
 * 
 * This file demonstrates how to use the VectorVisualizer and EigenVisualizer
 * classes in the Matrix Commander application.
 * 
 * Author: Matrix Commander Development Team
 * Date: May 6, 2026
 */

#include "VectorVisualizer.h"
#include "EigenVisualizer.h"
#include "MatrixEngineAdapter.h"
#include <QApplication>
#include <QMainWindow>
#include <QTabWidget>
#include <QVBoxLayout>

// ============================================================================
// EXAMPLE 1: Basic Vector Visualization
// ============================================================================

void example1_BasicVectors()
{
    VectorVisualizer *visualizer = new VectorVisualizer();
    
    // Add some vectors to visualize
    visualizer->addVector(2.0, 1.0, Qt::blue);     // Blue vector at (2, 1)
    visualizer->addVector(-1.0, 2.0, Qt::red);     // Red vector at (-1, 2)
    visualizer->addVector(1.5, -1.5, Qt::green);   // Green vector at (1.5, -1.5)
    
    visualizer->show();
}

// ============================================================================
// EXAMPLE 2: Matrix Transformation Animation
// ============================================================================

void example2_MatrixTransformation()
{
    VectorVisualizer *visualizer = new VectorVisualizer();
    
    // Add initial vectors
    visualizer->addVector(1.0, 0.0, Qt::blue);
    visualizer->addVector(0.0, 1.0, Qt::red);
    visualizer->addVector(1.0, 1.0, Qt::green);
    
    // Create a rotation matrix (45 degrees)
    Matrix rotationMatrix(2, 2);
    double angle = M_PI / 4.0;  // 45 degrees
    rotationMatrix.setValue(0, 0, cos(angle));
    rotationMatrix.setValue(0, 1, -sin(angle));
    rotationMatrix.setValue(1, 0, sin(angle));
    rotationMatrix.setValue(1, 1, cos(angle));
    
    // Set the transformation
    visualizer->setTransformationMatrix(rotationMatrix);
    
    // Animate the transformation over 2 seconds
    visualizer->animateTransformation(2000);
    
    visualizer->show();
}

// ============================================================================
// EXAMPLE 3: Scaling Transformation
// ============================================================================

void example3_ScalingTransformation()
{
    VectorVisualizer *visualizer = new VectorVisualizer();
    
    // Add vectors
    visualizer->addVector(1.0, 1.0, Qt::blue);
    visualizer->addVector(-1.0, 1.0, Qt::red);
    
    // Create a scaling matrix (2x in X, 0.5x in Y)
    Matrix scaleMatrix(2, 2);
    scaleMatrix.setValue(0, 0, 2.0);   // Scale X by 2
    scaleMatrix.setValue(0, 1, 0.0);
    scaleMatrix.setValue(1, 0, 0.0);
    scaleMatrix.setValue(1, 1, 0.5);   // Scale Y by 0.5
    
    visualizer->setTransformationMatrix(scaleMatrix);
    visualizer->animateTransformation(1500);
    
    visualizer->show();
}

// ============================================================================
// EXAMPLE 4: Shear Transformation
// ============================================================================

void example4_ShearTransformation()
{
    VectorVisualizer *visualizer = new VectorVisualizer();
    
    // Add a grid of vectors to see the shear effect
    for (int i = -2; i <= 2; i++) {
        for (int j = -2; j <= 2; j++) {
            if (i == 0 && j == 0) continue;
            QColor color = (i + j) % 2 == 0 ? Qt::blue : Qt::red;
            visualizer->addVector(i, j, color.lighter(120));
        }
    }
    
    // Create a shear matrix
    Matrix shearMatrix(2, 2);
    shearMatrix.setValue(0, 0, 1.0);
    shearMatrix.setValue(0, 1, 0.5);  // Shear factor
    shearMatrix.setValue(1, 0, 0.0);
    shearMatrix.setValue(1, 1, 1.0);
    
    visualizer->setTransformationMatrix(shearMatrix);
    visualizer->setShowBasisVectors(true);  // Show how basis vectors transform
    
    visualizer->show();
}

// ============================================================================
// EXAMPLE 5: Eigenvalue Visualization
// ============================================================================

void example5_EigenvalueVisualization()
{
    EigenVisualizer *eigenViz = new EigenVisualizer();
    
    // Create a matrix with clear eigenvectors
    // This matrix stretches by 3 in the (1,1) direction and by 0.5 in the (1,-1) direction
    Matrix matrix(2, 2);
    matrix.setValue(0, 0, 1.75);   // a
    matrix.setValue(0, 1, 1.25);   // b
    matrix.setValue(1, 0, 1.25);   // c
    matrix.setValue(1, 1, 1.75);   // d
    
    eigenViz->setMatrix(matrix);
    eigenViz->show();
}

// ============================================================================
// EXAMPLE 6: Diagonal Matrix (Easy Eigenvalues)
// ============================================================================

void example6_DiagonalMatrix()
{
    EigenVisualizer *eigenViz = new EigenVisualizer();
    
    // Diagonal matrix: eigenvalues are the diagonal entries
    // Eigenvectors are the standard basis vectors
    Matrix diagonal(2, 2);
    diagonal.setValue(0, 0, 3.0);   // Eigenvalue 1
    diagonal.setValue(0, 1, 0.0);
    diagonal.setValue(1, 0, 0.0);
    diagonal.setValue(1, 1, 0.5);   // Eigenvalue 2
    
    eigenViz->setMatrix(diagonal);
    
    // Add comparison vectors to see the difference
    eigenViz->addComparisonVector(1.0, 1.0);   // Not an eigenvector
    eigenViz->addComparisonVector(1.5, 0.5);   // Not an eigenvector
    
    eigenViz->setShowComparisonVectors(true);
    eigenViz->show();
}

// ============================================================================
// EXAMPLE 7: Rotation Matrix (Complex Eigenvalues)
// ============================================================================

void example7_RotationMatrix()
{
    EigenVisualizer *eigenViz = new EigenVisualizer();
    
    // Pure rotation has complex eigenvalues - no real eigenvectors!
    Matrix rotation(2, 2);
    double angle = M_PI / 6.0;  // 30 degrees
    rotation.setValue(0, 0, cos(angle));
    rotation.setValue(0, 1, -sin(angle));
    rotation.setValue(1, 0, sin(angle));
    rotation.setValue(1, 1, cos(angle));
    
    eigenViz->setMatrix(rotation);
    // Will show a message that there are no real eigenvectors
    // (rotations in 2D don't have invariant directions)
    
    eigenViz->show();
}

// ============================================================================
// EXAMPLE 8: Combined Visualization in Tabs
// ============================================================================

void example8_CombinedVisualization()
{
    QMainWindow *window = new QMainWindow();
    QTabWidget *tabs = new QTabWidget();
    
    // Vector transformation tab
    VectorVisualizer *vectorViz = new VectorVisualizer();
    vectorViz->addVector(2.0, 1.0, Qt::blue);
    vectorViz->addVector(1.0, 2.0, Qt::red);
    
    Matrix transform(2, 2);
    transform.setValue(0, 0, 1.0);
    transform.setValue(0, 1, 1.0);
    transform.setValue(1, 0, 0.0);
    transform.setValue(1, 1, 1.0);
    
    vectorViz->setTransformationMatrix(transform);
    tabs->addTab(vectorViz, "Vector Transformation");
    
    // Eigen analysis tab
    EigenVisualizer *eigenViz = new EigenVisualizer();
    eigenViz->setMatrix(transform);
    tabs->addTab(eigenViz, "Eigenvalue Analysis");
    
    window->setCentralWidget(tabs);
    window->resize(900, 700);
    window->setWindowTitle("Matrix Commander - Visualization System");
    window->show();
}

// ============================================================================
// EXAMPLE 9: Educational Demonstration - ML Application
// ============================================================================

void example9_MLPCAVisualization()
{
    // This demonstrates PCA (Principal Component Analysis) - 
    // a fundamental ML technique that uses eigenvalues/eigenvectors
    
    VectorVisualizer *vectorViz = new VectorVisualizer();
    EigenVisualizer *eigenViz = new EigenVisualizer();
    
    // Simulate data points (vectors) with correlation
    QVector<QPointF> dataPoints;
    for (int i = 0; i < 10; i++) {
        double t = i / 10.0;
        // Points roughly along a line with some noise
        dataPoints.append(QPointF(t * 2 - 1, t * 1.5 - 0.75));
    }
    
    vectorViz->setVectors(dataPoints);
    
    // Covariance matrix (simplified)
    Matrix covMatrix(2, 2);
    covMatrix.setValue(0, 0, 1.0);
    covMatrix.setValue(0, 1, 0.75);
    covMatrix.setValue(1, 0, 0.75);
    covMatrix.setValue(1, 1, 0.9);
    
    eigenViz->setMatrix(covMatrix);
    
    // The eigenvectors show the principal components!
    // The larger eigenvalue points in the direction of maximum variance
    
    vectorViz->show();
    eigenViz->show();
}

// ============================================================================
// EXAMPLE 10: Export Visualizations
// ============================================================================

void example10_ExportVisualizations()
{
    VectorVisualizer *visualizer = new VectorVisualizer();
    
    // Create interesting transformation
    visualizer->addVector(1.0, 0.0, Qt::blue);
    visualizer->addVector(0.0, 1.0, Qt::red);
    visualizer->addVector(1.0, 1.0, Qt::green);
    
    Matrix matrix(2, 2);
    matrix.setValue(0, 0, 2.0);
    matrix.setValue(0, 1, 1.0);
    matrix.setValue(1, 0, 0.5);
    matrix.setValue(1, 1, 1.5);
    
    visualizer->setTransformationMatrix(matrix);
    
    // Export at high resolution
    visualizer->exportToPNG("transformation_visualization.png", 1920, 1080);
    
    visualizer->show();
}

// ============================================================================
// MAIN FUNCTION - Run Examples
// ============================================================================

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);
    
    // Uncomment the example you want to run:
    
    // example1_BasicVectors();
    // example2_MatrixTransformation();
    // example3_ScalingTransformation();
    // example4_ShearTransformation();
    // example5_EigenvalueVisualization();
    // example6_DiagonalMatrix();
    // example7_RotationMatrix();
    example8_CombinedVisualization();  // Recommended to start
    // example9_MLPCAVisualization();
    // example10_ExportVisualizations();
    
    return app.exec();
}

/**
 * INTEGRATION INTO MATRIX COMMANDER
 * 
 * To integrate these visualizers into your main application:
 * 
 * 1. In MainWindow.h, add:
 *    #include "VectorVisualizer.h"
 *    #include "EigenVisualizer.h"
 * 
 *    private:
 *        VectorVisualizer *vectorVisualizer;
 *        EigenVisualizer *eigenVisualizer;
 * 
 * 2. In MainWindow.cpp constructor, create the visualizers:
 *    vectorVisualizer = new VectorVisualizer(this);
 *    eigenVisualizer = new EigenVisualizer(this);
 * 
 * 3. Add menu actions or buttons to show visualizers:
 *    connect(visualizeVectorsAction, &QAction::triggered, [this]() {
 *        vectorVisualizer->show();
 *    });
 * 
 * 4. When user performs matrix operations, update visualizers:
 *    void MainWindow::onMatrixMultiply() {
 *        Matrix result = matrixA * matrixB;
 *        vectorVisualizer->setTransformationMatrix(result);
 *        vectorVisualizer->animateTransformation(1000);
 *    }
 * 
 * 5. For eigenvalue analysis:
 *    void MainWindow::onEigenAnalysis() {
 *        Matrix matrix = getCurrentMatrix();
 *        eigenVisualizer->setMatrix(matrix);
 *        eigenVisualizer->show();
 *    }
 */
