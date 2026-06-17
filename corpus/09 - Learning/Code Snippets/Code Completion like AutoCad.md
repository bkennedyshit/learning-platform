---
date: 2026-05-26
title: "Code Completion like AutoCad"
tags: [learning, code-snippets, python]
status: reference
type: note
---

Okay, let's get you set up with Python 3.13 and VS Code for a good development experience, including autocompletion.

~~**1. Install Python 3.13:**~~

- ~~Go to the official Python website: [Python.org](https://www.python.org/downloads/).~~
- ~~Download the installer for your operating system (Windows, macOS, or Linux).~~
- ~~Run the installer and follow the instructions. Make sure to check the box that says "Add Python to PATH" during installation. This is important for VS Code to find your Python installation.~~
- ~~Open a terminal or command prompt and type `python --version` to verify that Python 3.13 is installed correctly.~~ 

~~**2. Install VS Code:**~~

- ~~Go to the official VS Code website: [Visual Studio Code](https://code.visualstudio.com/docs/getstarted/getting-started).~~
- ~~Download the installer for your operating system.~~
- ~~Run the installer and follow the instructions.~~ 

**3. Install the Python Extension for VS Code:**

- Open VS Code.
- Click on the Extensions icon in the Activity Bar (it looks like four squares).
- Search for "Python" and install the extension published by Microsoft.
- This extension provides core Python development features, including IntelliSense (autocompletion), linting, debugging, and more. 

**4. Select the Python Interpreter:**

- Open a Python file (or create a new one).
- Click on the Python interpreter selection in the Status Bar (usually in the bottom-left corner of the window).
- Select your Python 3.13 interpreter from the list. VS Code will automatically detect Python interpreters installed on your system.
- If it's not listed, you can manually specify the interpreter path. 

**5. Test Autocompletion:**

- Create a new Python file (e.g., `test.py`).
- Start typing Python code, such as `import` followed by a space.
- VS Code should now suggest available modules and packages.
- You can also try typing the name of a function or variable you've defined to see suggestions. 

**Optional: Setting up Virtual Environments (Recommended):**

- For managing project dependencies, create a virtual environment for your Python project.
- Open the Command Palette (`Ctrl+Shift+P` or `Cmd+Shift+P`) and type "Python: Create Environment".
- Follow the prompts to create and activate a virtual environment for your project. 

**Explanation:**

- **Python Extension:** The Python extension for VS Code is essential for providing Python language support.
- **IntelliSense:** IntelliSense is the code completion and suggestion engine in VS Code. It analyzes your code and provides suggestions based on the context.
- **Interpreter Selection:** Selecting the correct Python interpreter ensures that IntelliSense uses the right version of Python and its associated libraries. 

By following these steps, you should have a working Python 3.13 development environment in VS Code with autocompletion enabled.

---

## **Code Generation vs. Autocompletion (IntelliSense)**

It is important to distinguish between autocompletion and code generation:

- **Autocompletion (IntelliSense):** This VS Code feature suggests code while typing, based on context such as keywords, functions, and variables. It supports writing code manually.
- **Code Generation:** This automatically creates code from a template, specification, or model. It can create boilerplate code, data structures, or entire applications based on predefined rules. 

**Code Generation Tools in Python** 

Python offers various code generation tools to automate repetitive coding tasks:

- **Jinja2:** A powerful templating engine. Define a template and pass variables to generate text (which can be Python code). This is useful for creating similar code structures with varying parameters.
- **Mako:** Another templating engine, similar to Jinja2, which provides more control over the generation process.
- **Code generators built into libraries:** Many libraries have built-in code generation functionality for specific use cases, such as generating classes from database schemas or creating API client code.
- **Custom scripts:** Write Python scripts to parse data, generate code based on a set of rules, and write the generated code to files. 

**Using Code Generation with VS Code**

1. **Choose a Code Generation Tool:** Select a tool or library based on your needs.
2. **Create Templates:** Define templates for the code to generate.
3. **Write a Script:** Write a Python script to generate code using the chosen tool.
4. **VS Code Integration:** Integrate code generation scripts into VS Code in several ways:
    - **Tasks:** Define VS Code tasks to run the code generation script.
    - **Extensions:** Write or install VS Code extensions that automate the code generation process.
    - **External tools:** Run the script directly from the terminal within VS Code, or call it as an external tool. 

**Example (Jinja2)**

python

```
# code_generator.py
from jinja2 import Environment, FileSystemLoader

template_loader = FileSystemLoader(searchpath="./templates")  # Assumes templates are in a 'templates' folder
template_env = Environment(loader=template_loader)

template = template_env.get_template("class_template.txt")

class_data = {
    "class_name": "MyClass",
    "attributes": ["name", "age", "address"],
    "methods": ["get_info", "update_address"]
}
output_code = template.render(class_data)

with open("generated_class.py", "w") as file:
    file.write(output_code)
```

Use code with caution.

```
# templates/class_template.txt (Jinja2 template)
class {{ class_name }}:
    def __init__(self, {% for attr in attributes %}{{ attr }}: str, {% endfor %}):
        {% for attr in attributes %}
        self.{{ attr }} = {{ attr }}
        {% endfor %}

    {% for method in methods %}
    def {{ method }}(self):
      pass
    {% endfor %}
```

**Benefits of Code Generation**

- **Automation:** Eliminates repetitive manual coding.
- **Consistency:** Generates code according to predefined rules, reducing errors.
- **Efficiency:** Speeds up development.
- **Maintainability:** Changes can be made in templates rather than in many individual files. 

**In Summary:**

Code generation is a useful technique that can be combined with VS Code's features (like autocompletion) to improve the Python development workflow. VS Code provides a great environment for creating, running, and integrating code generation scripts into projects.

---

## Related Notes
- [[Coding Shortcuts]] - Shared code-snippets/learning focus
- [[Docker CLI Cheat Sheet]] - Shared code-snippets/learning focus
- [[20 - Computational Design Intro]] - Shared learning/python focus
- [[Python Reference & Cheatsheets]] - Shared learning/python focus
- [[Using rembg (Remove Background)]] - Shared learning/python focus
