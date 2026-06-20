/**
 * QUICK REFERENCE - Derivative Engine API
 * ========================================
 */

#include "DerivativeEngine.h"

// BASIC USAGE
// ===========

DerivativeEngine engine;

// 1. COMPUTE SIMPLE DERIVATIVE
auto result = engine.computeDerivative("x^2 + 3*x");
std::cout << result.simplifiedDerivative;  // "2*x + 3"

// 2. COMPUTE WITH DIFFERENT VARIABLE
auto result = engine.computeDerivative("y^3 + 2*y", "y");

// 3. GET STEP-BY-STEP EXPLANATION
auto result = engine.computeDerivative("sin(x^2)");
std::cout << engine.formatSteps(result);

// 4. HIGHER-ORDER DERIVATIVES
auto result = engine.computeNthDerivative("x^4", 2);  // 2nd derivative
auto result = engine.computeNthDerivative("x^4", 3);  // 3rd derivative

// 5. PARTIAL DERIVATIVES
auto result = engine.computePartialDerivative("x^2 + y^2", "x");  // ∂f/∂x
auto result = engine.computePartialDerivative("x^2 + y^2", "y");  // ∂f/∂y

// 6. EVALUATE AT A POINT
std::map<std::string, double> vars = {{"x", 2.0}};
double val = engine.evaluate("x^2 + 3*x", vars);  // f(2)

// 7. FIND CRITICAL POINTS (where f'(x) = 0)
auto criticalPts = engine.findCriticalPoints("x^3 - 3*x", -5, 5);
for (const auto& cp : criticalPts) {
    std::cout << "x=" << cp.x << ", f(x)=" << cp.y << " [" << cp.type << "]\n";
}

// 8. FIND INFLECTION POINTS (where f''(x) = 0)
auto inflectionPts = engine.findInflectionPoints("x^3", -3, 3);
for (const auto& ip : inflectionPts) {
    std::cout << "x=" << ip.x << ", f(x)=" << ip.y << "\n";
}

// SUPPORTED EXPRESSIONS
// ======================

// Polynomials
"x^2 + 3*x + 5"
"2*x^3 - 5*x^2 + x - 7"

// Trigonometric
"sin(x)"
"cos(x)"
"tan(x)"
"sin(x) + cos(x)"

// Exponential & Logarithmic
"exp(x)"           // e^x
"ln(x)"            // natural log
"log(x)"           // base-10 log
"exp(2*x)"

// Composite Functions (Chain Rule)
"sin(x^2)"
"exp(sin(x))"
"ln(x^2 + 1)"
"sqrt(x^2 + 1)"    // √(x²+1)

// Product Rule
"x * sin(x)"
"x^2 * exp(x)"

// Quotient Rule
"sin(x) / x"
"x / (x^2 + 1)"

// Complex Nested
"exp(sin(x^2))"
"(x^2 + 1)^3"
"x * sin(x) * exp(x)"

// Multivariable
"x^2 + y^2"
"3*x*y + x^2"
"sin(x) * cos(y)"

// RESULT STRUCTURE
// =================

DerivativeResult {
    std::unique_ptr<ExpressionNode> expression;      // Original parsed expression
    std::unique_ptr<ExpressionNode> derivative;      // Derivative expression
    std::vector<DerivativeStep> steps;               // Step-by-step explanation
    std::string originalExpression;                  // Original string
    std::string derivativeExpression;                // Derivative as string
    std::string simplifiedDerivative;                // Simplified derivative
    bool success;                                     // True if successful
    std::string errorMessage;                        // Error message if failed
}

// CRITICAL POINT STRUCTURE
// =========================

CriticalPoint {
    double x;              // x-coordinate
    double y;              // f(x) value
    std::string type;      // "local minimum", "local maximum", "saddle", etc.
}

// INFLECTION POINT STRUCTURE
// ===========================

InflectionPoint {
    double x;              // x-coordinate
    double y;              // f(x) value
}

// DERIVATIVE STEP STRUCTURE
// ==========================

DerivativeStep {
    std::string expression;     // Current expression
    std::string rule;           // Rule applied (e.g., "Power Rule")
    std::string explanation;    // Detailed explanation
}

// COMMON PATTERNS
// ===============

// Pattern 1: Compute and display derivative
{
    auto result = engine.computeDerivative("x^2 + 3*x");
    if (result.success) {
        std::cout << "f'(x) = " << result.simplifiedDerivative << "\n";
    } else {
        std::cout << "Error: " << result.errorMessage << "\n";
    }
}

// Pattern 2: Full analysis of a function
{
    std::string func = "x^3 - 3*x";
    
    // 1st derivative
    auto d1 = engine.computeNthDerivative(func, 1);
    std::cout << "f'(x)  = " << d1.simplifiedDerivative << "\n";
    
    // 2nd derivative
    auto d2 = engine.computeNthDerivative(func, 2);
    std::cout << "f''(x) = " << d2.simplifiedDerivative << "\n";
    
    // Critical points
    auto cps = engine.findCriticalPoints(func, -5, 5);
    for (const auto& cp : cps) {
        std::cout << "Critical: x=" << cp.x << " [" << cp.type << "]\n";
    }
    
    // Inflection points
    auto ips = engine.findInflectionPoints(func, -5, 5);
    for (const auto& ip : ips) {
        std::cout << "Inflection: x=" << ip.x << "\n";
    }
}

// Pattern 3: Gradient (multiple partial derivatives)
{
    std::string func = "x^2 + 3*x*y + y^2";
    
    auto dx = engine.computePartialDerivative(func, "x");
    auto dy = engine.computePartialDerivative(func, "y");
    
    std::cout << "∇f = (" << dx.simplifiedDerivative 
              << ", " << dy.simplifiedDerivative << ")\n";
}

// Pattern 4: Tangent line at a point
{
    std::string func = "x^2";
    double x0 = 2.0;
    
    // Get f(x0)
    std::map<std::string, double> vars = {{"x", x0}};
    double y0 = engine.evaluate(func, vars);
    
    // Get f'(x0)
    auto deriv = engine.computeDerivative(func);
    auto expr = deriv.derivative.get();
    double slope = engine.evaluate(expr, vars);
    
    std::cout << "Tangent line at x=" << x0 << ":\n";
    std::cout << "y - " << y0 << " = " << slope << "(x - " << x0 << ")\n";
}

// ERROR HANDLING
// ==============

auto result = engine.computeDerivative("invalid expression");
if (!result.success) {
    std::cout << "Parse error: " << result.errorMessage << "\n";
    std::cout << "Last error: " << engine.getLastError() << "\n";
}

// PERFORMANCE TIPS
// ================

// 1. Reuse engine instance (parser caching)
DerivativeEngine engine;
for (const auto& expr : expressions) {
    auto result = engine.computeDerivative(expr);
}

// 2. Simplify explicitly if needed
auto expr = engine.parseExpression("(x+0)*1");
auto simplified = engine.simplify(std::move(expr));

// 3. Reduce sample count for faster critical point finding
auto cps = engine.findCriticalPoints("x^3", -10, 10, 100);  // 100 samples instead of default 1000
