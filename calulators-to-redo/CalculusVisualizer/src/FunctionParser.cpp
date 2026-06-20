#include "FunctionParser.h"
#include <cctype>
#include <stdexcept>
#include <algorithm>

namespace Calculus {

FunctionParser::FunctionParser() : currentToken(0) {}

std::unique_ptr<ExpressionNode> FunctionParser::parse(const std::string& expression) {
    errorMessage.clear();
    tokens.clear();
    currentToken = 0;
    
    try {
        tokenize(expression);
        
        if (tokens.empty() || (tokens.size() == 1 && tokens[0].type == TokenType::End)) {
            setError("Empty expression");
            return nullptr;
        }
        
        auto result = parseExpression();
        
        if (!check(TokenType::End)) {
            setError("Unexpected tokens after expression");
            return nullptr;
        }
        
        return result;
    }
    catch (const std::exception& e) {
        setError(e.what());
        return nullptr;
    }
}

void FunctionParser::tokenize(const std::string& expression) {
    size_t i = 0;
    
    while (i < expression.length()) {
        // Skip whitespace
        if (isWhitespace(expression[i])) {
            i++;
            continue;
        }
        
        // Numbers
        if (isDigit(expression[i]) || (expression[i] == '.' && i + 1 < expression.length() && isDigit(expression[i + 1]))) {
            std::string number;
            while (i < expression.length() && (isDigit(expression[i]) || expression[i] == '.')) {
                number += expression[i++];
            }
            tokens.push_back(Token(TokenType::Number, number));
            continue;
        }
        
        // Variables and functions
        if (isAlpha(expression[i])) {
            std::string identifier;
            while (i < expression.length() && isAlphaNumeric(expression[i])) {
                identifier += expression[i++];
            }
            
            // Check if it's a known function
            std::string lower = identifier;
            std::transform(lower.begin(), lower.end(), lower.begin(), ::tolower);
            
            if (lower == "sin" || lower == "cos" || lower == "tan" || 
                lower == "exp" || lower == "log" || lower == "ln" || 
                lower == "sqrt") {
                tokens.push_back(Token(TokenType::Function, lower));
            }
            else {
                // It's a variable
                tokens.push_back(Token(TokenType::Variable, identifier));
            }
            continue;
        }
        
        // Operators and parentheses
        switch (expression[i]) {
            case '+':
                tokens.push_back(Token(TokenType::Plus));
                i++;
                break;
            case '-':
                tokens.push_back(Token(TokenType::Minus));
                i++;
                break;
            case '*':
                tokens.push_back(Token(TokenType::Multiply));
                i++;
                break;
            case '/':
                tokens.push_back(Token(TokenType::Divide));
                i++;
                break;
            case '^':
                tokens.push_back(Token(TokenType::Power));
                i++;
                break;
            case '(':
                tokens.push_back(Token(TokenType::LeftParen));
                i++;
                break;
            case ')':
                tokens.push_back(Token(TokenType::RightParen));
                i++;
                break;
            default:
                throw std::runtime_error(std::string("Unexpected character: ") + expression[i]);
        }
    }
    
    tokens.push_back(Token(TokenType::End));
}

bool FunctionParser::isWhitespace(char c) const {
    return c == ' ' || c == '\t' || c == '\n' || c == '\r';
}

bool FunctionParser::isDigit(char c) const {
    return c >= '0' && c <= '9';
}

bool FunctionParser::isAlpha(char c) const {
    return (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') || c == '_';
}

bool FunctionParser::isAlphaNumeric(char c) const {
    return isAlpha(c) || isDigit(c);
}

Token FunctionParser::peek() const {
    if (currentToken < tokens.size()) {
        return tokens[currentToken];
    }
    return Token(TokenType::End);
}

Token FunctionParser::advance() {
    Token current = peek();
    if (currentToken < tokens.size()) {
        currentToken++;
    }
    return current;
}

bool FunctionParser::match(TokenType type) {
    if (check(type)) {
        advance();
        return true;
    }
    return false;
}

bool FunctionParser::check(TokenType type) const {
    return peek().type == type;
}

void FunctionParser::setError(const std::string& message) {
    errorMessage = message;
}

// Expression: Term (('+' | '-') Term)*
std::unique_ptr<ExpressionNode> FunctionParser::parseExpression() {
    auto left = parseTerm();
    
    while (match(TokenType::Plus) || match(TokenType::Minus)) {
        Token op = tokens[currentToken - 1];
        auto right = parseTerm();
        
        if (op.type == TokenType::Plus) {
            left = makeAdd(std::move(left), std::move(right));
        }
        else {
            left = makeSubtract(std::move(left), std::move(right));
        }
    }
    
    return left;
}

// Term: Factor (('*' | '/') Factor)*
std::unique_ptr<ExpressionNode> FunctionParser::parseTerm() {
    auto left = parseFactor();
    
    while (match(TokenType::Multiply) || match(TokenType::Divide)) {
        Token op = tokens[currentToken - 1];
        auto right = parseFactor();
        
        if (op.type == TokenType::Multiply) {
            left = makeMultiply(std::move(left), std::move(right));
        }
        else {
            left = makeDivide(std::move(left), std::move(right));
        }
    }
    
    return left;
}

// Factor: Power
// We need this level to handle implicit multiplication (like 2x or xsin(x))
std::unique_ptr<ExpressionNode> FunctionParser::parseFactor() {
    auto left = parsePower();
    
    // Handle implicit multiplication: if next token is a primary without an operator
    while (check(TokenType::Number) || check(TokenType::Variable) || 
           check(TokenType::Function) || check(TokenType::LeftParen)) {
        auto right = parsePower();
        left = makeMultiply(std::move(left), std::move(right));
    }
    
    return left;
}

// Power: Unary ('^' Unary)*
std::unique_ptr<ExpressionNode> FunctionParser::parsePower() {
    auto base = parseUnary();
    
    if (match(TokenType::Power)) {
        // Right-associative: a^b^c = a^(b^c)
        auto exponent = parsePower();
        return makePower(std::move(base), std::move(exponent));
    }
    
    return base;
}

// Unary: ('-' | '+') Unary | Primary
std::unique_ptr<ExpressionNode> FunctionParser::parseUnary() {
    if (match(TokenType::Minus)) {
        auto expr = parseUnary();
        return makeNegate(std::move(expr));
    }
    
    if (match(TokenType::Plus)) {
        return parseUnary();
    }
    
    return parsePrimary();
}

// Primary: Number | Variable | Function '(' Expression ')' | '(' Expression ')'
std::unique_ptr<ExpressionNode> FunctionParser::parsePrimary() {
    // Number
    if (match(TokenType::Number)) {
        Token num = tokens[currentToken - 1];
        return makeNumber(std::stod(num.value));
    }
    
    // Variable
    if (match(TokenType::Variable)) {
        Token var = tokens[currentToken - 1];
        return makeVariable(var.value);
    }
    
    // Function call
    if (match(TokenType::Function)) {
        Token func = tokens[currentToken - 1];
        
        if (!match(TokenType::LeftParen)) {
            throw std::runtime_error("Expected '(' after function name");
        }
        
        auto argument = parseExpression();
        
        if (!match(TokenType::RightParen)) {
            throw std::runtime_error("Expected ')' after function argument");
        }
        
        // Create appropriate function node
        if (func.value == "sin") {
            return makeSin(std::move(argument));
        }
        else if (func.value == "cos") {
            return makeCos(std::move(argument));
        }
        else if (func.value == "tan") {
            return makeTan(std::move(argument));
        }
        else if (func.value == "exp") {
            return makeExp(std::move(argument));
        }
        else if (func.value == "log") {
            return makeLog(std::move(argument));
        }
        else if (func.value == "ln") {
            return makeLn(std::move(argument));
        }
        else if (func.value == "sqrt") {
            return makeSqrt(std::move(argument));
        }
        else {
            throw std::runtime_error("Unknown function: " + func.value);
        }
    }
    
    // Parenthesized expression
    if (match(TokenType::LeftParen)) {
        auto expr = parseExpression();
        
        if (!match(TokenType::RightParen)) {
            throw std::runtime_error("Expected ')' to match '('");
        }
        
        return expr;
    }
    
    throw std::runtime_error("Expected number, variable, function, or '('");
}

} // namespace Calculus
