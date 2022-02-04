### Common Patterns

  * Notable Practices -
    - Create and inherit from classes instead of writing new methods to existing classes - base classes should be very general and abstract.
    - Create methods/classes for adding/customising objects.

  * Single Responsibility (Separation of Concern) -
    - A class should have a single responsibility - class files shouldn't be bloated doing all kinds of operations.
    - The class should have a single reason to change which should be related to its primary responsibility.
    - This begs the question - what are the various types of responsibilities?
      - Loading data - for 1 resource
      - Storing data - for 1 resource - storing can be argued to be something that can be same across each class - loading not necessarily as it might involve
        additional parsing/filtering of the fetched data.
      - Manipulating data - for 1 resource
      - Initializing data
    - Antipattern - God object, wherein one object does everything

  * Open Close Principle - class should be open for extension, closed for modification
    - Extension - ex. method overloading, inheriting from a base class
    - Modification is adding methods that give new functionality, often by adding functions.
    - Hard to use - need to write base classes and inherit those base classes instead of adding methods to base classes.
    - State space explosion - when adding criterias for some operation can lead to increase in possible ways for performing operation by combining criterias.
    - Ex. a class for filtering data of any other class based on some criterias => color, size, price - 7 ways to combine - if we add one more criteria then there
      are 15 ways to combine - so 8 new methods. Better to have a base class for filter and criterias, and keep extending criterias.

  * Liskov Substitution Principle - an interface which works with a class must also work with the classes that inherit that class
    - It's a principle that might be broken in very limited scenarios, especially when there's dependency between the instance variables of the class?
    - One possible case is when changing one property leads to a change in another property, and this can lead to bugs in the code which is making these changes.

  * Interface Segregation Principle - have separate, smaller interfaces to facilitate ease of programming
    - Break interfaces with many functions which are not necessarily going to be present in every class implementing that interface - domain specific.
    - Promotes multiple inheritance.

  * Dependency Inversion Principle - high level modules shouldn't depend on low level modules, rather on high level abstractions
    - This is different from dependency injection - although it is one way to implement dependency inversion
    - With dependency inversion, we can swap one class with another if required given that they've the same interface.
    - This is different from duck typing wherein one type is used instead of other if their interfaces are the same - but since they're different interfaces, changes
      in one won't necessarily be reflected in the other and would be a source for runtime errors - in dependency inversion, the classes must have same interface.
    - Major benefits include flexibility in unit testing, early and easy expression of specifications and easy to understand code.
    - https://stackoverflow.com/a/5698522

  * Gamma Categorization -
    - Creational patterns - explicit and implicit, single statement vs multistatement initialization
    - Structural patterns - a wrapper around a class, API design (ie, interface)
    - Behavioral patterns - for specific problems

  * Builder -
    - For multistep initialization of objects, builder object provides an API for their construction
    - A multistep builder can be created by initializing the object in a base class and then creating subclasses which initialize different aspects of the object,
      and the init method for those subclasses will call the init method of the base class - ie, base.init() -> base.transition(obj) -> sub.init(obj) -> base.init(obj)
    - Variables of parent class are accessible in child class obviously.
    - We could also have a chain of inheritance, every sub builder can inherit from another sub builder - seems unnecessary - this is to avoid breaking open close
      principle.

  * Factories -
    - For single step initialization of objects, factories can be used - factory methods, factory classes and abstract factory classes (interfaces).
    - Factory Method - any method that creates an object (eg, conditional initialization of objects can be replaced by separate methods). typically static methods.
    - Factory Class - an implementation of SRP or seaparation of concern - a class for initializing. Can be an inner class of the class for which it creates objects
      as well - an object of the inner class can be a member variable of the outer class (making the methods static). Class can provide many initializer methods.
    - Abstract Factories - when there's an interface being implemented by various types, we could've a factory base class as well and have separate factories for those
      by inheriting from the factory base class - factory base class must've a common set of methods of course (ie, an interface itself).

  * Prototype -
    - Complicated objects aren't designed from scratch - they use existing designs.
    - Existing (partially/fully constructed) design is a prototype - clone the prototype and customize it - use factories.
    - It's basically having a deep copy method for a class and then utilize that method to create and customize new objects - nested objects must be deep copied.
    - Prototype Factory - use a factory to create objects via prebuilt prototypes which can be deep copied and customized (static methods again).

  * Singleton -
    - Component (class) that needs to be initialized just once - eg, DB connection, factories
    - Use the same instance everywhere - isn't it dependency injectiona as well?
    - Prevent creation of additional copies and initialize only when needed (lazy initialization) - initialization cost is reduced.
    - Whenever the class is used, a new object will be created - but it must be prevented, ie, once one object is initialized, subsequent calls must return that.
    - Using decorators - decorate a class as singleton and the decorator method ensures there's only one copy
    - Using metaclass - a Singleton metaclass with a method similar to decorator.
    - Using monostate - have a constant and private kind of variable and that can be assigned (shallow copy) to the object at every initialization.
