### Ruby Object Model
  * Primary Sources - http://rubymonk.com, https://hokstad.com/ruby-object-model
  * BasicObject => Object, Kernel => Module => Class
  * Class::BasicObject (parent none) - instance\_eval, method\_missing, equal?
  * Module::Kernel (parent none) - puts, rand, loop, p, define\_method, autoload, Integer, Float, Array, Hash, sleep, raise, catch, require, lambda
  * Class::Object (parent BasicObject) - object\_id, class, instance\_of?, respond\_to?, inspect, equal, instance\_variables, is\_a, method, nil?, send, methods
  * Class::Module (parent Object) - method\_missing, attr\_accessor, include, remove\_method, class\_eval, module\_eval
  * Class::Class (parent Module) - new, superclass
  * send() - foo.method is equivalent to foo.send(:method)
  * method(method\_name) - returns the Method object that holds method\_name
  * respond\_to? - checks if an object can respond to a given method (can be used instead of re-defining method\_missing)
  * clone and freeze - object references are stored always (like node/python) and hence "=" leads to shallow copy. use "clone" for deep copy to avoid changing the
    original object. "freeze" can be used to make an object immutable and "frozen?" tells whether an object is mutable or not.
  * singleton\_method and singleton\_class - 

### Summary
  * Primary Source - http://rubymonk.com
  * Enumerable class - important for performing operations on collection of elements (without reinventing the wheel, in an optimized, natively supported form) - eg,
    map for 1-1 transformation for each element of the set, inject for reduce operation on a set, select for picking up elements of a set based on criterias, etc.
  * Constants can be changed before runtime, but not at runtime (ie, within a method), represented starting with capital letter, class names are constants
  * Variables - class variables (using @@) have the same value even in the child classes despite redefining. A way to overcome this is to use class instance 
    variables (using @, but defining outside a method, like a class variable) - these have to be redefined in child classes so they can have a separate copy.
  * Method Overriding - a thing to note while calling an instance method from another is that we can just use the name of the method, but if we're calling an
    instance method which is overridden in the current class, then need to call it using self - this is only true when the method name contains '=' in it.
  * Must Read - blank/empty/nil/present - https://blog.appsignal.com/2018/09/11/differences-between-nil-empty-blank-and-present.html
  * Bug Reduction Suggestions By The Book
    - use to\_enum to convert Arrays to Enumerators - makes them immutable, no need for deep copies, etc.
  * Performance Suggestions By The Book
    - define efficient initialize\_copy method (from where?) in your class based on use\_cases to have fast deep copies
    - Use symbols wherever possible as hash keys - pretty fast. Use symbols wherever possible in general?
    - Avoid invoking methods via Method objects, avoid using Method objects completely.
    - Use parallel assignments if understand fully.
  * Ease Of Programming Suggestions/Features By The Book
    - Use hashes as parameters if want to have named parameters in any order (not supported by default) - more support for increased usage
    - In place operations - eg, sub!(initial, later) replaces a string in place.
  * Ease Of Programming To Ease The Reading For Others Suggestions By The Book
    - Avoid using functional programming
    - Use common syntaxes
  * Finishing a 400 page book on a language with lots of objects and abstractions is not easy for average folks like myself - some opinions are helping (writing
    notes on github, etc helps to track progress, provides extrinsic motivation, and the understanding can be scrutinized easily) -
    - Practical - https://www.quora.com/How-do-programmers-read-large-programming-books-I%E2%80%99m-aware-that-it%E2%80%99s-necessary-to-read-books-if-I-want-to-be-an-expert-programmer-How-do-I-read-them-and-understand-I-forget-things-easily/answer/Joe-Coffman-1
    - Short - https://www.quora.com/How-do-programmers-read-large-programming-books-I%E2%80%99m-aware-that-it%E2%80%99s-necessary-to-read-books-if-I-want-to-be-an-expert-programmer-How-do-I-read-them-and-understand-I-forget-things-easily/answer/Ryan-Cook-55
    - Indian - https://www.quora.com/How-do-programmers-read-large-programming-books-I%E2%80%99m-aware-that-it%E2%80%99s-necessary-to-read-books-if-I-want-to-be-an-expert-programmer-How-do-I-read-them-and-understand-I-forget-things-easily/answer/Mayank-Jaiswal
    - Long - https://www.quora.com/How-do-programmers-read-large-programming-books-I%E2%80%99m-aware-that-it%E2%80%99s-necessary-to-read-books-if-I-want-to-be-an-expert-programmer-How-do-I-read-them-and-understand-I-forget-things-easily/answer/Charles-Glover-65
    - Privileged - https://www.quora.com/How-do-programmers-read-large-programming-books-I%E2%80%99m-aware-that-it%E2%80%99s-necessary-to-read-books-if-I-want-to-be-an-expert-programmer-How-do-I-read-them-and-understand-I-forget-things-easily/answer/Kurt-Guntheroth-1
    - Professor - https://www.quora.com/How-do-programmers-read-large-programming-books-I%E2%80%99m-aware-that-it%E2%80%99s-necessary-to-read-books-if-I-want-to-be-an-expert-programmer-How-do-I-read-them-and-understand-I-forget-things-easily/answer/Norm-Matloff
