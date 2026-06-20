#ifndef DERIVATIVEENGINE_H
#define DERIVATIVEENGINE_H

#include "ExpressionTree.h"
#include "FunctionParser.h"
#include <string>
#include <vector>
#include <memory>
#include <map>

namespace Calculus {

struct DerivativeResult {
    std::unique_ptr<ExpressionNode> expression;
    std::unique_ptr<ExpressionNode> derivative;
    std::vector<DerivativeStep> steps;
    std::string originalExpression;
    std::string derivativeExpression;
    std::string simplifiedDerivative;
    bool success;
    std::string errorMessage;
};

struct CriticalPoint {
    double x;
    double y;
    std::string type; // "local min", "local max", "saddle", "unknown"
};

struct InflectionPoint {
    double x;
    double y;
};

class DerivativeEngine {
public:
    DerivativeEngine();
    
    // Parse and compute derivative with step-by-step explanations
    DerivativeResult computeDerivative(const std::string& expression, const std::string& variable = "x");
    
    // Compute higher-order derivatives
    DerivativeResult computeNthDerivative(const std::string& expression, int order, const std::string& variable = "x");
    
    // Partial derivative (specify which variable to differentiate with respect to)
    DerivativeResult computePartialDerivative(const std::string& expression, const std::string& variable);
    
    // Evaluate expression at a point
    double evaluate(const std::string& expression, const std::map<std::string, double>& variables);
    double evaluate(const ExpressionNode* expr, const std::map<std::string, double>& variables);
    
    // Find critical points where f'(x) = 0 in a range
    std::vector<CriticalPoint> findCriticalPoints(const std::string& expression, double xMin, double xMax, int samples = 1000);
    
    // Find inflection points where f''(x) = 0 in a range
    std::vector<InflectionPoint> findInflectionPoints(const std::string& expression, double xMin, double xMax, int samples = 1000);
    
    // Get formatted step-by-step solution
    std::string formatSteps(const DerivativeResult& result) const;
    
    // Simplify an expression
    std::unique_ptr<ExpressionNode> simplify(std::unique_ptr<ExpressionNode> expr);
    
    // Parse an expression
    std::unique_ptr<ExpressionNode> parseExpression(const std::string& expression);
    
    // Get last error
    std::string getLastError() const { return lastError; }

private:
    FunctionParser parser;
    std::string lastError;
    
    // Helper methods
    void setError(const std::string& message);
    double findZeroNewton(const ExpressionNode* expr, double initialGuess, int maxIterations = 50);
    std::string classifyCriticalPoint(const ExpressionNode* originalFunc, double x);
};

} // namespace Calculus

#endif // DERIVATIVEENGINE_H
