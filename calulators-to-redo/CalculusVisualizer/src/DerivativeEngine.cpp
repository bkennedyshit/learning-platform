#include "DerivativeEngine.h"
#include <sstream>
#include <cmath>
#include <algorithm>
#include <set>

namespace Calculus {

DerivativeEngine::DerivativeEngine() {}

void DerivativeEngine::setError(const std::string& message) {
    lastError = message;
}

std::unique_ptr<ExpressionNode> DerivativeEngine::parseExpression(const std::string& expression) {
    auto result = parser.parse(expression);
    if (!result) {
        setError("Parse error: " + parser.getError());
    }
    return result;
}

std::unique_ptr<ExpressionNode> DerivativeEngine::simplify(std::unique_ptr<ExpressionNode> expr) {
    if (!expr) return nullptr;
    
    // Apply simplification multiple times until no more changes
    auto current = std::move(expr);
    for (int i = 0; i < 5; i++) {
        auto simplified = current->simplify();
        if (simplified->toString() == current->toString()) {
            return simplified;
        }
        current = std::move(simplified);
    }
    return current;
}

DerivativeResult DerivativeEngine::computeDerivative(const std::string& expression, const std::string& variable) {
    DerivativeResult result;
    result.success = false;
    result.originalExpression = expression;
    
    // Parse the expression
    auto expr = parseExpression(expression);
    if (!expr) {
        result.errorMessage = lastError;
        return result;
    }
    
    // Compute derivative
    std::vector<DerivativeStep> steps;
    steps.push_back({"f(" + variable + ") = " + expr->toString(), "Original Function", "Starting expression"});
    
    auto derivative = expr->differentiate(variable, steps);
    
    if (!derivative) {
        result.errorMessage = "Failed to compute derivative";
        return result;
    }
    
    // Simplify the derivative
    auto simplified = simplify(std::move(derivative));
    
    result.expression = std::move(expr);
    result.derivative = simplified->clone();
    result.steps = steps;
    result.derivativeExpression = result.derivative->toString();
    result.simplifiedDerivative = simplified->toString();
    result.success = true;
    
    return result;
}

DerivativeResult DerivativeEngine::computeNthDerivative(const std::string& expression, int order, const std::string& variable) {
    if (order < 1) {
        DerivativeResult result;
        result.success = false;
        result.errorMessage = "Order must be at least 1";
        return result;
    }
    
    if (order == 1) {
        return computeDerivative(expression, variable);
    }
    
    // Compute derivative iteratively
    auto expr = parseExpression(expression);
    if (!expr) {
        DerivativeResult result;
        result.success = false;
        result.errorMessage = lastError;
        return result;
    }
    
    DerivativeResult result;
    result.originalExpression = expression;
    result.success = true;
    
    std::vector<DerivativeStep> allSteps;
    allSteps.push_back({"f(" + variable + ") = " + expr->toString(), "Original Function", "Starting expression"});
    
    auto current = std::move(expr);
    
    for (int i = 1; i <= order; i++) {
        std::vector<DerivativeStep> steps;
        std::string orderSuffix = (i == 1) ? "'" : 
                                  (i == 2) ? "''" : 
                                  (i == 3) ? "'''" : 
                                  "^(" + std::to_string(i) + ")";
        
        steps.push_back({"f" + orderSuffix + "(" + variable + ")", 
                        "Computing derivative #" + std::to_string(i), 
                        "Differentiating with respect to " + variable});
        
        auto derivative = current->differentiate(variable, steps);
        
        if (!derivative) {
            result.success = false;
            result.errorMessage = "Failed to compute derivative at order " + std::to_string(i);
            return result;
        }
        
        current = simplify(std::move(derivative));
        
        allSteps.insert(allSteps.end(), steps.begin(), steps.end());
        allSteps.push_back({"f" + orderSuffix + "(" + variable + ") = " + current->toString(), 
                           "Result (Order " + std::to_string(i) + ")", 
                           "Simplified derivative of order " + std::to_string(i)});
    }
    
    result.derivative = std::move(current);
    result.steps = allSteps;
    result.derivativeExpression = result.derivative->toString();
    result.simplifiedDerivative = result.derivative->toString();
    
    return result;
}

DerivativeResult DerivativeEngine::computePartialDerivative(const std::string& expression, const std::string& variable) {
    // Partial derivatives work the same as regular derivatives
    // The difference is in interpretation - other variables are treated as constants
    auto result = computeDerivative(expression, variable);
    
    if (result.success) {
        // Update the notation to indicate partial derivative
        result.steps.insert(result.steps.begin(), 
            {"∂/∂" + variable + "[" + expression + "]", 
             "Partial Derivative", 
             "Computing partial derivative with respect to " + variable});
    }
    
    return result;
}

double DerivativeEngine::evaluate(const std::string& expression, const std::map<std::string, double>& variables) {
    auto expr = parseExpression(expression);
    if (!expr) {
        return 0.0;
    }
    return expr->evaluate(variables);
}

double DerivativeEngine::evaluate(const ExpressionNode* expr, const std::map<std::string, double>& variables) {
    if (!expr) return 0.0;
    return expr->evaluate(variables);
}

double DerivativeEngine::findZeroNewton(const ExpressionNode* expr, double initialGuess, int maxIterations) {
    // Newton's method: x_{n+1} = x_n - f(x_n) / f'(x_n)
    
    // Compute derivative
    std::vector<DerivativeStep> steps;
    auto derivative = expr->differentiate("x", steps);
    if (!derivative) return initialGuess;
    
    double x = initialGuess;
    const double tolerance = 1e-8;
    
    for (int i = 0; i < maxIterations; i++) {
        std::map<std::string, double> vars = {{"x", x}};
        double fx = expr->evaluate(vars);
        double fpx = derivative->evaluate(vars);
        
        if (std::abs(fpx) < tolerance) {
            // Derivative too small, might be at a critical point or saddle
            break;
        }
        
        double nextX = x - fx / fpx;
        
        if (std::abs(nextX - x) < tolerance) {
            return nextX;
        }
        
        x = nextX;
    }
    
    return x;
}

std::string DerivativeEngine::classifyCriticalPoint(const ExpressionNode* originalFunc, double x) {
    // Use second derivative test
    std::vector<DerivativeStep> steps1, steps2;
    auto firstDeriv = originalFunc->differentiate("x", steps1);
    if (!firstDeriv) return "unknown";
    
    auto secondDeriv = firstDeriv->differentiate("x", steps2);
    if (!secondDeriv) return "unknown";
    
    std::map<std::string, double> vars = {{"x", x}};
    double fpp = secondDeriv->evaluate(vars);
    
    if (std::abs(fpp) < 1e-6) {
        return "saddle or inconclusive";
    }
    else if (fpp > 0) {
        return "local minimum";
    }
    else {
        return "local maximum";
    }
}

std::vector<CriticalPoint> DerivativeEngine::findCriticalPoints(const std::string& expression, double xMin, double xMax, int samples) {
    std::vector<CriticalPoint> criticalPoints;
    
    // Parse the function
    auto func = parseExpression(expression);
    if (!func) return criticalPoints;
    
    // Compute first derivative
    std::vector<DerivativeStep> steps;
    auto derivative = func->differentiate("x", steps);
    if (!derivative) return criticalPoints;
    
    auto simplified = simplify(std::move(derivative));
    
    // Find sign changes in derivative (indicating zeros)
    std::set<double> candidatePoints;
    double dx = (xMax - xMin) / samples;
    
    double prevValue = 0;
    bool prevSet = false;
    
    for (int i = 0; i <= samples; i++) {
        double x = xMin + i * dx;
        std::map<std::string, double> vars = {{"x", x}};
        double value = simplified->evaluate(vars);
        
        if (prevSet && std::signbit(value) != std::signbit(prevValue)) {
            // Sign change detected - there's a zero between prev and current
            double zero = findZeroNewton(simplified.get(), (x + (x - dx)) / 2.0);
            
            if (zero >= xMin && zero <= xMax) {
                candidatePoints.insert(zero);
            }
        }
        
        prevValue = value;
        prevSet = true;
    }
    
    // Also check if derivative is very close to zero at sample points
    for (int i = 0; i <= samples; i++) {
        double x = xMin + i * dx;
        std::map<std::string, double> vars = {{"x", x}};
        double value = simplified->evaluate(vars);
        
        if (std::abs(value) < 1e-6) {
            candidatePoints.insert(x);
        }
    }
    
    // Verify and classify each candidate
    for (double x : candidatePoints) {
        std::map<std::string, double> vars = {{"x", x}};
        double fpx = simplified->evaluate(vars);
        
        // Verify it's actually close to zero
        if (std::abs(fpx) < 0.01) {
            CriticalPoint cp;
            cp.x = x;
            cp.y = func->evaluate(vars);
            cp.type = classifyCriticalPoint(func.get(), x);
            criticalPoints.push_back(cp);
        }
    }
    
    // Remove duplicates (points very close to each other)
    std::vector<CriticalPoint> uniquePoints;
    for (const auto& cp : criticalPoints) {
        bool isDuplicate = false;
        for (const auto& existing : uniquePoints) {
            if (std::abs(cp.x - existing.x) < 0.001) {
                isDuplicate = true;
                break;
            }
        }
        if (!isDuplicate) {
            uniquePoints.push_back(cp);
        }
    }
    
    return uniquePoints;
}

std::vector<InflectionPoint> DerivativeEngine::findInflectionPoints(const std::string& expression, double xMin, double xMax, int samples) {
    std::vector<InflectionPoint> inflectionPoints;
    
    // Parse the function
    auto func = parseExpression(expression);
    if (!func) return inflectionPoints;
    
    // Compute second derivative
    std::vector<DerivativeStep> steps1, steps2;
    auto firstDeriv = func->differentiate("x", steps1);
    if (!firstDeriv) return inflectionPoints;
    
    auto secondDeriv = firstDeriv->differentiate("x", steps2);
    if (!secondDeriv) return inflectionPoints;
    
    auto simplified = simplify(std::move(secondDeriv));
    
    // Find sign changes in second derivative
    std::set<double> candidatePoints;
    double dx = (xMax - xMin) / samples;
    
    double prevValue = 0;
    bool prevSet = false;
    
    for (int i = 0; i <= samples; i++) {
        double x = xMin + i * dx;
        std::map<std::string, double> vars = {{"x", x}};
        double value = simplified->evaluate(vars);
        
        if (prevSet && std::signbit(value) != std::signbit(prevValue)) {
            // Sign change detected
            double zero = findZeroNewton(simplified.get(), (x + (x - dx)) / 2.0);
            
            if (zero >= xMin && zero <= xMax) {
                candidatePoints.insert(zero);
            }
        }
        
        prevValue = value;
        prevSet = true;
    }
    
    // Check sample points
    for (int i = 0; i <= samples; i++) {
        double x = xMin + i * dx;
        std::map<std::string, double> vars = {{"x", x}};
        double value = simplified->evaluate(vars);
        
        if (std::abs(value) < 1e-6) {
            candidatePoints.insert(x);
        }
    }
    
    // Verify each candidate
    for (double x : candidatePoints) {
        std::map<std::string, double> vars = {{"x", x}};
        double fppx = simplified->evaluate(vars);
        
        if (std::abs(fppx) < 0.01) {
            InflectionPoint ip;
            ip.x = x;
            ip.y = func->evaluate(vars);
            inflectionPoints.push_back(ip);
        }
    }
    
    // Remove duplicates
    std::vector<InflectionPoint> uniquePoints;
    for (const auto& ip : inflectionPoints) {
        bool isDuplicate = false;
        for (const auto& existing : uniquePoints) {
            if (std::abs(ip.x - existing.x) < 0.001) {
                isDuplicate = true;
                break;
            }
        }
        if (!isDuplicate) {
            uniquePoints.push_back(ip);
        }
    }
    
    return uniquePoints;
}

std::string DerivativeEngine::formatSteps(const DerivativeResult& result) const {
    if (!result.success) {
        return "Error: " + result.errorMessage;
    }
    
    std::ostringstream oss;
    oss << "DERIVATIVE CALCULATION\n";
    oss << "=====================\n\n";
    
    oss << "Original: " << result.originalExpression << "\n\n";
    
    oss << "STEP-BY-STEP SOLUTION:\n";
    oss << "----------------------\n\n";
    
    int stepNum = 1;
    for (const auto& step : result.steps) {
        oss << "Step " << stepNum++ << ": " << step.rule << "\n";
        oss << "  " << step.explanation << "\n";
        if (!step.expression.empty()) {
            oss << "  → " << step.expression << "\n";
        }
        oss << "\n";
    }
    
    oss << "FINAL RESULT:\n";
    oss << "-------------\n";
    oss << "f'(x) = " << result.simplifiedDerivative << "\n";
    
    return oss.str();
}

} // namespace Calculus
