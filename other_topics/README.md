# Notes On "-w" While Interpretation -
  * Whitespace after a method name

# Notes On Syntactic Structure -
  * Primary expressions - basic unit of syntax which directly represent values, eg, number, string, variables, self, nil, etc
  * Expression - basic unit of syntax, built by combining primary expressions with operators, and evaluating to a value, eg, "x = x + 1"
  * Statements - another basic unit, built by combining expressions with keywords, eg, if, while statements
  * Methods, Classes, Modules - above combine to make methods, which can combine to form classes (related methods) and modules (unrelated methods)
  * Blocks and Body - basically, everything inside, say, a loop, ie, the body of the loop, can also be represented via '{ }', in which case it becomes block. Put another way, keywords serve as '{' or '}' in case of multiline Ruby code.
  * Never put a space between method name and opening paranthesis

# Notes On Encoding - Mostly Irrelevant -
  * Obviously by default Ruby uses ASCII. And supports other encodings too. In fact, define your own encoding or whatever, just map it to ASCII and tell Ruby how to read it (how to tell?)
  * Source Encoding - this means the encoding used to read a particular Ruby script by the interpreter.
    1. In 1.8, only 1 type of encoding could be supported for all Ruby scripts for a process (ASCII, or anything else) since it was done via a command line options related to "-K". Later, each of the scripts could have a different encoding, which needs to be specified at the top of the script (line 1, or line 2 in case line 1 is a shebang).
    2. Also, the specification of the encoding is flexible, ie, is only requires having a few characters (eg, #, coding, utf-8, :, =) in order to identify the encoding, so a user can specify additional characters too (eg, prefixes to 'coding') in case it helps them indicate about the encoding to their editor too (eg, vim, emacs, VS, etc). Also, either case is supported.
    3. \_\_ENCODING\_\_ is a keyword that returns an Encoding object and can be used anywhere in the program to return the current file's encoding.
    4. UTF-8 can also be identified using Byte Order Mark. See book for examples when needed.
  * Default External Encoding - this means the encoding used to read all other files (I/O) except for Ruby scripts.
    1. By default, it's picked up from the system's locale (env/bash settings). Also, there can be only 1 encoding for a single Ruby process. This is exactly what was being used in 1.8 and earlier to support an encoding other than ASCII for all the Ruby scripts.
    2. Can be specified via "-E"/"--encoding" options now. Only 1 per process though.
    3. \_\_ENCODING\_\_, which gives Encoding object, can be used to get these - Encoding.default\_external and Encoding.locale\_charmap (from the locale).

# Program Execution -
  * Start Of Execution - Interpreter first looks for BEGIN statement, if found, executes related code block, and then returns back to line-1 to continue further execution. No main method.
  * Module, Class, Method definitions - In compiled languages, these are obviously special keywords processed by compiler to do various things studied in Compiler Design. Ruby interpreters consider these as statements and executes them, so a class or method definition is executed and a new class/method comes into existence (which probably means they're organized somehow, maybe similar to things studied in Compiler Design). At the time a method is called, the actual method statements are executed.
  * Termination - (a) some statement is encountered which leads to termination, (b) reaches the end of file - most frequent cases. (c) reads a line with the token \_\_END\_\_.. Unless explicitly terminated via exit! method, the program will (a) execute code blocks related to the END statements, (b) execute code blocks registered with the at\_exit method (a shutdown hook).
