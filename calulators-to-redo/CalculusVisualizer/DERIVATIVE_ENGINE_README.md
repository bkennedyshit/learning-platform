---
date: 2026-05-26
title: "Calculus Visualizer - Derivative Calculation Engine"
tags: [learning, calculusvisualizer]
status: reference
type: note
---

# Calculus Visualizer - Derivative Calculation Engine

## Overview

A complete symbolic differentiation engine built from scratch in C++ (no external dependencies like SymEngine). Designed for educational purposes with step-by-step explanations to help students understand calculus concepts.

## Features

### ✅ Core Capabilities

- **Parse Mathematical Expressions**: Polynomials, trigonometric, exponential, logarithmic, and rational functions
- **Symbolic Differentiation**: All calculus rules implemented
- **Step-by-Step Explanations**: Shows which rule was applied at each step (critical for learning!)
- **Higher-Order Derivatives**: 2nd, 3rd, 4th, ... nth derivatives
- **Partial Derivatives**: Support for multivariable functions
- **Simplification**: Algebraic simplification of results
- **Evaluation**: Compute function values at specific points
- **Critical Points**: Find where f'(x) = 0 (local min/max)
- **Inflection Points**: Find where f''(x) = 0 (concavity changes)

### 📚 Differentiation Rules Implemented

1. **Constant Rule**: d/dx[c] = 0
2. **Power Rule**: d/dx[x^n] = n·x^(n-1)
3. **Sum Rule**: d/dx[f + g] = f' + g'
4. **Difference Rule**: d/dx[f - g] = f' - g'
5. **Product Rule**: d/dx[f·g] = f'·g + f·g'
6. **Quotient Rule**: d/dx[f/g] = (f'·g - f·g')/g²
7. **Chain Rule**: d/dx[f(g(x))] = f'(g(x))·g'(x)
8. **Trigonometric**:
   - d/dx[sin(x)] = cos(x)
   - d/dx[cos(x)] = -sin(x)
   - d/dx[tan(x)] = sec²(x)
9. **Exponential/Logarithmic**:
   - d/dx[e^x] = e^x
   - d/dx[ln(x)] = 1/x
   - d/dx[log(x)] = 1/(x·ln(10))
10. **General Power Rule**: d/dx[f^g] = f^g·(g'·ln(f) + g·f'/f)

## Architecture

### File Structure

```
src/
├── ExpressionTree.h          - AST node definitions
├── ExpressionTree.cpp        - Expression tree implementation
├── FunctionParser.h          - Parser interface
├── FunctionParser.cpp        - Recursive descent parser
├── DerivativeEngine.h        - High-level engine interface
├── DerivativeEngine.cpp      - Engine implementation
└── DerivativeEngineExample.cpp - Usage examples
```

### Components

#### 1. **ExpressionTree** (AST)
Represents mathematical expressions as an Abstract Syntax Tree:
- `NumberNode` - Constants (e.g., 5, 3.14)
- `VariableNode` - Variables (e.g., x, y, z)
- `BinaryOpNode` - Binary operations (+, -, *, /, ^)
- `UnaryOpNode` - Unary operations (sin, cos, tan, exp, ln, sqrt, negate)

Each node supports:
- `evaluate()` - Compute numerical value
- `differentiate()` - Symbolic differentiation
- `simplify()` - Algebraic simplification
- `toString()` - Convert to string representation

#### 2. **FunctionParser**
Recursive descent parser that converts string expressions to AST:
- Tokenizer with support for numbers, variables, operators, functions
- Operator precedence handling (^, *, /, +, -)
- Function calls (sin, cos, exp, etc.)
- Parentheses grouping
- Error reporting

#### 3. **DerivativeEngine**
High-level interface for calculus operations:
- Parse expressions
- Compute derivatives with step-by-step explanations
- Higher-order derivatives
- Critical point analysis
- Inflection point detection
- Newton's method for root finding

## Usage Examples

### Basic Derivative

```cpp
#include "DerivativeEngine.h"

using namespace Calculus;

int main() {
    DerivativeEngine engine;
    
    // Compute derivative of x^2 + 3*x + 5
    auto result = engine.computeDerivative("x^2 + 3*x + 5");
    
    std::cout << "f'(x) = " << result.simplifiedDerivative << "\n";
    // Output: f'(x) = 2*x + 3
    
    return 0;
}
```

### Step-by-Step Solution

```cpp
DerivativeEngine engine;

auto result = engine.computeDerivative("sin(x^2)");

// Print detailed steps
std::cout << engine.formatSteps(result);
```

Output:
```
DERIVATIVE CALCULATION
=====================

Original: sin(x^2)

STEP-BY-STEP SOLUTION:
----------------------

Step 1: Original Function
  Starting expression
  → f(x) = sin(x^2)

Step 2: Chain Rule (sin)
  d/dx[sin(x^2)] = cos(x^2) * d/dx(x^2)

Step 3: Power Rule
  d/dx(x^2) = 2*x

FINAL RESULT:
-------------
f'(x) = cos(x^2) * 2 * x
```

### Higher-Order Derivatives

```cpp
DerivativeEngine engine;

// Compute 3rd derivative
auto result = engine.computeNthDerivative("x^4 - 3*x^2 + 2*x", 3);

std::cout << "f'''(x) = " << result.simplifiedDerivative << "\n";
// Output: f'''(x) = 24*x
```

### Finding Critical Points

```cpp
DerivativeEngine engine;

// Find where f'(x) = 0
auto criticalPoints = engine.findCriticalPoints("x^3 - 3*x^2 + 2", -5, 5);

for (const auto& cp : criticalPoints) {
    std::cout << "x = " << cp.x 
              << ", f(x) = " << cp.y 
              << " (" << cp.type << ")\n";
}
```

Output:
```
x = 0.0000, f(x) = 2.0000 (local maximum)
x = 2.0000, f(x) = -2.0000 (local minimum)
```

### Partial Derivatives

```cpp
DerivativeEngine engine;

// Multivariable function: f(x,y) = x^2 + 3*x*y + y^2
auto dx = engine.computePartialDerivative("x^2 + 3*x*y + y^2", "x");
auto dy = engine.computePartialDerivative("x^2 + 3*x*y + y^2", "y");

std::cout << "∂f/∂x = " << dx.simplifiedDerivative << "\n";
std::cout << "∂f/∂y = " << dy.simplifiedDerivative << "\n";
```

### Evaluation at Points

```cpp
DerivativeEngine engine;

std::map<std::string, double> vars = {{"x", 2.0}};
double value = engine.evaluate("x^2 + 2*x + 1", vars);

std::cout << "f(2) = " << value << "\n";
// Output: f(2) = 9
```

## Supported Functions

### Arithmetic Operators
- Addition: `+`
- Subtraction: `-`
- Multiplication: `*`
- Division: `/`
- Power: `^`

### Functions
- `sin(x)` - Sine
- `cos(x)` - Cosine
- `tan(x)` - Tangent
- `exp(x)` - Exponential (e^x)
- `ln(x)` - Natural logarithm
- `log(x)` - Base-10 logarithm
- `sqrt(x)` - Square root
- `-x` - Negation

### Expression Examples

```cpp
"x^2 + 3*x + 5"                    // Polynomial
"sin(x) + cos(x)"                  // Trigonometric
"exp(x) * x^2"                     // Exponential
"ln(x) / x"                        // Logarithmic
"sin(x^2 + 1)"                     // Composite (chain rule)
"x * sin(x)"                       // Product rule
"sin(x) / x"                       // Quotient rule
"(x^2 + 1)^3"                      // Power of polynomial
"exp(sin(x^2))"                    // Nested functions
"x^2 + 3*x*y + y^2"               // Multivariable
```

## Educational Value

This engine is designed with learning in mind:

1. **Step-by-Step Explanations**: Shows which calculus rule is applied at each step
2. **Rule Identification**: Explicitly names Power Rule, Chain Rule, Product Rule, etc.
3. **Detailed Breakdowns**: Explains the thought process behind each differentiation
4. **Critical for Understanding Backpropagation**: Chain rule is fundamental to neural networks!

### Example Learning Output

When computing d/dx[sin(x^2)]:

```
Step 1: Chain Rule (sin)
  d/dx[sin(x^2)] = cos(x^2) * d/dx(x^2)
  → cos(x^2) needs to be multiplied by derivative of inner function

Step 2: Power Rule
  d/dx(x^2) = 2*x
  → Applied power rule: bring down exponent, reduce power by 1

Final: cos(x^2) * 2 * x
```

## Implementation Details

### Simplification Rules

The engine applies these simplifications:
- `x + 0 = x`
- `x * 0 = 0`
- `x * 1 = x`
- `x / 1 = x`
- `x^0 = 1`
- `x^1 = x`
- Constant folding (e.g., `2 + 3 = 5`)

### Newton's Method for Root Finding

Used for finding critical and inflection points:
```
x_{n+1} = x_n - f(x_n) / f'(x_n)
```

### Critical Point Classification

Uses second derivative test:
- If f''(x) > 0: local minimum
- If f''(x) < 0: local maximum
- If f''(x) ≈ 0: saddle point or inconclusive

## Compilation

```bash
# Compile the example
g++ -std=c++17 -o derivative_engine \
    ExpressionTree.cpp \
    FunctionParser.cpp \
    DerivativeEngine.cpp \
    DerivativeEngineExample.cpp

# Run examples
./derivative_engine
```

## Future Enhancements

Potential additions:
- [ ] Integration engine (symbolic antiderivatives)
- [ ] Taylor/Maclaurin series expansion
- [ ] Limit computation
- [ ] L'Hôpital's rule for indeterminate forms
- [ ] Implicit differentiation
- [ ] Parametric derivatives
- [ ] Vector calculus (gradient, divergence, curl)
- [ ] Optimization (constraint optimization)
- [ ] LaTeX output for formatted math

## Why Build From Scratch?

Advantages of custom implementation vs. using SymEngine/SymPy:
1. **Educational**: Understand exactly how differentiation works
2. **Lightweight**: No heavy dependencies
3. **Customizable**: Full control over step-by-step output
4. **Fast**: Optimized for specific use case
5. **Transparent**: Clear code for learning

## License

Educational open-source project. Use freely for learning and teaching calculus!

## Author

Built for the Calculus Visualizer educational tool.

---

**Learning Goal**: Master derivatives by seeing every step of the calculation!

---

## Related Notes
- [[BUILD]] - Shared calculusvisualizer/learning focus
- [[BUILDING]] - Shared calculusvisualizer/learning focus
- [[IMPLEMENTATION_SUMMARY]] - Shared calculusvisualizer/learning focus
- [[PROJECT_SUMMARY]] - Shared calculusvisualizer/learning focus
- [[QUICKSTART]] - Shared calculusvisualizer/learning focus
