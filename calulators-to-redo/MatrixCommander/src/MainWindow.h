#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QWidget>
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QLabel>
#include <QStatusBar>
#include <QPushButton>
#include <QTextEdit>
#include <QSplitter>
#include <QClipboard>
#include <QApplication>
#include <QMouseEvent>
#include <QPoint>
#include "MatrixWidget.h"
#include "OperationPanel.h"
#include "MatrixEngineAdapter.h"

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

protected:
    void mousePressEvent(QMouseEvent *event) override;
    void mouseMoveEvent(QMouseEvent *event) override;
    void mouseReleaseEvent(QMouseEvent *event) override;
    void keyPressEvent(QKeyEvent *event) override;

private slots:
    void onMatrixOperation(const QString &operation);
    void onMatrixChanged();
    void onMatrix2Changed();
    void exportResults();
    void copyToClipboard();
    void pasteFromClipboard();
    void clearAll();
    void minimizeWindow();
    void closeWindow();

private:
    void setupUI();
    void setupMenuBar();
    void setupConnections();
    void applyMatlabTheme();
    void updateStatusBar();
    void displayResult(const Matrix &result, const QString &operationName);
    void displayError(const QString &error);
    Matrix getCurrentMatrix();
    Matrix getSecondMatrix();

    // UI Components
    MatrixWidget *matrix1Widget;
    MatrixWidget *matrix2Widget;
    OperationPanel *operationPanel;
    QTextEdit *resultsDisplay;
    QLabel *matrix1Label;
    QLabel *matrix2Label;
    QLabel *resultsLabel;
    QPushButton *exportBtn;
    QPushButton *clearBtn;
    QPushButton *minimizeBtn;
    QPushButton *closeBtn;
    QWidget *titleBar;
    QLabel *titleLabel;
    
    // Matrix Engine
    MatrixEngineAdapter *engine;
    
    // Window dragging
    bool isDragging;
    QPoint dragPosition;
    
    // Status tracking
    QString lastOperation;
    Matrix lastResult;
};

#endif // MAINWINDOW_H
