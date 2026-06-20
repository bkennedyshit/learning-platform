#ifndef SOFTMAXVISUALIZER_H
#define SOFTMAXVISUALIZER_H

#include <QWidget>
#include <QSlider>
#include <QLabel>
#include <QLineEdit>
#include <QVector>
#include <QPushButton>

namespace QtCharts {
    class QChart;
    class QChartView;
    class QBarSet;
    class QBarSeries;
}

class SoftmaxVisualizer : public QWidget
{
    Q_OBJECT

public:
    explicit SoftmaxVisualizer(QWidget *parent = nullptr);
    ~SoftmaxVisualizer();

private slots:
    void onTemperatureChanged(int value);
    void onInputChanged();
    void randomizeInputs();
    void updateVisualization();

private:
    void setupUI();
    QVector<double> computeSoftmax(const QVector<double> &logits, double temperature);
    
    QSlider *temperatureSlider;
    QLabel *temperatureLabel;
    QLabel *temperatureValue;
    
    QVector<QLineEdit*> logitInputs;
    QVector<QLabel*> probabilityLabels;
    QPushButton *randomizeButton;
    
    QtCharts::QChartView *chartView;
    QtCharts::QChart *chart;
    QtCharts::QBarSeries *barSeries;
    
    QLabel *infoLabel;
    QLabel *entropyLabel;
    
    double temperature;
    static constexpr int NUM_CLASSES = 5;
};

#endif // SOFTMAXVISUALIZER_H
