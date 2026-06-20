#include "OperationPanel.h"
#include <QTimer>

OperationPanel::OperationPanel(QWidget *parent)
    : QWidget(parent)
{
    setupUI();
    applyTheme();
}

void OperationPanel::setupUI()
{
    mainLayout = new QVBoxLayout(this);
    mainLayout->setSpacing(12);
    mainLayout->setContentsMargins(10, 10, 10, 10);
    
    QLabel *titleLabel = new QLabel("⚡ OPERATIONS");
    titleLabel->setStyleSheet("font-size: 13px; font-weight: bold; color: #00d9ff; padding: 5px;");
    mainLayout->addWidget(titleLabel);
    
    // Basic Operations Group
    basicOpsGroup = new QGroupBox("Basic");
    basicOpsGroup->setObjectName("operationGroup");
    QVBoxLayout *basicLayout = new QVBoxLayout();
    basicLayout->setSpacing(6);
    
    createOperationButton("➕ Add", "Add", "A + B", basicLayout);
    createOperationButton("➖ Subtract", "Subtract", "A - B", basicLayout);
    createOperationButton("✖ Multiply", "Multiply", "A × B", basicLayout);
    createOperationButton("↻ Transpose", "Transpose", "A^T", basicLayout);
    
    basicOpsGroup->setLayout(basicLayout);
    mainLayout->addWidget(basicOpsGroup);
    
    // Advanced Operations Group
    advancedOpsGroup = new QGroupBox("Advanced");
    advancedOpsGroup->setObjectName("operationGroup");
    QVBoxLayout *advancedLayout = new QVBoxLayout();
    advancedLayout->setSpacing(6);
    
    createOperationButton("⁻¹ Inverse", "Inverse", "A^(-1)", advancedLayout);
    createOperationButton("📐 Determinant", "Determinant", "det(A)", advancedLayout);
    createOperationButton("🔢 Rank", "Rank", "rank(A)", advancedLayout);
    createOperationButton("➰ Trace", "Trace", "tr(A)", advancedLayout);
    
    advancedOpsGroup->setLayout(advancedLayout);
    mainLayout->addWidget(advancedOpsGroup);
    
    // Decomposition Group
    decompositionGroup = new QGroupBox("Decomposition");
    decompositionGroup->setObjectName("operationGroup");
    QVBoxLayout *decompLayout = new QVBoxLayout();
    decompLayout->setSpacing(6);
    
    createOperationButton("🔺 LU", "LU", "LU Decomposition", decompLayout);
    createOperationButton("🔷 QR", "QR", "QR Decomposition", decompLayout);
    createOperationButton("⚡ Eigenvalues", "Eigenvalues", "λ eigenvalues", decompLayout);
    
    decompositionGroup->setLayout(decompLayout);
    mainLayout->addWidget(decompositionGroup);
    
    // Properties Group
    propertiesGroup = new QGroupBox("Properties");
    propertiesGroup->setObjectName("operationGroup");
    QVBoxLayout *propsLayout = new QVBoxLayout();
    propsLayout->setSpacing(6);
    
    createOperationButton("📏 Norm", "Norm", "||A||", propsLayout);
    createOperationButton("🔍 Condition", "Condition", "κ(A)", propsLayout);
    
    propertiesGroup->setLayout(propsLayout);
    mainLayout->addWidget(propertiesGroup);
    
    mainLayout->addStretch();
    
    // Scroll area wrapper
    QScrollArea *scrollArea = new QScrollArea();
    scrollArea->setWidget(this);
    scrollArea->setWidgetResizable(true);
    scrollArea->setFrameShape(QFrame::NoFrame);
}

void OperationPanel::createOperationButton(const QString &text, const QString &operation,
                                           const QString &tooltip, QVBoxLayout *layout)
{
    QPushButton *btn = new QPushButton(text);
    btn->setObjectName("operationBtn");
    btn->setProperty("operation", operation);
    btn->setToolTip(tooltip);
    btn->setMinimumHeight(40);
    btn->setCursor(Qt::PointingHandCursor);
    
    connect(btn, &QPushButton::clicked, this, &OperationPanel::onOperationClicked);
    
    layout->addWidget(btn);
}

void OperationPanel::onOperationClicked()
{
    QPushButton *btn = qobject_cast<QPushButton*>(sender());
    if (btn) {
        QString operation = btn->property("operation").toString();
        emit operationRequested(operation);
        
        // Visual feedback
        btn->setStyleSheet(btn->styleSheet() + 
            "background-color: #1f6feb; border-color: #58a6ff;");
        QTimer::singleShot(200, [btn]() {
            btn->setStyleSheet("");
        });
    }
}

void OperationPanel::applyTheme()
{
    QString stylesheet = R"(
        QWidget {
            background-color: #1e1e1e;
        }
        
        #operationGroup {
            background-color: #0d1117;
            border: 2px solid #21262d;
            border-radius: 8px;
            margin-top: 12px;
            padding: 10px;
            font-weight: bold;
            color: #8b949e;
        }
        
        #operationGroup::title {
            subcontrol-origin: margin;
            subcontrol-position: top left;
            padding: 5px 10px;
            color: #58a6ff;
        }
        
        #operationBtn {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                       stop:0 #238636, stop:1 #1a6b28);
            border: 2px solid #2ea043;
            border-radius: 6px;
            color: #ffffff;
            font-size: 13px;
            font-weight: bold;
            padding: 8px;
            text-align: left;
        }
        
        #operationBtn:hover {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                       stop:0 #2ea043, stop:1 #238636);
            border-color: #3fb950;
        }
        
        #operationBtn:pressed {
            background-color: #1f6feb;
            border-color: #58a6ff;
        }
        
        QGroupBox {
            font-size: 11px;
        }
    )";
    
    setStyleSheet(stylesheet);
}
