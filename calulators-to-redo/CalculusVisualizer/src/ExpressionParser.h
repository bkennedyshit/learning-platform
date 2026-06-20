/**
 * ExpressionParser.h - Mathematical expression parser and evaluator
 */

#ifndef EXPRESSIONPARSER_H
#define EXPRESSIONPARSER_H

#include <QString>
#include <QMap>
#include <cmath>

class ExpressionParser
{
public:
    ExpressionParser();
    
    /**
     * @brief Evaluate mathematical expression with variable substitution
     * @param expression Expression string (e.g., "x^2 + 3*x - 5")
     * @param x Value to substitute for variable x
     * @return double Result of evaluation
     */
    double evaluate(const QString &expression, double x);
    
    /**
     * @brief Parse and validate expression
     * @param expression Expression to validate
     * @return bool True if valid
     */
    bool isValid(const QString &expression);
    
    /**
     * @brief Get last error message
     * @return QString Error message
     */
    QString getLastError() const;

private:
    double parseExpression(const QString &expr, double x);
    double parseTerm(const QString &expr, int &pos, double x);
    double parseFactor(const QString &expr, int &pos, double x);
    double parsePower(const QString &expr, int &pos, double x);
    double parseNumber(const QString &expr, int &pos);
    double parseFunction(const QString &name, double arg);
    
    QString preprocessExpression(const QString &expr);
    void skipWhitespace(const QString &expr, int &pos);
    
    QString lastError;
    
    // Mathematical constants
    static const QMap<QString, double> constants;
};

#endif // EXPRESSIONPARSER_H
