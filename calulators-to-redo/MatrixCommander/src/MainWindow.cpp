#include "MainWindow.h"
#include <QMessageBox>
#include <QFileDialog>
#include <QTextStream>
#include <QFile>
#include <QShortcut>
#include <QTimer>
#include <QRegularExpression>
#include <QKeyEvent>

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , engine(new MatrixEngineAdapter())
    , isDragging(false)
{
    setWindowFlags(Qt::FramelessWindowHint | Qt::WindowStaysOnTopHint);
    setAttribute(Qt::WA_TranslucentBackground, false);
    setMinimumSize(1200, 800);
    resize(1400, 900);
    
    setupUI();
    setupConnections();
    applyMatlabTheme();
    updateStatusBar();
}

MainWindow::~MainWindow()
{
    delete engine;
}

void MainWindow::setupUI()
{
    QWidget *centralWidget = new QWidget(this);
    QVBoxLayout *mainLayout = new QVBoxLayout(centralWidget);
    mainLayout->setContentsMargins(0, 0, 0, 0);
    mainLayout->setSpacing(0);
    
    // Custom Title Bar
    titleBar = new QWidget();
    titleBar->setObjectName("titleBar");
    titleBar->setFixedHeight(40);
    QHBoxLayout *titleLayout = new QHBoxLayout(titleBar);
    titleLayout->setContentsMargins(15, 0, 5, 0);
    
    titleLabel = new QLabel("⚡ Matrix Commander");
    titleLabel->setStyleSheet("font-size: 16px; font-weight: bold; color: #00d9ff;");
    
    QWidget *spacer = new QWidget();
    spacer->setSizePolicy(QSizePolicy::Expanding, QSizePolicy::Preferred);
    
    minimizeBtn = new QPushButton("─");
    minimizeBtn->setObjectName("windowBtn");
    minimizeBtn->setFixedSize(40, 30);
    
    closeBtn = new QPushButton("✕");
    closeBtn->setObjectName("closeBtn");
    closeBtn->setFixedSize(40, 30);
    
    titleLayout->addWidget(titleLabel);
    titleLayout->addWidget(spacer);
    titleLayout->addWidget(minimizeBtn);
    titleLayout->addWidget(closeBtn);
    
    mainLayout->addWidget(titleBar);
    
    // Main Content Area
    QWidget *contentWidget = new QWidget();
    QHBoxLayout *contentLayout = new QHBoxLayout(contentWidget);
    contentLayout->setContentsMargins(15, 15, 15, 15);
    contentLayout->setSpacing(15);
    
    // Left Panel - Matrix Inputs
    QWidget *leftPanel = new QWidget();
    QVBoxLayout *leftLayout = new QVBoxLayout(leftPanel);
    leftLayout->setSpacing(15);
    
    matrix1Label = new QLabel("Matrix A");
    matrix1Label->setStyleSheet("font-size: 14px; font-weight: bold; color: #ffffff;");
    matrix1Widget = new MatrixWidget(3, 3);
    
    QWidget *separator1 = new QWidget();
    separator1->setFixedHeight(2);
    separator1->setStyleSheet("background-color: #2a2a2a;");
    
    matrix2Label = new QLabel("Matrix B");
    matrix2Label->setStyleSheet("font-size: 14px; font-weight: bold; color: #ffffff;");
    matrix2Widget = new MatrixWidget(3, 3);
    
    leftLayout->addWidget(matrix1Label);
    leftLayout->addWidget(matrix1Widget);
    leftLayout->addWidget(separator1);
    leftLayout->addWidget(matrix2Label);
    leftLayout->addWidget(matrix2Widget);
    
    // Middle Panel - Operations
    operationPanel = new OperationPanel();
    
    // Right Panel - Results
    QWidget *rightPanel = new QWidget();
    QVBoxLayout *rightLayout = new QVBoxLayout(rightPanel);
    rightLayout->setSpacing(10);
    
    resultsLabel = new QLabel("Results");
    resultsLabel->setStyleSheet("font-size: 14px; font-weight: bold; color: #ffffff;");
    
    resultsDisplay = new QTextEdit();
    resultsDisplay->setReadOnly(true);
    resultsDisplay->setObjectName("resultsDisplay");
    resultsDisplay->setFont(QFont("Consolas", 10));
    
    QHBoxLayout *buttonLayout = new QHBoxLayout();
    exportBtn = new QPushButton("📋 Export");
    exportBtn->setObjectName("actionBtn");
    exportBtn->setMinimumHeight(35);
    
    clearBtn = new QPushButton("🗑 Clear All");
    clearBtn->setObjectName("actionBtn");
    clearBtn->setMinimumHeight(35);
    
    buttonLayout->addWidget(exportBtn);
    buttonLayout->addWidget(clearBtn);
    
    rightLayout->addWidget(resultsLabel);
    rightLayout->addWidget(resultsDisplay);
    rightLayout->addLayout(buttonLayout);
    
    // Add panels to content
    contentLayout->addWidget(leftPanel, 2);
    contentLayout->addWidget(operationPanel, 1);
    contentLayout->addWidget(rightPanel, 2);
    
    mainLayout->addWidget(contentWidget);
    
    // Status Bar
    QStatusBar *status = statusBar();
    status->setStyleSheet("background-color: #1a1a1a; color: #aaaaaa; border-top: 1px solid #2a2a2a;");
    status->showMessage("Ready | Matrix Commander v1.0");
    
    setCentralWidget(centralWidget);
    
    // Keyboard Shortcuts
    new QShortcut(QKeySequence("Ctrl+C"), this, SLOT(copyToClipboard()));
    new QShortcut(QKeySequence("Ctrl+V"), this, SLOT(pasteFromClipboard()));
    new QShortcut(QKeySequence("Ctrl+Q"), this, SLOT(close()));
    new QShortcut(QKeySequence("Esc"), this, SLOT(clearAll()));
}

void MainWindow::setupConnections()
{
    connect(operationPanel, &OperationPanel::operationRequested, 
            this, &MainWindow::onMatrixOperation);
    connect(matrix1Widget, &MatrixWidget::matrixChanged, 
            this, &MainWindow::onMatrixChanged);
    connect(matrix2Widget, &MatrixWidget::matrixChanged, 
            this, &MainWindow::onMatrix2Changed);
    connect(exportBtn, &QPushButton::clicked, 
            this, &MainWindow::exportResults);
    connect(clearBtn, &QPushButton::clicked, 
            this, &MainWindow::clearAll);
    connect(minimizeBtn, &QPushButton::clicked, 
            this, &MainWindow::minimizeWindow);
    connect(closeBtn, &QPushButton::clicked, 
            this, &MainWindow::closeWindow);
}

void MainWindow::applyMatlabTheme()
{
    QString stylesheet = R"(
        QMainWindow {
            background-color: #1e1e1e;
        }
        
        #titleBar {
            background-color: #0a0a0a;
            border-bottom: 2px solid #00d9ff;
        }
        
        #windowBtn {
            background-color: #2a2a2a;
            border: none;
            border-radius: 3px;
            color: #ffffff;
            font-size: 18px;
            font-weight: bold;
        }
        
        #windowBtn:hover {
            background-color: #3a3a3a;
        }
        
        #closeBtn {
            background-color: #2a2a2a;
            border: none;
            border-radius: 3px;
            color: #ffffff;
            font-size: 16px;
            font-weight: bold;
        }
        
        #closeBtn:hover {
            background-color: #e63946;
        }
        
        QWidget {
            background-color: #1e1e1e;
            color: #ffffff;
        }
        
        #resultsDisplay {
            background-color: #0d1117;
            border: 2px solid #30363d;
            border-radius: 6px;
            color: #00ff88;
            padding: 10px;
            font-family: 'Consolas', 'Courier New', monospace;
        }
        
        #actionBtn {
            background-color: #238636;
            border: none;
            border-radius: 6px;
            color: #ffffff;
            font-size: 13px;
            font-weight: bold;
            padding: 8px 16px;
        }
        
        #actionBtn:hover {
            background-color: #2ea043;
        }
        
        #actionBtn:pressed {
            background-color: #1a6b28;
        }
        
        QStatusBar {
            background-color: #0a0a0a;
            color: #8b949e;
            font-size: 11px;
        }
    )";
    
    setStyleSheet(stylesheet);
}

void MainWindow::updateStatusBar()
{
    Matrix m1 = getCurrentMatrix();
    Matrix m2 = getSecondMatrix();
    QString status = QString("Matrix A: %1×%2 | Matrix B: %3×%4 | %5")
                        .arg(m1.rows).arg(m1.cols)
                        .arg(m2.rows).arg(m2.cols)
                        .arg(lastOperation.isEmpty() ? "Ready" : lastOperation);
    statusBar()->showMessage(status);
}

void MainWindow::onMatrixOperation(const QString &operation)
{
    try {
        Matrix m1 = getCurrentMatrix();
        Matrix m2 = getSecondMatrix();
        Matrix result;
        QString resultText;
        
        lastOperation = operation;
        
        if (operation == "Add") {
            result = engine->add(m1, m2);
            displayResult(result, "A + B");
        }
        else if (operation == "Subtract") {
            result = engine->subtract(m1, m2);
            displayResult(result, "A - B");
        }
        else if (operation == "Multiply") {
            result = engine->multiply(m1, m2);
            displayResult(result, "A × B");
        }
        else if (operation == "Transpose") {
            result = engine->transpose(m1);
            displayResult(result, "A^T");
        }
        else if (operation == "Inverse") {
            result = engine->inverse(m1);
            displayResult(result, "A^(-1)");
        }
        else if (operation == "Determinant") {
            double det = engine->determinant(m1);
            resultText = QString("╔════════════════════════════╗\n");
            resultText += QString("║   Determinant of A         ║\n");
            resultText += QString("╠════════════════════════════╣\n");
            resultText += QString("║   det(A) = %-15.6f ║\n").arg(det);
            resultText += QString("╚════════════════════════════╝\n");
            resultsDisplay->setPlainText(resultText);
            lastResult = Matrix(); // No matrix result
        }
        else if (operation == "Eigenvalues") {
            auto eigenvalues = engine->eigenvalues(m1);
            resultText = QString("╔════════════════════════════╗\n");
            resultText += QString("║   Eigenvalues of A         ║\n");
            resultText += QString("╠════════════════════════════╣\n");
            for (size_t i = 0; i < eigenvalues.size(); ++i) {
                resultText += QString("║   λ%1 = %-18.6f ║\n").arg(i+1).arg(eigenvalues[i]);
            }
            resultText += QString("╚════════════════════════════╝\n");
            resultsDisplay->setPlainText(resultText);
            lastResult = Matrix();
        }
        else if (operation == "Rank") {
            int rank = engine->rank(m1);
            resultText = QString("╔════════════════════════════╗\n");
            resultText += QString("║   Rank of A                ║\n");
            resultText += QString("╠════════════════════════════╣\n");
            resultText += QString("║   rank(A) = %-14d ║\n").arg(rank);
            resultText += QString("╚════════════════════════════╝\n");
            resultsDisplay->setPlainText(resultText);
            lastResult = Matrix();
        }
        else if (operation == "Trace") {
            double trace = engine->trace(m1);
            resultText = QString("╔════════════════════════════╗\n");
            resultText += QString("║   Trace of A               ║\n");
            resultText += QString("╠════════════════════════════╣\n");
            resultText += QString("║   tr(A) = %-16.6f ║\n").arg(trace);
            resultText += QString("╚════════════════════════════╝\n");
            resultsDisplay->setPlainText(resultText);
            lastResult = Matrix();
        }
        else if (operation == "LU") {
            auto [L, U] = engine->luDecomposition(m1);
            QString luText = "╔══════════════════════════════════════╗\n";
            luText += "║   LU Decomposition of A              ║\n";
            luText += "╠══════════════════════════════════════╣\n";
            luText += "║   Lower Triangle (L):                ║\n";
            luText += formatMatrix(L);
            luText += "║   Upper Triangle (U):                ║\n";
            luText += formatMatrix(U);
            luText += "╚══════════════════════════════════════╝\n";
            resultsDisplay->setPlainText(luText);
            lastResult = L; // Store L for export
        }
        else if (operation == "QR") {
            auto [Q, R] = engine->qrDecomposition(m1);
            QString qrText = "╔══════════════════════════════════════╗\n";
            qrText += "║   QR Decomposition of A              ║\n";
            qrText += "╠══════════════════════════════════════╣\n";
            qrText += "║   Orthogonal Matrix (Q):             ║\n";
            qrText += formatMatrix(Q);
            qrText += "║   Upper Triangular (R):              ║\n";
            qrText += formatMatrix(R);
            qrText += "╚══════════════════════════════════════╝\n";
            resultsDisplay->setPlainText(qrText);
            lastResult = Q; // Store Q for export
        }
        
        updateStatusBar();
        
    } catch (const std::exception &e) {
        displayError(e.what());
    }
}

void MainWindow::displayResult(const Matrix &result, const QString &operationName)
{
    lastResult = result;
    QString text = QString("╔══════════════════════════════════════╗\n");
    text += QString("║   Result: %-26s ║\n").arg(operationName);
    text += QString("╠══════════════════════════════════════╣\n");
    text += QString("║   Dimensions: %1×%2%-19s║\n")
                .arg(result.rows).arg(result.cols).arg("");
    text += QString("╠══════════════════════════════════════╣\n");
    
    for (int i = 0; i < result.rows; ++i) {
        QString row = "║   ";
        for (int j = 0; j < result.cols; ++j) {
            row += QString("%1 ").arg(result.data[i][j], 8, 'f', 3);
        }
        // Pad to align
        while (row.length() < 39) row += " ";
        row += "║\n";
        text += row;
    }
    
    text += QString("╚══════════════════════════════════════╝\n");
    resultsDisplay->setPlainText(text);
}

void MainWindow::displayError(const QString &error)
{
    QString errorText = QString("╔══════════════════════════════════════╗\n");
    errorText += QString("║   ⚠ ERROR                            ║\n");
    errorText += QString("╠══════════════════════════════════════╣\n");
    errorText += QString("║   %1%-32s║\n").arg(error.left(32)).arg("");
    errorText += QString("╚══════════════════════════════════════╝\n");
    resultsDisplay->setPlainText(errorText);
    statusBar()->showMessage("Error: " + error);
}

Matrix MainWindow::getCurrentMatrix()
{
    return matrix1Widget->getMatrix();
}

Matrix MainWindow::getSecondMatrix()
{
    return matrix2Widget->getMatrix();
}

void MainWindow::onMatrixChanged()
{
    updateStatusBar();
}

void MainWindow::onMatrix2Changed()
{
    updateStatusBar();
}

void MainWindow::exportResults()
{
    QString fileName = QFileDialog::getSaveFileName(this,
        "Export Results", "", "CSV Files (*.csv);;Text Files (*.txt);;All Files (*)");
    
    if (fileName.isEmpty()) return;
    
    QFile file(fileName);
    if (!file.open(QIODevice::WriteOnly | QIODevice::Text)) {
        QMessageBox::warning(this, "Export Error", "Could not open file for writing.");
        return;
    }
    
    QTextStream out(&file);
    
    if (lastResult.rows > 0 && lastResult.cols > 0) {
        for (int i = 0; i < lastResult.rows; ++i) {
            for (int j = 0; j < lastResult.cols; ++j) {
                out << lastResult.data[i][j];
                if (j < lastResult.cols - 1) out << ",";
            }
            out << "\n";
        }
    } else {
        out << resultsDisplay->toPlainText();
    }
    
    file.close();
    statusBar()->showMessage("Results exported to " + fileName, 3000);
}

void MainWindow::copyToClipboard()
{
    QClipboard *clipboard = QApplication::clipboard();
    clipboard->setText(resultsDisplay->toPlainText());
    statusBar()->showMessage("Results copied to clipboard", 2000);
}

void MainWindow::pasteFromClipboard()
{
    QClipboard *clipboard = QApplication::clipboard();
    QString text = clipboard->text();
    
    // Try to parse clipboard as matrix data
    // Simple CSV parsing
    QStringList rows = text.split('\n', Qt::SkipEmptyParts);
    if (rows.isEmpty()) return;
    
    QStringList firstRow = rows[0].split(QRegularExpression("[,\\s\\t]+"), Qt::SkipEmptyParts);
    int cols = firstRow.size();
    int rowCount = rows.size();
    
    matrix1Widget->setDimensions(rowCount, cols);
    
    for (int i = 0; i < rowCount && i < rows.size(); ++i) {
        QStringList values = rows[i].split(QRegularExpression("[,\\s\\t]+"), Qt::SkipEmptyParts);
        for (int j = 0; j < cols && j < values.size(); ++j) {
            bool ok;
            double val = values[j].toDouble(&ok);
            if (ok) {
                matrix1Widget->setValue(i, j, val);
            }
        }
    }
    
    statusBar()->showMessage("Matrix pasted from clipboard", 2000);
}

void MainWindow::clearAll()
{
    matrix1Widget->clear();
    matrix2Widget->clear();
    resultsDisplay->clear();
    lastOperation.clear();
    lastResult = Matrix();
    updateStatusBar();
}

void MainWindow::minimizeWindow()
{
    showMinimized();
}

void MainWindow::closeWindow()
{
    close();
}

void MainWindow::mousePressEvent(QMouseEvent *event)
{
    if (event->button() == Qt::LeftButton) {
        QWidget *widget = childAt(event->pos());
        if (widget && (widget == titleBar || widget->parent() == titleBar)) {
            isDragging = true;
            dragPosition = event->globalPos() - frameGeometry().topLeft();
            event->accept();
        }
    }
}

void MainWindow::mouseMoveEvent(QMouseEvent *event)
{
    if (isDragging && (event->buttons() & Qt::LeftButton)) {
        move(event->globalPos() - dragPosition);
        event->accept();
    }
}

void MainWindow::mouseReleaseEvent(QMouseEvent *event)
{
    if (event->button() == Qt::LeftButton) {
        isDragging = false;
    }
}

void MainWindow::keyPressEvent(QKeyEvent *event)
{
    QMainWindow::keyPressEvent(event);
}
