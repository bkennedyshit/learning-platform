#ifndef OPERATIONPANEL_H
#define OPERATIONPANEL_H

#include <QWidget>
#include <QPushButton>
#include <QVBoxLayout>
#include <QGroupBox>
#include <QLabel>
#include <QScrollArea>

class OperationPanel : public QWidget
{
    Q_OBJECT

public:
    explicit OperationPanel(QWidget *parent = nullptr);

signals:
    void operationRequested(const QString &operation);

private slots:
    void onOperationClicked();

private:
    void setupUI();
    void createOperationButton(const QString &text, const QString &operation, 
                               const QString &tooltip, QVBoxLayout *layout);
    void applyTheme();

    QVBoxLayout *mainLayout;
    QGroupBox *basicOpsGroup;
    QGroupBox *advancedOpsGroup;
    QGroupBox *decompositionGroup;
    QGroupBox *propertiesGroup;
};

#endif // OPERATIONPANEL_H
