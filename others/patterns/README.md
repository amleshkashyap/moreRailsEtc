### General

  * Trivia -
    - Design patterns almost always increase abstractions [to reduce complexity].
    - Abstractions can be understood better by working through a good number of these concrete scenarios.

  * Notable Practices -
    - Create and inherit from classes instead of writing new methods to existing classes - base classes should be very general and abstract.
    - Create methods/classes for adding/customising objects.

  * Gamma Categorization -
    - Creational patterns - explicit and implicit, single statement vs multistatement initialization
    - Structural patterns - a wrapper around a class, API design (ie, interface)
    - Behavioral patterns - for specific problems

#### SOLID Principles

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

#### Gang of Four Patterns

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
    - Problems - using Singleton class directly in methods has a disadvantage of making it harder to write good unit tests - if the data contained within the class
      changes, then the unit tests must change.

  * Adapter -
    - Converts/adapts an existing interface X to the required interface Y.
    - Adapter can be a service or a middleware - adapters come into picture when both interface are already written and one needs them to interact without change.
    - Sometimes, there might be multiple conversions of the same object to another, and we may want to cache those conversion.
    - Caching can be achieved in various ways, typically dictionary wherein the key is the hash of input object and value is the converted object.
    - Ex - converting yaml to json with different schemas for both formats.

  * Decorator -
    - Update the behaviour of an object -
      - If documentation exists, one might want to do this by updating the existing code.
      - However, this breaks OCP.
    - There are other ways to do it -
      - Creating a child class and adding the behaviour in child class, followed by using the child class - this can add and overrides behaviours.
        - Generally the child class should inherit from the base class of the object in question [if one exists].
        - This leads to a problem that the actual object's instance methods aren't accessible to this new class - unless we inherit from each of the child classes
          of the base class [assuming all/most of them need to be updated].
      - Passing the method to be
    - In python, we can have decorators which are methods which accept and return methods - can operate on the input method.
    - Classic decorators - augments the fucntionality of an existing class [
    - Dynamic decorators - runtime addition of methods to existing class - obviously required metaclass.

  * Command -

  * Chain Of Responsibility -

  * Interpreter -

  * Observer -

  * Mediator -

  * Composite -
    - Mechanism for treating single (scalar) and composite objects uniformly - since some scalar and composite objects might behave in similar ways.
    - A class can serve as a scalar (ie, can contain an array of objects) or as a composite (ie, can contain an array of [objects + array of objects] - many layers)
    - One of the tricks is to convert a scalar class (ie, returning a single object at init) to iterable (returning just itself).
    - Another trick is to use a separate class for performing composition related operations and have the relevant classes (which use it) inherit from it.
      - Explore - how is it connected to/used it rails DB compositions?
    - In python, make a class iterable using \_\_iter\_\_() method yielding self, or inheriting from Iterable [an abstract base class].

  * Bridge -
    - Prevents cartesian product complexity explosion - eg, filtering (text search, attribute based) for datastore (mongodb, elastic search, mysql)
      - Usual - 6 leaf classes, 2 parent, 1 base - 9
      - Using bridge - 3 leaf classes with 1 parent class, 2 classes which are also inherited by leaf, 1 base - 7 classes
    - Bridge decouples interface from implementation
    - Can be done by injecting one base class into another as a dependency
    - Eg, mongodb, elastic search and mysql classes - their init's have either text search or attribute based filter as input - used for mongodb.filter() method.
    - This pattern is useful only when a cartesian product of classes needs to be created. It is just a stronger form of encapsulation.
    - This pattern obviously has to break the open close principle which would've demanded the creation of many classes.

  * Iterator
