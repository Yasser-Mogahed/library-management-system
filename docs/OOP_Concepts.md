# OOP Concepts: Tasks 1-20

All examples are Python. Where a concept does not exist natively in Python, the answer says so and shows the closest equivalent.

---

## Task 1: What is Object-Oriented Programming (OOP)?

A programming paradigm that organizes software around **objects**, which bundle data (attributes) and behavior (methods). Its four pillars are encapsulation, abstraction, inheritance, and polymorphism. It makes large programs easier to model, reuse, and maintain.

## Task 2: Class vs Object

| Class | Object |
|---|---|
| Blueprint / template | Instance built from the blueprint |
| Defined once | Many can be created |
| Holds no per-instance data itself | Holds its own attribute values |

```python
class Car:                    # class
    def __init__(self, color): self.color = color

a, b = Car("red"), Car("blue")   # two objects
```

## Task 3: Encapsulation vs Abstraction

| Encapsulation | Abstraction |
|---|---|
| Hides **data** and controls access to it | Hides **complexity**, exposes only what is needed |
| Solves "how do I protect state?" | Solves "what should the user see?" |
| Done with private attributes, properties | Done with abstract classes / interfaces |

```python
class Account:
    def __init__(self): self.__balance = 0          # encapsulation
    @property
    def balance(self): return self.__balance
```

## Task 4: Inheritance vs Composition

**Inheritance** = "is-a" (`Dog` is an `Animal`). **Composition** = "has-a" (`Car` has an `Engine`). Prefer composition when classes are not truly a subtype; it is more flexible and less tightly coupled.

```python
class Animal: ...
class Dog(Animal): ...          # inheritance

class Engine: ...
class Car:
    def __init__(self): self.engine = Engine()   # composition
```

## Task 5: Method Overloading vs Method Overriding

| Overloading | Overriding |
|---|---|
| Same name, different parameters, same class | Same name and signature, in a subclass |
| **Not supported natively in Python** (last definition wins) | Supported |
| Simulated with default args, `*args`, or `functools.singledispatch` | Uses inheritance |

```python
def area(w, h=None):            # simulated overloading
    return w * w if h is None else w * h

class Shape:
    def draw(self): print("shape")
class Circle(Shape):
    def draw(self): print("circle")   # overriding
```

## Task 6: Compile-Time vs Run-Time Polymorphism

| Compile-time (static) | Run-time (dynamic) |
|---|---|
| Resolved before execution | Resolved while the program runs |
| Method/operator overloading (Java, C++) | Method overriding |
| Not native in Python | Native in Python (duck typing, overriding) |

Python's closest compile-time equivalent is operator overloading (`__add__`).

## Task 7: Abstract Class vs Interface

| Abstract class | Interface |
|---|---|
| Can hold implemented methods and state | Only method contracts (in classic definition) |
| A class inherits from only one (in Java) | A class can implement many |
| Python: `abc.ABC` + `@abstractmethod` | Python has no `interface` keyword; use an ABC with only abstract methods, or `typing.Protocol` |

```python
from abc import ABC, abstractmethod
class Notifier(ABC):                 # acts as an interface
    @abstractmethod
    def send(self, msg): ...
```

## Task 8: Association vs Aggregation vs Composition (conceptual)

| Type | Relationship | Lifetime | Example |
|---|---|---|---|
| Association | "uses / knows" | Independent | Teacher and Student |
| Aggregation | "has-a" (weak) | Parts live without the whole | Library and Books |
| Composition | "owns-a" (strong) | Parts die with the whole | House and Rooms |

In this project: `Library` aggregates items; `Member` composes `Loan`s.

## Task 9: Static Members vs Instance Members

| Static / class members | Instance members |
|---|---|
| Belong to the class, shared by all objects | Belong to each object |
| Defined in class body, `@classmethod`, `@staticmethod` | Defined with `self` in `__init__` |

```python
class Item:
    count = 0                       # static
    def __init__(self): self.name = "x"; Item.count += 1   # name is instance
```

## Task 10: Constructor vs Destructor

| Constructor | Destructor |
|---|---|
| `__init__` (after `__new__` creates the object) | `__del__` |
| Runs when the object is created | Runs when the object is about to be destroyed |
| Initializes state | Releases resources |

In Python, `__del__` timing is not guaranteed; prefer context managers (`with`) for cleanup.

## Task 11: Access Modifiers

Python has no enforced modifiers; it uses naming conventions.

| Level | Syntax | Meaning |
|---|---|---|
| Public | `name` | Accessible everywhere |
| Protected | `_name` | Internal use / subclasses (convention) |
| Private | `__name` | Name-mangled to `_Class__name` to avoid accidents |

## Task 12: Mutable vs Immutable Objects

| Mutable | Immutable |
|---|---|
| Can change after creation | Cannot change after creation |
| `list`, `dict`, `set`, most custom objects | `int`, `str`, `tuple`, `frozenset` |
| Not hashable by default | Hashable (usable as dict keys) |

```python
a = [1]; a.append(2)        # same object changed
s = "hi"; s += "!"          # new string created
```

Custom immutable classes: `@dataclass(frozen=True)`.

## Task 13: Shallow Copy vs Deep Copy

| Shallow (`copy.copy`) | Deep (`copy.deepcopy`) |
|---|---|
| Copies the outer object only | Copies the object and everything nested |
| Nested objects are **shared** | Nested objects are **independent** |

```python
import copy
a = [[1, 2], [3]]
s, d = copy.copy(a), copy.deepcopy(a)
a[0].append(99)
print(s[0])   # [1, 2, 99]  shared
print(d[0])   # [1, 2]      independent
```

## Task 14: Tight Coupling vs Loose Coupling

| Tight | Loose |
|---|---|
| Class depends on a concrete class | Class depends on an abstraction |
| Hard to change or test | Easy to swap and test |

```python
class Tight:
    def __init__(self): self.n = ConsoleNotifier()   # hard-wired

class Loose:
    def __init__(self, n: Notifier): self.n = n      # any Notifier works
```

## Task 15: Dependency Injection vs Direct Dependency (basic)

**Direct dependency**: a class creates the objects it needs. **Dependency injection**: the objects are passed in from outside (constructor, setter, or argument). In this project, `Library(name, notifier=SilentNotifier())` lets tests replace the console notifier.

## Task 16: OOP vs Procedural Programming

| OOP | Procedural |
|---|---|
| Organized around objects | Organized around functions |
| Data and behavior together | Data and functions separate |
| Better for large, evolving systems | Simple for small scripts |
| Encapsulation, inheritance, polymorphism | Top-down step-by-step flow |

## Task 17: OOP vs Functional Programming

| OOP | Functional |
|---|---|
| Objects with mutable state | Pure functions, immutable data |
| Behavior attached to objects | Functions are first-class values |
| Side effects are common | Side effects avoided |
| Reuse via inheritance/composition | Reuse via function composition, `map`/`filter`/`reduce` |

Python supports both, and they mix well.

## Task 18: Runtime Binding vs Compile-Time Binding

| Compile-time (early / static) | Runtime (late / dynamic) |
|---|---|
| Method call linked before execution | Method call linked while running |
| Static, private, final methods in Java/C++ | Overridden (virtual) methods |
| Faster, less flexible | Flexible, enables polymorphism |

Python uses **runtime binding for everything** because it is dynamically typed:

```python
for shape in [Circle(), Square()]:
    shape.draw()        # which draw() runs is decided at runtime
```

## Task 19: Multiple vs Multilevel Inheritance

| Multiple | Multilevel |
|---|---|
| One class has **several parents** | A **chain**: grandparent -> parent -> child |
| `class C(A, B)` | `class C(B)`, `class B(A)` |
| Can cause the diamond problem | No ambiguity |

Python resolves multiple inheritance with the **MRO** (C3 linearization), viewable via `C.__mro__`. This project uses both: `StudentMember -> Member -> Person` is multilevel, and `Member(Person, ABC)` is multiple.

## Task 20: Garbage Collection vs Manual Memory Management

| Garbage collection | Manual management |
|---|---|
| Runtime frees unused memory automatically | Programmer allocates and frees (`malloc/free`, `new/delete`) |
| Safer (fewer leaks, no dangling pointers) | Faster and more predictable, but error-prone |
| Python, Java, C# | C, C++ |

Python uses **reference counting** plus a **cyclic garbage collector** (`gc` module) for reference cycles.
