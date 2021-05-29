# Numeric Datatypes -
  * Integer (Fixnum with 31 bits, Bignum), Float, Complex, BigDecimal, Rational - last 3 in standard lib, not ruby.
  * Start a numeric literal with 0x/0X for hex, 0b/0B for binary and 0[0-9]+ (eg, 034) for octal. Otherwise it's decimal.
  * 1\_00\_00 is same as 10000.
  * Good stuff - all integer overflows/underflows are automatically handled (ie, Fixnum to Bignum and vice versa). Floating point has special value for infinities (overflows) it underflows to zero. 0.0/0.0 is mostly NaN. Also, integers can be queried as arrays (like string to chars) with index[0] being LSB.
  * Weird stuff - (-7/3) (ie, -2.33) equals -3, not -2 like other languages, ie, negative divisions tend towards infinity instead of zero. Gets weirder - (-7/3) is said to be evaluated as (7/-3) and not -(7/3) like other langs, so (-7%3) somehow gives 2 instead of the expected value of -1. Google gives => (a) -2 for "7%(-3)", (b) 2 for "(-7)%3", (c) -1 for both "(-7)%(-3)" and "-(7%3)"
  * remainder, a different operator, behaves similar to modulo operator of other languages. "power of" operator is Fortran's ** (right to left eval).
  * IEEE-754 - it suffers from this problem => "0.4 - 0.3 == 0.1" evaluates to false (the whole specification is faulty of course - although binary representation can approximate 0.4, 0.3 and 0.1 almost perfectly). BigDecimal works with actual decimal handling of real numbers at the hardware (how? - https://ruby-doc.org/stdlib-2.5.1/libdoc/bigdecimal/rdoc/BigDecimal.html) thus avoiding such problems, but then it's significantly slower for large computations (fine for "typical" financial computations though).

# Textual Datatypes -
  * 
