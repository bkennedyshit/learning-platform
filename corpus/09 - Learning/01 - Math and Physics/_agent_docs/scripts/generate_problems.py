import sympy as sp
import random
import argparse
import os
from datetime import datetime

def get_functions_by_difficulty(x, difficulty):
    """Returns a list of SymPy expressions based on difficulty tier."""
    if difficulty == "easy":
        return [
            x**random.randint(2, 5),
            random.randint(2, 5) * x + random.randint(1, 10),
            sp.sin(x),
            sp.exp(x)
        ]
    elif difficulty == "medium":
        return [
            sp.sin(random.randint(2, 5) * x) * sp.exp(random.randint(1, 3) * x),
            x**random.randint(2, 4) * sp.cos(x),
            sp.log(x) * x**random.randint(1, 3),
            (x**2 + random.randint(1, 5)) / (x + random.randint(1, 3))
        ]
    elif difficulty == "hard":
        return [
            sp.sin(x**random.randint(2, 4)) * sp.log(x),
            sp.exp(x * sp.cos(x)),
            sp.log(x**2 + random.randint(1, 10)) / x,
            (x**3 - random.randint(1, 5)*x) / (sp.sin(x) + 2)
        ]
    elif difficulty == "exam":
        return [
            sp.exp(sp.sin(x**2)) * sp.cos(x),
            sp.log(sp.sqrt(x**2 + 1) + x) / (x**2 + 1),
            (sp.sin(x)**random.randint(2,4) * sp.cos(x)**random.randint(2,4)),
            sp.asin(x) * x**2
        ]
    else:
        raise ValueError("Invalid difficulty level")

def generate_integration_problem(difficulty):
    x = sp.Symbol('x')
    funcs = get_functions_by_difficulty(x, difficulty)
    f = random.choice(funcs)
    F = sp.integrate(f, x)
    
    latex_f = sp.latex(f)
    latex_F = sp.latex(F)
    
    markdown = f"""### 📝 Integration Drill ({difficulty.capitalize()})

**Evaluate the following integral:**

$$
\int {latex_f} \, dx
$$

?

#### Step 1: Set up the integral
The problem requires computing the indefinite integral:

$$
\int {latex_f} \, dx
$$

#### Step 2: Integration via analytical methods (SymPy Engine)
Applying appropriate integration techniques yields:

$$
{latex_F} + C
$$

**Final Answer:**

$$
\int {latex_f} \, dx = {latex_F} + C
$$
"""
    return markdown

def generate_derivative_problem(difficulty):
    x = sp.Symbol('x')
    funcs = get_functions_by_difficulty(x, difficulty)
    f = random.choice(funcs)
    df = sp.diff(f, x)
    
    latex_f = sp.latex(f)
    latex_df = sp.latex(df)
    
    markdown = f"""### 📝 Derivative Drill ({difficulty.capitalize()})

**Find the first derivative of the following function with respect to $x$:**

$$
f(x) = {latex_f}
$$

?

#### Step 1: Apply differentiation rules
Applying the chain rule, product rule, and quotient rule as necessary to:

$$
\frac{{d}}{{dx}} \left( {latex_f} \right)
$$

#### Step 2: Compute derivative
The exact analytical derivative is:

$$
f'(x) = {latex_df}
$$

**Final Answer:**

$$
f'(x) = {latex_df}
$$
"""
    return markdown

def main():
    parser = argparse.ArgumentParser(description="Generate math problems for Obsidian.")
    parser.add_argument("--difficulty", choices=["easy", "medium", "hard", "exam"], default="medium", help="Problem difficulty level")
    parser.add_argument("--subject-dir", type=str, required=True, help="Absolute path to the subject directory (e.g., '.../01 - Mathematical Foundations & Calculus')")
    parser.add_argument("--type", choices=["integration", "derivative", "both"], default="both", help="Type of problem to generate")
    
    args = parser.parse_args()
    
    practice_dir = os.path.join(args.subject_dir, "_practice")
    os.makedirs(practice_dir, exist_ok=True)
    
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"{date_str}_Calculus_Drill_{args.difficulty.capitalize()}.md"
    filepath = os.path.join(practice_dir, filename)
    
    content = f"# Calculus Practice: {date_str}\n\n"
    content += "---\n#review/math\n\n"
    
    if args.type in ["integration", "both"]:
        content += generate_integration_problem(args.difficulty) + "\n---\n\n"
    
    if args.type in ["derivative", "both"]:
        content += generate_derivative_problem(args.difficulty) + "\n---\n\n"
        
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
        
    print(f"✅ Generated {args.difficulty} problems and saved to:\n{filepath}")

if __name__ == "__main__":
    main()
