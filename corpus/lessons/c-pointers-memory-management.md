---
title: "C++ Pointers & Memory Management"
subject: "C++"
catalog: advanced
audience_tier: higher-education
chapter: "Chapter 1"
type: code-reference
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

# C++ Pointers & Memory Management

## Pointer Basics
```cpp
// Declaration
int x = 10;
int* ptr;              // Pointer to int
ptr = &x;              // ptr stores address of x

// Dereference (access value)
cout << *ptr;          // 10
*ptr = 20;             // Changes x to 20

// Address
cout << &x;            // Memory address of x
cout << ptr;           // Same address (value of ptr)
cout << &ptr;          // Address of pointer itself
```

## Null Pointers
```cpp
// Old way
int* ptr = NULL;

// C++11 way (BETTER!)
int* ptr = nullptr;

// Always check before dereferencing
if(ptr != nullptr) {
    cout << *ptr;
}
```

## Pointer Arithmetic
```cpp
int arr[] = {10, 20, 30, 40, 50};
int* ptr = arr;        // Points to first element

cout << *ptr;          // 10
cout << *(ptr + 1);    // 20 (next element)
cout << *(ptr + 2);    // 30

ptr++;                 // Move to next element
cout << *ptr;          // 20
```

## References
```cpp
// Reference = alias for variable
int x = 10;
int& ref = x;          // ref is another name for x

ref = 20;              // Changes x to 20
cout << x;             // 20

// References must be initialized
// int& ref;           // ERROR!

// Can't reassign reference
int y = 30;
ref = y;               // This assigns y's VALUE to x, doesn't change ref!
```

## Pass by Value vs Reference vs Pointer
```cpp
// Pass by value (copy made)
void modifyValue(int x) {
    x = 100;           // Only modifies local copy
}

// Pass by reference (modifies original)
void modifyReference(int& x) {
    x = 100;           // Modifies original
}

// Pass by pointer (can modify original)
void modifyPointer(int* x) {
    *x = 100;          // Modifies original
}

// Usage
int num = 50;
modifyValue(num);      // num still 50
modifyReference(num);  // num now 100
modifyPointer(&num);   // num now 100

// Const reference (can't modify, no copy)
void display(const int& x) {
    cout << x;         // Can read, can't write
    // x = 10;         // ERROR!
}
```

## Dynamic Memory Allocation
```cpp
// Allocate single value
int* ptr = new int;         // Allocate
*ptr = 10;                  // Use
delete ptr;                 // MUST delete!
ptr = nullptr;              // Good practice

// Allocate with initial value
int* ptr = new int(42);

// Allocate array
int* arr = new int[10];     // Array of 10 ints
arr[0] = 1;
arr[1] = 2;
delete[] arr;               // MUST use delete[]!
arr = nullptr;

// Object allocation
class Player {
public:
    Player(string n) { cout << "Created " << n << endl; }
    ~Player() { cout << "Destroyed" << endl; }
};

Player* p = new Player("Billy");
p->display();              // Use -> for pointers
delete p;
```

## Memory Leaks (AVOID!)
```cpp
// BAD - memory leak!
void badFunction() {
    int* ptr = new int(10);
    // Function ends, ptr deleted, but memory not freed!
}

// GOOD - proper cleanup
void goodFunction() {
    int* ptr = new int(10);
    // ... use ptr ...
    delete ptr;
}

// BAD - losing pointer
int* ptr = new int(10);
ptr = new int(20);         // Lost first allocation - leak!

// GOOD
int* ptr = new int(10);
delete ptr;
ptr = new int(20);
delete ptr;
```

## Smart Pointers (C++11 - AUTO CLEANUP!)
```cpp
#include <memory>

// unique_ptr - single owner
{
    unique_ptr<int> ptr = make_unique<int>(10);
    cout << *ptr;
    // Auto deleted when out of scope!
}

// unique_ptr with objects
unique_ptr<Player> player = make_unique<Player>("Billy");
player->attack();
// Auto deleted

// Can't copy unique_ptr (only one owner)
// unique_ptr<int> p2 = p1;  // ERROR!

// But can move ownership
unique_ptr<int> p2 = move(p1);  // p1 now nullptr

// shared_ptr - multiple owners
shared_ptr<Player> p1 = make_shared<Player>("Billy");
shared_ptr<Player> p2 = p1;    // Both own it
p1.use_count();                // 2 (reference count)
// Deleted when LAST owner dies

// weak_ptr - doesn't affect reference count
weak_ptr<Player> weak = p1;
if(auto ptr = weak.lock()) {   // Check if still valid
    ptr->attack();
}
```

## Arrays vs Pointers
```cpp
// Array name is pointer to first element
int arr[5] = {1, 2, 3, 4, 5};
int* ptr = arr;                // No & needed!

cout << arr[0];                // 1
cout << *arr;                  // 1 (same thing!)
cout << *(arr + 1);            // 2

// But arrays know their size (kind of)
sizeof(arr);                   // 20 (5 * 4 bytes)
sizeof(ptr);                   // 8 (pointer size)

// Pass array to function
void processArray(int* arr, int size) {
    for(int i = 0; i < size; i++) {
        cout << arr[i] << " ";
    }
}

int arr[5] = {1, 2, 3, 4, 5};
processArray(arr, 5);
```

## Pointer to Pointer
```cpp
int x = 10;
int* ptr = &x;
int** pptr = &ptr;    // Pointer to pointer

cout << **pptr;       // 10 (double dereference)

// Modify pointer through pointer
int y = 20;
*pptr = &y;           // Now ptr points to y
cout << *ptr;         // 20
```

## Function Pointers
```cpp
// Pointer to function
int add(int a, int b) { return a + b; }
int subtract(int a, int b) { return a - b; }

int (*operation)(int, int);  // Function pointer

operation = add;
cout << operation(5, 3);     // 8

operation = subtract;
cout << operation(5, 3);     // 2

// Callback pattern
void calculate(int a, int b, int (*func)(int, int)) {
    cout << func(a, b);
}

calculate(10, 5, add);       // 15
calculate(10, 5, subtract);  // 5
```

## This Pointer
```cpp
class Player {
    int health;
    
public:
    Player(int health) {
        this->health = health;  // Disambiguate parameter
    }
    
    Player& setHealth(int h) {
        health = h;
        return *this;           // Return reference to self
    }
    
    // Method chaining
    Player& heal(int amount) {
        health += amount;
        return *this;
    }
};

// Usage
Player p(100);
p.setHealth(80).heal(20);      // Chaining!
```

## Common Pitfalls
```cpp
// 1. Dangling pointer
int* ptr = new int(10);
delete ptr;
cout << *ptr;          // UNDEFINED BEHAVIOR!
ptr = nullptr;         // Fix: set to nullptr after delete

// 2. Double delete
int* ptr = new int(10);
delete ptr;
delete ptr;            // CRASH!
ptr = nullptr;         // Fix: set to nullptr

// 3. Returning pointer to local
int* badFunction() {
    int x = 10;
    return &x;         // BAD! x destroyed when function ends
}

// Fix: return by value or use dynamic allocation
int* goodFunction() {
    return new int(10);  // Caller must delete!
}

// Better: use smart pointers
unique_ptr<int> betterFunction() {
    return make_unique<int>(10);  // Auto cleanup!
}

// 4. Array delete mismatch
int* ptr = new int[10];
delete ptr;            // WRONG! Should be delete[]
delete[] ptr;          // CORRECT
```

## Quick Rules for Game Dev
1. **Use smart pointers** instead of raw `new`/`delete`
2. **unique_ptr** for single ownership (most common)
3. **shared_ptr** when multiple objects need same resource
4. **Always** `delete` what you `new` (or use smart pointers)
5. **Always** `delete[]` for arrays
6. Set pointers to `nullptr` after deleting
7. Pass large objects by `const &` to avoid copies
8. Use references for function parameters when possible
9. Check `nullptr` before dereferencing
10. Avoid raw pointers in game code when possible

## Game Dev Examples
```cpp
// Managing game objects
class GameObjectManager {
    vector<unique_ptr<GameObject>> objects;
    
public:
    void addObject(unique_ptr<GameObject> obj) {
        objects.push_back(move(obj));
    }
    
    void update() {
        for(auto& obj : objects) {
            obj->update();
        }
    }
};

// Usage
GameObjectManager manager;
manager.addObject(make_unique<Player>("Billy"));
manager.addObject(make_unique<Enemy>("Goblin"));

// Resource management
class Texture {
    unsigned char* data;
    int width, height;
    
public:
    Texture(const char* filename) {
        // Load texture data
        data = new unsigned char[width * height * 4];
    }
    
    ~Texture() {
        delete[] data;  // Auto cleanup
    }
    
    // Prevent copying (or implement proper copy)
    Texture(const Texture&) = delete;
    Texture& operator=(const Texture&) = delete;
};
```

---

## Related Notes
- [C++ Basics for Game Dev](C++-Basics-for-Game-Dev)
- [C++ Smart Pointers](C++-Smart-Pointers)
- [Memory Management Patterns](Memory-Management-Patterns)
- [C++ STL Containers](C++-STL-Containers)
- [RAII Pattern](RAII-Pattern)
