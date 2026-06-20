/**
 * Example usage of the Derivative Calculation Engine
 * 
 * This demonstrates the core features:
 * - Parsing mathematical expressions
 * - Computing derivatives with step-by-step explanations
 * - Higher-order derivatives
 * - Finding critical points and inflection points
 * - Evaluating expressions
 */

#include "DerivativeEngine.h"
#include <iostream>
#include <iomanip>

using namespace Calculus;

void printSeparator() {
    std::cout << "\n" << std::string(70, '=') << "\n\n";
}

void example1_BasicDerivatives() {
    std::cout << "EXAMPLE 1: Basic Derivatives\n";
    std::cout << "-----------------------------\n\n";
    
    DerivativeEngine engine;
    
    // Simple polynomial
    std::cout << "1. f(x) = x^2 + 3*x + 5\n";
    auto result1 = engine.computeDerivative("x^2 + 3*x + 5");
    std::cout << "   f'(x) = " << result1.simplifiedDerivative << "\n\n";
    
    // Trigonometric
    std::cout << "2. f(x) = sin(x) + cos(x)\n";
    auto result2 = engine.computeDerivative("sin(x) + cos(x)");
    std::cout << "   f'(x) = " << result2.simplifiedDerivative << "\n\n";
    
    // Exponential
    std::cout << "3. f(x) = exp(x) + 2*x\n";
    auto result3 = engine.computeDerivative("exp(x) + 2*x");
    std::cout << "   f'(x) = " << result3.simplifiedDerivative << "\n\n";
}

void example2_ChainRule() {
    std::cout << "EXAMPLE 2: Chain Rule (Composite Functions)\n";
    std::cout << "-------------------------------------------\n\n";
    
    DerivativeEngine engine;
    
    // Nested function
    std::cout << "f(x) = sin(x^2)\n\n";
    auto result = engine.computeDerivative("sin(x^2)");
    
    std::cout << "Step-by-step solution:\n";
    std::cout << engine.formatSteps(result) << "\n";
    
    std::cout << "\nFinal Result: f'(x) = " << result.simplifiedDerivative << "\n\n";
}

void example3_ProductAndQuotientRules() {
    std::cout << "EXAMPLE 3: Product & Quotient Rules\n";
    std::cout << "-----------------------------------\n\n";
    
    DerivativeEngine engine;
    
    // Product rule
    std::cout << "1. Product Rule: f(x) = x^2 * sin(x)\n";
    auto result1 = engine.computeDerivative("x^2 * sin(x)");
    std::cout << "   f'(x) = " << result1.simplifiedDerivative << "\n\n";
    
    // Quotient rule
    std::cout << "2. Quotient Rule: f(x) = sin(x) / x\n";
    auto result2 = engine.computeDerivative("sin(x) / x");
    std::cout << "   f'(x) = " << result2.simplifiedDerivative << "\n\n";
}

void example4_HigherOrderDerivatives() {
    std::cout << "EXAMPLE 4: Higher-Order Derivatives\n";
    std::cout << "-----------------------------------\n\n";
    
    DerivativeEngine engine;
    
    std::cout << "f(x) = x^4 - 3*x^2 + 2*x\n\n";
    
    // First derivative
    auto result1 = engine.computeNthDerivative("x^4 - 3*x^2 + 2*x", 1);
    std::cout << "f'(x)   = " << result1.simplifiedDerivative << "\n";
    
    // Second derivative
    auto result2 = engine.computeNthDerivative("x^4 - 3*x^2 + 2*x", 2);
    std::cout << "f''(x)  = " << result2.simplifiedDerivative << "\n";
    
    // Third derivative
    auto result3 = engine.computeNthDerivative("x^4 - 3*x^2 + 2*x", 3);
    std::cout << "f'''(x) = " << result3.simplifiedDerivative << "\n";
    
    // Fourth derivative
    auto result4 = engine.computeNthDerivative("x^4 - 3*x^2 + 2*x", 4);
    std::cout << "f⁴(x)   = " << result4.simplifiedDerivative << "\n\n";
}

void example5_CriticalPoints() {
    std::cout << "EXAMPLE 5: Finding Critical Points\n";
    std::cout << "----------------------------------\n\n";
    
    DerivativeEngine engine;
    
    std::cout << "f(x) = x^3 - 3*x^2 + 2\n\n";
    
    // Find critical points where f'(x) = 0
    auto criticalPoints = engine.findCriticalPoints("x^3 - 3*x^2 + 2", -5, 5);
    
    std::cout << "Critical points (where f'(x) = 0):\n";
    for (const auto& cp : criticalPoints) {
        std::cout << "  x = " << std::fixed << std::setprecision(4) << cp.x 
                  << ", f(x) = " << cp.y 
                  << " (" << cp.type << ")\n";
    }
    std::cout << "\n";
}

void example6_InflectionPoints() {
    std::cout << "EXAMPLE 6: Finding Inflection Points\n";
    std::cout << "------------------------------------\n\n";
    
    DerivativeEngine engine;
    
    std::cout << "f(x) = x^3\n\n";
    
    // Find inflection points where f''(x) = 0
    auto inflectionPoints = engine.findInflectionPoints("x^3", -3, 3);
    
    std::cout << "Inflection points (where f''(x) = 0):\n";
    for (const auto& ip : inflectionPoints) {
        std::cout << "  x = " << std::fixed << std::setprecision(4) << ip.x 
                  << ", f(x) = " << ip.y << "\n";
    }
    std::cout << "\n";
}

void example7_ComplexExpressions() {
    std::cout << "EXAMPLE 7: Complex Expressions\n";
    std::cout << "------------------------------\n\n";
    
    DerivativeEngine engine;
    
    // Complex composite function
    std::cout << "1. f(x) = exp(sin(x^2))\n";
    auto result1 = engine.computeDerivative("exp(sin(x^2))");
    std::cout << "   f'(x) = " << result1.simplifiedDerivative << "\n\n";
    
    // Product of multiple terms
    std::cout << "2. f(x) = x * sin(x) * exp(x)\n";
    auto result2 = engine.computeDerivative("x * sin(x) * exp(x)");
    std::cout << "   f'(x) = " << result2.simplifiedDerivative << "\n\n";
    
    // Nested power
    std::cout << "3. f(x) = (x^2 + 1)^3\n";
    auto result3 = engine.computeDerivative("(x^2 + 1)^3");
    std::cout << "   f'(x) = " << result3.simplifiedDerivative << "\n\n";
}

void example8_PartialDerivatives() {
    std::cout << "EXAMPLE 8: Partial Derivatives\n";
    std::cout << "------------------------------\n\n";
    
    DerivativeEngine engine;
    
    std::cout << "f(x, y) = x^2 + 3*x*y + y^2\n\n";
    
    // Partial derivative with respect to x
    auto result_x = engine.computePartialDerivative("x^2 + 3*x*y + y^2", "x");
    std::cout << "∂f/∂x = " << result_x.simplifiedDerivative << "\n";
    
    // Partial derivative with respect to y
    auto result_y = engine.computePartialDerivative("x^2 + 3*x*y + y^2", "y");
    std::cout << "∂f/∂y = " << result_y.simplifiedDerivative << "\n\n";
}

void example9_EvaluateAtPoint() {
    std::cout << "EXAMPLE 9: Evaluate at Specific Points\n";
    std::cout << "--------------------------------------\n\n";
    
    DerivativeEngine engine;
    
    std::cout << "f(x) = x^2 + 2*x + 1\n\n";
    
    // Evaluate at different points
    std::map<std::string, double> vars1 = {{"x", 0}};
    double value1 = engine.evaluate("x^2 + 2*x + 1", vars1);
    std::cout << "f(0) = " << value1 << "\n";
    
    std::map<std::string, double> vars2 = {{"x", 1}};
    double value2 = engine.evaluate("x^2 + 2*x + 1", vars2);
    std::cout << "f(1) = " << value2 << "\n";
    
    std::map<std::string, double> vars3 = {{"x", -1}};
    double value3 = engine.evaluate("x^2 + 2*x + 1", vars3);
    std::cout << "f(-1) = " << value3 << "\n\n";
}

void example10_FullWorkflow() {
    std::cout << "EXAMPLE 10: Complete Analysis of a Function\n";
    std::cout << "-------------------------------------------\n\n";
    
    DerivativeEngine engine;
    
    std::string function = "x^3 - 6*x^2 + 9*x + 1";
    std::cout << "Analyzing: f(x) = " << function << "\n\n";
    
    // First derivative
    auto first = engine.computeNthDerivative(function, 1);
    std::cout << "1st derivative: f'(x)  = " << first.simplifiedDerivative << "\n";
    
    // Second derivative
    auto second = engine.computeNthDerivative(function, 2);
    std::cout << "2nd derivative: f''(x) = " << second.simplifiedDerivative << "\n\n";
    
    // Critical points
    std::cout << "Critical points:\n";
    auto criticalPoints = engine.findCriticalPoints(function, -2, 5);
    for (const auto& cp : criticalPoints) {
        std::cout << "  x = " << std::fixed << std::setprecision(4) << cp.x 
                  << ", f(x) = " << cp.y 
                  << " [" << cp.type << "]\n";
    }
    std::cout << "\n";
    
    // Inflection points
    std::cout << "Inflection points:\n";
    auto inflectionPoints = engine.findInflectionPoints(function, -2, 5);
    for (const auto& ip : inflectionPoints) {
        std::cout << "  x = " << std::fixed << std::setprecision(4) << ip.x 
                  << ", f(x) = " << ip.y << "\n";
    }
    std::cout << "\n";
}

int main() {
    std::cout << "\n";
    std::cout << "╔══════════════════════════════════════════════════════════════╗\n";
    std::cout << "║     CALCULUS VISUALIZER - DERIVATIVE ENGINE EXAMPLES         ║\n";
    std::cout << "║               Symbolic Differentiation System                 ║\n";
    std::cout << "╚══════════════════════════════════════════════════════════════╝\n";
    
    printSeparator();
    example1_BasicDerivatives();
    
    printSeparator();
    example2_ChainRule();
    
    printSeparator();
    example3_ProductAndQuotientRules();
    
    printSeparator();
    example4_HigherOrderDerivatives();
    
    printSeparator();
    example5_CriticalPoints();
    
    printSeparator();
    example6_InflectionPoints();
    
    printSeparator();
    example7_ComplexExpressions();
    
    printSeparator();
    example8_PartialDerivatives();
    
    printSeparator();
    example9_EvaluateAtPoint();
    
    printSeparator();
    example10_FullWorkflow();
    
    printSeparator();
    std::cout << "All examples completed successfully!\n\n";
    
    return 0;
}
