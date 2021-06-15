# Numeric Datatypes
  * Integer (Fixnum with 31 bits, Bignum), Float, Complex, BigDecimal, Rational - last 3 in standard lib, not ruby.
  * Start a numeric literal with 0x/0X for hex, 0b/0B for binary and 0[0-9]+ (eg, 034) for octal. Otherwise it's decimal.
  * 1\_00\_00 is same as 10000.
  * Good stuff - all integer overflows/underflows are automatically handled (ie, Fixnum to Bignum and vice versa). Floating point has special value for infinities
    (overflows) it underflows to zero. 0.0/0.0 is mostly NaN. Also, integers can be queried as arrays of bits with index[0] being LSB.
  * Weird stuff - (-7/3) (ie, -2.33) equals -3, not -2 like other languages, ie, negative divisions tend towards infinity instead of zero. Gets weirder - (-7/3) is
    said to be evaluated as (7/-3) and not -(7/3) like other langs, so (-7%3) somehow gives 2 instead of the expected value of -1. Google gives => (a) -2 for
    "7%(-3)", (b) 2 for "(-7)%3", (c) -1 for both "(-7)%(-3)" and "-(7%3)"
  * remainder, a different operator, behaves similar to modulo operator of other languages. "power of" operator is Fortran's ** (right to left eval).
  * IEEE-754 - it suffers from this problem => "0.4 - 0.3 == 0.1" evaluates to false (the whole specification is faulty of course - although binary representation
    can approximate 0.4, 0.3 and 0.1 almost perfectly). BigDecimal works with actual decimal handling of real numbers at the hardware (how? -
    https://ruby-doc.org/stdlib-2.5.1/libdoc/bigdecimal/rdoc/BigDecimal.html) thus avoiding such problems, but then it's significantly slower for large computations
    (fine for "typical" financial computations though).

# Textual Datatypes
  * Strings mostly - will return later.

# Arrays
  * Accessing an index which doesn't exist doesn't throw an error, just returns nil.
  * For a size n array, attempting to insert at n+2 doesn't throw an error, just creates a nil entry at n+1. Although doing so before first index throws an error.
  * Special cases - (1) %w[this is a test] = ['this', 'is', 'a', 'test'], (2) %w| ( [ { < | = ['(', '[', '{', '<'], (3) %W(\s \t \r \n) = ["\s", "\t", "\r", "\n"]
  * Subarray access possible - arr[0,5] returns 5 elements starting from index 0.
  * "+" can be used to concatenate 2 arrays only. "-" can be used to eliminate all instances of all elements of the right side array from the left one. "\*" can be
    used for replicating the elements of an array.
  * Check - compact!, delete\_if, each\_index, fill, flatten!, index, join, reverse\_each, rindex, shift, uniq!, unshift

# Hashes
  * (a) hash["a"] = 1, (b) hash = { "a" => 1 }, (c) hash = { :a => 1 }, (d) hash = { a: 1 } - last two being most efficient forms of hashes with immutable symbol keys
  * String hash keys are a special case handled by ruby and a private copy of keys is kept for virtual immutability - note that all this burden because "apparently"
    a hash can become corrupt (what does that even mean) if the keys are mutated which ultimately will mutate it's hashcode. This private copy for string keys makes
    it less efficient.
  * Can use other mutable objects as keys as well but then need to handle the mutability thing manually.
  * As stated somewhere else to, overriding eql? method in a class makes it mandatory to override the hash method too.

# Ranges
  * two dots if need to include the right hand object, three dots if need to exclude it.
  * Ordering - comparison operator <=>, used to evaluate ordering among elements of a class, eg, Integer/String, must be defined for the class whose objects are used
    to define a range (ie, the endpoints).
  * Iteration - if the class whose objects are used to define a range have a 'succ' method, then a range can be iterated, ie, there's an ordering where the next
    element can be found via the succ method. Eg, 'a'..'d'.to\_a will give ['a', 'b', 'c', 'd']. similarly each, step and Enumerable methods (like to\_a). Float
    doesn't have a succ method (hence, can't be iterated like each due to no definition of "next element", but defining the "next element" is possible via "step"
    method - ie, "0.25..0.45.step(0.1)" gives 0.25, 0.35, 0.45). This iteration seems very similar to Iterators - are they same?
  * Membership Tests - as obvious, testing membership via succ method is going to be slow, compared to <=> (ie, comparisons). After 1.8, cover? method tests
    membership via the comparison operator always, while include? and member? do this via comparison operator for Floats, but via succ method for other discrete
    classes (string/int) which is slow and can give different results than 1.8 and earlier (where these two always used comparison).

# Symbols
  * Symbol table used by Ruby interpreter to hold classes, methods, vars, etc using symbols. These are also usable in programs.
  * Can be thought of as immutable strings (as string methods defined for these).
  * Symbol tables holding symbols are fast for comparison because their address is known (ie, one symbol has a fixed address) - strings can be created as a
    different object everytime we mention it (even if it's the same string, can be a diff object), thus making comparison slower (need to understand more).

# Booleans
  * No booleans - TrueClass, FalseClass and NilClass for true, false, and nil. also, true != 1, and false != 0 as they're separate objects themselves of those classes.

# Objects
  * A very funny sentence says - method arguments are passed by value rather than reference - in C passing by reference would mean using * or &, but here even though
    a reference is being passed, it's actually a value (appropriate to call it value? why not variable/identifier/token name) which happens to be an object reference.
  * Garbage collection obviously, for objects with no references or references from other objects with no references. Avoid global variables as caches (or use some
    regular deletion mechanism). Every object is uniquely identified via a Fixnum identifier (constant, unique till object exists in memory). Can be obtained via
    object\_id method or \_\_id\_\_ keyword in case the former is overridden. hash method implemented to return this object\_id.
  * class and type problem - respond\_to? method has a shortcoming that it doesn't check the arguments (just method name). Hence, one can override a method of one
    class in a different class with a different argument and use it incorrectly. There is nothing called type, and it's merely the fact that objects from 2 different
    class might work with same methods throughout their lifetime and hence might appear to be same - but the arguments to those methods might be different (by, say,
    class, ie, one takes only String arguments, other takes only Fixnums) thus creating the concept of type - ie, the set of methods an object can respond to rather
    than just the class of the object.
  * equal? method - compares whether 2 operands refer to the same object. same as comparing object\_id for both operands (operands are literals refering to objects).
  * == method - same as equal? method in Object. Other classes override (eg, String to compare same characters). numerical classes do type conversions while overriding
    '==' so that equality is possible to check for different classes, ie, Fixnum/Float. String/Array/Hash might do a class (or type?) comparison first, by calling some
    method (eg, to\_str) on the right hand operand (to convert it to string? - bit unclear - can we have '1' == 1 or 1 == '1' return true? not on my irb), and then
    using its '==' operator to compare with left operand. != doesn't have to be a separate method, basically invert the result of '==' method.
  * eql? method - same as equal?, but generally can be overridden to emulate a '==' without the conversions (eg, Fixnum to Float etc).
  * === method - same as '==' method unless overridden (eg, Range, Regexp (checks if a string satisfies regex), Class, Symbol (matches with string too)).
  * =~ method - only for String/Regexp pattern matching.
  * Order - already discussed with Ranges, <=> method should return -1, 0, 1, nil only. If defined, elements are ordered (eg, Numeric, String). Comparable is a mixin
    that has <, <=, =, >= and > methods (among others like between?) and is included with classes defining <=>. With all this flexibility, it is possible to have a
    class where <=> and == can return different results for equality comparison, although not recommended.

# Object Conversions
  * Explicit conversion - to\_s, to\_i, etc - in fancy words, "methods which return a representation of an object as a value of another class"
  * Implicit conversion - eg, in 1.8, the Exception class was almost identical to String class (ie, one's object converted to another while comparison). Implicit
    conversions exist other places as well, not well documented.
    - Back to the "==" method for String, if both sides are String, they're compared, if not, the right-hand operand is checked for to\_str method, and if it exists,
      then the "==" method of the class to which the right-hand operator belongs to is invoked and asked to decide.
    - try\_convert method in 1.9, whose argument is tried to be converted to the relevant class (ie, String.try\_convert(s) tries to convert to String) and returns nil
      if not possible.
  * Kernel Module Conversion Functions - they attempt to convert the arguments to the same class as their names, and if not possible, return different results -
    Array (tries converting using to\_ary, then to\_a, then returns a new array with the argument as its element), Float (converts Numeric types to Float directly,
    else calls to\_f), Integer (truncates Floats, String no non-numeric trailing characters allowed, for the rest tries to\_int and then to\_i), String (just the
    to\_s method).
  * Coerce - returns an array of 2 elements of same type - (1) the type can be same as the object on which it's called, (2) can be a more generic type than both the
    object and the argument.
    - Numeric operators like "+" - if they encounter a right-hand operator with unknown type (eg, Rational from standard library), then they call the coerce method on
      the right-hand operand with left-hand as the argument, thus returning the result in right-hand operator type, followed by calling the "+" operator of the right
      hand type object. eg, Fixnum + Rational will call Rational.coerce(Fixnum) = [Rational, Rational] and then add those Rationals.
  * Boolean type conversions - anything except false/nil behaves like true (although true is a different object). no way to convert string to boolean. 0.0/0 also
    behaves like true.

# Object Operations
  * Copying - clone, dup - they call the initialize\_copy method of the class they're invoked on - if not defined, then a simple shallow copy is performed. Classes can
    override these two and defined initialize\_copy. clone can copy frozen and tainted states of an object, as well as any singleton methods it has - dup can only copy
    the tainted state, calling on frozen object unfreezes it.
  * Marshaling - Marshal.dump - converts given object (and any objects it references) to binary and optionally writes it to an I/O stream object. Marshal.load does
    opposite. Binary format used is version dependent. Also, useful for writing deep copy methods (ie, Marshal.load(Marshal.dump)). YAML is similar, only it converts
    to human readable text format.
  * Freezing - It restricts any mutations on the object. A frozen class object would mean can't add any methods to the class.
  * Tainting - To inform about potential security problems, identify and prevent them accordingly, an object can be marked as tainted. Any objects created from the
    original tainted object (eg, via clone/dup, via substring, or upcase, etc) are also marked tainted. $SAFE global variable can be utilized to tell what to restrict
    for these tainted objects. All command line arguments, env variables, and command line inputs using gets are tainted by default.

# Expressions
  * If a . or :: appears in an expression, it's treated as a method call and constant respectively (:: allowed for method call as well).
  * Uninitialized vars/consts - (1) Class vars - throws name error, (2) Global vars - assumea nil, (3) Instance vars - assumes nil, (4) Local vars - (a) check if it's
    method, (b) if not, then throw name error, (c) local vars come to existence only after they've been assigned a value, (d) one exception to (c) is that even if
    they've not been assigned a value but there's a conditional statement which can assign them a value if true, then they're treated as local variables with nil value,
    (5) Constants - don't exist and throw a name error if not assigned.
  * Methods calls - assumed to be on self if no object used. 
    - Code blocks can be passed after method calls (ie, after arguments). 
    - Ruby objects don't expose associated variables rather expose functions (see attr\_accessors). 
    - Other exs - "a[0]" and "a.[](0)" are same, obj.length=(3) and obj.length = 3 are same (assume length= is defined), arr[x] = y and arr.[]=(x, y) are same. With
      all these examples, it is obvious that a lot of operators are defined as methods and can be overridden in other classes. 
    - Global functions - functions in the Kernel module (eg, puts). These functions are also private to Object class, hence, are implicitly invocable in any context.
    - super - reserved word, passes arguments of current method to method with same name in superclass.

# Assignments
  * Parallel - all assignments happen in parallel and results might differ if done sequentially. Avoid these in general.
    - Same lvalues and rvalues - assume 2 arrays and assign values by index
    - One lvalue, 1+ rvalue - x = 1, 2, 3 would be x = [1, 2, 3] but x, = 1, 2, 3 would be x = 1 (assumes more lvalues and ignores them)
    - 1+ lvalues, One rvalue - if rvalue has to\_ary method, invoke it to make an ar

# Operators
  * 
