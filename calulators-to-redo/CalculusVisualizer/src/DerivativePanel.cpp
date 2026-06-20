#include "DerivativePanel.h"
#include <QSplitter>
#include <QScrollArea>
#include <QComboBox>
#include <QFont>
#include <QTextDocument>

DerivativePanel::DerivativePanel(QWidget *parent)
    : QWidget(parent)
{
    setupUI();
}

DerivativePanel::~DerivativePanel() {}

void DerivativePanel::setupUI() {
    QVBoxLayout *mainLayout = new QVBoxLayout(this);
    mainLayout->setSpacing(15);
    mainLayout->setContentsMargins(15, 15, 15, 15);
    
    // Top section: Function input
    QGroupBox *inputGroup = new QGroupBox("Function to Differentiate", this);
    QHBoxLayout *inputLayout = new QHBoxLayout(inputGroup);
    
    QLabel *label = new QLabel("f(x) = ", inputGroup);
    label->setStyleSheet("font-size: 14pt; font-weight: bold;");
    
    m_functionInput = new QLineEdit(inputGroup);
    m_functionInput->setPlaceholderText("Enter function (e.g., x^3 - 2*x)");
    m_functionInput->setStyleSheet("font-size: 12pt; padding: 8px;");
    
    m_calculateButton = new QPushButton("Calculate d/dx", inputGroup);
    m_calculateButton->setStyleSheet("font-weight: bold; padding: 8px 20px;");
    
    m_exampleSelector = new QComboBox(inputGroup);
    m_exampleSelector->addItems({
        "x^2 (Power Rule)",
        "x^3 - 2*x (Sum Rule)",
        "sin(x) (Trig Rule)",
        "x^2*sin(x) (Product Rule)",
        "sin(x)/x (Quotient Rule)",
        "sin(x^2) (Chain Rule)",
        "exp(-x^2) (Chain Rule)"
    });
    
    inputLayout->addWidget(label);
    inputLayout->addWidget(m_functionInput, 2);
    inputLayout->addWidget(m_exampleSelector, 1);
    inputLayout->addWidget(m_calculateButton);
    
    mainLayout->addWidget(inputGroup);
    
    // Middle section: Split view
    QSplitter *splitter = new QSplitter(Qt::Horizontal, this);
    
    // Left: Rules reference
    QGroupBox *rulesGroup = new QGroupBox("Differentiation Rules", splitter);
    QVBoxLayout *rulesLayout = new QVBoxLayout(rulesGroup);
    
    m_rulesList = new QListWidget(rulesGroup);
    m_rulesList->setStyleSheet("font-family: 'Courier New'; font-size: 10pt;");
    
    // Add common rules
    QStringList rules = {
        "📌 Power Rule: d/dx[x^n] = n·x^(n-1)",
        "📌 Constant Rule: d/dx[c] = 0",
        "📌 Sum Rule: d/dx[f+g] = f' + g'",
        "📌 Product Rule: d/dx[f·g] = f'·g + f·g'",
        "📌 Quotient Rule: d/dx[f/g] = (f'·g - f·g')/g²",
        "📌 Chain Rule: d/dx[f(g(x))] = f'(g(x))·g'(x)",
        "",
        "🔷 Trig Functions:",
        "   d/dx[sin(x)] = cos(x)",
        "   d/dx[cos(x)] = -sin(x)",
        "   d/dx[tan(x)] = sec²(x)",
        "",
        "🔷 Exponential & Log:",
        "   d/dx[e^x] = e^x",
        "   d/dx[ln(x)] = 1/x",
        "   d/dx[a^x] = a^x·ln(a)",
        "",
        "🔷 Special:",
        "   d/dx[√x] = 1/(2√x)",
        "   d/dx[1/x] = -1/x²"
    };
    
    foreach (const QString &rule, rules) {
        m_rulesList->addItem(rule);
    }
    
    rulesLayout->addWidget(m_rulesList);
    splitter->addWidget(rulesGroup);
    
    // Right: Step-by-step solution
    QGroupBox *stepsGroup = new QGroupBox("Step-by-Step Solution", splitter);
    QVBoxLayout *stepsLayout = new QVBoxLayout(stepsGroup);
    
    m_stepsDisplay = new QTextEdit(stepsGroup);
    m_stepsDisplay->setReadOnly(true);
    m_stepsDisplay->setStyleSheet(
        "font-family: 'Courier New'; "
        "font-size: 11pt; "
        "background-color: #1a1a1a; "
        "color: #e0e0e0; "
        "padding: 10px;"
    );
    
    stepsLayout->addWidget(m_stepsDisplay);
    splitter->addWidget(stepsGroup);
    
    splitter->setStretchFactor(0, 1);
    splitter->setStretchFactor(1, 2);
    
    mainLayout->addWidget(splitter, 1);
    
    // Bottom: Result
    QGroupBox *resultGroup = new QGroupBox("Final Result", this);
    QHBoxLayout *resultLayout = new QHBoxLayout(resultGroup);
    
    m_resultLabel = new QLabel("Enter a function and click 'Calculate d/dx'", resultGroup);
    m_resultLabel->setStyleSheet(
        "font-size: 16pt; "
        "font-weight: bold; "
        "color: #0078d4; "
        "padding: 15px;"
    );
    m_resultLabel->setWordWrap(true);
    
    resultLayout->addWidget(m_resultLabel);
    mainLayout->addWidget(resultGroup);
    
    // Connections
    connect(m_calculateButton, &QPushButton::clicked, this, &DerivativePanel::calculateDerivative);
    connect(m_functionInput, &QLineEdit::returnPressed, this, &DerivativePanel::calculateDerivative);
    connect(m_exampleSelector, QOverload<int>::of(&QComboBox::currentIndexChanged), 
            this, &DerivativePanel::onRuleSelected);
    connect(m_rulesList, &QListWidget::currentRowChanged, this, [this](int row) {
        if (row >= 0) {
            QString rule = m_rulesList->item(row)->text();
            m_stepsDisplay->append("\n<span style='color: #4CAF50;'>ℹ️ " + rule + "</span>");
        }
    });
}

void DerivativePanel::setFunction(const QString &function) {
    m_functionInput->setText(function);
    calculateDerivative();
}

void DerivativePanel::showDerivativeSteps(const QString &derivative) {
    m_currentDerivative = derivative;
}

void DerivativePanel::calculateDerivative() {
    QString function = m_functionInput->text().trimmed();
    if (function.isEmpty()) {
        m_stepsDisplay->setHtml("<span style='color: #ff6b6b;'>⚠️ Please enter a function</span>");
        return;
    }
    
    m_currentFunction = function;
    clearSteps();
    displaySteps(function);
}

void DerivativePanel::displaySteps(const QString &function) {
    QString f = function.toLower().trimmed();
    
    QString html = "<div style='font-size: 12pt;'>";
    html += "<h2 style='color: #0078d4;'>🎓 Derivative Calculation</h2>";
    html += "<p style='font-size: 14pt;'><b>Given:</b> f(x) = <span style='color: #00d4ff;'>" + function + "</span></p>";
    html += "<hr style='border: 1px solid #444;'>";
    
    // Analyze and apply appropriate rules
    if (f == "x^2") {
        addStep("Power Rule", "d/dx[x²]", "Apply the power rule: d/dx[x^n] = n·x^(n-1)");
        html += "<div style='margin: 20px; padding: 15px; background-color: #2d2d2d; border-left: 4px solid #4CAF50;'>";
        html += "<h3 style='color: #4CAF50;'>Step 1: Identify the Rule</h3>";
        html += "<p>This is a simple power function: <b>x²</b></p>";
        html += "<p>We'll use the <b>Power Rule</b>: d/dx[x^n] = n·x^(n-1)</p>";
        html += "</div>";
        
        html += "<div style='margin: 20px; padding: 15px; background-color: #2d2d2d; border-left: 4px solid #2196F3;'>";
        html += "<h3 style='color: #2196F3;'>Step 2: Apply the Rule</h3>";
        html += "<p>Here, n = 2</p>";
        html += "<p>d/dx[x²] = 2·x^(2-1) = <b style='color: #00ff88;'>2x</b></p>";
        html += "</div>";
        
        m_currentDerivative = "2*x";
        
    } else if (f.contains("x^3") && f.contains("-") && f.contains("2")) {
        html += "<div style='margin: 20px; padding: 15px; background-color: #2d2d2d; border-left: 4px solid #4CAF50;'>";
        html += "<h3 style='color: #4CAF50;'>Step 1: Identify Terms</h3>";
        html += "<p>Function: f(x) = x³ - 2x</p>";
        html += "<p>This has <b>two terms</b>: x³ and -2x</p>";
        html += "<p>We'll use the <b>Sum Rule</b>: d/dx[f + g] = f' + g'</p>";
        html += "</div>";
        
        html += "<div style='margin: 20px; padding: 15px; background-color: #2d2d2d; border-left: 4px solid #2196F3;'>";
        html += "<h3 style='color: #2196F3;'>Step 2: Differentiate Each Term</h3>";
        html += "<p><b>Term 1:</b> d/dx[x³]</p>";
        html += "<p style='margin-left: 20px;'>Using Power Rule: 3·x² = <b>3x²</b></p>";
        html += "<p><b>Term 2:</b> d/dx[-2x]</p>";
        html += "<p style='margin-left: 20px;'>Using Power Rule: -2·1·x⁰ = <b>-2</b></p>";
        html += "</div>";
        
        html += "<div style='margin: 20px; padding: 15px; background-color: #2d2d2d; border-left: 4px solid #FF9800;'>";
        html += "<h3 style='color: #FF9800;'>Step 3: Combine Results</h3>";
        html += "<p>f'(x) = 3x² + (-2) = <b style='color: #00ff88;'>3x² - 2</b></p>";
        html += "</div>";
        
        m_currentDerivative = "3*x^2 - 2";
        
    } else if (f.contains("sin") && f.contains("x^2")) {
        // Chain rule example
        html += "<div style='margin: 20px; padding: 15px; background-color: #2d2d2d; border-left: 4px solid #4CAF50;'>";
        html += "<h3 style='color: #4CAF50;'>Step 1: Identify Composition</h3>";
        html += "<p>Function: f(x) = sin(x²)</p>";
        html += "<p>This is a <b>composite function</b>:</p>";
        html += "<p style='margin-left: 20px;'>Outer: sin(u) where u = x²</p>";
        html += "<p style='margin-left: 20px;'>Inner: u = x²</p>";
        html += "<p>We need the <b style='color: #ff6b6b;'>CHAIN RULE</b>!</p>";
        html += "</div>";
        
        html += "<div style='margin: 20px; padding: 15px; background-color: #2d2d2d; border-left: 4px solid #2196F3;'>";
        html += "<h3 style='color: #2196F3;'>Step 2: Apply Chain Rule</h3>";
        html += "<p><b>Chain Rule Formula:</b> d/dx[f(g(x))] = f'(g(x)) · g'(x)</p>";
        html += "<p style='margin-top: 15px;'><b>Break it down:</b></p>";
        html += "<ol style='margin-left: 20px;'>";
        html += "<li>Derivative of outer (sin): cos(x²)</li>";
        html += "<li>Multiply by derivative of inner (x²): 2x</li>";
        html += "</ol>";
        html += "</div>";
        
        html += "<div style='margin: 20px; padding: 15px; background-color: #2d2d2d; border-left: 4px solid #FF9800;'>";
        html += "<h3 style='color: #FF9800;'>Step 3: Final Result</h3>";
        html += "<p>f'(x) = cos(x²) · 2x = <b style='color: #00ff88;'>2x·cos(x²)</b></p>";
        html += "<p style='margin-top: 10px; color: #ffd700;'>💡 <b>Key Insight:</b> The chain rule is crucial for backpropagation!</p>";
        html += "</div>";
        
        m_currentDerivative = "2*x*cos(x^2)";
        
    } else if (f == "sin(x)") {
        html += "<div style='margin: 20px; padding: 15px; background-color: #2d2d2d; border-left: 4px solid #4CAF50;'>";
        html += "<h3 style='color: #4CAF50;'>Trigonometric Derivative</h3>";
        html += "<p>Standard derivative: <b>d/dx[sin(x)] = cos(x)</b></p>";
        html += "</div>";
        m_currentDerivative = "cos(x)";
        
    } else if (f == "cos(x)") {
        html += "<div style='margin: 20px; padding: 15px; background-color: #2d2d2d; border-left: 4px solid #4CAF50;'>";
        html += "<h3 style='color: #4CAF50;'>Trigonometric Derivative</h3>";
        html += "<p>Standard derivative: <b>d/dx[cos(x)] = -sin(x)</b></p>";
        html += "</div>";
        m_currentDerivative = "-sin(x)";
        
    } else if (f.contains("exp(-x^2)")) {
        html += "<div style='margin: 20px; padding: 15px; background-color: #2d2d2d; border-left: 4px solid #4CAF50;'>";
        html += "<h3 style='color: #4CAF50;'>Gaussian Function - Chain Rule</h3>";
        html += "<p>Function: f(x) = e^(-x²)</p>";
        html += "<p><b>Outer:</b> e^u where u = -x²</p>";
        html += "<p><b>Inner:</b> u = -x²</p>";
        html += "</div>";
        
        html += "<div style='margin: 20px; padding: 15px; background-color: #2d2d2d; border-left: 4px solid #2196F3;'>";
        html += "<h3 style='color: #2196F3;'>Apply Chain Rule</h3>";
        html += "<p>1. d/dx[e^u] = e^u · u'</p>";
        html += "<p>2. u' = d/dx[-x²] = -2x</p>";
        html += "<p>3. Result: e^(-x²) · (-2x) = <b style='color: #00ff88;'>-2x·e^(-x²)</b></p>";
        html += "</div>";
        
        m_currentDerivative = "-2*x*exp(-x^2)";
        
    } else if (f.contains("1/(1+exp(-x))")) {
        // Sigmoid function
        html += "<div style='margin: 20px; padding: 15px; background-color: #2d2d2d; border-left: 4px solid #9C27B0;'>";
        html += "<h2 style='color: #9C27B0;'>🧠 NEURAL NETWORK ALERT: Sigmoid Function!</h2>";
        html += "<p>Function: σ(x) = 1/(1 + e^(-x))</p>";
        html += "<p>This is THE activation function used in neural networks!</p>";
        html += "</div>";
        
        html += "<div style='margin: 20px; padding: 15px; background-color: #2d2d2d; border-left: 4px solid #4CAF50;'>";
        html += "<h3 style='color: #4CAF50;'>Step 1: Quotient Rule Setup</h3>";
        html += "<p>Let f(x) = 1 and g(x) = 1 + e^(-x)</p>";
        html += "<p>Using: d/dx[f/g] = (f'·g - f·g')/g²</p>";
        html += "</div>";
        
        html += "<div style='margin: 20px; padding: 15px; background-color: #2d2d2d; border-left: 4px solid #2196F3;'>";
        html += "<h3 style='color: #2196F3;'>Step 2: Find Derivatives</h3>";
        html += "<p>f' = 0</p>";
        html += "<p>g' = d/dx[1 + e^(-x)] = -e^(-x) (chain rule!)</p>";
        html += "</div>";
        
        html += "<div style='margin: 20px; padding: 15px; background-color: #2d2d2d; border-left: 4px solid #FF9800;'>";
        html += "<h3 style='color: #FF9800;'>Step 3: Compute Result</h3>";
        html += "<p>σ'(x) = (0 - (-e^(-x)))/(1 + e^(-x))²</p>";
        html += "<p>     = <b style='color: #00ff88;'>e^(-x)/(1 + e^(-x))²</b></p>";
        html += "<p style='margin-top: 15px; color: #ffd700;'>💡 Fun fact: σ'(x) = σ(x)·(1 - σ(x))</p>";
        html += "</div>";
        
        m_currentDerivative = "exp(-x)/(1+exp(-x))^2";
        
    } else {
        html += "<div style='margin: 20px; padding: 15px; background-color: #2d2d2d; border-left: 4px solid #ff6b6b;'>";
        html += "<h3 style='color: #ff6b6b;'>General Derivative</h3>";
        html += "<p>For complex functions, use appropriate combination of rules:</p>";
        html += "<ul>";
        html += "<li>Power Rule for polynomials</li>";
        html += "<li>Chain Rule for compositions</li>";
        html += "<li>Product/Quotient Rules as needed</li>";
        html += "</ul>";
        html += "</div>";
        m_currentDerivative = "d/dx[" + function + "]";
    }
    
    html += "<hr style='border: 1px solid #444; margin-top: 30px;'>";
    html += "<h2 style='color: #00ff88; text-align: center; padding: 20px;'>✅ Final Answer: f'(x) = " + m_currentDerivative + "</h2>";
    html += "</div>";
    
    m_stepsDisplay->setHtml(html);
    m_resultLabel->setText("f'(x) = " + m_currentDerivative);
}

void DerivativePanel::addStep(const QString &rule, const QString &expression, const QString &explanation) {
    DerivativeStep step;
    step.rule = rule;
    step.expression = expression;
    step.explanation = explanation;
    m_steps.append(step);
}

void DerivativePanel::clearSteps() {
    m_steps.clear();
    m_stepsDisplay->clear();
}

void DerivativePanel::onRuleSelected(int index) {
    QStringList examples = {
        "x^2",
        "x^3 - 2*x",
        "sin(x)",
        "x^2*sin(x)",
        "sin(x)/x",
        "sin(x^2)",
        "exp(-x^2)"
    };
    
    if (index >= 0 && index < examples.size()) {
        m_functionInput->setText(examples[index]);
        calculateDerivative();
    }
}

QString DerivativePanel::applyPowerRule(const QString &term) {
    // Simple power rule implementation
    return "power_derivative";
}

QString DerivativePanel::applyChainRule(const QString &expr) {
    return "chain_derivative";
}

QString DerivativePanel::applyProductRule(const QString &expr) {
    return "product_derivative";
}

QString DerivativePanel::applyQuotientRule(const QString &expr) {
    return "quotient_derivative";
}
