#ifndef SURFACE3DWIDGET_H
#define SURFACE3DWIDGET_H

#include <QtDataVisualization/Q3DSurface>
#include <QtDataVisualization/QSurfaceDataProxy>
#include <QtDataVisualization/QSurface3DSeries>
#include <QWidget>
#include <QComboBox>
#include <QCheckBox>
#include <QSlider>
#include <QLabel>
#include <functional>

namespace QtDataVisualization {
    class Q3DSurface;
    class QSurfaceDataProxy;
    class QSurface3DSeries;
}

class Surface3DWidget : public QWidget
{
    Q_OBJECT

public:
    using LossFunction = std::function<double(double, double)>;
    
    explicit Surface3DWidget(QWidget *parent = nullptr);
    ~Surface3DWidget();

    // Predefined loss functions
    static double rosenbrock(double x, double y);
    static double himmelblau(double x, double y);
    static double beale(double x, double y);
    static double rastrigin(double x, double y);
    static double sphere(double x, double y);
    static double saddle(double x, double y);
    
    void setLossFunction(const QString& functionName);
    void setCustomFunction(LossFunction func);
    void updateSurface();
    
    QtDataVisualization::Q3DSurface* getSurface() { return m_surface; }

signals:
    void functionChanged(const QString& name);

private slots:
    void onFunctionChanged(int index);
    void onResolutionChanged(int value);
    void onSurfaceModeToggled(bool checked);
    void onGridToggled(bool checked);
    void onSmoothToggled(bool checked);

private:
    void setupUI();
    void populateSurfaceData();
    void setupGradientColor();
    
    QtDataVisualization::Q3DSurface* m_surface;
    QtDataVisualization::QSurface3DSeries* m_series;
    
    QComboBox* m_functionCombo;
    QSlider* m_resolutionSlider;
    QLabel* m_resolutionLabel;
    QCheckBox* m_solidSurfaceCheck;
    QCheckBox* m_gridCheck;
    QCheckBox* m_smoothCheck;
    
    LossFunction m_currentFunction;
    QString m_currentFunctionName;
    
    // Surface parameters
    double m_minX = -5.0;
    double m_maxX = 5.0;
    double m_minY = -5.0;
    double m_maxY = 5.0;
    int m_resolution = 50;
    
    struct FunctionInfo {
        QString name;
        LossFunction func;
        double minX, maxX, minY, maxY;
    };
    
    QList<FunctionInfo> m_functions;
};

#endif // SURFACE3DWIDGET_H
