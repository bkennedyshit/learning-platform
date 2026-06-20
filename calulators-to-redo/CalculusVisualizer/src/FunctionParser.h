#ifndef FUNCTIONPARSER_H
#define FUNCTIONPARSER_H

#include "ExpressionTree.h"
#include <string>
#include <vector>
#include <memory>

namespace Calculus {

enum class TokenType {
    Number,
    Variable,
    Plus,
    Minus,
    Multiply,
    Divide,
    Power,
    LeftParen,
    RightParen,
    Function,
    End
};

struct Token {
    TokenType type;
    std::string value;
    
    Token(TokenType t, const std::string& v = "") : type(t), value(v) {}
};

class FunctionParser {
public:
    FunctionParser();
    
    // Parse a mathematical expression string into an expression tree
    std::unique_ptr<ExpressionNode> parse(const std::string& expression);
    
    // Get the last error message if parsing failed
    std::string getError() const { return errorMessage; }
    
private:
    std::vector<Token> tokens;
    size_t currentToken;
    std::string errorMessage;
    
    // Tokenizer
    void tokenize(const std::string& expression);
    bool isWhitespace(char c) const;
    bool isDigit(char c) const;
    bool isAlpha(char c) const;
    bool isAlphaNumeric(char c) const;
    
    // Recursive descent parser
    std::unique_ptr<ExpressionNode> parseExpression();
    std::unique_ptr<ExpressionNode> parseTerm();
    std::unique_ptr<ExpressionNode> parseFactor();
    std::unique_ptr<ExpressionNode> parsePower();
    std::unique_ptr<ExpressionNode> parseUnary();
    std::unique_ptr<ExpressionNode> parsePrimary();
    
    // Helper methods
    Token peek() const;
    Token advance();
    bool match(TokenType type);
    bool check(TokenType type) const;
    void setError(const std::string& message);
};

} // namespace Calculus

#endif // FUNCTIONPARSER_H
