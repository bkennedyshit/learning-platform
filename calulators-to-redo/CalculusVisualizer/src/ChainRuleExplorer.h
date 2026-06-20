/**
 * ChainRuleExplorer.h - Interactive chain rule breakdown for understanding backpropagation
 */

#ifndef CHAINRULEEXPLORER_H
#define CHAINRULEEXPLORER_H

#include <QWidget>
#include <QLineEdit>
#include <QTextEdit>
#include <QPushButton>
#include <QTreeWidget>
#include <QLabel>

class ChainRuleExplorer : public QWidget
{
    Q_OBJECT

public:
    explicit ChainRuleExplorer(QWidget *parent = nullptr);
    ~ChainRuleExplorer() override;

private slots:
    void onComputeChainRule();
    void onExampleSelected(int index);
    void onClearAll();

private:
    void setupUI();
    void setupConnections();
    void analyzeComposition(const QString &expression);
    void displayChainRuleSteps(const QString &expression);
    void addExample(const QString &name, const QString &expression);
    QString extractOuterFunction(const QString &expr);
    QString extractInnerFunction(const QString &expr);
    
    // UI Components
    QLineEdit *expressionInput;
    QPushButton *computeBtn;
    QPushButton *clearBtn;
    QComboBox *examplesComboBox;
    
    QTreeWidget *decompositionTree;
    QTextEdit *stepsOutput;
    QTextEdit *backpropExplanation;
    
    QLabel *outerFunctionLabel;
    QLabel *innerFunctionLabel;
    QLabel *resultLabel;
    
    struct ChainComponent {
        QString name;
        QString expression;
        QString derivative;
        int level;
    };
    
    QVector<ChainComponent> components;
};

#endif // CHAINRULEEXPLORER_H
