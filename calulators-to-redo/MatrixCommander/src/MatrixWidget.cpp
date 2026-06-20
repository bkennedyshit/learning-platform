#include "MatrixWidget.h"
#include <QTableWidgetItem>
#include <QHeaderView>
#include <random>
#include <ctime>

MatrixWidget::MatrixWidget(int rows, int cols, QWidget *parent)
    : QWidget(parent)
    , currentRows(rows)
    , currentCols(cols)
{
    setupUI();
    updateTable();
    applyTheme();
}

void MatrixWidget::setupUI()
{
    QVBoxLayout *mainLayout = new QVBoxLayout(this);
    mainLayout->setSpacing(8);
    mainLayout->setContentsMargins(0, 0, 0, 0);
    
    // Dimension controls
    QHBoxLayout *controlLayout = new QHBoxLayout();
    
    QLabel *rowLabel = new QLabel("Rows:");
    rowLabel->setStyleSheet("color: #aaaaaa; font-size: 11px;");
    rowSpinBox = new QSpinBox();
    rowSpinBox->setRange(1, 10);
    rowSpinBox->setValue(currentRows);
    rowSpinBox->setFixedWidth(60);
    rowSpinBox->setObjectName("dimensionSpin");
    
    QLabel *colLabel = new QLabel("Cols:");
    colLabel->setStyleSheet("color: #aaaaaa; font-size: 11px;");
    colSpinBox = new QSpinBox();
    colSpinBox->setRange(1, 10);
    colSpinBox->setValue(currentCols);
    colSpinBox->setFixedWidth(60);
    colSpinBox->setObjectName("dimensionSpin");
    
    randomBtn = new QPushButton("🎲");
    randomBtn->setToolTip("Fill with random values");
    randomBtn->setFixedSize(30, 25);
    randomBtn->setObjectName("quickBtn");
    
    identityBtn = new QPushButton("I");
    identityBtn->setToolTip("Identity matrix");
    identityBtn->setFixedSize(30, 25);
    identityBtn->setObjectName("quickBtn");
    
    zeroBtn = new QPushButton("0");
    zeroBtn->setToolTip("Zero matrix");
    zeroBtn->setFixedSize(30, 25);
    zeroBtn->setObjectName("quickBtn");
    
    controlLayout->addWidget(rowLabel);
    controlLayout->addWidget(rowSpinBox);
    controlLayout->addSpacing(10);
    controlLayout->addWidget(colLabel);
    controlLayout->addWidget(colSpinBox);
    controlLayout->addStretch();
    controlLayout->addWidget(randomBtn);
    controlLayout->addWidget(identityBtn);
    controlLayout->addWidget(zeroBtn);
    
    // Table widget for matrix
    tableWidget = new QTableWidget(currentRows, currentCols);
    tableWidget->setObjectName("matrixTable");
    tableWidget->horizontalHeader()->setVisible(false);
    tableWidget->verticalHeader()->setVisible(false);
    tableWidget->horizontalHeader()->setSectionResizeMode(QHeaderView::Stretch);
    tableWidget->verticalHeader()->setSectionResizeMode(QHeaderView::Stretch);
    tableWidget->setMinimumHeight(200);
    tableWidget->setMaximumHeight(400);
    
    mainLayout->addLayout(controlLayout);
    mainLayout->addWidget(tableWidget);
    
    // Connections
    connect(rowSpinBox, QOverload<int>::of(&QSpinBox::valueChanged),
            this, &MatrixWidget::onRowsChanged);
    connect(colSpinBox, QOverload<int>::of(&QSpinBox::valueChanged),
            this, &MatrixWidget::onColsChanged);
    connect(tableWidget, &QTableWidget::cellChanged,
            this, &MatrixWidget::onCellChanged);
    connect(randomBtn, &QPushButton::clicked,
            this, &MatrixWidget::onRandomFill);
    connect(identityBtn, &QPushButton::clicked,
            this, &MatrixWidget::onIdentityFill);
    connect(zeroBtn, &QPushButton::clicked,
            this, &MatrixWidget::onZeroFill);
}

void MatrixWidget::updateTable()
{
    tableWidget->blockSignals(true);
    tableWidget->setRowCount(currentRows);
    tableWidget->setColumnCount(currentCols);
    
    for (int i = 0; i < currentRows; ++i) {
        for (int j = 0; j < currentCols; ++j) {
            QTableWidgetItem *item = tableWidget->item(i, j);
            if (!item) {
                item = new QTableWidgetItem("0.0");
                item->setTextAlignment(Qt::AlignCenter);
                tableWidget->setItem(i, j, item);
            }
        }
    }
    
    tableWidget->blockSignals(false);
}

void MatrixWidget::applyTheme()
{
    QString stylesheet = R"(
        #matrixTable {
            background-color: #0d1117;
            border: 2px solid #30363d;
            border-radius: 6px;
            gridline-color: #21262d;
            color: #58a6ff;
            font-size: 12px;
            font-family: 'Consolas', 'Courier New', monospace;
        }
        
        #matrixTable::item {
            padding: 5px;
            border: 1px solid #21262d;
        }
        
        #matrixTable::item:selected {
            background-color: #1f6feb;
            color: #ffffff;
        }
        
        #dimensionSpin {
            background-color: #0d1117;
            border: 1px solid #30363d;
            border-radius: 4px;
            color: #ffffff;
            padding: 3px;
        }
        
        #dimensionSpin::up-button, #dimensionSpin::down-button {
            background-color: #21262d;
            border: none;
        }
        
        #dimensionSpin::up-button:hover, #dimensionSpin::down-button:hover {
            background-color: #30363d;
        }
        
        #quickBtn {
            background-color: #21262d;
            border: 1px solid #30363d;
            border-radius: 4px;
            color: #ffffff;
            font-weight: bold;
        }
        
        #quickBtn:hover {
            background-color: #30363d;
            border-color: #58a6ff;
        }
        
        #quickBtn:pressed {
            background-color: #1f6feb;
        }
    )";
    
    setStyleSheet(stylesheet);
}

Matrix MatrixWidget::getMatrix() const
{
    Matrix matrix;
    matrix.rows = currentRows;
    matrix.cols = currentCols;
    matrix.data.resize(currentRows, std::vector<double>(currentCols, 0.0));
    
    for (int i = 0; i < currentRows; ++i) {
        for (int j = 0; j < currentCols; ++j) {
            QTableWidgetItem *item = tableWidget->item(i, j);
            if (item) {
                bool ok;
                double value = item->text().toDouble(&ok);
                matrix.data[i][j] = ok ? value : 0.0;
            }
        }
    }
    
    return matrix;
}

void MatrixWidget::setMatrix(const Matrix &matrix)
{
    if (matrix.rows != currentRows || matrix.cols != currentCols) {
        setDimensions(matrix.rows, matrix.cols);
    }
    
    tableWidget->blockSignals(true);
    for (int i = 0; i < matrix.rows; ++i) {
        for (int j = 0; j < matrix.cols; ++j) {
            QTableWidgetItem *item = tableWidget->item(i, j);
            if (!item) {
                item = new QTableWidgetItem();
                item->setTextAlignment(Qt::AlignCenter);
                tableWidget->setItem(i, j, item);
            }
            item->setText(QString::number(matrix.data[i][j], 'f', 3));
        }
    }
    tableWidget->blockSignals(false);
    
    emit matrixChanged();
}

void MatrixWidget::setDimensions(int rows, int cols)
{
    if (rows < 1 || cols < 1 || rows > 10 || cols > 10) return;
    
    currentRows = rows;
    currentCols = cols;
    
    rowSpinBox->blockSignals(true);
    colSpinBox->blockSignals(true);
    rowSpinBox->setValue(rows);
    colSpinBox->setValue(cols);
    rowSpinBox->blockSignals(false);
    colSpinBox->blockSignals(false);
    
    updateTable();
    emit dimensionsChanged(rows, cols);
    emit matrixChanged();
}

void MatrixWidget::setValue(int row, int col, double value)
{
    if (row < 0 || row >= currentRows || col < 0 || col >= currentCols) return;
    
    QTableWidgetItem *item = tableWidget->item(row, col);
    if (!item) {
        item = new QTableWidgetItem();
        item->setTextAlignment(Qt::AlignCenter);
        tableWidget->setItem(row, col, item);
    }
    
    tableWidget->blockSignals(true);
    item->setText(QString::number(value, 'f', 3));
    tableWidget->blockSignals(false);
}

double MatrixWidget::getValue(int row, int col) const
{
    if (row < 0 || row >= currentRows || col < 0 || col >= currentCols) return 0.0;
    
    QTableWidgetItem *item = tableWidget->item(row, col);
    if (!item) return 0.0;
    
    bool ok;
    double value = item->text().toDouble(&ok);
    return ok ? value : 0.0;
}

void MatrixWidget::clear()
{
    fillZero();
}

void MatrixWidget::fillRandom(double min, double max)
{
    static std::mt19937 gen(static_cast<unsigned int>(std::time(nullptr)));
    std::uniform_real_distribution<double> dist(min, max);
    
    tableWidget->blockSignals(true);
    for (int i = 0; i < currentRows; ++i) {
        for (int j = 0; j < currentCols; ++j) {
            double value = dist(gen);
            QTableWidgetItem *item = tableWidget->item(i, j);
            if (item) {
                item->setText(QString::number(value, 'f', 2));
            }
        }
    }
    tableWidget->blockSignals(false);
    
    emit matrixChanged();
}

void MatrixWidget::fillIdentity()
{
    tableWidget->blockSignals(true);
    for (int i = 0; i < currentRows; ++i) {
        for (int j = 0; j < currentCols; ++j) {
            QTableWidgetItem *item = tableWidget->item(i, j);
            if (item) {
                item->setText(i == j ? "1.0" : "0.0");
            }
        }
    }
    tableWidget->blockSignals(false);
    
    emit matrixChanged();
}

void MatrixWidget::fillZero()
{
    tableWidget->blockSignals(true);
    for (int i = 0; i < currentRows; ++i) {
        for (int j = 0; j < currentCols; ++j) {
            QTableWidgetItem *item = tableWidget->item(i, j);
            if (item) {
                item->setText("0.0");
            }
        }
    }
    tableWidget->blockSignals(false);
    
    emit matrixChanged();
}

void MatrixWidget::onRowsChanged(int rows)
{
    setDimensions(rows, currentCols);
}

void MatrixWidget::onColsChanged(int cols)
{
    setDimensions(currentRows, cols);
}

void MatrixWidget::onCellChanged(int row, int col)
{
    Q_UNUSED(row);
    Q_UNUSED(col);
    emit matrixChanged();
}

void MatrixWidget::onRandomFill()
{
    fillRandom(-10.0, 10.0);
}

void MatrixWidget::onIdentityFill()
{
    fillIdentity();
}

void MatrixWidget::onZeroFill()
{
    fillZero();
}
