# Numeric Datatypes -
  * Integer (Fixnum with 31 bits, Bignum), Float, Complex, BigDecimal, Rational - last 3 in standard lib, not ruby.
  * Start a numeric literal with 0x/0X for hex, 0b/0B for binary and 0[0-9]+ (eg, 034) for octal. Otherwise it's decimal.
  * 1\_00\_00 is same as 10000.
  * Good stuff - all integer overflows/underflows are automatically handled (ie, Fixnum to Bignum and vice versa). Floating point has special value for infinities (overflows) it underflows to zero. 0.0/0.0 is mostly NaN. Also, integers can be queried as arrays of bits with index[0] being LSB.
  * Weird stuff - (-7/3) (ie, -2.33) equals -3, not -2 like other languages, ie, negative divisions tend towards infinity instead of zero. Gets weirder - (-7/3) is said to be evaluated as (7/-3) and not -(7/3) like other langs, so (-7%3) somehow gives 2 instead of the expected value of -1. Google gives => (a) -2 for "7%(-3)", (b) 2 for "(-7)%3", (c) -1 for both "(-7)%(-3)" and "-(7%3)"
  * remainder, a different operator, behaves similar to modulo operator of other languages. "power of" operator is Fortran's ** (right to left eval).
  * IEEE-754 - it suffers from this problem => "0.4 - 0.3 == 0.1" evaluates to false (the whole specification is faulty of course - although binary representation can approximate 0.4, 0.3 and 0.1 almost perfectly). BigDecimal works with actual decimal handling of real numbers at the hardware (how? - https://ruby-doc.org/stdlib-2.5.1/libdoc/bigdecimal/rdoc/BigDecimal.html) thus avoiding such problems, but then it's significantly slower for large computations (fine for "typical" financial computations though).

# Textual Datatypes -
  * Strings mostly - will return later.

# Arrays -
  * Accessing an index which doesn't exist doesn't throw an error, just returns nil.
  * For a size n array, attempting to insert at n+2 doesn't throw an error, just creates a nil entry at n+1. Although doing so before first index throws an error.
  * Special cases - (1) %w[this is a test] = ['this', 'is', 'a', 'test'], (2) %w| ( [ { < | = ['(', '[', '{', '<'], (3) %W(\s \t \r \n) = ["\s", "\t", "\r", "\n"]
  * Subarray access possible - arr[0,5] returns 5 elements starting from index 0.
  * + can be used to concatenate 2 arrays only. - can be used to eliminate all instances of all elements of the right side array from the left one. * can be used for replicating the elements of an array.
  * Check - compact!, delete\_if, each\_index, fill, flatten!, index, join, reverse\_each, rindex, shift, uniq!, unshift

# Hashes -
  * (a) hash["a"] = 1, (b) hash = { "a" => 1 }, (c) hash = { :a => 1 }, (d) hash = { a: 1 } - last two being most efficient forms of hashes with immutable symbol keys
  * String hash keys are a special case handled by ruby and a private copy of keys is kept for virtual immutability - note that all this burden because "apparently" a hash can become corrupt (what does that even mean) if the keys are mutated which ultimately will mutate it's hashcode. This private copy for string keys makes it less efficient.
  * Can use other mutable objects as keys as well but then need to handle the mutability thing manually.
  * As stated somewhere else to, overriding eql? method in a class makes it mandatory to override the hash method too.

# Ranges -
  * two dots if need to include the right hand object, three dots if need to exclude it.
  * Ordering - comparison operator <=>, used to evaluate ordering among elements of a class, eg, Integer/String, must be defined for the class whose objects are used to define a range (ie, the endpoints).
  * Iteration - if the class whose objects are used to define a range have a 'succ' method, then a range can be iterated, ie, there's an ordering where the next element can be found via the succ method. Eg, 'a'..'d'.to\_a will give ['a', 'b', 'c', 'd']. similarly each, step and Enumerable (to\_a) methods. Float doesn't have a succ method (hence, can't be iterated, it's gives continuous ranges obviously).
  * Membership Tests - as obvious, testing membership via succ method is going to be slow, compared to <=> (ie, comparisons). After 1.8, cover? method tests membership via the comparison operator always, while include? and member? do this via comparison operator for Floats, but via succ method for other discrete classes (string/int) which is slow and can give different results than 1.8 and earlier (where these two always used comparison).

# Symbols -
  * Symbol table used by Ruby interpreter to hold classes, methods, vars, etc using symbols. These are also usable in programs.
  * Can be thought of as immutable strings (as string methods defined for these).
  * Symbol tables holding symbols are fast for comparison because their address is known (ie, one symbol has a fixed address) - strings can be created as a different object everytime we mention it (even if it's the same string, can be a diff object), thus making comparison slower (need to understand more).

# Booleans -
  * No booleans - TrueClass, FalseClass and NilClass for true, false, and nil. also, true != 1, and false != 0 as they're separate objects themselves of those classes.

# Objects -
  * A very funny sentence says - method arguments are passed by value rather than reference - in C passing by reference would mean using * or &, but here even though a reference is being passed, it's actually a value (appropriate to call it value? why not variable or literal) which happens to be an object reference.
  * Garbage collection obviously, for objects with no references or references from other objects with no references. Avoid global variables as caches (or use some regular deletion mechanism). Every object is uniquely identified via a Fixnum identifier (constant, unique till object exists in memory). Can be obtained via object\_id method or \_\_id\_\_ keyword in case the former is overridden. hash method implemented to return this object\_id.
  * class and type problem - respond\_to? method has a shortcoming that it doesn't check the arguments (just method name). Hence, one can override a method of one class in a different class with a different argument and use it incorrectly. There is nothing called type, and it's merely the fact that objects from 2 different class might work with same methods throughout their lifetime and hence might appear to be same - but the arguments to those methods might be different (by, say, class, ie, one takes only String arguments, other takes only Fixnums) thus creating the concept of type - ie, the set of methods an object can respond to rather than just the class of the object.
  * equal? method - compares whether 2 operands refer to the same object. same as comparing object\_id for both operands (operands are literals refering to objects).
  * == method - same as equal? method in Object. Other classes override (eg, String to compare same characters). numerical classes do type conversions while overriding '==' so that equality is possible to check for different classes, ie, Fixnum/Float. String/Array/Hash might do a class (or type?) comparison first, by calling some method (eg, to\_str) on the right hand operand (to convert it to string? - bit unclear - can we have '1' == 1 or 1 == '1' return true? not on my irb), and then using its '==' operator to compare with left operand. != doesn't have to be a separate method, basically invert the result of '==' method.
  * eql? method - same as equal?, but generally can be overridden to emulate a '==' without the conversions (eg, Fixnum to Float etc).
  * === method - same as '==' method unless overridden (eg, Range, Regexp (checks if a string satisfies regex), Class, Symbol (matches with string too)).
  * =~ method - only for String/Regexp pattern matching.
  * Order - already discussed with Ranges, <=> method should return -1, 0, 1, nil only. If defined, elements are ordered (eg, Numeric, String). Comparable is a mixin that has <, <=, =, >= and > methods (among others like between?) and is included with classes defining <=>. With all this flexibility, it is possible to have a class where <=> and == can return different results for equality comparison, although not recommended.

# More On Objects -
  * Explicity conversion - to\_s, to\_i, etc - in fancy words, "methods which return a representation of an object as a value of another class"
  * Boolean type conversions - anything except false/nil behaves like true (although true is a different object). no way to convert string to boolean. 0.0/0 also behaves like true.
