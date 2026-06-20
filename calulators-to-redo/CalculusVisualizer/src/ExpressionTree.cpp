#include "ExpressionTree.h"
#include <cmath>
#include <sstream>
#include <iomanip>

namespace Calculus {

// Helper to format numbers nicely
static std::string formatNumber(double value) {
    if (std::abs(value - std::round(value)) < 1e-10) {
        return std::to_string((int)std::round(value));
    }
    std::ostringstream oss;
    oss << std::setprecision(6) << std::noshowpoint << value;
    return oss.str();
}

// NumberNode implementation
double NumberNode::evaluate(const std::map<std::string, double>& variables) const {
    return value;
}

std::unique_ptr<ExpressionNode> NumberNode::clone() const {
    return std::make_unique<NumberNode>(value);
}

std::string NumberNode::toString() const {
    return formatNumber(value);
}

std::unique_ptr<ExpressionNode> NumberNode::differentiate(const std::string& variable, std::vector<DerivativeStep>& steps) const {
    steps.push_back({toString(), "Constant Rule", "The derivative of a constant is 0"});
    return std::make_unique<NumberNode>(0);
}

std::unique_ptr<ExpressionNode> NumberNode::simplify() const {
    return clone();
}

bool NumberNode::equals(const ExpressionNode* other) const {
    if (other->getType() != NodeType::Number) return false;
    const NumberNode* num = static_cast<const NumberNode*>(other);
    return std::abs(value - num->value) < 1e-10;
}

// VariableNode implementation
double VariableNode::evaluate(const std::map<std::string, double>& variables) const {
    auto it = variables.find(name);
    if (it != variables.end()) {
        return it->second;
    }
    return 0.0; // Default value if variable not found
}

std::unique_ptr<ExpressionNode> VariableNode::clone() const {
    return std::make_unique<VariableNode>(name);
}

std::string VariableNode::toString() const {
    return name;
}

std::unique_ptr<ExpressionNode> VariableNode::differentiate(const std::string& variable, std::vector<DerivativeStep>& steps) const {
    if (name == variable) {
        steps.push_back({toString(), "Power Rule", "d/d" + variable + "(" + variable + ") = 1"});
        return std::make_unique<NumberNode>(1);
    } else {
        steps.push_back({toString(), "Constant Rule", variable + " is treated as constant with respect to " + name});
        return std::make_unique<NumberNode>(0);
    }
}

std::unique_ptr<ExpressionNode> VariableNode::simplify() const {
    return clone();
}

bool VariableNode::equals(const ExpressionNode* other) const {
    if (other->getType() != NodeType::Variable) return false;
    const VariableNode* var = static_cast<const VariableNode*>(other);
    return name == var->name;
}

// BinaryOpNode implementation
std::string BinaryOpNode::getOperatorSymbol() const {
    switch (type) {
        case NodeType::Add: return "+";
        case NodeType::Subtract: return "-";
        case NodeType::Multiply: return "*";
        case NodeType::Divide: return "/";
        case NodeType::Power: return "^";
        default: return "?";
    }
}

double BinaryOpNode::evaluate(const std::map<std::string, double>& variables) const {
    double l = left->evaluate(variables);
    double r = right->evaluate(variables);
    
    switch (type) {
        case NodeType::Add: return l + r;
        case NodeType::Subtract: return l - r;
        case NodeType::Multiply: return l * r;
        case NodeType::Divide: return r != 0 ? l / r : 0;
        case NodeType::Power: return std::pow(l, r);
        default: return 0;
    }
}

std::unique_ptr<ExpressionNode> BinaryOpNode::clone() const {
    return std::make_unique<BinaryOpNode>(type, left->clone(), right->clone());
}

std::string BinaryOpNode::toString() const {
    std::string leftStr = left->toString();
    std::string rightStr = right->toString();
    std::string op = getOperatorSymbol();
    
    // Add parentheses based on precedence
    if (type == NodeType::Multiply || type == NodeType::Divide) {
        if (left->getType() == NodeType::Add || left->getType() == NodeType::Subtract) {
            leftStr = "(" + leftStr + ")";
        }
        if (right->getType() == NodeType::Add || right->getType() == NodeType::Subtract) {
            rightStr = "(" + rightStr + ")";
        }
    }
    
    if (type == NodeType::Power) {
        if (left->getType() == NodeType::Add || left->getType() == NodeType::Subtract ||
            left->getType() == NodeType::Multiply || left->getType() == NodeType::Divide) {
            leftStr = "(" + leftStr + ")";
        }
        return leftStr + "^" + rightStr;
    }
    
    return leftStr + " " + op + " " + rightStr;
}

std::unique_ptr<ExpressionNode> BinaryOpNode::differentiate(const std::string& variable, std::vector<DerivativeStep>& steps) const {
    std::string originalExpr = toString();
    
    switch (type) {
        case NodeType::Add: {
            // Sum rule: (f + g)' = f' + g'
            steps.push_back({originalExpr, "Sum Rule", "d/d" + variable + "(" + left->toString() + " + " + right->toString() + ") = d/d" + variable + "(" + left->toString() + ") + d/d" + variable + "(" + right->toString() + ")"});
            
            std::vector<DerivativeStep> leftSteps, rightSteps;
            auto leftDeriv = left->differentiate(variable, leftSteps);
            auto rightDeriv = right->differentiate(variable, rightSteps);
            
            steps.insert(steps.end(), leftSteps.begin(), leftSteps.end());
            steps.insert(steps.end(), rightSteps.begin(), rightSteps.end());
            
            return makeAdd(std::move(leftDeriv), std::move(rightDeriv));
        }
        
        case NodeType::Subtract: {
            // Difference rule: (f - g)' = f' - g'
            steps.push_back({originalExpr, "Difference Rule", "d/d" + variable + "(" + left->toString() + " - " + right->toString() + ") = d/d" + variable + "(" + left->toString() + ") - d/d" + variable + "(" + right->toString() + ")"});
            
            std::vector<DerivativeStep> leftSteps, rightSteps;
            auto leftDeriv = left->differentiate(variable, leftSteps);
            auto rightDeriv = right->differentiate(variable, rightSteps);
            
            steps.insert(steps.end(), leftSteps.begin(), leftSteps.end());
            steps.insert(steps.end(), rightSteps.begin(), rightSteps.end());
            
            return makeSubtract(std::move(leftDeriv), std::move(rightDeriv));
        }
        
        case NodeType::Multiply: {
            // Product rule: (f * g)' = f' * g + f * g'
            steps.push_back({originalExpr, "Product Rule", "d/d" + variable + "(" + left->toString() + " * " + right->toString() + ") = [d/d" + variable + "(" + left->toString() + ")] * " + right->toString() + " + " + left->toString() + " * [d/d" + variable + "(" + right->toString() + ")]"});
            
            std::vector<DerivativeStep> leftSteps, rightSteps;
            auto leftDeriv = left->differentiate(variable, leftSteps);
            auto rightDeriv = right->differentiate(variable, rightSteps);
            
            steps.insert(steps.end(), leftSteps.begin(), leftSteps.end());
            steps.insert(steps.end(), rightSteps.begin(), rightSteps.end());
            
            // f' * g + f * g'
            auto term1 = makeMultiply(std::move(leftDeriv), right->clone());
            auto term2 = makeMultiply(left->clone(), std::move(rightDeriv));
            return makeAdd(std::move(term1), std::move(term2));
        }
        
        case NodeType::Divide: {
            // Quotient rule: (f / g)' = (f' * g - f * g') / g^2
            steps.push_back({originalExpr, "Quotient Rule", "d/d" + variable + "(" + left->toString() + " / " + right->toString() + ") = ([d/d" + variable + "(" + left->toString() + ")] * " + right->toString() + " - " + left->toString() + " * [d/d" + variable + "(" + right->toString() + ")]) / (" + right->toString() + ")^2"});
            
            std::vector<DerivativeStep> leftSteps, rightSteps;
            auto leftDeriv = left->differentiate(variable, leftSteps);
            auto rightDeriv = right->differentiate(variable, rightSteps);
            
            steps.insert(steps.end(), leftSteps.begin(), leftSteps.end());
            steps.insert(steps.end(), rightSteps.begin(), rightSteps.end());
            
            // (f' * g - f * g') / g^2
            auto numeratorTerm1 = makeMultiply(std::move(leftDeriv), right->clone());
            auto numeratorTerm2 = makeMultiply(left->clone(), std::move(rightDeriv));
            auto numerator = makeSubtract(std::move(numeratorTerm1), std::move(numeratorTerm2));
            auto denominator = makePower(right->clone(), makeNumber(2));
            return makeDivide(std::move(numerator), std::move(denominator));
        }
        
        case NodeType::Power: {
            // Power rule with chain rule
            if (right->isConstant(variable) && left->isConstant(variable)) {
                // Both constant - derivative is 0
                steps.push_back({originalExpr, "Constant Rule", "Both base and exponent are constants"});
                return makeNumber(0);
            }
            else if (right->isConstant(variable)) {
                // f(x)^n where n is constant - Power rule + chain rule
                steps.push_back({originalExpr, "Power Rule + Chain Rule", "d/d" + variable + "[(" + left->toString() + ")^" + right->toString() + "] = " + right->toString() + " * (" + left->toString() + ")^(" + right->toString() + " - 1) * d/d" + variable + "(" + left->toString() + ")"});
                
                std::vector<DerivativeStep> baseSteps;
                auto baseDeriv = left->differentiate(variable, baseSteps);
                steps.insert(steps.end(), baseSteps.begin(), baseSteps.end());
                
                // n * f^(n-1) * f'
                auto exponentMinusOne = makeSubtract(right->clone(), makeNumber(1));
                auto powerTerm = makePower(left->clone(), std::move(exponentMinusOne));
                auto coeffTerm = makeMultiply(right->clone(), std::move(powerTerm));
                return makeMultiply(std::move(coeffTerm), std::move(baseDeriv));
            }
            else if (left->isConstant(variable)) {
                // a^g(x) where a is constant - Exponential rule
                steps.push_back({originalExpr, "Exponential Rule", "d/d" + variable + "[" + left->toString() + "^(" + right->toString() + ")] = " + left->toString() + "^(" + right->toString() + ") * ln(" + left->toString() + ") * d/d" + variable + "(" + right->toString() + ")"});
                
                std::vector<DerivativeStep> expSteps;
                auto expDeriv = right->differentiate(variable, expSteps);
                steps.insert(steps.end(), expSteps.begin(), expSteps.end());
                
                // a^g * ln(a) * g'
                auto lnBase = makeLn(left->clone());
                auto powerClone = makePower(left->clone(), right->clone());
                auto term = makeMultiply(std::move(powerClone), std::move(lnBase));
                return makeMultiply(std::move(term), std::move(expDeriv));
            }
            else {
                // f(x)^g(x) - General power rule: d/dx[f^g] = f^g * (g' * ln(f) + g * f'/f)
                steps.push_back({originalExpr, "General Power Rule", "d/d" + variable + "[f^g] = f^g * (g' * ln(f) + g * f'/f)"});
                
                std::vector<DerivativeStep> baseSteps, expSteps;
                auto baseDeriv = left->differentiate(variable, baseSteps);
                auto expDeriv = right->differentiate(variable, expSteps);
                steps.insert(steps.end(), baseSteps.begin(), baseSteps.end());
                steps.insert(steps.end(), expSteps.begin(), expSteps.end());
                
                // f^g * (g' * ln(f) + g * f'/f)
                auto lnBase = makeLn(left->clone());
                auto term1 = makeMultiply(std::move(expDeriv), std::move(lnBase));
                auto fPrimeOverF = makeDivide(std::move(baseDeriv), left->clone());
                auto term2 = makeMultiply(right->clone(), std::move(fPrimeOverF));
                auto bracket = makeAdd(std::move(term1), std::move(term2));
                auto power = makePower(left->clone(), right->clone());
                return makeMultiply(std::move(power), std::move(bracket));
            }
        }
        
        default:
            return makeNumber(0);
    }
}

std::unique_ptr<ExpressionNode> BinaryOpNode::simplify() const {
    auto leftSimp = left->simplify();
    auto rightSimp = right->simplify();
    
    // Check if both are numbers
    if (leftSimp->getType() == NodeType::Number && rightSimp->getType() == NodeType::Number) {
        double l = static_cast<NumberNode*>(leftSimp.get())->getValue();
        double r = static_cast<NumberNode*>(rightSimp.get())->getValue();
        
        switch (type) {
            case NodeType::Add: return makeNumber(l + r);
            case NodeType::Subtract: return makeNumber(l - r);
            case NodeType::Multiply: return makeNumber(l * r);
            case NodeType::Divide: return r != 0 ? makeNumber(l / r) : makeDivide(std::move(leftSimp), std::move(rightSimp));
            case NodeType::Power: return makeNumber(std::pow(l, r));
            default: break;
        }
    }
    
    // Algebraic simplifications
    if (type == NodeType::Add) {
        if (leftSimp->getType() == NodeType::Number && static_cast<NumberNode*>(leftSimp.get())->getValue() == 0) {
            return rightSimp;
        }
        if (rightSimp->getType() == NodeType::Number && static_cast<NumberNode*>(rightSimp.get())->getValue() == 0) {
            return leftSimp;
        }
    }
    
    if (type == NodeType::Subtract) {
        if (rightSimp->getType() == NodeType::Number && static_cast<NumberNode*>(rightSimp.get())->getValue() == 0) {
            return leftSimp;
        }
    }
    
    if (type == NodeType::Multiply) {
        if (leftSimp->getType() == NodeType::Number) {
            double val = static_cast<NumberNode*>(leftSimp.get())->getValue();
            if (val == 0) return makeNumber(0);
            if (val == 1) return rightSimp;
        }
        if (rightSimp->getType() == NodeType::Number) {
            double val = static_cast<NumberNode*>(rightSimp.get())->getValue();
            if (val == 0) return makeNumber(0);
            if (val == 1) return leftSimp;
        }
    }
    
    if (type == NodeType::Divide) {
        if (rightSimp->getType() == NodeType::Number && static_cast<NumberNode*>(rightSimp.get())->getValue() == 1) {
            return leftSimp;
        }
        if (leftSimp->getType() == NodeType::Number && static_cast<NumberNode*>(leftSimp.get())->getValue() == 0) {
            return makeNumber(0);
        }
    }
    
    if (type == NodeType::Power) {
        if (rightSimp->getType() == NodeType::Number) {
            double exp = static_cast<NumberNode*>(rightSimp.get())->getValue();
            if (exp == 0) return makeNumber(1);
            if (exp == 1) return leftSimp;
        }
    }
    
    return std::make_unique<BinaryOpNode>(type, std::move(leftSimp), std::move(rightSimp));
}

bool BinaryOpNode::isConstant(const std::string& variable) const {
    return left->isConstant(variable) && right->isConstant(variable);
}

bool BinaryOpNode::equals(const ExpressionNode* other) const {
    if (other->getType() != type) return false;
    const BinaryOpNode* bin = static_cast<const BinaryOpNode*>(other);
    return left->equals(bin->left.get()) && right->equals(bin->right.get());
}

// UnaryOpNode implementation
std::string UnaryOpNode::getFunctionName() const {
    switch (type) {
        case NodeType::Sin: return "sin";
        case NodeType::Cos: return "cos";
        case NodeType::Tan: return "tan";
        case NodeType::Exp: return "exp";
        case NodeType::Log: return "log";
        case NodeType::Ln: return "ln";
        case NodeType::Sqrt: return "sqrt";
        case NodeType::Negate: return "-";
        default: return "?";
    }
}

double UnaryOpNode::evaluate(const std::map<std::string, double>& variables) const {
    double val = operand->evaluate(variables);
    
    switch (type) {
        case NodeType::Sin: return std::sin(val);
        case NodeType::Cos: return std::cos(val);
        case NodeType::Tan: return std::tan(val);
        case NodeType::Exp: return std::exp(val);
        case NodeType::Log: return std::log10(val);
        case NodeType::Ln: return std::log(val);
        case NodeType::Sqrt: return std::sqrt(val);
        case NodeType::Negate: return -val;
        default: return 0;
    }
}

std::unique_ptr<ExpressionNode> UnaryOpNode::clone() const {
    return std::make_unique<UnaryOpNode>(type, operand->clone());
}

std::string UnaryOpNode::toString() const {
    if (type == NodeType::Negate) {
        return "-" + operand->toString();
    }
    return getFunctionName() + "(" + operand->toString() + ")";
}

std::unique_ptr<ExpressionNode> UnaryOpNode::differentiate(const std::string& variable, std::vector<DerivativeStep>& steps) const {
    std::string originalExpr = toString();
    
    switch (type) {
        case NodeType::Sin: {
            // d/dx[sin(f)] = cos(f) * f'
            steps.push_back({originalExpr, "Chain Rule (sin)", "d/d" + variable + "[sin(" + operand->toString() + ")] = cos(" + operand->toString() + ") * d/d" + variable + "(" + operand->toString() + ")"});
            
            std::vector<DerivativeStep> innerSteps;
            auto innerDeriv = operand->differentiate(variable, innerSteps);
            steps.insert(steps.end(), innerSteps.begin(), innerSteps.end());
            
            auto cosInner = makeCos(operand->clone());
            return makeMultiply(std::move(cosInner), std::move(innerDeriv));
        }
        
        case NodeType::Cos: {
            // d/dx[cos(f)] = -sin(f) * f'
            steps.push_back({originalExpr, "Chain Rule (cos)", "d/d" + variable + "[cos(" + operand->toString() + ")] = -sin(" + operand->toString() + ") * d/d" + variable + "(" + operand->toString() + ")"});
            
            std::vector<DerivativeStep> innerSteps;
            auto innerDeriv = operand->differentiate(variable, innerSteps);
            steps.insert(steps.end(), innerSteps.begin(), innerSteps.end());
            
            auto sinInner = makeSin(operand->clone());
            auto negSin = makeNegate(std::move(sinInner));
            return makeMultiply(std::move(negSin), std::move(innerDeriv));
        }
        
        case NodeType::Tan: {
            // d/dx[tan(f)] = sec^2(f) * f' = (1/cos^2(f)) * f'
            steps.push_back({originalExpr, "Chain Rule (tan)", "d/d" + variable + "[tan(" + operand->toString() + ")] = sec²(" + operand->toString() + ") * d/d" + variable + "(" + operand->toString() + ") = [1/cos²(" + operand->toString() + ")] * d/d" + variable + "(" + operand->toString() + ")"});
            
            std::vector<DerivativeStep> innerSteps;
            auto innerDeriv = operand->differentiate(variable, innerSteps);
            steps.insert(steps.end(), innerSteps.begin(), innerSteps.end());
            
            auto cosInner = makeCos(operand->clone());
            auto cosSquared = makePower(std::move(cosInner), makeNumber(2));
            auto sec2 = makeDivide(makeNumber(1), std::move(cosSquared));
            return makeMultiply(std::move(sec2), std::move(innerDeriv));
        }
        
        case NodeType::Exp: {
            // d/dx[e^f] = e^f * f'
            steps.push_back({originalExpr, "Chain Rule (exp)", "d/d" + variable + "[e^(" + operand->toString() + ")] = e^(" + operand->toString() + ") * d/d" + variable + "(" + operand->toString() + ")"});
            
            std::vector<DerivativeStep> innerSteps;
            auto innerDeriv = operand->differentiate(variable, innerSteps);
            steps.insert(steps.end(), innerSteps.begin(), innerSteps.end());
            
            auto expInner = makeExp(operand->clone());
            return makeMultiply(std::move(expInner), std::move(innerDeriv));
        }
        
        case NodeType::Ln: {
            // d/dx[ln(f)] = f'/f
            steps.push_back({originalExpr, "Chain Rule (ln)", "d/d" + variable + "[ln(" + operand->toString() + ")] = [d/d" + variable + "(" + operand->toString() + ")] / " + operand->toString()});
            
            std::vector<DerivativeStep> innerSteps;
            auto innerDeriv = operand->differentiate(variable, innerSteps);
            steps.insert(steps.end(), innerSteps.begin(), innerSteps.end());
            
            return makeDivide(std::move(innerDeriv), operand->clone());
        }
        
        case NodeType::Log: {
            // d/dx[log10(f)] = f'/(f * ln(10))
            steps.push_back({originalExpr, "Chain Rule (log)", "d/d" + variable + "[log(" + operand->toString() + ")] = [d/d" + variable + "(" + operand->toString() + ")] / (" + operand->toString() + " * ln(10))"});
            
            std::vector<DerivativeStep> innerSteps;
            auto innerDeriv = operand->differentiate(variable, innerSteps);
            steps.insert(steps.end(), innerSteps.begin(), innerSteps.end());
            
            auto ln10 = makeNumber(std::log(10));
            auto denominator = makeMultiply(operand->clone(), std::move(ln10));
            return makeDivide(std::move(innerDeriv), std::move(denominator));
        }
        
        case NodeType::Sqrt: {
            // d/dx[sqrt(f)] = d/dx[f^(1/2)] = (1/2) * f^(-1/2) * f' = f'/(2*sqrt(f))
            steps.push_back({originalExpr, "Chain Rule (sqrt)", "d/d" + variable + "[√(" + operand->toString() + ")] = [d/d" + variable + "(" + operand->toString() + ")] / (2 * √(" + operand->toString() + "))"});
            
            std::vector<DerivativeStep> innerSteps;
            auto innerDeriv = operand->differentiate(variable, innerSteps);
            steps.insert(steps.end(), innerSteps.begin(), innerSteps.end());
            
            auto sqrtInner = makeSqrt(operand->clone());
            auto twoSqrt = makeMultiply(makeNumber(2), std::move(sqrtInner));
            return makeDivide(std::move(innerDeriv), std::move(twoSqrt));
        }
        
        case NodeType::Negate: {
            // d/dx[-f] = -f'
            steps.push_back({originalExpr, "Constant Multiple Rule", "d/d" + variable + "[-(" + operand->toString() + ")] = -[d/d" + variable + "(" + operand->toString() + ")]"});
            
            std::vector<DerivativeStep> innerSteps;
            auto innerDeriv = operand->differentiate(variable, innerSteps);
            steps.insert(steps.end(), innerSteps.begin(), innerSteps.end());
            
            return makeNegate(std::move(innerDeriv));
        }
        
        default:
            return makeNumber(0);
    }
}

std::unique_ptr<ExpressionNode> UnaryOpNode::simplify() const {
    auto innerSimp = operand->simplify();
    
    if (innerSimp->getType() == NodeType::Number) {
        double val = static_cast<NumberNode*>(innerSimp.get())->getValue();
        
        switch (type) {
            case NodeType::Sin: return makeNumber(std::sin(val));
            case NodeType::Cos: return makeNumber(std::cos(val));
            case NodeType::Tan: return makeNumber(std::tan(val));
            case NodeType::Exp: return makeNumber(std::exp(val));
            case NodeType::Log: return makeNumber(std::log10(val));
            case NodeType::Ln: return makeNumber(std::log(val));
            case NodeType::Sqrt: return makeNumber(std::sqrt(val));
            case NodeType::Negate: return makeNumber(-val);
            default: break;
        }
    }
    
    return std::make_unique<UnaryOpNode>(type, std::move(innerSimp));
}

bool UnaryOpNode::isConstant(const std::string& variable) const {
    return operand->isConstant(variable);
}

bool UnaryOpNode::equals(const ExpressionNode* other) const {
    if (other->getType() != type) return false;
    const UnaryOpNode* unary = static_cast<const UnaryOpNode*>(other);
    return operand->equals(unary->operand.get());
}

// Helper functions
std::unique_ptr<ExpressionNode> makeNumber(double value) {
    return std::make_unique<NumberNode>(value);
}

std::unique_ptr<ExpressionNode> makeVariable(const std::string& name) {
    return std::make_unique<VariableNode>(name);
}

std::unique_ptr<ExpressionNode> makeAdd(std::unique_ptr<ExpressionNode> left, std::unique_ptr<ExpressionNode> right) {
    return std::make_unique<BinaryOpNode>(NodeType::Add, std::move(left), std::move(right));
}

std::unique_ptr<ExpressionNode> makeSubtract(std::unique_ptr<ExpressionNode> left, std::unique_ptr<ExpressionNode> right) {
    return std::make_unique<BinaryOpNode>(NodeType::Subtract, std::move(left), std::move(right));
}

std::unique_ptr<ExpressionNode> makeMultiply(std::unique_ptr<ExpressionNode> left, std::unique_ptr<ExpressionNode> right) {
    return std::make_unique<BinaryOpNode>(NodeType::Multiply, std::move(left), std::move(right));
}

std::unique_ptr<ExpressionNode> makeDivide(std::unique_ptr<ExpressionNode> left, std::unique_ptr<ExpressionNode> right) {
    return std::make_unique<BinaryOpNode>(NodeType::Divide, std::move(left), std::move(right));
}

std::unique_ptr<ExpressionNode> makePower(std::unique_ptr<ExpressionNode> base, std::unique_ptr<ExpressionNode> exponent) {
    return std::make_unique<BinaryOpNode>(NodeType::Power, std::move(base), std::move(exponent));
}

std::unique_ptr<ExpressionNode> makeSin(std::unique_ptr<ExpressionNode> expr) {
    return std::make_unique<UnaryOpNode>(NodeType::Sin, std::move(expr));
}

std::unique_ptr<ExpressionNode> makeCos(std::unique_ptr<ExpressionNode> expr) {
    return std::make_unique<UnaryOpNode>(NodeType::Cos, std::move(expr));
}

std::unique_ptr<ExpressionNode> makeTan(std::unique_ptr<ExpressionNode> expr) {
    return std::make_unique<UnaryOpNode>(NodeType::Tan, std::move(expr));
}

std::unique_ptr<ExpressionNode> makeExp(std::unique_ptr<ExpressionNode> expr) {
    return std::make_unique<UnaryOpNode>(NodeType::Exp, std::move(expr));
}

std::unique_ptr<ExpressionNode> makeLog(std::unique_ptr<ExpressionNode> expr) {
    return std::make_unique<UnaryOpNode>(NodeType::Log, std::move(expr));
}

std::unique_ptr<ExpressionNode> makeLn(std::unique_ptr<ExpressionNode> expr) {
    return std::make_unique<UnaryOpNode>(NodeType::Ln, std::move(expr));
}

std::unique_ptr<ExpressionNode> makeSqrt(std::unique_ptr<ExpressionNode> expr) {
    return std::make_unique<UnaryOpNode>(NodeType::Sqrt, std::move(expr));
}

std::unique_ptr<ExpressionNode> makeNegate(std::unique_ptr<ExpressionNode> expr) {
    return std::make_unique<UnaryOpNode>(NodeType::Negate, std::move(expr));
}

} // namespace Calculus
