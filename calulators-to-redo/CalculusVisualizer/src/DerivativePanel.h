#ifndef DERIVATIVEPANEL_H
#define DERIVATIVEPANEL_H

#include <QWidget>
#include <QTextEdit>
#include <QLineEdit>
#include <QPushButton>
#include <QVBoxLayout>
#include <QLabel>
#include <QGroupBox>
#include <QListWidget>

class DerivativePanel : public QWidget {
    Q_OBJECT

public:
    explicit DerivativePanel(QWidget *parent = nullptr);
    ~DerivativePanel() override;

    void setFunction(const QString &function);
    void showDerivativeSteps(const QString &derivative);

private slots:
    void calculateDerivative();
    void onRuleSelected(int index);

private:
    void setupUI();
    void displaySteps(const QString &function);
    void addStep(const QString &rule, const QString &expression, const QString &explanation);
    void clearSteps();
    
    QString applyPowerRule(const QString &term);
    QString applyChainRule(const QString &expr);
    QString applyProductRule(const QString &expr);
    QString applyQuotientRule(const QString &expr);
    
    // UI Components
    QLineEdit *m_functionInput;
    QPushButton *m_calculateButton;
    QTextEdit *m_stepsDisplay;
    QListWidget *m_rulesList;
    QLabel *m_resultLabel;
    QComboBox *m_exampleSelector;
    
    QString m_currentFunction;
    QString m_currentDerivative;
    
    // Step-by-step data
    struct DerivativeStep {
        QString rule;
        QString expression;
        QString explanation;
        QString formula;
    };
    
    QVector<DerivativeStep> m_steps;
};

#endif // DERIVATIVEPANEL_H
