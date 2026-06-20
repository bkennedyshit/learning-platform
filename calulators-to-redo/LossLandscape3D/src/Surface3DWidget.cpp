#include "Surface3DWidget.h"
#include <QtDataVisualization/QValue3DAxis>
#include <QtDataVisualization/Q3DTheme>
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QGroupBox>
#include <cmath>

using namespace QtDataVisualization;

Surface3DWidget::Surface3DWidget(QWidget *parent)
    : QWidget(parent)
    , m_surface(new Q3DSurface())
    , m_series(new QSurface3DSeries())
{
    // Initialize predefined functions
    m_functions = {
        {"Rosenbrock (Banana Valley)", rosenbrock, -2.0, 2.0, -1.0, 3.0},
        {"Himmelblau (Multiple Minima)", himmelblau, -5.0, 5.0, -5.0, 5.0},
        {"Beale Function", beale, -4.5, 4.5, -4.5, 4.5},
        {"Rastrigin (Many Local Minima)", rastrigin, -5.12, 5.12, -5.12, 5.12},
        {"Sphere (Simple Bowl)", sphere, -5.0, 5.0, -5.0, 5.0},
        {"Saddle Point (x² - y²)", saddle, -3.0, 3.0, -3.0, 3.0}
    };
    
    setupUI();
    setLossFunction("Rosenbrock (Banana Valley)");
}

Surface3DWidget::~Surface3DWidget()
{
    delete m_surface;
}

void Surface3DWidget::setupUI()
{
    QVBoxLayout* mainLayout = new QVBoxLayout(this);
    
    // Create container for 3D surface
    QWidget* container = QWidget::createWindowContainer(m_surface);
    container->setSizePolicy(QSizePolicy::Expanding, QSizePolicy::Expanding);
    
    // Configure surface
    m_surface->setAxisX(new QValue3DAxis);
    m_surface->setAxisY(new QValue3DAxis);
    m_surface->setAxisZ(new QValue3DAxis);
    
    m_surface->axisX()->setTitle("X");
    m_surface->axisY()->setTitle("Loss");
    m_surface->axisZ()->setTitle("Y");
    
    m_surface->axisX()->setLabelFormat("%.2f");
    m_surface->axisY()->setLabelFormat("%.1f");
    m_surface->axisZ()->setLabelFormat("%.2f");
    
    // Enable shadow quality for better visuals
    m_surface->setShadowQuality(QAbstract3DGraph::ShadowQualityMedium);
    
    // Configure series
    m_series->setDrawMode(QSurface3DSeries::DrawSurfaceAndWireframe);
    m_series->setFlatShadingEnabled(false);
    
    m_surface->addSeries(m_series);
    
    setupGradientColor();
    
    // Control panel
    QGroupBox* controlBox = new QGroupBox("Surface Controls");
    QVBoxLayout* controlLayout = new QVBoxLayout(controlBox);
    
    // Function selector
    QHBoxLayout* funcLayout = new QHBoxLayout();
    funcLayout->addWidget(new QLabel("Loss Function:"));
    m_functionCombo = new QComboBox();
    for (const auto& func : m_functions) {
        m_functionCombo->addItem(func.name);
    }
    funcLayout->addWidget(m_functionCombo);
    controlLayout->addLayout(funcLayout);
    
    // Resolution slider
    QHBoxLayout* resLayout = new QHBoxLayout();
    resLayout->addWidget(new QLabel("Resolution:"));
    m_resolutionSlider = new QSlider(Qt::Horizontal);
    m_resolutionSlider->setRange(20, 100);
    m_resolutionSlider->setValue(50);
    resLayout->addWidget(m_resolutionSlider);
    m_resolutionLabel = new QLabel("50");
    resLayout->addWidget(m_resolutionLabel);
    controlLayout->addLayout(resLayout);
    
    // Display options
    m_solidSurfaceCheck = new QCheckBox("Solid Surface");
    m_solidSurfaceCheck->setChecked(false);
    controlLayout->addWidget(m_solidSurfaceCheck);
    
    m_gridCheck = new QCheckBox("Show Grid");
    m_gridCheck->setChecked(true);
    controlLayout->addWidget(m_gridCheck);
    
    m_smoothCheck = new QCheckBox("Smooth Shading");
    m_smoothCheck->setChecked(true);
    controlLayout->addWidget(m_smoothCheck);
    
    // Connect signals
    connect(m_functionCombo, QOverload<int>::of(&QComboBox::currentIndexChanged),
            this, &Surface3DWidget::onFunctionChanged);
    connect(m_resolutionSlider, &QSlider::valueChanged,
            this, &Surface3DWidget::onResolutionChanged);
    connect(m_solidSurfaceCheck, &QCheckBox::toggled,
            this, &Surface3DWidget::onSurfaceModeToggled);
    connect(m_gridCheck, &QCheckBox::toggled,
            this, &Surface3DWidget::onGridToggled);
    connect(m_smoothCheck, &QCheckBox::toggled,
            this, &Surface3DWidget::onSmoothToggled);
    
    // Add to main layout
    mainLayout->addWidget(container, 1);
    mainLayout->addWidget(controlBox);
}

void Surface3DWidget::setupGradientColor()
{
    // Create gradient from blue (low) to red (high)
    QLinearGradient gradient;
    gradient.setColorAt(0.0, Qt::darkBlue);
    gradient.setColorAt(0.2, Qt::blue);
    gradient.setColorAt(0.4, Qt::cyan);
    gradient.setColorAt(0.6, Qt::green);
    gradient.setColorAt(0.8, Qt::yellow);
    gradient.setColorAt(1.0, Qt::red);
    
    m_series->setBaseGradient(gradient);
    m_series->setColorStyle(Q3DTheme::ColorStyleRangeGradient);
}

void Surface3DWidget::setLossFunction(const QString& functionName)
{
    for (const auto& func : m_functions) {
        if (func.name == functionName) {
            m_currentFunction = func.func;
            m_currentFunctionName = func.name;
            m_minX = func.minX;
            m_maxX = func.maxX;
            m_minY = func.minY;
            m_maxY = func.maxY;
            
            updateSurface();
            emit functionChanged(functionName);
            break;
        }
    }
}

void Surface3DWidget::setCustomFunction(LossFunction func)
{
    m_currentFunction = func;
    m_currentFunctionName = "Custom";
    updateSurface();
}

void Surface3DWidget::updateSurface()
{
    populateSurfaceData();
    
    // Update axis ranges
    m_surface->axisX()->setRange(m_minX, m_maxX);
    m_surface->axisZ()->setRange(m_minY, m_maxY);
}

void Surface3DWidget::populateSurfaceData()
{
    if (!m_currentFunction) return;
    
    QSurfaceDataArray* dataArray = new QSurfaceDataArray;
    dataArray->reserve(m_resolution);
    
    double stepX = (m_maxX - m_minX) / (m_resolution - 1);
    double stepY = (m_maxY - m_minY) / (m_resolution - 1);
    
    double minZ = std::numeric_limits<double>::max();
    double maxZ = std::numeric_limits<double>::lowest();
    
    // First pass: find min/max for better visualization
    for (int i = 0; i < m_resolution; ++i) {
        double y = m_minY + i * stepY;
        for (int j = 0; j < m_resolution; ++j) {
            double x = m_minX + j * stepX;
            double z = m_currentFunction(x, y);
            minZ = std::min(minZ, z);
            maxZ = std::max(maxZ, z);
        }
    }
    
    // Second pass: populate data
    for (int i = 0; i < m_resolution; ++i) {
        QSurfaceDataRow* newRow = new QSurfaceDataRow(m_resolution);
        double y = m_minY + i * stepY;
        
        for (int j = 0; j < m_resolution; ++j) {
            double x = m_minX + j * stepX;
            double z = m_currentFunction(x, y);
            
            // Clamp extreme values for better visualization
            if (std::abs(z) > 1000.0) {
                z = (z > 0) ? 1000.0 : -1000.0;
            }
            
            (*newRow)[j].setPosition(QVector3D(x, z, y));
        }
        *dataArray << newRow;
    }
    
    m_series->dataProxy()->resetArray(dataArray);
    
    // Update Y axis range
    m_surface->axisY()->setRange(minZ, maxZ);
}

// Predefined loss functions
double Surface3DWidget::rosenbrock(double x, double y)
{
    double a = 1.0;
    double b = 100.0;
    return (a - x) * (a - x) + b * (y - x * x) * (y - x * x);
}

double Surface3DWidget::himmelblau(double x, double y)
{
    return (x * x + y - 11) * (x * x + y - 11) + 
           (x + y * y - 7) * (x + y * y - 7);
}

double Surface3DWidget::beale(double x, double y)
{
    double t1 = 1.5 - x + x * y;
    double t2 = 2.25 - x + x * y * y;
    double t3 = 2.625 - x + x * y * y * y;
    return t1 * t1 + t2 * t2 + t3 * t3;
}

double Surface3DWidget::rastrigin(double x, double y)
{
    const double A = 10.0;
    const double PI = 3.14159265358979323846;
    return 2 * A + (x * x - A * std::cos(2 * PI * x)) + 
                   (y * y - A * std::cos(2 * PI * y));
}

double Surface3DWidget::sphere(double x, double y)
{
    return x * x + y * y;
}

double Surface3DWidget::saddle(double x, double y)
{
    return x * x - y * y;
}

// Slots
void Surface3DWidget::onFunctionChanged(int index)
{
    if (index >= 0 && index < m_functions.size()) {
        setLossFunction(m_functions[index].name);
    }
}

void Surface3DWidget::onResolutionChanged(int value)
{
    m_resolution = value;
    m_resolutionLabel->setText(QString::number(value));
    updateSurface();
}

void Surface3DWidget::onSurfaceModeToggled(bool checked)
{
    if (checked) {
        m_series->setDrawMode(QSurface3DSeries::DrawSurface);
    } else {
        m_series->setDrawMode(QSurface3DSeries::DrawSurfaceAndWireframe);
    }
}

void Surface3DWidget::onGridToggled(bool checked)
{
    if (!checked) {
        m_series->setDrawMode(QSurface3DSeries::DrawSurface);
        m_solidSurfaceCheck->setChecked(true);
    } else if (!m_solidSurfaceCheck->isChecked()) {
        m_series->setDrawMode(QSurface3DSeries::DrawSurfaceAndWireframe);
    }
}

void Surface3DWidget::onSmoothToggled(bool checked)
{
    m_series->setFlatShadingEnabled(!checked);
}
