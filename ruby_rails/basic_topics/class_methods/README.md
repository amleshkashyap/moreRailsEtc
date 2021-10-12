### Methods
  * Not an object by default (like blocks), although can be converted into one with identical behavior.
  * undef (used to undefine methods) has an interesting use case - undefining a method in child class (which doesn't affect the parent class) - although it's not 
    common, rather redefine is used (like other OOP langs). Alternatively, can use undef\_method.
  * "alias new\_name original\_name" => for giving a new name to a method. Recall include? and member? methods from Range class which do the same thing post 1.9
    Using it for "naturalness" is pointless as it creates ambiguity. A good usecase is to redefine a method outside the class but use the contents of original
    definition, thus the original method can be invoked inside the new definition via its alias.
  * Had been wondering how to do this - pass method arguments in arbitrary order using argument names - Ruby doesn't officially support this. An approximation is
    supported though, via passing a hash as argument and then accessing from that (but nothing unique about it). But then, instead of passing a hash like fun({}),
    Ruby supports fun() with keys of the hash laid out in the open (only if it's the last argument though) in any order (bare hash) thus almost reaching there.
  * Method args don't need to be wrapped inside ().
    ```Ruby
      fun(a) == fun a
      fun({:a=>1, :b=>2}) == fun(:b=>2, :a=>1)   # using bare hash for passing args in any order
      fun({:a=>1, :b=>2}) != fun {:b=>2, :a=>1}  # throws a syntax error, ie, when using bare hash arguments
      fun({:a=>1, :b=>2}) == fun :b=>2, :a=>1    # need to use this for bare hash args
    ```
  * Methods have access only to their local variables - unlike blocks which can access even outside - thus methods can't help in creating closures (all below).
    - so anything which is present in the definition of an entity isn't said to have a "binding" relationship, eg, local vars of methods/blocks aren't bindings.
    - anything which outside the definition but a necessity in order for the entity to be useful is a "binding" relationship, eg, objects on which methods are called.
    - apart from objects, methods aren't binded to anything else - although, they can be unbounded (ie, bound to nothing) - they do nothing until binded.
  * Method class behaves similar to Proc class - its methods are to\_proc, arity, call (and hence, .(), []) - less efficient than invoking normally
    - Can convert a method object to a lambda object by using '&' - which will convert using to\_proc
    - method object invokation follows invokation semantics (hence more like lambda) and statements like return/rescue/break, etc behave similar as a method.
    - method can be converted to a Proc when passing as an argument - also, define\_method accepts a block to be converted to a method - that block can in turn be
      another method or proc object.
    ```Ruby
      def func(a); p a; end
      fun = Object.method(:func)
      fun.call(a) == fun.(a) == fun[a]  # fun(a) throws an error though, method object isn't exactly same as a regular method
    ```
  * UnboundMethod class is interesting, it objects are methods which aren't bounded but can be bounded.
    - They're like methods from Modules. Method doesn't have 'bind' instance method, and 'unbind' instance method is not "in place" (ie, it returns a new object).
    - It's unclear whether unbounded methods can be non-object (like methods are by default). They're an object from this class, which can be used to create objects
      from Methods class via binding.

    ```Ruby
      plus = Fixnum.instance_method('+')  # unbound method plus, can't be invoked using plus.call/plus[]/plus.()
      plus_two = plus.bind(2)  # plus_two is binded to 2, plus remains unbounded
      plus_two.call(3)  # returns 2 + 3 = 5
      plus_again = plus_two.unbind  # plus_again is unbounded, plus_two remains bounded
    ```

### Blocks
  * Not an object by default but can be converted into one - multiple options available with varying properties (lambda and proc).
  * Pass block of code to methods (after the list of arguments) and then invoke the computation in the block - 
    - using yield (nothing to be mentioned about the block in the method's formal parameters)
    - using call (formal parameters must include '&block' as the last argument and the block is invoked using 'block.call' - yield can be used here too actually)
    - Latter method is for better readability and reduces ambiguity (should be preferred almost always?)
    - Here, 'block' becomes a Proc object instead of being a block. This doesn't imply all Proc objects have to be mentioned with '&' in formal parameters
  * Blocks can encapsulate larger expressions/statements - eg, pass a for loop as an argument to another method - what're the practical use cases?
  * Blocks can use local vars/arguments defined outside it (belonging to the method) - this property leads to existence of closures (similar to the JS closures mostly).
  * Blocks can have parameters, will call them block\_params always and not change any other lingo.
  * 1.8 - if any vars/args outside the block are used as params/locals inside the block, then updating them means updating them outside the block too.
  * 1.9 - all block params are local to the block despite name clashes. also, provision to define block local variables with name clashes too.
  * Basically - 
    - in 1.8, the local vars/args of the method with same names are shared between method and block (which has consequences when working with closures).
    - in 1.9, block\_params are always local despite name clashes, but vars local to the block/method are shared by default and can cause problems.
  * "&" is used before a formal parameter to represent a Proc object (or to indicate a possible block that needs to be converted to a Proc object). It can be used
    before actual parameters too as long as those objects have a to\_proc method (method's class also defines it, facilitating passing a method as an argument to
    iterators). Other use cases too.
  * "\*" is used before a formal parameter to represent an array of params, while it can be used before an actual param to indicate an array to be unpacked.

### proc and lambda -
  * Class "Proc" has objects of type - lambda, proc. lambda is like a method/function, proc is like a block. "lambda?" method to differentiate Proc objects.
  * One way to create a proc is via using '&block' argument and passing a block at invocation.
  * (a) Proc.new \<block\>, or just, (Kernel.)proc \<block\> (for proc), (b).(i) (Kernel.)lambda \<block\> (for lambda), (ii) lambda {|x| p x} == ->(x){ p x }, 
    (iii) also, (ii) supports default arguments, eg, ->(x, y=2){ p x, y }
  * proc/lambda objects to be invoked using call method. any object with call method can be invoked via .() as well, ie, proc.call(x) == proc.(x) { == proc[x] }
  * lambda, like proc, isn't a block - passing lambda to a method expecting a block would mean using '&' before the lambda based block in actual arguments - avoid.
  * There's a concept of arity, ie, number of arguments to the block, which get confusing when arguments can variable (ie, uses \*). Ignoring.
  * Two Proc objects will return true for equality test when created using clone/dup methods - write a parser to identify equivalent blocks in a large codebase?

### Closures - 
  * lambdas/procs can be defined inside a method using blocks, and these blocks can use the local vars/args of the method.
  * These Proc objects can then be created outside the method using specific argument "values" to the method (ie, the method would return lambdas/procs specifically
    created using those "values"). Now these procs/lambdas must be able to retain those "values" if they're to be of any use, ie, when they're invoked after creation.
  * Achieving this forces the interpreter to store more information, thus leading to multiple potential benefits - in fact, looks like all the vars/args of the
    method inside which these lambdas/procs are defined, are stored till the lifetime of these lambdas/procs. This property is called closure.
    - Does the interpreter store updates these variables specifically to provide a separate feature (ie, to have dynamic/changing values - instead of fixed values) or
      it had to return for some other reason and thus it was easy to add this capability too?
  * Above creates the concept of shared variable among procs/lambdas (created within the same method) - ie, one of them can change it, and other works on this 
    changed value (eg, a setter/getter method) - this seems to be the foundation for Classes/OOP (similar to JS).
  * multiple lambdas/procs can be created using a loop inside a method - and these lambdas can in turn use the loop index as local variables which is a potential
    source of bugs. Avoid.
     ```Ruby
       # simple example that works fine in 2.7
       def multipliers(a, b, *args)
         normal_lambda_one = ->(m){ a*m }
         normal_lambda_two = lambda { |m| b*m }
         lambda_array = []
         args.map {|i| lambda_array.push(lambda {|y| i*y })}
         return normal_lambda_one, normal_lambda_two, *lambda_array
       end

       single,double,triple,tetra = multipliers(1, 2, 3, 4)
       single.call(1); single.call(2);  # 1, 2 - same in 1.8
       double.call(1); double.call(2);  # 2, 4 - same in 1.8
       triple.call(1); triple.call(2);  # 3, 6 - 4, 8 in 1.8
       tetra.call(1); tetra.call(2);    # 4, 8 - same in 1.8
     ```
  * binding method on Proc object returns a Binding object with description for those closures (ie, Proc objects). Binding object can be passed as second argument
    to eval method to provide context for evaluating the String using eval. Binding also seems to be the a general mechanism of storing information for methods.

### Iterators
  * Caution? can some methods can be parallel?
  * eg, times, each, map, upto - these are followed by a block. if each is defined for the object, then a for loop can be used to loop on the object.
  * Basic iterator methods (meaning which iterate on the object based on defined ways and process the given block based on the iterations) -
    - Integer - upto, downto, times - take an init value, then call the "succ" method till the end value is reached, or some count is satisfied. eg, 3.times { block }
    - Float - ex, 0.step(Math::PI, 0.1) { block } goes from 0 till pi in steps of 0.1 (since no succ method defined for floats)
    - String - each\_char, each\_byte, each\_line -  eg, "hello".each\_char { block }
    - Enumerator object is a tuple - first element is an object, second element is an iterator method.
    - notice each iterator method is followed by a block - if there's no block, then the iterator method simply returns an Enumerator object,
      ex, "hello".each\_char, [].each, 4.times, {}.each_with_index - we can call Enumerable module functions (eg, map/inject) on this
  * Enumerables - Array, Hash, Range, etc - primarily "each" iterator and related iterators in the Enumerable module, eg, each\_with\_index
    - others are collect/map (output/input same length), select, reject, inject/reduce (single output)
  * Enumerators - convert an object to an Enumerator using to\_enum aka enum\_for (if done without an argument, "each" is considered the default)
    - first argument to enum\_for should be an iterator method - following are the same -
      ```Ruby
        "hello".each\_char
        Enumerator.new("hello", :each_char)
        "hello".enum_for(:each_char)   # alternatively, "hello".to_enum(:each_char)
        # all the above are supposed to work on ['h', 'e', 'l', 'l', 'o'] - "hello".chars also returns this array
        "hello".enum_for(:each_char).map { |c| c.succ } == "hello".chars.map { |c| c.succ }  # ['i', 'f', 'm', 'm', 'p']
      ```
    - any arguments after the first are used as arguments to the iterator method. also, I will not remember all these syntaxes.
    - Apart from using them for applying Enumerable module functions, they can also be used to prevent bugs - eg, if passing an array as an argument, then
      converting it to Enumerator (eg, array.to\_enum) before passing will give an immutable object (thus no need for deep copy to prevent object changes).
  * Summary - iterators and iteration is possible only upon a set of elements - specifically countable (but non-infinite) sets.
    - Array, Hash, Range, etc are naturally sets of (finite) elements - so we can directly move across the set in well defined ways (eg, "each" method), and also,
      manipulate the elements while moving (eg, map, inject, select). These methods to navigate across and manipulate the sets are in Enumerable module.
    - Integer, String are not a natural set of elements, but some tweaks can convert them to sets, and then methods from the Enumerable module can be used on them.
    - This tweaking is done via converting to Enumerator object - first element is the original object, second is the method to be applied on it to make it a set.
    - so, 4.times = [0, 1, 2, 3], "hello".each\_char = ['h', 'e', 'l', 'l', 'o']. Enumerator is just a good feature to have - we can create these arrays without it,
      sometimes, even more efficiently perhaps.

### Towards Functional Style
  * return statement returns from the method where it's called. break without a loop acts as a return.
  * return in a proc takes it outside the method obviously in normal cases. if a meth1 asks meth2 to create a proc from a block and return it so that it can "call" it,
    and that block has a return statement, then after meth1 calls the proc, a jump error is thrown after executing the block, because, supposedly, there are two
    returns, one from the block, and then another from meth2 which contains the block. My solution - don't do such things, I mean why do you want to use a return
    in a block/proc. If needed, use lambda - where return statement leads to return from the lambda only. So many corner cases.
  * break/next/redo/retry - avoid these in lambdas/blocks/procs.
  * raise - exceptions inside a block/proc/lambda looks for a rescue clause inside the enclosing entity, followed by returning to the invoker method (ie, yield/call)
  * Invocation semantics - method invocation follows a strict way to assign actual params to formal params (and throws errors for mismatches). lambdas have these
    semantics. procs have more flexibility, ie, the assignments are similar to parallel assignment rules (ie, multiple lvalue/rvalue scenarios etc). Bunch of rules.
    procs - yield semantics, lambdas - invocation semantics

### Functional Programming
  * Common functions - map, inject (inject is a reducer with an initial value to start the reduction with as the argument).
  * Modules - Functional
  * What are the implications on performance? How difficult to read the code and how many people use such paradigms? Will return later

### Class
  * class is an expression referred to by a value which is a constant. it's value is the last expression in it's body - typically an instance method using def.
    The value of the def statement is nil - however, following happened -
    ```Ruby
      obj = class Num
        def method_name
          p "Ok"
        end
      end
      obj  # output - :method_name - in 2.7
    ```
  * initialize method is private, invoked after object creation (probably in the memory/symbol tables) using new().
  * instance variables always belong to whatever object self refers to - so a class can have instance variables too (apart from class variables @@).
  * setter methods with assignment expressions should be used only via an object, eg, obj.x = 2 if there's a setter x=(value). doing it inside another instance method
    would mean using self.x = 2 instead of x = 2. similar issue seen before while overriding the ==(val) method (probably it's like = = val hence the issue)

### Operator, etc Overloading
  * For an object obj, if there's a "def \*(num)" instance method, then obj * 2 works, but 2 * obj calls the "\*" method of Integer (assume num is an integer).
    Probably similar for other operators. As seen earlier with adding Rational and Fixnum, coerce can be utlized - override coerce to switch the order, so that
    2 * obj is computer as obj * 2, eg,
    ```Ruby
      # coerce is an important method used by Ruby internally?
      def coerce(other)
        [self, other]
      end
    ```
  * Depending on the instance variables an object can have, some common operators/methods can be overridden to simplify programming - eg, assuming a class has 10
    instance variables, then override [] for allowing vars to be accessed as array elements, override each to make it Enumerable, etc. This would be more useful
    if all the variables of the object need to be updated after some changes (more suitable if all vars are updated according to some formula and bitmask maybe).
  * Doing the above has drawbacks in reality -
    - It can be confusing for others who don't read everything, and even for the writer if they don't understand completely.
    - Better way is to do these via named methods, eg, plus, is\_equal?, get\_index, etc - this forces readers to read the definition of the method instead of assuming
      (like they would for +, -, *, etc).
    - Overriding "each" seems inevitable if want to take benefits of Enumerable mixins.
    - This overriding problem is true for quite a few predefined methods for common operation, especially if other languages use it in different ways than Ruby
      (already seen for modulo and division operators) - strange that languages don't have standards for some must have operations.
    - Have to be careful while overriding (and even using) these groups -
      - ==, eql?, equal?, ===
      - empty?, blank?, present?, nil?
      - size, length
    - It's recommended to use the same operators inside while overriding it - eg, use eql? if overriding it in a class and so on.
  * Hash key problem again -
    - as mentioned, use symbols (immutable) or strings (immutability handled by Ruby). If an instance variable of an object is used as a Hash
      key, then retrieving it's value is possible only when same instance variable is passed (avoid these things) - unless we redefine eql? method in the class (because
      Hash uses eql? method for key comparisons, not for value though) - so eql? method can be overridden so that 2 instance variables (ie, 2 separate memory locations)
      can be used to retrieve the value from Hash if their values are same (again, avoid it and directly use the value as string/symbol), hash[@p] and hash[@q] should
      return the same value when p == q (and eql? is overridden). When does one need to use an instance variable as a Hash key?
    - now if eql? is overridden, hash method has to be overriden obviously (for computing hashcode according to the new definitions in eql?)
    - comparing object equality is a common operation - so ==/eql?/hash might need to be overridden. All of this suggest instance variables storage in memory is done
      using hashes by Ruby - remember objects have a pointer to a structure for storing instance variables (Ruby done in C).
    - finding a good hash is anyways a difficult problem, depending on the scenario. Following general purpose definition to be remembered
    ```Ruby
      # assume 10 instance variables a till j
      # one hash function can be @a.hash + @b.hash + .. + @j.hash
      # above is valid but leads to poor performance - probably due to higher number of possible collisions?
      # below is recommended
      def hash
        code = 17
        code = 37*code + @a.hash
        code = 37*code + @b.hash
        ...
        code = 37*code + @j.hash
        code
      end
    ```
  * More things recommended for overriding - OOPS doesn't seem very relevant for writing code where objects don't have long lifetime in programs - if they're to be
    stored into and fetched from DB, then having so many concepts and things are probably irrelevant - redis + DB + some simple language to connect things may be
    better. Imagine something like molecular dynamics or climate simulation where objects have to live for long durations, or even some games which last longer -
    OOPS, in its full complexity, might be much better suited there - but definitely OOP is more maintainable and looks organized/readable and hence, in reality,
    probably why its used and is so widespread. With that said, <=> can be also overridden to define ordering in a class.
  * Struct in Ruby - it can be used to create new classes quickly.
    ```Ruby
      Struct.new("SomeClass", :a, :b, :c)  # SomeClass is a new class Struct::SomeClass with 3 instance variables a,b,c
      Struct::SomeClass.class.to_s         # Class
      NewClass = Struct.new(:a, :b, :c)    # an unnamed class with 3 instance variables is created and assigned to a constant NewClass
      NewClass.class.to_s                  # Class - the constant NewClass is the name of the unnamed class created above
      BlankClass = Class.new               # a blank class - Class.new is a new class with no name, and assigned to a constant BlankClass
      BlankClass.class.to_s                # Class - BlankClass has now become the name of the unnamed class above
      obj = BlankClass.new                 # new object of the BlankClass
      obj.class.to_s                       # "BlankClass" - obj is an object of BlankClass (which was just a constant earlier)
    ```
    - Provides [] and []= operators. also provides each, each\_pair iterators, override == and define a to\_s.
    - Can open the class again and redefine new methods if required - Struct is a good quick way to have new classes.
  * Good syntax for a new class, with isolation among various entities
    ```Ruby
      class Something
        @@b  # class variable, shared with the child classes, can be used inside instance methods
        def initialize
          @x, @y = 2, 3  # instance variables
        end

        SomeConstant = "xyz"  # useful constants

        # instance methods
        def some_meth
        end

        def some_new_meth
        end

        # use this section to define the set of class methods, instead of doing def Something.some_class_meth or self.some_class_meth - cleaner
        class << self
          # class instance variable, not shared with the child classes, can't be used inside instance methods (they're variables of the Class object itself)
          # can also use attr_accessor :var, :nvar
          @var, @nvar = 2, 3
          # class methods
          def some_class_meth
          end

          def some_new_class_meth
          end
        end
      end
    ```
  * Define constants in a class above the initialize method (if the constants use instance variables). Define them from outside the class too, eg, Class::Constant = 3.


### Inheritance
  * A class that doesn't extend anything, extends Object.
  * One class can have only one parent - so there's a tree like hierarchy - although multiple inheritance can be achieved via mixins.
  * In Java/C++, contructor methods have same name as the class - so they're not inherited by default. here, initialize method is inherited too.
  * Struct based classes can have children as well (anyways Struct.new gives a class).
  * If a class has methods which invoke undefined methods, it's abstract (Ruby's Abstract classes) - subclasses can define these methods.
  * Since private methods are also inherited, it can be dangerous, since those are prone to being overridden - but that's a generic problem.
  * super - use this in subclass' instance method to invoke a method of the same name in the parent class (or any ancestor class). Better to explicitly pass
    arguments, no arguments would send the current instance method's actual arguments (with modified values, if modified).
  * Class methods are inherited too, can be overridden, and super can be used.
  * Better to call class methods with the actual class name for which they're invoked, eg, Child.some\_meth shouldn't be used if class method some\_meth isn't
    overridden in Child class, better use Parent.some\_meth. "new" method is an exception.
  * Inheritance is to utilize the behavior of parents in child - ie, methods - instance variables are states of the actual objects of a class - let's say a class has
    10 objects, then those 10 objects can follow similar processes (ie, methods) but on different initial states, represented by the instance variables. Thus, even
    for objects of same class, only the processes/methods are same, instance variables aren't. With this argument, it doesn't make sense to talk about inheritance
    of instance variables - subclasses will follow similar processes as their parent (with new/modified processes), and instance variables will be the initial states.
  * Class instance variables aren't inherited - class methods are inherited by the child class' class object though.
  * Since child/parent classes are an object of Class, it's difficult to digest that an object is inheriting behavior of another object.
  * There's a concept of static variables of a class in Java, wherein there's just one copy of the variable no matter how many objects of the class exist. These
    static variables are class variables - and by their very nature of being a single memory location, are also shared with the subclasses (and their objects). Same
    goes for static methods and class methods, but it's more relevant to think of this in case of class variables since they're prone to bugs.
  * Constants are also inherited, and can be redefined, like methods. Constants are anyways referrable as Parent::Constant and Child::Constant, so there's no
    warning of redefinition. If this redefined constant has to be used in a method which is not overridden in the child class, then that method call will use
    will work with the parent's constant, since constants are looked up in the lexical scope of where they're used - avoid these things.
  * Using Modules and Multiple Inheritance -
    - modules can be included in a class and the class thus has a new set of instance methods to be used only by the instances (not by Class itself).
    - modules can be extended in a class and the class object (not the instance objects though) have new set of class methods.
    - there is a complicated way to both include and extend the module to a class (via included method) - https://culttt.com/2015/07/08/working-with-mixins-in-ruby/
    - so a class can therefore inherit its parents behavior, and then mixin a bunch of methods (behaviors) too, thus giving the multiple inheritance effect.
    - class\_methods do is a shorthand provided by some gems to allow adding class methods via modules instead of doing all the above.
  * If a module is included in a class, then it's added to the ancestors of that class.
    - ancestors and superclass methods aren't defined for instance objects, superclass method isn't defined for modules.
    - There's a constant confusion between these methods - "class", "superclass", "ancestors", "is\_a?", "instance\_of?" - but it's easy to resolve wrt Ruby.
    - Luckily, only 2 things can be created using keywords followed by some code, followed by end -
      1. class - create an object which will return "Class" for "class" method - always
      2. module - create an object which will return "Module" for "class" method, "Object" for "superclass" method - always
    - Also, lambda creates an object which will return "Proc" for "class" method, "Object" for "superclass" method - no end required, just a block.
    - Consider this - this clarifies the constant/method resolution algo too somewhat, and useful for metaprogramming -
    ```Ruby
      module FirstIN; end; module LastIN; end;
      module FirstLH; end; module LastLH; end; module ConfuseLH; end;
      module FirstRH; end; module LastRH; end; module ConfuseRH; end;
      module IN; include FirstIN; include LastIN; end;
      class RHS; include FirstRH; include ConfuseRH; include IN; include LastRH; end;
      {'class' => ["< RHS", ".new"], 'module' => ['', '']}.each do |key, rhs|
        eval("#{key} LHS#{key.capitalize} #{rhs[0]}; include IN; end;")
        instance_obj = eval("LHS#{key.capitalize}#{rhs[1]}")
        p "Printing for #{key} - class, superclass, ancestors"
        p eval("LHS#{key.capitalize}.class")
        p eval("if LHS#{key.capitalize}.respond_to?(:superclass); LHS#{key.capitalize}.superclass; else; 'No superclass method defined for LHS#{key.capitalize}'; end")
        p eval("LHS#{key.capitalize}.ancestors")
        puts ""
        p "Printing for instance_obj - class, superclass, ancestors"
        p eval("if instance_obj.respond_to?(:class); instance_obj.class; else; 'No class method defined for instance_obj'; end")
        p eval("if instance_obj.respond_to?(:superclass); instance_obj.superclass; else; 'No superclass method defined for instance_obj'; end")
        p eval("if instance_obj.respond_to?(:ancestors); instance_obj.ancestors; else; 'No ancestors method defined for instance_obj'; end")
        puts ""
        puts ""
      end

      # prints this
        # "Printing for class - class, superclass, ancestors"
        # Class
        # RHS
        # [LHSClass, LastLH, ConfuseLH, FirstLH, RHS, LastRH, IN, LastIN, FirstIN, ConfuseRH, FirstRH, Object, Kernel, BasicObject]

        # "Printing for instance_obj - class, superclass, ancestors"
        # LHSClass
        # "No superclass method defined for instance_obj"
        # "No ancestors method defined for instance_obj"


        # "Printing for module - class, superclass, ancestors"
        # Module
        # "No superclass method defined for LHSModule"
        # [LHSModule, LastLH, ConfuseLH, IN, LastIN, FirstIN, ConfuseRH, FirstLH]

        # "Printing for instance_obj - class, superclass, ancestors"
        # Module
        # "No superclass method defined for instance_obj"
        # [LHSModule, LastLH, ConfuseLH, IN, LastIN, FirstIN, ConfuseRH, FirstLH]
    ```
    - instance\_of? is a straighforward method => obj.instance\_of?(X) method returns true only when X == obj.class. objects created using module and class keywords
      are instance\_of? Module and Class respectively. Any instance object is an instance\_of? its class (even class/module does a Class.new/Module.new).
    - is\_a? is a complicated method -
      1. an object ModObj whose class is Module - is\_a? returns true for every element of Module.ancestors
      2. an object ClObj whose class is Class, and superclass is SuperClass - is\_a? returns true for every element of Class.ancestors
      3. an object InstObj whose class is ClObj (ie, from (2)) - is\_a? returns true for every element of ClObj.ancestors
      4. summary - for an object AnyObj, is_a? returns true for every element of AnyObj.class.ancestors

### Modules
  * Clearly, modules don't have the inheritance property (although it has ancestors) - no superclass method.
  * Modules don't have a new method too, so an instance object is always an instance of an object whose class is Class (never Module).
    - Module can have instance and class methods - it's instance methods are useless unless the module is included in some class.
    - Its class methods are it's "own" methods - any instance of anything doesn't have access to it.
  * In the hierarchy seen earlier, BasicObject, Object, Module, Class - since for these, class is Class, they're inherited, eg, Numeric, String, Hash, SomeClass, but
    Kernel, Enumerable, etc aren't.
  * The class "Class" is a child of "Module", so it has all the properties of Module - eg, nesting.
  * Modules can have constants, methods and class variables too.
  * Module namespacing is good for some global methods, classes can be namespaced too.
  * Mixins - Module Mod can be included and extended in another class SomeClass.
    - When included, Mod's instance methods act as SomeClass' instance methods.
    - When extended, Mod's instance methods act as SomeClass' class methods.
      * Worth noting that extending a module means adding methods of the modules into singleton methods of the receiver object, eg, the extending Class in this case.
      * Would this mean that an instance object can also extend a module dynamically to provide itself with some singleton methods, if needed?
    - When included and extended, Mod's instance methods act as SomeClass' instance and class methods.
      * It is not possible to have separate class and instance methods for SomeClass when Mod is included and extended - all instance methods of Mod act as both.
      * This can be done though - Mod needs to have a nested module NestMod - SomeClass should include Mod, and extend NestMod. included method simplifies it.
    - When Mod is used as mixin, there should be a way to allow Mod to have its own private methods which need not be instance/class methods of SomeClass
      * They're the class_methods of Mod, defined as self.some\_meth or Mod.some\_meth inside the module => these need to be always invoked as Mod.some\_meth.
    - include is not a keyword - since method invocation need not have brackets for arguments. include Mod == include(Mod)
    - Clearly, including modules effects the is\_a? method
    - With all of this mixin, Module can effectively be seen as a class (if one removes the "own" methods) - and thus the multiple inheritance usecase.
    - Instance methods of a module can be converted to its "own" methods by using a keyword module\_function - should be avoided.

### Singleton Methods, Singleton/Eigen/Meta Class
  * singleton is a class with only one instance - so a new Class object, ClObj = Class.new, is just one object - it can have a singleton/meta class.
    - ClObj can have many instance objects - each of those have a singleton/meta class.
    - class methods of ClObj are stored in its metaclass, say, ClObjMeta
    - new class methods can be dynamically added to ClObjMeta
    - instance object of ClObj, say cl\_instance, are stored in its metaclass, say ClInstanceMeta.
    - new class methods can be added to ClInstanceMeta too.
    - If ClObj inherits from ClParentObj with a metaclass ClParentObjMeta, then ClParentObjMeta is the parent of ClObjMeta - this is why class methods are inherited.
    - ClInstanceMeta has no parent.


### Method Resolution
  1. check for singleton methods of the object (ie, defined specifically for that instance, stored in the metaclass of the object). Also, if the metaclass of an object
     has ancestors, then check there as well => metaclasses of normal objects don't have any ancestors, but metaclasses of Class object do have ancestors, eg,
     "metaclass of Fixnum object" (not an instance object of Fixnum) has "metaclass of Integer object" as its ancestor (and other ancestors too).
  2. check for instance methods in the object's class
  3. check for methods in the modules included in object's class - check the last included module first
  4. check for ancestor class' instance methods
     - (3) and (4) can be given by ancestors method, if unique modules are included in the class and its parents.
  5. if not found, check for method\_missing method, starting from (1) till (4) - it'll always be found in (4), ie, the Kernel module (ancestor's module).

### Constant Resolution
  * Say a constant is referred in class SomeClass which maybe be defined inside another class or module.
  1. check for the constant definition in the results of Module.nesting method - it includes all classes/module lexically above SomeClass.
     - all enclosing modules, if present, are checked, before checking included modules
  2. check in the ancestors of SomeClass - ancestors methods is above
  3. check in Object class (this means returning back to Object again after checking all ancestors) - all global constants are part of Object class.
     - when a constant is referenced from a module, ancestors of the module are checked, followed by Object class (for global constants)
     - since Kernel is after Object in ancestry, any constants in Kernel can be overridden by Object.
  4. check if const\_missing method is defined in SomeClass

### More
  * instance/class variables aren't thread safe - this would mean an object is supposed to be handled by one thread (since objects can't be ignored) and class
    variables are to be ignored - this is for multithreading in Ruby - while deployment, Phusion Passenger works via processes.
  * Memory locations being modified are almost always unsafe for anything global - with DB in picture, many processes can be trying to write.
