### Metaprogramming
  * Primary Source - https://viewsourcecode.org/why/hacking/seeingMetaclassesClearly.html
  * Classes are objects too, but with some more properties - they can store methods as well, but normal objects can't, they can only have instance variables
  ```C
   struct RObject {
     struct RBasic basic;
     struct st_table *iv_tbl;
   };

   struct RClass {
     struct RBasic basic;
     struct st_table *iv_tbl;
     struct st_table *m_tbl;		// for storing methods
     VALUE super;			// pointer to superclass
   };
   ```
  * Other Resources - 
    - https://www.toptal.com/ruby/ruby-metaprogramming-cooler-than-it-sounds - building up metaprogramming using the define\_method and method\_missing
    - https://medium.com/swlh/metaprogramming-in-ruby-1b69b1b54202 - read this before the above
    - https://franck.verrot.fr/blog/2015/07/12/benchmarking-ruby-method-missing-and-define-method - some benchmarking
    - https://web.stanford.edu/~ouster/cgi-bin/cs142-winter15/classEval.php - class\_eval and instance\_eval

  * Metaclass (Singleton/Eigen Class) -
    - a class that an object uses to redefine itself - the object can be a Class object or some normal object (or worse, some metaclass object)
    - an object can redefine itself by creating a class in a specific way

     ```Ruby
       class Mailers
         @@service_providers = []
         def initialize(a)
           @provider = a
         end
       end

       m = Mailers.new("gmail")
     ```

     ```Ruby
       # this is a singleton method for the metaclass of instance "m" of class "Mailers"
       class << m 
         def <method>
           p "do xyz work"
         end
       end
     ```

     ```Ruby
       # singleton method way of doing the above - ie, <method> is only available to the object "m" - this is same as the above code
       def m.<method>
         p "do xyz work"
       end
      ```

      ```Ruby
        class Mailers
          # self is the object "Mailers" class, not an instance object of "Mailers" class - below is a metaclass of the class object "Mailers"
          class << self
            # this is a class method, available to all instances of "Mailers" as opposed to the singleton methods above. Note: what's the scope?
            def <new_method>
              p "do abc work"
            end
          end
        end
      ```
    - they hold instance methods, like "Class" objects, and can be attached to an object which can use these methods (now called "singleton methods")
    - as stated above, metaclasses stores all class methods as well
    - IMP: each object has its own metaclass, hence, it can have its own instance method too created at runtime, the infra for which can be setup in its class

  * meta\_def 
    - can be used to write a class method in class X which adds a class method to a derived class Y, but doesn't add it to X itself

  * define\_method 
    - originally, a method of the class "Module". this can be used to create a new method (usually, using a method) at the runtime

  * method\_missing 
    - originally, a method of the module "Kernel" (high up the hierarchy) which is eventually called if the method called for an object doesn't exist
      in the set of instance methods for the class or in any other ancestors 
    - this knowledge along with metaprogramming can be used to redefine method\_missing and then do something, eg, either create the method with some default 
      operation, or throw a different error message, etc

  * eval - evaluates a string argument - can evaluate in context of a Binding object (ie, bunch of stored information) if Binding object is 2nd argument.
    - can call Binding.eval too instead of passing Binding as argument to eval (ie, Kernel.eval)
    - can pass Proc object as second argument too - by creating a Binding object for a block of code via Proc.binding
    - must be avoided at all costs if input to eval is not known (unsafe code)
    - with the second argument possible, and the fact that it would be somewhere converting the string to a block - we've some spinoffs below.

  * instance\_eval
    - The arguments to this can be a string as well as a block (eval takes a string only)
    - The string/block is evaluated in context of the receiver object (self, if nothing specified) - the attributes of the receiver object are accessible in the
      arguments passed for evaluation - although if any attributes are not used, it's similar to eval (if string is passed).
    - Since a block/string can be evaluated in context of the (only one) receiver object, it's possible to add singleton methods to that object -
      1. for class object, class methods are added (ie, to the metaclass of the class)
      2. for instance object, singleton methods are added to that object's metaclass

  * class\_eval (also called module\_eval)
    - this method is used to create a method for a class which is visible to every instance of the class (ie, it becomes part of the metaclass of every instance).

  * instance\_exec, class\_exec
    - instance\_exec is like instance\_eval, but it doesn't accept string arguments, only blocks
      1. with this limitation, there's an extension that the passed block can accept arguments
      2. so instance\_exec has access to receiver object's variables + some extra arguments
    - class\_exec similar to class\_eval with above differences.

  * Hooks
    - In Object, Module, Class - method names end with "ed" generally for easy identification.
    - an example is the included method seen earlier in Module for separating class/instance methods. similarly we have extended method.
    - inherited - called on the superclass which is being inherited by another (when the latter is defined, this is called).
    - method\_added, method\_removed, method\_undefined - whenever a new method is added/removed/undefined from a class/module.
    - singleton\_method\_added, singleton\_method\_removed, singleton\_method\_undefined - for tracking singleton methods like above.

