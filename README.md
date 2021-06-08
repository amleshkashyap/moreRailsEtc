# Ruby Object Model
  * Primary Sources - http://rubymonk.com, https://hokstad.com/ruby-object-model
  * BasicObject => Object, Kernel => Module => Class
  * Class::BasicObject (parent none) - instance\_eval, method\_missing, equal?
  * Module::Kernel (parent none) - puts, rand, loop, p, define\_method, autoload, Integer, Float, Array, Hash, sleep, raise, catch, require, lambda
  * Class::Object (parent BasicObject) - object\_id, class, instance\_of?, respond\_to?, inspect, equal, instance\_variables, is\_a, method, nil?, send, methods
  * Class::Module (parent Object) - method\_missing, attr\_accessor, include, remove\_method, class\_eval, module\_eval
  * Class::Class (parent Module) - new, superclass
  * send() - foo.method is equivalent to foo.send(:method)
  * method(method\_name) - returns the method object that hold method\_name
  * respond\_to? - checks if an object can respond to a given method (can be used instead of re-defining method\_missing)
  * clone and freeze - object references are stored always (like node/python) and hence "=" leads to shallow copy. use "clone" for deep copy to avoid changing the
    original object. "freeze" can be used to make an object immutable and "frozen?" tells whether an object is mutable or not.
  * singleton\_method and singleton\_class - 

# Collections, Literals, Constants and Variables
  * Primary Source - http://rubymonk.com
  * in place operations - eg, sub!(initial, later) replaces a string in place.
  * Enumerator Object - 
  * Class::Enumerable - 
  * Constants can be changed before runtime, but not at runtime (ie, within a method), represented starting with capital letter, class names are constants
  * Variables - class variables (using @@) have the same value even in the child classes despite redefining. A way to overcome this is to use class instance 
    variables (using @, but defining outside a method, like a class variable) - these have to be redefined in child classes so they can have a separate copy.
  * Method Overriding - a thing to note while calling an instance method from another is that we can just use the name of the method, but if we're calling an
    instance method which is overridden in the current class, then need to call it using self.
