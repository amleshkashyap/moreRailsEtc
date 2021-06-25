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

## proc and lambda -
  * Class "Proc" has objects of type - lambda, proc. lambda is like a method/function, proc is like a block. "lambda?" method to differentiate Proc objects.
  * One way to create a proc is via using '&block' argument and passing a block at invocation.
  * (a) Proc.new \<block\>, or just, (Kernel.)proc \<block\> (for proc), (b).(i) (Kernel.)lambda \<block\> (for lambda), (ii) lambda {|x| p x} == ->(x){ p x }, 
    (iii) also, (ii) supports default arguments, eg, ->(x, y=2){ p x, y }
  * proc/lambda objects to be invoked using call method. any object with call method can be invoked via .() as well, ie, proc.call(x) == proc.(x) { == proc[x] }
  * lambda, like proc, isn't a block - passing lambda to a method expecting a block would mean using '&' before the lambda based block in actual arguments - avoid.
  * There's a concept of arity, ie, number of arguments to the block, which get confusing when arguments can variable (ie, uses \*). Ignoring.
  * Two Proc objects will return true for equality test when created using clone/dup methods - write a parser to identify equivalent blocks in a large codebase?

## Closures - 
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
  * operator overloading in classes - for an object obj, if there's a "def \*(num)" instance method, then obj * 2 works, but 2 * obj calls the "\*" method of Integer
    (assume num is an integer). Probably similar for other operators. As seen earlier with adding Rational and Fixnum, coerce can be utlized - override coerce to
    switch the order, so that 2 * obj is computer as obj * 2, eg, def coerce(other); [self, other]; end;
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
  * Memory in Ruby, Multithreading, Thread safety, Background jobs -
    - https://gettalong.org/blog/2017/memory-conscious-programming-in-ruby.html
    - https://www.sitepoint.com/ruby-uses-memory/
    - When multithreading in Ruby, be careful while modifying an object via different threads - instance/class variables aren't thread safe - this is of relevance
      when threads are invoked from within the code (and hence, can potentially operate on same object)
    - Software concurrency is a difficult thing, unlike hardware concurrency, which is well defined - eg, for a small supercomputer, it looks like this -
      system -> level-1 -> level-2 -> ... -> fast-group-1 (set of cpu/gpu, eg, blade/rack/node) -> chip (eg, multicore cpu/gpu) -> 1/many threads
    - In sidekiq, organization per sidekiq process is - (queues, workers) -> jobs -> actual code with loops - can utilize threading at any place. now the basic unit
      of work in sidekiq is job, ie, a queue can have 10s of workers, with each workers having 10s of jobs (or, a worker having 10s of queues), but finally, sidekiq
      actually does the computation at job level - thus concurrency works there. One can complicate things by spawning threads within jobs (they're Ruby threads) -
      and then, have a great time debugging, if not done carefully.
    - https://blog.appsignal.com/2019/10/29/sidekiq-optimization-and-monitoring.html, https://dzone.com/articles/thread-safe-apis-and-sidekiq
    - Sidekiq thread safety - https://github.com/mperham/sidekiq/wiki/Problems-and-Troubleshooting#threading
    - Now since sidekiq threads are operating on jobs, what is thread safety? Rails is running constantly, and a sidekiq process is separately running, and then
      something is sent to sidekiq for execution - still, how likely it is that multiple threads of sidekiq access same class/instance variables?
    - Will return on this topic - multiple scenarios.

  * 
