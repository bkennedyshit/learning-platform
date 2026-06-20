#include "BayesCalculator.h"
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QGridLayout>
#include <QGroupBox>
#include <QGraphicsTextItem>
#include <QGraphicsRectItem>
#include <QGraphicsLineItem>
#include <QGraphicsEllipseItem>
#include <QPen>
#include <QBrush>
#include <QFont>
#include <cmath>

BayesCalculator::BayesCalculator(QWidget *parent)
    : QWidget(parent)
    , prior(0.5)
    , likelihood(0.8)
    , evidence(0.5)
    , posterior(0.8)
{
    setupUI();
    updateCalculation();
}

BayesCalculator::~BayesCalculator()
{
}

void BayesCalculator::setupUI()
{
    QVBoxLayout *mainLayout = new QVBoxLayout(this);
    
    // Title
    QLabel *title = new QLabel("<h2>Bayes' Theorem Calculator</h2>");
    title->setAlignment(Qt::AlignCenter);
    mainLayout->addWidget(title);
    
    // Info
    QLabel *info = new QLabel(
        "🎯 <b>Foundation of Bayesian ML!</b> Update beliefs based on new evidence.<br>"
        "Used in: Naive Bayes classifiers, Bayesian optimization, uncertainty quantification, A/B testing."
    );
    info->setWordWrap(true);
    info->setStyleSheet("QLabel { background-color: #f3e5f5; padding: 10px; border-radius: 5px; }");
    mainLayout->addWidget(info);
    
    QHBoxLayout *topLayout = new QHBoxLayout();
    
    // Left: Controls
    QGroupBox *controlGroup = new QGroupBox("Bayes' Theorem Components");
    QGridLayout *controlLayout = new QGridLayout(controlGroup);
    
    // Prior P(H)
    controlLayout->addWidget(new QLabel("<b>P(H)</b> - Prior Probability:"), 0, 0);
    priorSlider = new QSlider(Qt::Horizontal);
    priorSlider->setRange(1, 99);
    priorSlider->setValue(50);
    connect(priorSlider, &QSlider::valueChanged, this, &BayesCalculator::onPriorChanged);
    controlLayout->addWidget(priorSlider, 0, 1);
    priorValue = new QLabel("0.50");
    priorValue->setMinimumWidth(50);
    priorValue->setStyleSheet("QLabel { font-weight: bold; }");
    controlLayout->addWidget(priorValue, 0, 2);
    controlLayout->addWidget(new QLabel("<i>Initial belief before evidence</i>"), 1, 0, 1, 3);
    
    // Likelihood P(E|H)
    controlLayout->addWidget(new QLabel("<b>P(E|H)</b> - Likelihood:"), 2, 0);
    likelihoodSlider = new QSlider(Qt::Horizontal);
    likelihoodSlider->setRange(1, 99);
    likelihoodSlider->setValue(80);
    connect(likelihoodSlider, &QSlider::valueChanged, this, &BayesCalculator::onLikelihoodChanged);
    controlLayout->addWidget(likelihoodSlider, 2, 1);
    likelihoodValue = new QLabel("0.80");
    likelihoodValue->setMinimumWidth(50);
    likelihoodValue->setStyleSheet("QLabel { font-weight: bold; }");
    controlLayout->addWidget(likelihoodValue, 2, 2);
    controlLayout->addWidget(new QLabel("<i>Probability of evidence given hypothesis is true</i>"), 3, 0, 1, 3);
    
    // Evidence P(E)
    controlLayout->addWidget(new QLabel("<b>P(E)</b> - Evidence:"), 4, 0);
    evidenceSlider = new QSlider(Qt::Horizontal);
    evidenceSlider->setRange(1, 99);
    evidenceSlider->setValue(50);
    connect(evidenceSlider, &QSlider::valueChanged, this, &BayesCalculator::onEvidenceChanged);
    controlLayout->addWidget(evidenceSlider, 4, 1);
    evidenceValue = new QLabel("0.50");
    evidenceValue->setMinimumWidth(50);
    evidenceValue->setStyleSheet("QLabel { font-weight: bold; }");
    controlLayout->addWidget(evidenceValue, 4, 2);
    controlLayout->addWidget(new QLabel("<i>Total probability of seeing the evidence</i>"), 5, 0, 1, 3);
    
    // Add spacing
    controlLayout->setRowMinimumHeight(6, 10);
    
    // Posterior P(H|E)
    controlLayout->addWidget(new QLabel("<h3>P(H|E) - Posterior:</h3>"), 7, 0);
    posteriorValue = new QLabel("0.80");
    posteriorValue->setStyleSheet("QLabel { font-size: 20pt; font-weight: bold; color: #1976d2; "
                                 "background-color: #e3f2fd; padding: 10px; border-radius: 5px; }");
    controlLayout->addWidget(posteriorValue, 7, 1, 1, 2);
    controlLayout->addWidget(new QLabel("<i>Updated belief after seeing evidence</i>"), 8, 0, 1, 3);
    
    topLayout->addWidget(controlGroup);
    
    // Right: Formula and examples
    QVBoxLayout *rightLayout = new QVBoxLayout();
    
    // Formula
    formulaLabel = new QLabel();
    formulaLabel->setStyleSheet("QLabel { background-color: white; padding: 15px; "
                                "border: 2px solid #1976d2; border-radius: 5px; }");
    formulaLabel->setWordWrap(true);
    rightLayout->addWidget(formulaLabel);
    
    // Example buttons
    QGroupBox *exampleGroup = new QGroupBox("Quick Examples");
    QVBoxLayout *exampleLayout = new QVBoxLayout(exampleGroup);
    
    exampleButtons[0] = new QPushButton("🏥 Medical Test (Sensitivity 95%, Prior 1%)");
    exampleButtons[1] = new QPushButton("📧 Spam Filter (Accuracy 90%, Prior 30%)");
    exampleButtons[2] = new QPushButton("🤖 ML Classifier (99% accurate, rare event 0.1%)");
    
    for (int i = 0; i < 3; ++i) {
        connect(exampleButtons[i], &QPushButton::clicked, [this, i]() { loadExample(i); });
        exampleLayout->addWidget(exampleButtons[i]);
    }
    
    rightLayout->addWidget(exampleGroup);
    rightLayout->addStretch();
    
    topLayout->addLayout(rightLayout);
    mainLayout->addLayout(topLayout);
    
    // Probability tree visualization
    QGroupBox *treeGroup = new QGroupBox("Probability Tree Diagram");
    QVBoxLayout *treeLayout = new QVBoxLayout(treeGroup);
    
    explanationLabel = new QLabel();
    explanationLabel->setWordWrap(true);
    explanationLabel->setStyleSheet("QLabel { padding: 5px; }");
    treeLayout->addWidget(explanationLabel);
    
    treeScene = new QGraphicsScene();
    treeView = new QGraphicsView(treeScene);
    treeView->setMinimumHeight(250);
    treeLayout->addWidget(treeView);
    
    mainLayout->addWidget(treeGroup);
}

void BayesCalculator::onPriorChanged(int value)
{
    prior = value / 100.0;
    priorValue->setText(QString::number(prior, 'f', 2));
    updateCalculation();
}

void BayesCalculator::onLikelihoodChanged(int value)
{
    likelihood = value / 100.0;
    likelihoodValue->setText(QString::number(likelihood, 'f', 2));
    updateCalculation();
}

void BayesCalculator::onEvidenceChanged(int value)
{
    evidence = value / 100.0;
    evidenceValue->setText(QString::number(evidence, 'f', 2));
    updateCalculation();
}

void BayesCalculator::updateCalculation()
{
    // Bayes' Theorem: P(H|E) = P(E|H) * P(H) / P(E)
    if (evidence > 0.001) {
        posterior = (likelihood * prior) / evidence;
        posterior = std::min(posterior, 1.0);  // Cap at 1.0
    } else {
        posterior = 0.0;
    }
    
    posteriorValue->setText(QString::number(posterior, 'f', 3));
    
    // Update formula with actual values
    QString formula = QString(
        "<center><h3>Bayes' Theorem</h3>"
        "<p style='font-size: 14pt;'><b>P(H|E) = [P(E|H) × P(H)] / P(E)</b></p>"
        "<p style='font-size: 12pt;'><b>%1 = [%2 × %3] / %4</b></p>"
        "<p style='font-size: 12pt;'><b>%1 = %5 / %4</b></p>"
        "</center>"
    ).arg(QString::number(posterior, 'f', 3))
     .arg(QString::number(likelihood, 'f', 2))
     .arg(QString::number(prior, 'f', 2))
     .arg(QString::number(evidence, 'f', 2))
     .arg(QString::number(likelihood * prior, 'f', 4));
    
    formulaLabel->setText(formula);
    
    // Update explanation
    double bayesFactor = likelihood / evidence;
    QString interp;
    if (posterior > prior * 1.5) {
        interp = "📈 Evidence <b>strongly supports</b> the hypothesis (posterior > prior)";
    } else if (posterior > prior * 1.1) {
        interp = "📊 Evidence <b>weakly supports</b> the hypothesis";
    } else if (posterior < prior * 0.7) {
        interp = "📉 Evidence <b>contradicts</b> the hypothesis (posterior < prior)";
    } else {
        interp = "➡️ Evidence has <b>minimal impact</b> on belief";
    }
    
    explanationLabel->setText(QString(
        "<b>Interpretation:</b> %1<br>"
        "<b>Bayes Factor:</b> %2 (ratio of likelihood to evidence)<br>"
        "<b>Belief Update:</b> Prior %3 → Posterior %4 (%5%6 change)"
    ).arg(interp)
     .arg(QString::number(bayesFactor, 'f', 2))
     .arg(QString::number(prior, 'f', 2))
     .arg(QString::number(posterior, 'f', 3))
     .arg(posterior > prior ? "+" : "")
     .arg(QString::number((posterior - prior) / prior * 100, 'f', 1)));
    
    drawProbabilityTree();
}

void BayesCalculator::drawProbabilityTree()
{
    treeScene->clear();
    
    // Tree dimensions
    double width = 600;
    double height = 200;
    double nodeRadius = 40;
    
    QPen pen(Qt::black, 2);
    QBrush blueBrush(QColor("#2196f3"));
    QBrush greenBrush(QColor("#4caf50"));
    QBrush orangeBrush(QColor("#ff9800"));
    
    QFont labelFont("Arial", 10, QFont::Bold);
    QFont probFont("Arial", 9);
    
    // Root node
    QGraphicsEllipseItem *root = treeScene->addEllipse(-nodeRadius, -nodeRadius, 
                                                       2*nodeRadius, 2*nodeRadius, 
                                                       pen, blueBrush);
    root->setPos(50, height/2);
    QGraphicsTextItem *rootText = treeScene->addText("Start", labelFont);
    rootText->setPos(50 - 20, height/2 - 10);
    
    // H branch (hypothesis true)
    QGraphicsLineItem *lineH = treeScene->addLine(50 + nodeRadius, height/2 - 10,
                                                   250 - nodeRadius, height/2 - 60,
                                                   pen);
    QGraphicsEllipseItem *nodeH = treeScene->addEllipse(-nodeRadius, -nodeRadius,
                                                        2*nodeRadius, 2*nodeRadius,
                                                        pen, greenBrush);
    nodeH->setPos(250, height/2 - 60);
    QGraphicsTextItem *textH = treeScene->addText("H", labelFont);
    textH->setPos(250 - 8, height/2 - 70);
    QGraphicsTextItem *probH = treeScene->addText(QString("P=%1").arg(prior, 0, 'f', 2), probFont);
    probH->setPos(130, height/2 - 50);
    
    // ¬H branch (hypothesis false)
    QGraphicsLineItem *lineNotH = treeScene->addLine(50 + nodeRadius, height/2 + 10,
                                                      250 - nodeRadius, height/2 + 60,
                                                      pen);
    QGraphicsEllipseItem *nodeNotH = treeScene->addEllipse(-nodeRadius, -nodeRadius,
                                                           2*nodeRadius, 2*nodeRadius,
                                                           pen, orangeBrush);
    nodeNotH->setPos(250, height/2 + 60);
    QGraphicsTextItem *textNotH = treeScene->addText("¬H", labelFont);
    textNotH->setPos(250 - 12, height/2 + 50);
    QGraphicsTextItem *probNotH = treeScene->addText(QString("P=%1").arg(1-prior, 0, 'f', 2), probFont);
    probNotH->setPos(130, height/2 + 40);
    
    // E|H branch
    QGraphicsLineItem *lineEgivenH = treeScene->addLine(250 + nodeRadius, height/2 - 60,
                                                        450 - nodeRadius, height/2 - 80,
                                                        pen);
    QGraphicsEllipseItem *nodeEgivenH = treeScene->addEllipse(-nodeRadius/2, -nodeRadius/2,
                                                               nodeRadius, nodeRadius,
                                                               pen, QColor("#81c784"));
    nodeEgivenH->setPos(450, height/2 - 80);
    QGraphicsTextItem *textEgivenH = treeScene->addText("E", labelFont);
    textEgivenH->setPos(450 - 8, height/2 - 90);
    QGraphicsTextItem *probEgivenH = treeScene->addText(QString("P=%1").arg(likelihood, 0, 'f', 2), probFont);
    probEgivenH->setPos(330, height/2 - 95);
    
    // ¬E|H branch
    QGraphicsLineItem *lineNotEgivenH = treeScene->addLine(250 + nodeRadius, height/2 - 60,
                                                           450 - nodeRadius, height/2 - 40,
                                                           QPen(QColor("#cccccc"), 1, Qt::DashLine));
    
    // E|¬H branch
    double pEgivenNotH = (evidence - likelihood * prior) / (1 - prior);
    pEgivenNotH = std::max(0.0, std::min(1.0, pEgivenNotH));
    
    QGraphicsLineItem *lineEgivenNotH = treeScene->addLine(250 + nodeRadius, height/2 + 60,
                                                           450 - nodeRadius, height/2 + 40,
                                                           QPen(QColor("#999999"), 1, Qt::DashLine));
    QGraphicsTextItem *probEgivenNotH = treeScene->addText(QString("P=%1").arg(pEgivenNotH, 0, 'f', 2), probFont);
    probEgivenNotH->setPos(330, height/2 + 30);
    
    // Joint probability P(E,H)
    double jointProb = likelihood * prior;
    QGraphicsTextItem *jointText = treeScene->addText(
        QString("P(E,H) = %1").arg(jointProb, 0, 'f', 3), 
        QFont("Arial", 9, QFont::Bold)
    );
    jointText->setDefaultTextColor(QColor("#1976d2"));
    jointText->setPos(460, height/2 - 120);
    
    // Highlight the path we care about
    lineH->setPen(QPen(QColor("#1976d2"), 3));
    lineEgivenH->setPen(QPen(QColor("#1976d2"), 3));
    
    // Legend
    QGraphicsTextItem *legend = treeScene->addText(
        "Bold blue path: P(E,H) = P(E|H) × P(H)\n"
        "P(H|E) = P(E,H) / P(E)",
        QFont("Arial", 8)
    );
    legend->setPos(10, 10);
    
    treeScene->setSceneRect(0, 0, width, height);
}

void BayesCalculator::loadExample(int index)
{
    switch (index) {
        case 0:  // Medical test
            // Rare disease (1% prevalence), highly sensitive test (95%)
            // But P(E) includes false positives!
            priorSlider->setValue(1);  // 1% have disease
            likelihoodSlider->setValue(95);  // 95% sensitivity
            evidenceSlider->setValue(10);  // ~10% test positive (including false positives)
            break;
            
        case 1:  // Spam filter
            priorSlider->setValue(30);  // 30% of emails are spam
            likelihoodSlider->setValue(90);  // 90% of spam triggers filter
            evidenceSlider->setValue(35);  // 35% of all emails trigger filter
            break;
            
        case 2:  // ML rare event
            priorSlider->setValue(1);  // 0.1% rate -> use 1%
            likelihoodSlider->setValue(99);  // 99% accurate on positive class
            evidenceSlider->setValue(2);  // Model predicts positive 2% of time
            break;
    }
}
