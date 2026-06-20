#ifndef BAYESCALCULATOR_H
#define BAYESCALCULATOR_H

#include <QWidget>
#include <QSlider>
#include <QLabel>
#include <QLineEdit>
#include <QPushButton>
#include <QGraphicsView>
#include <QGraphicsScene>

class BayesCalculator : public QWidget
{
    Q_OBJECT

public:
    explicit BayesCalculator(QWidget *parent = nullptr);
    ~BayesCalculator();

private slots:
    void onPriorChanged(int value);
    void onLikelihoodChanged(int value);
    void onEvidenceChanged(int value);
    void updateCalculation();
    void loadExample(int index);

private:
    void setupUI();
    void drawProbabilityTree();
    
    QSlider *priorSlider;
    QSlider *likelihoodSlider;
    QSlider *evidenceSlider;
    
    QLabel *priorValue;
    QLabel *likelihoodValue;
    QLabel *evidenceValue;
    QLabel *posteriorValue;
    
    QLabel *formulaLabel;
    QLabel *explanationLabel;
    
    QGraphicsView *treeView;
    QGraphicsScene *treeScene;
    
    QPushButton *exampleButtons[3];
    
    double prior;       // P(H)
    double likelihood;  // P(E|H)
    double evidence;    // P(E)
    double posterior;   // P(H|E)
};

#endif // BAYESCALCULATOR_H
