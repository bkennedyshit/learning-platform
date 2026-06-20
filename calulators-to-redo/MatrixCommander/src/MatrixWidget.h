#ifndef MATRIXWIDGET_H
#define MATRIXWIDGET_H

#include <QWidget>
#include <QTableWidget>
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QSpinBox>
#include <QLabel>
#include <QPushButton>
#include <QHeaderView>
#include "MatrixEngineAdapter.h"

class MatrixWidget : public QWidget
{
    Q_OBJECT

public:
    explicit MatrixWidget(int rows = 3, int cols = 3, QWidget *parent = nullptr);
    
    Matrix getMatrix() const;
    void setMatrix(const Matrix &matrix);
    void setDimensions(int rows, int cols);
    void setValue(int row, int col, double value);
    double getValue(int row, int col) const;
    void clear();
    void fillRandom(double min = -10.0, double max = 10.0);
    void fillIdentity();
    void fillZero();

signals:
    void matrixChanged();
    void dimensionsChanged(int rows, int cols);

private slots:
    void onRowsChanged(int rows);
    void onColsChanged(int cols);
    void onCellChanged(int row, int col);
    void onRandomFill();
    void onIdentityFill();
    void onZeroFill();

private:
    void setupUI();
    void updateTable();
    void applyTheme();

    QTableWidget *tableWidget;
    QSpinBox *rowSpinBox;
    QSpinBox *colSpinBox;
    QPushButton *randomBtn;
    QPushButton *identityBtn;
    QPushButton *zeroBtn;
    
    int currentRows;
    int currentCols;
};

#endif // MATRIXWIDGET_H
