/**
 * ExpressionParser.cpp - Simple recursive descent parser for math expressions
 */

#include "ExpressionParser.h"
#include <QRegularExpression>
#include <cmath>

const QMap<QString, double> ExpressionParser::constants = {
    {"pi", M_PI},
    {"e", M_E},
    {"π", M_PI}
};

ExpressionParser::ExpressionParser()
{
}

double ExpressionParser::evaluate(const QString &expression, double x)
{
    try {
        QString processed = preprocessExpression(expression);
        processed.replace("x", QString::number(x, 'g', 15));
        
        int pos = 0;
        double result = parseTerm(processed, pos, x);
        
        skipWhitespace(processed, pos);
        if (pos < processed.length()) {
            lastError = "Unexpected characters at end of expression";
            return NAN;
        }
        
        return result;
        
    } catch (...) {
        lastError = "Error evaluating expression";
        return NAN;
    }
}

bool ExpressionParser::isValid(const QString &expression)
{
    double result = evaluate(expression, 0);
    return std::isfinite(result);
}

QString ExpressionParser::getLastError() const
{
    return lastError;
}

QString ExpressionParser::preprocessExpression(const QString &expr)
{
    QString result = expr.toLower();
    
    // Replace common patterns
    result.replace("^", "**");
    result.replace(" ", "");
    
    // Replace constants
    for (auto it = constants.begin(); it != constants.end(); ++it) {
        result.replace(it.key(), QString::number(it.value(), 'g', 15));
    }
    
    // Insert implicit multiplication
    QRegularExpression re(R"((\d)([a-z(]))");
    result.replace(re, "\\1*\\2");
    
    return result;
}

void ExpressionParser::skipWhitespace(const QString &expr, int &pos)
{
    while (pos < expr.length() && expr[pos].isSpace()) {
        pos++;
    }
}

double ExpressionParser::parseTerm(const QString &expr, int &pos, double x)
{
    skipWhitespace(expr, pos);
    double result = parseFactor(expr, pos, x);
    
    while (pos < expr.length()) {
        skipWhitespace(expr, pos);
        if (pos >= expr.length()) break;
        
        QChar op = expr[pos];
        if (op == '+' || op == '-') {
            pos++;
            double right = parseFactor(expr, pos, x);
            if (op == '+') {
                result += right;
            } else {
                result -= right;
            }
        } else {
            break;
        }
    }
    
    return result;
}

double ExpressionParser::parseFactor(const QString &expr, int &pos, double x)
{
    skipWhitespace(expr, pos);
    double result = parsePower(expr, pos, x);
    
    while (pos < expr.length()) {
        skipWhitespace(expr, pos);
        if (pos >= expr.length()) break;
        
        QChar op = expr[pos];
        if (op == '*') {
            pos++;
            result *= parsePower(expr, pos, x);
        } else if (op == '/') {
            pos++;
            double divisor = parsePower(expr, pos, x);
            if (std::abs(divisor) < 1e-10) {
                return NAN;
            }
            result /= divisor;
        } else {
            break;
        }
    }
    
    return result;
}

double ExpressionParser::parsePower(const QString &expr, int &pos, double x)
{
    skipWhitespace(expr, pos);
    double base = parseNumber(expr, pos);
    
    skipWhitespace(expr, pos);
    if (pos < expr.length() - 1 && expr[pos] == '*' && expr[pos + 1] == '*') {
        pos += 2;
        double exponent = parsePower(expr, pos, x);
        return std::pow(base, exponent);
    }
    
    return base;
}

double ExpressionParser::parseNumber(const QString &expr, int &pos)
{
    skipWhitespace(expr, pos);
    
    if (pos >= expr.length()) {
        lastError = "Unexpected end of expression";
        return NAN;
    }
    
    // Handle parentheses
    if (expr[pos] == '(') {
        pos++;
        double result = parseTerm(expr, pos, 0);
        skipWhitespace(expr, pos);
        if (pos >= expr.length() || expr[pos] != ')') {
            lastError = "Missing closing parenthesis";
            return NAN;
        }
        pos++;
        return result;
    }
    
    // Handle unary minus
    if (expr[pos] == '-') {
        pos++;
        return -parseNumber(expr, pos);
    }
    
    // Handle functions
    QString funcName;
    int funcStart = pos;
    while (pos < expr.length() && expr[pos].isLetter()) {
        funcName += expr[pos];
        pos++;
    }
    
    if (!funcName.isEmpty()) {
        skipWhitespace(expr, pos);
        if (pos < expr.length() && expr[pos] == '(') {
            pos++;
            double arg = parseTerm(expr, pos, 0);
            skipWhitespace(expr, pos);
            if (pos >= expr.length() || expr[pos] != ')') {
                lastError = "Missing closing parenthesis after function";
                return NAN;
            }
            pos++;
            return parseFunction(funcName, arg);
        } else {
            pos = funcStart;
        }
    }
    
    // Parse number
    QString numStr;
    while (pos < expr.length() && (expr[pos].isDigit() || expr[pos] == '.')) {
        numStr += expr[pos];
        pos++;
    }
    
    if (numStr.isEmpty()) {
        lastError = "Expected number";
        return NAN;
    }
    
    bool ok;
    double value = numStr.toDouble(&ok);
    if (!ok) {
        lastError = "Invalid number format";
        return NAN;
    }
    
    return value;
}

double ExpressionParser::parseFunction(const QString &name, double arg)
{
    if (name == "sin") return std::sin(arg);
    if (name == "cos") return std::cos(arg);
    if (name == "tan") return std::tan(arg);
    if (name == "asin") return std::asin(arg);
    if (name == "acos") return std::acos(arg);
    if (name == "atan") return std::atan(arg);
    if (name == "sinh") return std::sinh(arg);
    if (name == "cosh") return std::cosh(arg);
    if (name == "tanh") return std::tanh(arg);
    if (name == "exp") return std::exp(arg);
    if (name == "log" || name == "ln") return std::log(arg);
    if (name == "log10") return std::log10(arg);
    if (name == "sqrt") return std::sqrt(arg);
    if (name == "abs") return std::abs(arg);
    if (name == "floor") return std::floor(arg);
    if (name == "ceil") return std::ceil(arg);
    
    lastError = "Unknown function: " + name;
    return NAN;
}
