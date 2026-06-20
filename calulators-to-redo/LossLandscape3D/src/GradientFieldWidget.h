#ifndef GRADIENTFIELDWIDGET_H
#define GRADIENTFIELDWIDGET_H

#include <QWidget>
#include <QPainter>
#include <QSlider>
#include <QCheckBox>
#include <QComboBox>
#include <functional>

class GradientFieldWidget : public QWidget
{
    Q_OBJECT

public:
    using LossFunction = std::function<double(double, double)>;
    
    explicit GradientFieldWidget(QWidget *parent = nullptr);
    
    void setLossFunction(LossFunction func);
    void setBounds(double minX, double maxX, double minY, double maxY);
    void setArrowDensity(int density);
    void setColorByMagnitude(bool enable);
    void setShowHeatmap(bool show);
    
signals:
    void gradientClicked(double x, double y, double gx, double gy);

protected:
    void paintEvent(QPaintEvent* event) override;
    void mousePressEvent(QMouseEvent* event) override;
    void resizeEvent(QResizeEvent* event) override;

private slots:
    void onDensityChanged(int value);
    void onArrowSizeChanged(int value);
    void onColorModeChanged(int index);

private:
    void setupUI();
    void computeGradientField();
    void drawHeatmap(QPainter& painter);
    void drawQuiverPlot(QPainter& painter);
    void drawColorLegend(QPainter& painter);
    
    QPointF computeGradient(double x, double y) const;
    QColor magnitudeToColor(double magnitude, double maxMag) const;
    QPoint worldToScreen(double x, double y) const;
    QPointF screenToWorld(const QPoint& screen) const;
    
    LossFunction m_function;
    
    double m_minX = -5.0;
    double m_maxX = 5.0;
    double m_minY = -5.0;
    double m_maxY = 5.0;
    
    int m_arrowDensity = 25;
    double m_arrowSize = 1.0;
    bool m_colorByMagnitude = true;
    bool m_showHeatmap = false;
    
    enum ColorMode { Uniform, Magnitude, Direction };
    ColorMode m_colorMode = Magnitude;
    
    struct Arrow {
        QPointF position;
        QPointF gradient;
        double magnitude;
    };
    QVector<Arrow> m_arrows;
    
    double m_maxMagnitude = 1.0;
    
    // UI Components
    QWidget* m_canvas;
    QSlider* m_densitySlider;
    QSlider* m_arrowSizeSlider;
    QComboBox* m_colorModeCombo;
    QCheckBox* m_heatmapCheck;
    QCheckBox* m_normalizeCheck;
    
    bool m_normalizeArrows = false;
};

#endif // GRADIENTFIELDWIDGET_H
