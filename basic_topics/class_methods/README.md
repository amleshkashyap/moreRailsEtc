# Methods-1 -
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
  * 

# Procs, Block, Lambda - Towards Functional Style
  * A break without a loop acts like a return.
  * proc and lambdas are two objects which can be created from a block (which is not an object) - both belong to Proc class.
  * return in a proc block created using Proc.new will lead to an exit from the method (where it's created) after being called. This leads to the following scenario -
    when a proc1 is being built using Proc.new in another meth2 by an invocation in meth1, and after creating the proc1, it returns it to meth1, which then calls it
    using proc1.call, then, control flow 
