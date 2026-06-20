#ifndef EXPRESSIONTREE_H
#define EXPRESSIONTREE_H

#include <memory>
#include <string>
#include <vector>
#include <map>

namespace Calculus {

enum class NodeType {
    Number,
    Variable,
    Add,
    Subtract,
    Multiply,
    Divide,
    Power,
    Sin,
    Cos,
    Tan,
    Exp,
    Log,
    Ln,
    Sqrt,
    Negate
};

struct DerivativeStep {
    std::string expression;
    std::string rule;
    std::string explanation;
};

class ExpressionNode {
public:
    virtual ~ExpressionNode() = default;
    
    virtual NodeType getType() const = 0;
    virtual double evaluate(const std::map<std::string, double>& variables) const = 0;
    virtual std::unique_ptr<ExpressionNode> clone() const = 0;
    virtual std::string toString() const = 0;
    virtual std::unique_ptr<ExpressionNode> differentiate(const std::string& variable, std::vector<DerivativeStep>& steps) const = 0;
    virtual std::unique_ptr<ExpressionNode> simplify() const = 0;
    virtual bool isConstant(const std::string& variable) const = 0;
    virtual bool equals(const ExpressionNode* other) const = 0;
};

// Number node (constants)
class NumberNode : public ExpressionNode {
private:
    double value;

public:
    NumberNode(double val) : value(val) {}
    
    double getValue() const { return value; }
    
    NodeType getType() const override { return NodeType::Number; }
    double evaluate(const std::map<std::string, double>& variables) const override;
    std::unique_ptr<ExpressionNode> clone() const override;
    std::string toString() const override;
    std::unique_ptr<ExpressionNode> differentiate(const std::string& variable, std::vector<DerivativeStep>& steps) const override;
    std::unique_ptr<ExpressionNode> simplify() const override;
    bool isConstant(const std::string& variable) const override { return true; }
    bool equals(const ExpressionNode* other) const override;
};

// Variable node (x, y, etc.)
class VariableNode : public ExpressionNode {
private:
    std::string name;

public:
    VariableNode(const std::string& varName) : name(varName) {}
    
    std::string getName() const { return name; }
    
    NodeType getType() const override { return NodeType::Variable; }
    double evaluate(const std::map<std::string, double>& variables) const override;
    std::unique_ptr<ExpressionNode> clone() const override;
    std::string toString() const override;
    std::unique_ptr<ExpressionNode> differentiate(const std::string& variable, std::vector<DerivativeStep>& steps) const override;
    std::unique_ptr<ExpressionNode> simplify() const override;
    bool isConstant(const std::string& variable) const override { return name != variable; }
    bool equals(const ExpressionNode* other) const override;
};

// Binary operation node (+, -, *, /, ^)
class BinaryOpNode : public ExpressionNode {
private:
    NodeType type;
    std::unique_ptr<ExpressionNode> left;
    std::unique_ptr<ExpressionNode> right;

public:
    BinaryOpNode(NodeType op, std::unique_ptr<ExpressionNode> l, std::unique_ptr<ExpressionNode> r)
        : type(op), left(std::move(l)), right(std::move(r)) {}
    
    const ExpressionNode* getLeft() const { return left.get(); }
    const ExpressionNode* getRight() const { return right.get(); }
    
    NodeType getType() const override { return type; }
    double evaluate(const std::map<std::string, double>& variables) const override;
    std::unique_ptr<ExpressionNode> clone() const override;
    std::string toString() const override;
    std::unique_ptr<ExpressionNode> differentiate(const std::string& variable, std::vector<DerivativeStep>& steps) const override;
    std::unique_ptr<ExpressionNode> simplify() const override;
    bool isConstant(const std::string& variable) const override;
    bool equals(const ExpressionNode* other) const override;

private:
    std::string getOperatorSymbol() const;
};

// Unary operation node (sin, cos, tan, exp, log, sqrt, negate)
class UnaryOpNode : public ExpressionNode {
private:
    NodeType type;
    std::unique_ptr<ExpressionNode> operand;

public:
    UnaryOpNode(NodeType op, std::unique_ptr<ExpressionNode> expr)
        : type(op), operand(std::move(expr)) {}
    
    const ExpressionNode* getOperand() const { return operand.get(); }
    
    NodeType getType() const override { return type; }
    double evaluate(const std::map<std::string, double>& variables) const override;
    std::unique_ptr<ExpressionNode> clone() const override;
    std::string toString() const override;
    std::unique_ptr<ExpressionNode> differentiate(const std::string& variable, std::vector<DerivativeStep>& steps) const override;
    std::unique_ptr<ExpressionNode> simplify() const override;
    bool isConstant(const std::string& variable) const override;
    bool equals(const ExpressionNode* other) const override;

private:
    std::string getFunctionName() const;
};

// Helper functions for creating nodes
std::unique_ptr<ExpressionNode> makeNumber(double value);
std::unique_ptr<ExpressionNode> makeVariable(const std::string& name);
std::unique_ptr<ExpressionNode> makeAdd(std::unique_ptr<ExpressionNode> left, std::unique_ptr<ExpressionNode> right);
std::unique_ptr<ExpressionNode> makeSubtract(std::unique_ptr<ExpressionNode> left, std::unique_ptr<ExpressionNode> right);
std::unique_ptr<ExpressionNode> makeMultiply(std::unique_ptr<ExpressionNode> left, std::unique_ptr<ExpressionNode> right);
std::unique_ptr<ExpressionNode> makeDivide(std::unique_ptr<ExpressionNode> left, std::unique_ptr<ExpressionNode> right);
std::unique_ptr<ExpressionNode> makePower(std::unique_ptr<ExpressionNode> base, std::unique_ptr<ExpressionNode> exponent);
std::unique_ptr<ExpressionNode> makeSin(std::unique_ptr<ExpressionNode> expr);
std::unique_ptr<ExpressionNode> makeCos(std::unique_ptr<ExpressionNode> expr);
std::unique_ptr<ExpressionNode> makeTan(std::unique_ptr<ExpressionNode> expr);
std::unique_ptr<ExpressionNode> makeExp(std::unique_ptr<ExpressionNode> expr);
std::unique_ptr<ExpressionNode> makeLog(std::unique_ptr<ExpressionNode> expr);
std::unique_ptr<ExpressionNode> makeLn(std::unique_ptr<ExpressionNode> expr);
std::unique_ptr<ExpressionNode> makeSqrt(std::unique_ptr<ExpressionNode> expr);
std::unique_ptr<ExpressionNode> makeNegate(std::unique_ptr<ExpressionNode> expr);

} // namespace Calculus

#endif // EXPRESSIONTREE_H
