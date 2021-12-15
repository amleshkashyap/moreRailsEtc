### Basic Topics

#### Trivia
  * From C - expression syntax, control flow statements, basic datatypes, parameter passing, pointers, optimized machine code, efficient OS communication?
  * Others - packages, module interfaces and implementation, imports, declarations, method declaration syntax
  * Communicating Sequential Processes - parallel processes with no shared states, communicating via channels
    - Squeak/Newsqueak - functional language, garbage collection, for managing keyboard and mouse events
    - Alef - no garbage collection
  * defer is new.
  * Features for simplifying -
    - No implicit numeric conversion (see Ruby's coerce() method).
    - None of these - constructor/destructor, operator overloading, default param values, inheritance, generics, exceptions, macros, thread local storage, annotations
    - Data types and libary DS barely hide any - memory allocation, memory writes - see the Ruby feature where a variable declared and initialized based on a
      condition but used elsewhere too doesn't throw a runtime error when that condition for declaring and initializing isn't met (as it's auto-initialized as nil).
    - Multithreading driven by CSP - threads don't share memory and have lower overheads for even one thread - writing using channels is harder though??
    - Many packages whose usage isn't very difficult, and require minimal configuration to begin with.
  * Notes: often leads to extra lines of code (which take more time to read and debug), interface{} usage will not reduce simple errors.
    - [Useful read](https://medium.com/geekculture/golang-the-good-the-bad-and-the-ugly-880270a85848)
    - [Criticism of Go](https://raevskymichail.medium.com/why-golang-bad-for-smart-programmers-4535fce4210c)
    - "The realization came over me with full force that a good part of the remainder of my life was going to be spent in finding errors in my own programs." - MW
    - "Testing shows the presence, not the absence of bugs." - ED
    - "It is often a mistake to make a priori judgments about what parts of a program are really critical, since the universal experience of programmers who have been
       using measurement tools has been that their intuitive guesses fail." - DK

#### Basic
  * What we import are also packages, like the ones we create.
  * Strict - package name -> imports -> others (func/var/const/type)
  * Semicolons used in a line work like ruby. Also, incorrectly placed newlines lead to compilation errors.
  * gofmt eliminates the "code formatting standard" problem by fixing a bunch of rules and rewriting the files.
    - check goimports
    - check autoformat at file save
  * Slices - dynamic sized sequence of array elements - sl[a:b] always has elements including sl[a] but excluding sl[b]


#### Program Structure

##### Basics
  * Uncommon keywords - chan, defer, fallthrough, select
  * Uncommon constants, types, functions - iota, rune, error, imag, panic/recover => don't redeclare the predeclared (but unreserved) names
  * Zero values - all variables, even if not explicitly initialized, are initialized (to zero, if not explicitly initialized)
    - numbers - 0, bool - false, string - ""
    - references (pointers/slices/maps/channels/functions/interfaces) - nil
    - composites (structs, arrays) - zero values of individual elements
    - meaningful zero values for complicated types - how to ensure?
    - so a variable is - a fixed size piece of storage with a value?
    - var is used for variables with explicitly stated types, and zero values are figured out - in a := b kind of declaration + initialization, both would be done.
  * Short declaration (ie, ":=") -
    - It works as an assignment if the variable is already declared, else it's a declaration + assignment (initialization) - first part sounds like ease of coding.
    - The first part of above works only with multiple variables where at least one has to be a new variable, else compilation error - ie, not for ease of coding.
  * The only purpose served by multiple variable initialization in one line, is less lines of code (and in rare cases, grouping the variables meaningfully) - different
    languages will have different rules for such initializations, making it something not worth memorizing.
  * Pointers -
    - Differences from C -
      a. Garbage collection
      b. No pointer arithmetic
      c. It's safe in Go for a function to return the address of a local variable (is it at the cost of extra memory and larger binary?)
    - Similar to C -
      a. **Everything Else**
      b. Comparison of a pointer with nil - if a pointer points to a variable, then it can't be nil even if that variable's value is nil.
         ``` C
           #include <stdio.h>

           int main() {
               int *p;
               int c = NULL;
               p = &c;
               if (p == NULL) {
                   printf("NULL Hello");
               } else {
                   printf("Hello");
               }
               return 0;
           }
        ```

        ``` Go
          package main
          import "fmt"

          func main() {
              var p *int
              var c int
              p = &c
              if p == nil {
                  fmt.Printf("NULL Hello")
              } else {
                  fmt.Printf("Hello")
              }
          }
        ```
    - address-of operator (&) can be applied only to "addressable values" - not all values are addressable (but all variables are), eg, 4 in "x == 4".
    - A slightly irrelevant discussion on "a variable is a piece of storage with a value" (even C has this) - when the compiler parses the program, it must be able
      to create a somewhat static memory address for the variables which will go into the binary - the binary does the actual memory allocation for the variables
      and it probably does it based on this static memory address (which might be possible due to it being a separate process). Whenever a pointer to that variable
      is created, we're allocating further memory, despite the fact that the address already exists in the binary (in a static form probably) - rendering pointers
      effectively useless - although the book says that doing "&x" for a variable "var x int" returns a "int *" - this would mean the binary is actually going to
      create another pointer even if we don't before using it - maybe because there's no way to make use of that static address stored in the binary. Should study more!
    - See flag package.
  * new() -
    - p := new(int) -> it is a convenience method, allowing one to skip creating a local int variable and then the pointer references it, and updates its value going
      forward rather than doing it via that local variable - it's so pointless that the book has an example on how to redefine it (it's a predeclared function).
    - Using new() on size 0 variables may return the same address everytime, but not otherwise, eg, doing new(int) gives different addresses, but new([0]int) may not.
  * Lifetime of variables - as the functions returning pointers have suggested, this is not a simple concept and has many rules -
    - Package level variables and local variables of active functions
    - References to the variable - eg, via pointers - that lead to the variable
    - If there's no path to the variable by any means - then it'll be picked up by the garbage collector.
    - The traditional stack and heap from C aren't programmer controlled in Go - local variables can still go via heaps irrespective of the way it's declared and the
      variables declared via new can still go on stack (anyways the definition of new() is sufficient to know this).
    - However, it'd still be better to follow C, eg, don't use functions which return a pointer, if memory and performance are extremely crucial.
  * Assignment

##### Other Topics
  * Types - "type name underlying-type" => creates a new datatype which is of type "underlying-type". Preferably done at package level.
    - Prevent invalid or unintentional use of underlying types - one of the implications is, even if two variables are of same "underlying-type", we don't want anyone
      to compare them, eg, temperatures in celcius and farenheit shan't be compared. In a language like Ruby, the end-of-line method coerce() will still make it
      happen if we have separate classes for these (and is there even a way to avoid it)?
    - Comparisons - A var of named type can be directly compared with another of "underlying-type".
  * Type Conversions -
    - Avoid runtime failures - it's stated that **conversions never fail at runtime**.
    - Conversions are allowed, and maybe redundant in the following scenarios (note: values don't change, only type changes) -
      a. One type to other if both have same "underlying-type"
      b. If both are unnamed pointers pointing to variables of same underlying type
    - Conversions between different underlying types is natively supported for some scenarios at a cost - float to int, string to []byte
    - A var of named type can be compared with other named type of same "underlying-type" by converting one to the other or converting one to the "underlying-type".
    - Following example from the book shows the Ruby like possibilities we can have by using types.
    ``` Go
      package main
      import "fmt"

      type Celsius float64
      func (c Celsius) String() string {
          return fmt.Sprintf("%g°C", c)
      }

      func main() {
          var c Celsius
          c = Celsius(212.0)
          fmt.Println(c.String())  // prints "100°C"
          fmt.Printf("%v\n", c)    // prints "100°C" without calling String() method
          fmt.Printf("%s\n", c)    // prints "100°C"
          fmt.Println(c)           // prints "100°C"
          fmt.Printf("%g\n", c)    // prints "100" only
          fmt.Println(float64(c))  // prints "100" only - type conversion of 
      }
    ```
  * Packages -
    - Provides - modularity, encapsulation, separate compilation, reuse
    - All files in a package can access package level names - types and constants - defined in one package as if a single file. How about imports and global variables?
    - Package documentation using doc comment. [godoc](https://go.dev/blog/godoc) - for func/var/type/constant/package etc.
    - Initialization - all files in a package are ordered (eg, sorted by go), and then compiled one by one - imported packages are initialized first, and since the
      main package will have all local packages too, it's initialized at the last.
    - Using the init() method - in every file, all the init() methods are run first in the order they're defined (a file can have any number of init() methods) - each
      of these init() methods can be used to initialize global variables of composite types or any other initialization. It's simply - func init() { // do xyz }.
  * Scope - this is different from the variable's lifetime (which is a runtime property) - scope is a compile time property.


### Object Oriented Concepts

#### Methods
  * When an extra parameter appears before the function name, it's a method.
    ``` Go
      type User struct { fname string, lname string }
      func ConcatenatedNameFunction(p1 User, p2 User) string { }    // normal function
      func (p1 User) ConcatenatedNameMethod(p2 User) string { }     // method - here p1 is the "receiver object"
      u1 := User{"John", "Doe"}
      methodVal := u1.ConcatenatedNameMethod                        // methodVal is a "method value"
      u2 := User{"Jane", "Doe"}
      methodVal(u2)                                                 // similar to doing u1.ConcatenatedNameMethod(u2)
    ```
  * Method value -
    - In Ruby, all methods of a class are bounded to any object of that class. However, one can create a method object from that method which is unbounded (it belongs
      to the UnboundedMethod class) - and that can be used to create another method object which is bound to a specific object only. "methodVal" above is that last
      object - it seems to be useful while writing generic methods, in switching across different methods based on some input.
  * Encapsulation - this works only across packages, everything is public within a package - so a package should be similar to a class ofcourse?
    - Member variables - individual members of a struct can be exported via first letter capitalization - and this provides us with public/private vars.
    - Member functions - same as above. 

#### Interfaces
  * Need use-cases and relationships between - Concepts, Templates, Interfaces, Abstract Classes, Inheritance - from C++.
  * What we need most of the time is modularity which is easily expressed via classes in OO languages.
    - In Ruby, it's difficult to distinguish between classes and types - there's no basic or complex datatypes, everything is an object of some class.
    - The next thing we've for modularity in Ruby is modules - and it's somewhat similar to how we write NodeJS, exporting methods from files (and we utilize ORM based
      models when something similar to classes/objects have to be done without using those).
    - The ruby modules and non-ORM/non-OOP based NodeJS seem similar to the simplest package based organization of programs.
  * Interfaces are for abstractions of generalized behaviours of different datatypes. The datatype (which is often a struct) contains the "member variables" and
    set of "member function declarations" are provided via interfaces - methods are the implementations of these functions.
  * Ex. fmt.Printf and fmt.Sprintf are wrappers around fmt.Fprintf
  * Interface as generic datatype - interface{} represents anything.
  * Suggestions from authors -
    - Not recommended to have interfaces if there's only going to be one implementation of it - it's an unnecessary abstraction with some performance costs.
    - If there's only one implementation possible, then exporting should suffice - at least 2 or more types with similar behaviour should exist to have interfaces.
    - One exception to the above - when the only concrete type and it's interface can't be in the same package because of dependencies - decouple.
    - NOTE: grpc autogenerated code seems to violate this recommendation.
