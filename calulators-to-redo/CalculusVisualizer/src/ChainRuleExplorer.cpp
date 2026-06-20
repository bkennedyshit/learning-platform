/**
 * ChainRuleExplorer.cpp - Implementation of chain rule visualization
 */

#include "ChainRuleExplorer.h"
#include "DerivativeEngine.h"
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QGroupBox>
#include <QSplitter>
#include <QComboBox>
#include <QHeaderView>
#include <QRegularExpression>

ChainRuleExplorer::ChainRuleExplorer(QWidget *parent)
    : QWidget(parent)
{
    setupUI();
    setupConnections();
}

ChainRuleExplorer::~ChainRuleExplorer()
{
}

void ChainRuleExplorer::setupUI()
{
    auto *mainLayout = new QVBoxLayout(this);
    
    // Top section - Input and examples
    auto *inputGroup = new QGroupBox("Composite Function Input");
    auto *inputLayout = new QVBoxLayout(inputGroup);
    
    auto *inputRow = new QHBoxLayout();
    expressionInput = new QLineEdit();
    expressionInput->setPlaceholderText("Enter composite function (e.g., sin(x^2), exp(3*x + 1))");
    
    computeBtn = new QPushButton("Analyze Chain Rule");
    clearBtn = new QPushButton("Clear");
    
    inputRow->addWidget(new QLabel("f(x) ="));
    inputRow->addWidget(expressionInput, 1);
    inputRow->addWidget(computeBtn);
    inputRow->addWidget(clearBtn);
    
    // Examples dropdown
    auto *examplesRow = new QHBoxLayout();
    examplesComboBox = new QComboBox();
    examplesComboBox->addItem("-- Select Example --", "");
    addExample("Simple: sin(2x)", "sin(2*x)");
    addExample("Polynomial: (x² + 1)³", "(x^2 + 1)^3");
    addExample("Exponential: e^(x²)", "exp(x^2)");
    addExample("Nested: sin(cos(x))", "sin(cos(x))");
    addExample("Complex: √(1 + x²)", "sqrt(1 + x^2)");
    addExample("Neural Net: σ(wx + b)", "1/(1 + exp(-(3*x + 2)))");
    
    examplesRow->addWidget(new QLabel("Examples:"));
    examplesRow->addWidget(examplesComboBox, 1);
    examplesRow->addStretch();
    
    inputLayout->addLayout(inputRow);
    inputLayout->addLayout(examplesRow);
    
    // Middle section - Decomposition
    auto *splitter = new QSplitter(Qt::Horizontal);
    
    // Left: Tree decomposition
    auto *treeGroup = new QGroupBox("Function Decomposition");
    auto *treeLayout = new QVBoxLayout(treeGroup);
    
    decompositionTree = new QTreeWidget();
    decompositionTree->setHeaderLabels({"Component", "Expression", "Derivative"});
    decompositionTree->header()->setSectionResizeMode(QHeaderView::ResizeToContents);
    
    outerFunctionLabel = new QLabel("<b>Outer:</b> f(u) = ?");
    innerFunctionLabel = new QLabel("<b>Inner:</b> u = g(x) = ?");
    resultLabel = new QLabel("<b>Result:</b> f'(x) = ?");
    
    treeLayout->addWidget(decompositionTree, 1);
    treeLayout->addWidget(outerFunctionLabel);
    treeLayout->addWidget(innerFunctionLabel);
    treeLayout->addWidget(resultLabel);
    
    // Right: Step-by-step explanation
    auto *stepsGroup = new QGroupBox("Chain Rule Steps");
    auto *stepsLayout = new QVBoxLayout(stepsGroup);
    
    stepsOutput = new QTextEdit();
    stepsOutput->setReadOnly(true);
    stepsOutput->setPlaceholderText("Step-by-step chain rule application will appear here...");
    
    stepsLayout->addWidget(stepsOutput);
    
    splitter->addWidget(treeGroup);
    splitter->addWidget(stepsGroup);
    splitter->setStretchFactor(0, 1);
    splitter->setStretchFactor(1, 1);
    
    // Bottom section - Backpropagation connection
    auto *backpropGroup = new QGroupBox("Connection to Backpropagation");
    auto *backpropLayout = new QVBoxLayout(backpropGroup);
    
    backpropExplanation = new QTextEdit();
    backpropExplanation->setReadOnly(true);
    backpropExplanation->setMaximumHeight(150);
    backpropExplanation->setHtml(
        "<h4>Why Chain Rule Matters for Neural Networks:</h4>"
        "<p>In backpropagation, we compute gradients by repeatedly applying the chain rule:</p>"
        "<ul>"
        "<li><b>Forward pass:</b> Compose functions layer by layer: f(g(h(x)))</li>"
        "<li><b>Backward pass:</b> Compute ∂L/∂x = (∂L/∂f)(∂f/∂g)(∂g/∂h)(∂h/∂x)</li>"
        "<li><b>Each layer:</b> Applies chain rule to propagate gradients backward</li>"
        "</ul>"
        "<p style='color: #4a9eff;'><b>Understanding this visualization helps you understand how "
        "neural networks learn!</b></p>"
    );
    
    backpropLayout->addWidget(backpropExplanation);
    
    // Assemble main layout
    mainLayout->addWidget(inputGroup);
    mainLayout->addWidget(splitter, 1);
    mainLayout->addWidget(backpropGroup);
}

void ChainRuleExplorer::setupConnections()
{
    connect(computeBtn, &QPushButton::clicked, this, &ChainRuleExplorer::onComputeChainRule);
    connect(clearBtn, &QPushButton::clicked, this, &ChainRuleExplorer::onClearAll);
    connect(expressionInput, &QLineEdit::returnPressed, this, &ChainRuleExplorer::onComputeChainRule);
    connect(examplesComboBox, QOverload<int>::of(&QComboBox::currentIndexChanged),
            this, &ChainRuleExplorer::onExampleSelected);
}

void ChainRuleExplorer::addExample(const QString &name, const QString &expression)
{
    examplesComboBox->addItem(name, expression);
}

void ChainRuleExplorer::onComputeChainRule()
{
    QString expression = expressionInput->text().trimmed();
    if (expression.isEmpty()) {
        return;
    }
    
    analyzeComposition(expression);
    displayChainRuleSteps(expression);
}

void ChainRuleExplorer::onExampleSelected(int index)
{
    if (index <= 0) return;
    
    QString expression = examplesComboBox->itemData(index).toString();
    expressionInput->setText(expression);
    onComputeChainRule();
}

void ChainRuleExplorer::onClearAll()
{
    expressionInput->clear();
    decompositionTree->clear();
    stepsOutput->clear();
    outerFunctionLabel->setText("<b>Outer:</b> f(u) = ?");
    innerFunctionLabel->setText("<b>Inner:</b> u = g(x) = ?");
    resultLabel->setText("<b>Result:</b> f'(x) = ?");
    examplesComboBox->setCurrentIndex(0);
}

void ChainRuleExplorer::analyzeComposition(const QString &expression)
{
    decompositionTree->clear();
    components.clear();
    
    // Simple pattern matching for common compositions
    QString outer = extractOuterFunction(expression);
    QString inner = extractInnerFunction(expression);
    
    // Create tree structure
    QTreeWidgetItem *rootItem = new QTreeWidgetItem(decompositionTree);
    rootItem->setText(0, "Composite Function");
    rootItem->setText(1, expression);
    rootItem->setText(2, "f'(g(x)) · g'(x)");
    rootItem->setExpanded(true);
    
    QTreeWidgetItem *outerItem = new QTreeWidgetItem(rootItem);
    outerItem->setText(0, "Outer Function f(u)");
    outerItem->setText(1, outer);
    
    DerivativeEngine engine;
    QString outerDerivative = "f'(u)";
    outerItem->setText(2, outerDerivative);
    
    QTreeWidgetItem *innerItem = new QTreeWidgetItem(rootItem);
    innerItem->setText(0, "Inner Function u = g(x)");
    innerItem->setText(1, inner);
    
    QString innerDerivative = engine.computeDerivative(inner, "x");
    innerItem->setText(2, "g'(x) = " + innerDerivative);
    
    // Update labels
    outerFunctionLabel->setText("<b>Outer:</b> f(u) = " + outer);
    innerFunctionLabel->setText("<b>Inner:</b> u = " + inner);
    
    QString fullDerivative = engine.computeDerivative(expression, "x");
    resultLabel->setText("<b>Result:</b> f'(x) = " + fullDerivative);
}

void ChainRuleExplorer::displayChainRuleSteps(const QString &expression)
{
    DerivativeEngine engine;
    
    QString html = "<div style='font-family: Consolas, monospace;'>";
    html += "<h3>Chain Rule Breakdown for: " + expression + "</h3>";
    
    html += "<div style='background-color: #2a2a2a; padding: 15px; margin: 10px 0; "
            "border-left: 4px solid #2c5aa0;'>";
    html += "<h4>Step 1: Identify the composition</h4>";
    html += "<p>We have a composite function where:</p>";
    html += "<ul>";
    html += "<li><b>Outer function:</b> f(u)</li>";
    html += "<li><b>Inner function:</b> u = g(x)</li>";
    html += "</ul>";
    html += "</div>";
    
    html += "<div style='background-color: #2a2a2a; padding: 15px; margin: 10px 0; "
            "border-left: 4px solid #4a9eff;'>";
    html += "<h4>Step 2: Apply the Chain Rule</h4>";
    html += "<p>The chain rule states:</p>";
    html += "<p style='text-align: center; font-size: 16px; color: #4a9eff;'>";
    html += "<b>d/dx[f(g(x))] = f'(g(x)) · g'(x)</b>";
    html += "</p>";
    html += "</div>";
    
    html += "<div style='background-color: #2a2a2a; padding: 15px; margin: 10px 0; "
            "border-left: 4px solid #00aa00;'>";
    html += "<h4>Step 3: Compute derivatives</h4>";
    
    QString outer = extractOuterFunction(expression);
    QString inner = extractInnerFunction(expression);
    
    html += "<ol>";
    html += "<li><b>Outer derivative:</b> d/du[" + outer + "]</li>";
    html += "<li><b>Inner derivative:</b> d/dx[" + inner + "]</li>";
    html += "<li><b>Multiply them together</b></li>";
    html += "</ol>";
    html += "</div>";
    
    html += "<div style='background-color: #2a2a2a; padding: 15px; margin: 10px 0; "
            "border-left: 4px solid #ff9900;'>";
    html += "<h4>Backpropagation Analogy</h4>";
    html += "<p>In a neural network:</p>";
    html += "<ul>";
    html += "<li><code>x</code> = layer input</li>";
    html += "<li><code>g(x)</code> = weighted sum (z = wx + b)</li>";
    html += "<li><code>f(u)</code> = activation function (σ(z))</li>";
    html += "<li><b>Backprop:</b> ∂Loss/∂x = (∂Loss/∂f)(∂f/∂g)(∂g/∂x)</li>";
    html += "</ul>";
    html += "</div>";
    
    // Add actual derivative steps
    QString fullSteps = engine.getChainRuleBreakdown(expression);
    html += fullSteps;
    
    html += "</div>";
    
    stepsOutput->setHtml(html);
}

QString ChainRuleExplorer::extractOuterFunction(const QString &expr)
{
    // Simple pattern detection - in real implementation, use proper parsing
    QRegularExpression re(R"(^(\w+)\((.+)\)$)");
    QRegularExpressionMatch match = re.match(expr.trimmed());
    
    if (match.hasMatch()) {
        QString func = match.captured(1);
        return func + "(u)";
    }
    
    // For power expressions like (...)^n
    QRegularExpression powerRe(R"(\((.+)\)\^(\d+))");
    QRegularExpressionMatch powerMatch = powerRe.match(expr);
    if (powerMatch.hasMatch()) {
        return "u^" + powerMatch.captured(2);
    }
    
    return "f(u)";
}

QString ChainRuleExplorer::extractInnerFunction(const QString &expr)
{
    // Extract inner part
    QRegularExpression re(R"(^\w+\((.+)\)$)");
    QRegularExpressionMatch match = re.match(expr.trimmed());
    
    if (match.hasMatch()) {
        return match.captured(1);
    }
    
    // For power expressions
    QRegularExpression powerRe(R"(\((.+)\)\^(\d+))");
    QRegularExpressionMatch powerMatch = powerRe.match(expr);
    if (powerMatch.hasMatch()) {
        return powerMatch.captured(1);
    }
    
    return "g(x)";
}
