---
date: 2026-01-24
title: C++ Basics for Game Dev
mission: Essential C++ syntax and concepts for game development and coding tests
status: active-reference
tags: [cpp, c++, game-dev, basics, coding-test]
type: code-reference
---

# C++ Basics for Game Dev

## Basic Syntax
```cpp
#include <iostream>
#include <string>
#include <vector>

using namespace std;

int main() {
    cout << "Hello World" << endl;
    return 0;
}
```

## Variables & Data Types
```cpp
// Basic types
int age = 30;
float height = 5.10f;
double price = 19.99;
char grade = 'A';
bool is_active = true;
string name = "Billy";

// Constants
const int MAX_HEALTH = 100;
const float PI = 3.14159f;

// Auto type inference (C++11)
auto score = 100;      // int
auto ratio = 1.5f;     // float
auto text = "hello";   // const char*
auto message = string("hello");  // string
```

## Pointers & References (IMPORTANT!)
```cpp
// Pointer - stores memory address
int x = 10;
int* ptr = &x;         // ptr points to x
cout << *ptr;          // 10 (dereference)
*ptr = 20;             // Modifies x

// Reference - alias for variable
int& ref = x;          // ref is another name for x
ref = 30;              // Modifies x

// Null pointer
int* ptr = nullptr;    // C++11 (better than NULL)

// Pointer to pointer
int** pptr = &ptr;
```

## Arrays & Vectors
```cpp
// C-style array (fixed size)
int numbers[5] = {1, 2, 3, 4, 5};
numbers[0] = 10;
int size = sizeof(numbers) / sizeof(numbers[0]);

// Vector (dynamic array - USE THIS!)
#include <vector>
vector<int> nums = {1, 2, 3, 4, 5};
nums.push_back(6);     // Add element
nums.pop_back();       // Remove last
nums.size();           // Get size
nums[0] = 10;          // Access element
nums.clear();          // Remove all

// 2D vector
vector<vector<int>> matrix(3, vector<int>(3, 0));
matrix[0][0] = 1;
```

## Functions
```cpp
// Basic function
int add(int a, int b) {
    return a + b;
}

// Pass by reference (modifies original)
void increment(int& x) {
    x++;
}

// Pass by value (doesn't modify original)
void display(int x) {
    cout << x;
}

// Default parameters
int power(int base, int exp = 2) {
    int result = 1;
    for(int i = 0; i < exp; i++) {
        result *= base;
    }
    return result;
}

// Overloading (same name, different parameters)
int add(int a, int b) { return a + b; }
double add(double a, double b) { return a + b; }
```

## Classes & Objects (OOP)
```cpp
class Player {
private:
    string name;
    int health;
    
public:
    // Constructor
    Player(string n, int h) : name(n), health(h) {}
    
    // Getter
    int getHealth() { return health; }
    
    // Setter
    void setHealth(int h) { health = h; }
    
    // Method
    void takeDamage(int damage) {
        health -= damage;
        if(health < 0) health = 0;
    }
    
    // Const method (doesn't modify object)
    void display() const {
        cout << name << ": " << health << " HP" << endl;
    }
};

// Usage
Player player("Billy", 100);
player.takeDamage(20);
player.display();
```

## Constructors & Destructors
```cpp
class Enemy {
private:
    string name;
    int* data;
    
public:
    // Constructor
    Enemy(string n) : name(n) {
        data = new int[100];  // Allocate memory
        cout << "Enemy created" << endl;
    }
    
    // Destructor (cleanup)
    ~Enemy() {
        delete[] data;  // Free memory
        cout << "Enemy destroyed" << endl;
    }
    
    // Copy constructor
    Enemy(const Enemy& other) : name(other.name) {
        data = new int[100];
        // Copy data
    }
};
```

## Control Flow
```cpp
// If/else
if (health > 50) {
    cout << "Healthy";
} else if (health > 0) {
    cout << "Hurt";
} else {
    cout << "Dead";
}

// Ternary
string status = (health > 0) ? "Alive" : "Dead";

// Switch
switch(choice) {
    case 1:
        attack();
        break;
    case 2:
        defend();
        break;
    default:
        wait();
}

// For loop
for(int i = 0; i < 10; i++) {
    cout << i << " ";
}

// Range-based for (C++11)
vector<int> nums = {1, 2, 3, 4, 5};
for(int num : nums) {
    cout << num << " ";
}

// For with reference (can modify)
for(int& num : nums) {
    num *= 2;
}

// While
int count = 0;
while(count < 10) {
    count++;
}
```

## Memory Management (CRITICAL!)
```cpp
// Stack allocation (automatic cleanup)
int x = 10;
Player player("Billy", 100);

// Heap allocation (manual cleanup required)
int* ptr = new int(10);      // Single value
delete ptr;                   // Must delete!

int* arr = new int[10];       // Array
delete[] arr;                 // Must use delete[]

Player* p = new Player("Billy", 100);
delete p;

// Smart pointers (C++11 - auto cleanup!)
#include <memory>

// unique_ptr (one owner)
unique_ptr<Player> p1 = make_unique<Player>("Billy", 100);
// auto deletes when out of scope

// shared_ptr (multiple owners)
shared_ptr<Player> p2 = make_shared<Player>("Alex", 80);
shared_ptr<Player> p3 = p2;  // Both own it
// Deletes when last reference dies
```

## Strings
```cpp
#include <string>

string name = "Billy";

// Concatenation
string greeting = "Hello " + name;
greeting += "!";

// Length
int len = name.length();  // or name.size()

// Access
char first = name[0];
char last = name[name.length() - 1];

// Substring
string sub = name.substr(0, 4);  // "Bill"

// Find
size_t pos = name.find("ll");    // Returns position or string::npos

// Compare
if(name == "Billy") { }
if(name.compare("Billy") == 0) { }

// Convert
int num = stoi("123");           // string to int
float f = stof("3.14");          // string to float
string s = to_string(123);       // int to string
```

## Common STL Containers
```cpp
#include <vector>
#include <map>
#include <set>
#include <queue>
#include <stack>

// Vector (dynamic array)
vector<int> v = {1, 2, 3};
v.push_back(4);
v.pop_back();

// Map (key-value pairs)
map<string, int> scores;
scores["Billy"] = 100;
scores["Alex"] = 95;
scores.count("Billy");  // Check if exists
scores.erase("Billy");  // Remove

// Set (unique values)
set<int> unique_nums;
unique_nums.insert(1);
unique_nums.insert(1);  // Won't add duplicate
unique_nums.count(1);   // Check if exists

// Queue (FIFO)
queue<int> q;
q.push(1);
q.push(2);
int front = q.front();
q.pop();

// Stack (LIFO)
stack<int> s;
s.push(1);
s.push(2);
int top = s.top();
s.pop();
```

## File I/O
```cpp
#include <fstream>

// Write to file
ofstream outfile("data.txt");
outfile << "Hello World" << endl;
outfile << 123 << endl;
outfile.close();

// Read from file
ifstream infile("data.txt");
string line;
while(getline(infile, line)) {
    cout << line << endl;
}
infile.close();

// Read numbers
ifstream numfile("numbers.txt");
int num;
while(numfile >> num) {
    cout << num << endl;
}
numfile.close();
```

## Quick Tips for Game Dev
- Use `vector` instead of arrays (dynamic size)
- Use smart pointers (`unique_ptr`, `shared_ptr`) to avoid memory leaks
- Pass large objects by reference: `void func(const Player& p)`
- Use `const` for read-only parameters and methods
- Initialize member variables in constructor initializer list
- Always delete what you `new` (or use smart pointers)
- Use range-based for loops when possible
- `nullptr` instead of `NULL`

## Common Game Dev Patterns
```cpp
// Game loop structure
class Game {
    bool running;
    
public:
    void run() {
        running = true;
        while(running) {
            handleInput();
            update();
            render();
        }
    }
    
    void handleInput() {
        // Process keyboard/mouse
    }
    
    void update() {
        // Game logic
    }
    
    void render() {
        // Draw to screen
    }
};

// Entity class
class Entity {
protected:
    float x, y;
    float velocityX, velocityY;
    
public:
    virtual void update(float deltaTime) {
        x += velocityX * deltaTime;
        y += velocityY * deltaTime;
    }
    
    virtual void render() = 0;  // Pure virtual (must override)
};

// Inheritance
class Player : public Entity {
public:
    void render() override {
        // Draw player sprite
    }
};
```

---

## Related Notes
- [[C++ Memory Management]]
- [[C++ STL Containers]]
- [[C++ for Unity]]
- [[Object-Oriented Programming]]
- [[Game Dev Patterns]]
