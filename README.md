# Metaprogramming
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
     struct st_table *m_tbl;	// for storing methods
     VALUE super;		// pointer to superclass
   };
   ```
  * Other Resources - 
    - https://web.stanford.edu/~ouster/cgi-bin/cs142-winter15/classEval.php - class\_eval and instance\_eval
    - https://www.toptal.com/ruby/ruby-metaprogramming-cooler-than-it-sounds - building up metaprogramming using the define\_method and method\_missing
    - https://medium.com/swlh/metaprogramming-in-ruby-1b69b1b54202 - read this before the above
    - https://franck.verrot.fr/blog/2015/07/12/benchmarking-ruby-method-missing-and-define-method - some benchmarking
    - https://web.stanford.edu/~ouster/cgi-bin/cs142-winter15/classEval.php - class\_eval and instance\_eval

  * Metaclass -
    - a class that an object uses to redefine itself - the object can be a Class object or some normal object (or worse, some metaclass object)
    - an object can redefine a method by creating a class in a specific way
     ```Ruby
       class << m 
         def <method>
           <xyz work>
         end
       end
     ```
     ```Ruby
       def m.<method>
         <xyz work>
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

  * instance\_eval
    - this method is used to create a method for a class which isn't visible to the instances of the class (ie, it gets added to the metaclass of the class)

  * class\_eval
    - this method is used to create a method for a class which is visible to every instance of the class (ie, it becomes part of the metaclass of every instance)
