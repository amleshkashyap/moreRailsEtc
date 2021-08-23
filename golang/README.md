### Generic Notes on Go's Features, Syntax
#### Features
  * Type inference, faster compilation (compiled and linked, not interpreted), safe (??), interfaces and type embedding
  * Statically typed but allows dynamic typing (ie, type inference), garbage collection
  * Inbuilt concurrency - go routines, channels, selects
  * Not Present - classes and type inheritance, method/operator overloading, circular dependencies among packages, pointers, assertions, generic programming
  * Use packages for grouping - everything inside a type of package is available in every other files inside that package (ie, declaring package xyz).
  * Goroutines - lightweight thread, all goroutines are in same address space so need synchronization
  * Channels - like unix domain sockets, pipes if you will.
    - ch <- v     // send v to channel ch
    - v := <-ch   // receive from channel ch, assign to v
    - ch := make(chan int)    // create a channel which can receive integers - can't use one without creating
    - ch := make(chan int, 3)    // buffered channel, sending more elements than the buffer size?
    

#### Syntax
  * Declare packages, import packages
  * New keywords - chan, defer, fallthrough, select, Go, Goto
    - select - waits on multiple communication ops (blocks until one case can run), then runs one case when available - chosen at random when multiple
    - chan - for creating channels

  * Datatypes
    - Boolean (nil - all bytes are zero)
    - Numeric - integer (8-64 bits, signed unsigned), float (32, 64 bits)
    - String - immutable
    - Derived - Pointers, Arrays, Structures, Unions, Functions, Slices, Interfaces, Maps, Channels 
    - lvalues, rvalues - similar to Ruby - looks like a combination of Ruby and C

  * Functions, Operators, Expressions, Iteration - 
    - why give a goto
    - = is for assignment only, := is for declaration + assignment, ie, x := 10 => var x int = 10
    - Functions - func fn1 (x, int y) (string l, int m) { } => return vars/types can be specified too
      1. Function as values from JS - someFn := func (x) y { }
      2. Function as closures - similar to Ruby/JS - get the closure as a value and call the value as a function - invokation is like Ruby lambda.
      3. Function as methods - something like OOP. define a type, then create functions whose parameters are these types - and access the fields of those types.
         - Even in Ruby, classes are implemented somewhat like this and APIs are exposed for programming - using this form would be raw and hence fast.

  * Others
    - Array
      1. var arr [size] datatype // create an array of type "datatype" of size "size"
      2. mostly works like C with malloc's removed.
    - Pointers
      1. var ptr *datatype    // create a pointer of type "datatype"
      2. x := 10; ptr = &x    // ptr points to the address of x - mostly C here
    - Error handling - not a straightforward thing as other languages
      1. defer - creates functions that are called in reverse order of their declaration, at the end (end can be a successful return, or due to an error)
      2. panic - basically any error that stops normal execution. doesn't effect defer though.
      3. recover - captures and returns the value captured from a panic call. it makes sense to call it only in a defer function otherwise program will return when
         a panic is raised. if no panic, returns nil of course - so can still use it in defer functions - just don't do anything.
      4. defer and recover can act like a try/catch block for capturing the panics.
    - Structs - like C structs
      1. type <classname aka struct_variable_type> struct { member definition, ... }
    - Hash/Map
      1. var someMap map[datatype_of_keys]datatype_of_values  // declares a map, which has nil value
      2. someMap = make(map[datatype_of_keys]datatype_of_values)    // defines a map, always do for now
      3. use inbuilt delete function for deleting keys
    - Slice, Range
    - Maps, Pointers, Slices - passed by reference to a function so no need to use pointers.
    - Interface - set of 3 steps - define an interface, define a struct, implement interface methods for those structs
      1. type interface_name interface { concat() string; combined_length() int }    // defines interface with 2 functions that can be implemented
      2. type ThreeStrings struct { str1, str2, str3 string }    // defines struct with 3 string members
      3. func (struct_var ThreeStrings) concat() string { return (struct_var.str1 + struct_var.str2 + struct_var.str3) }    // implement concat() method

#### Sources
  * [How To Pass Generic Types In Go](https://medium.com/@motemen/achieving-type-generic-functions-in-go-without-using-reflections-40bc06111970)
  * [Tutorials Point](https://www.tutorialspoint.com/go/go_pointers.htm)
  * [Find Variable Types](https://www.geeksforgeeks.org/different-ways-to-find-the-type-of-variable-in-golang/)
  * [Concurrency In Golang](https://tour.golang.org/concurrency/1)
