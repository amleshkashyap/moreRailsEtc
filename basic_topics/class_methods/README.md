# Methods
  * Not an object by default (like blocks), although can be converted into one with identical behavior.
  * undef (used to undefine methods) has an interesting use case - undefining a method in child class (which doesn't affect the parent class) - although it's not 
    common, rather redefine is used (like other OOP langs). Alternatively, can use undef\_method.
  * alias new\_name original\_name => for giving a new name to a method. Recall include? and member? methods from Range class which do the same thing post 1.9
    Using it for "naturalness" is pointless as it creates ambiguity. A good usecase is to redefine a method outside the class but use the contents of original 
    definition, thus the original method can be invoked inside the new definition via its alias.
  * Had been wondering how to do this - pass method arguments in arbitrary order using argument names - Ruby doesn't officially support this. An approximation is
    supported though, via passing a hash as argument and then accessing from that (but nothing unique about it). But then, instead of passing a hash like fun({}),
    Ruby supports fun() with keys of the hash laid out in the open (only if it's the last argument though) in any order (bare hash) thus almost reaching there.
  * Method args don't need to be wrapped inside () - "fun(a) == fun a". Don't use this in above though, ie, "fun({:a=>1}) != fun {:a=>1}" throws a syntax error,
    instead we have "fun({:a=>1}) == fun :a=>1".
  * Methods have access only to their local variables - unlike blocks which can access even outside - thus methods can't help in creating closures (all below).
    - so anything which is present in the definition of an entity isn't said to have a "binding" relationship, eg, local vars of methods/blocks aren't bindings.
    - anything which outside the definition but a necessity in order for the entity to be useful is a "binding" relationship, eg, objects on which methods are called.
    - apart from objects, methods aren't binded to anything else - although, they can be unbounded (ie, bound to nothing) - they do nothing until binded.
  * Method class behaves similar to Proc class - its methods are to\_proc, arity, call (and hence, .(), []) - less efficient than invoking normally
    - Can convert a method object to a lambda object by using '&' - which will convert using to\_proc
    - method object invokation follows invokation semantics (hence more like lambda) and statements like return/rescue/break, etc behave similar as a method.
    - method can be converted to a Proc when passing as an argument - also, define\_method accepts a block to be converted to a method - that block can in turn be
      another method or proc object.
  * UnboundMethod class is interesting, it objects are methods which aren't bounded but can be bounded.
    - They're like methods from Modules
    - It's unclear whether unbounded methods can be non-object (like methods are by default). They're an object from this class, which can be used to create objects
      from Methods class via binding.

    ```Ruby
      plus = Fixnum.instance_method('+')  # unbound method plus, can't be invoked using plus.call/plus[]/plus.()
      plus_two = plus.bind(2)  # plus_two is binded to 2, plus remains unbounded
      plus_two.call(3)  # returns 2 + 3 = 5
      plus_again = plus_two.unbind  # plus_again is unbounded, plus_two remains bounded
    ```

# Blocks
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

# proc and lambda -
  * Class "Proc" has objects of type - lambda, proc. lambda is like a method/function, proc is like a block. "lambda?" method to differentiate Proc objects.
  * One way to create a proc is via using '&block' argument and passing a block at invocation.
  * (a) Proc.new \<block\>, or just, (Kernel.)proc \<block\> (for proc), (b).(i) (Kernel.)lambda \<block\> (for lambda), (ii) lambda {|x| p x} == ->(x){ p x }, 
    (iii) also, (ii) supports default arguments, eg, ->(x, y=2){ p x, y }
  * proc/lambda objects to be invoked using call method. any object with call method can be invoked via .() as well, ie, proc.call(x) == proc.(x) { == proc[x] }
  * lambda, like proc, isn't a block - passing lambda to a method expecting a block would mean using '&' before the lambda based block in actual arguments - avoid.
  * There's a concept of arity, ie, number of arguments to the block, which get confusing when arguments can variable (ie, uses \*). Ignoring.
  * Two Proc objects will return true for equality test when created using clone/dup methods - write a parser to identify equivalent blocks in a large codebase?

# Closures - 
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

# Towards Functional Style
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

# Functional Programming
  
