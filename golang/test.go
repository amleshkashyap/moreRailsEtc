package main

import ("fmt"; "reflect")    // for some reflection methods

// an interface which is implemented by an instance
type AssignAndPrint interface {
  addAttributes(interface {}) error
  printAttributes() error
}

// takes any pointer of basic datatypes, prints their values/addresses and above method names as if a class
type TestPointers struct {
  pointer_type string
  pointer_value string
  pointer_dereferenced_value string
  pointer_address string
  pointer_methods []string
  pointer_exists map[string]string
}


// implement the interface for above structure only
func (some_pointer TestPointers) addAttributes(actual_pointer interface{}) error {
  defer func() {
    if r := recover(); r != nil {
      err := r.(error)
      fmt.Println("An error has been caught while assigning values to TestPointer object: ", err, "\n")
    }
  }()

  var new_pointer interface{}
  is_basic_type := "true"

  switch actual_pointer.(type) {
    case *string:
      new_pointer = actual_pointer.(*string)    // typecasting interface
    case *int:
      new_pointer = actual_pointer.(*int)
    case *[]string:
      new_pointer = actual_pointer.(*[]string)
      is_basic_type = "false"
    case *bool:
      new_pointer = actual_pointer.(*bool)
    default:
      panic("some unexpected type")
  }

  some_pointer.pointer_type = fmt.Sprintf("%T", new_pointer)
  some_pointer.pointer_dereferenced_value = fmt.Sprintf("%S", reflect.ValueOf(new_pointer).Elem())
  some_pointer.pointer_value = fmt.Sprintf("%p", new_pointer)
  some_pointer.pointer_address = fmt.Sprintf("%p", &new_pointer)
  some_pointer.pointer_methods = append([]string{}, "addAttributes", "printAttributes")
  some_pointer.pointer_exists["is_basic_type"] = is_basic_type
  some_pointer.printAttributes()
  return nil
}

// implement other methods of the interface
func(some_pointer TestPointers) printAttributes() error {
  defer func() {
    if r := recover(); r != nil {
      err := r.(error)
      fmt.Println("An error has been caught while assigning values to TestPointer object: ", err, "\n")
    }
  }()

  fmt.Println("Type is: ", some_pointer.pointer_type)
  fmt.Println("Value is: ", some_pointer.pointer_value)
  fmt.Println("Dereferenced Value is: ", some_pointer.pointer_dereferenced_value)
  fmt.Println("Address is: ", some_pointer.pointer_address)
  fmt.Println("Methods are: ", some_pointer.pointer_methods)
  fmt.Println("Methods Exist: ", some_pointer.pointer_exists, "\n")
  return nil
}

// call the relevant methods of the interface
func callAddAttributes(some_value AssignAndPrint, some_ptr interface{}) error {
  return some_value.addAttributes(some_ptr)
}

func callPrintAttributes(some_value AssignAndPrint) error {
  return some_value.printAttributes()
}

// function closures
func usedInCode (somearg int) func() int {
  var x int = 5
  return func() int {
    return (x * somearg)
  }
}

// error handling
func printPointers (ptr *int) (err error) {
  fmt.Println("Printing the address pointed by the pointer, value stored via deferencing pointer, address of the pointer")
  defer func() {
    if r := recover(); r != nil {
      err = r.(error)
      fmt.Println("An error has been caught while executing printPointers: ", err, "\n")
    }
  }()
  fmt.Println(ptr)
  fmt.Println(*ptr)
  fmt.Println(&ptr)
  fmt.Println("")
  return
}

func main() {
  // function closures defined - ie, lambdas
  usedInCode1 := usedInCode(7)
  usedInCode2 := usedInCode(8)
  usedInCode3 := usedInCode(9)
  fmt.Println(usedInCode1())
  fmt.Println(usedInCode2())
  fmt.Println(usedInCode3())

  x := 20
  var ptr *int

  printPointers(ptr)

  ptr = &x

  printPointers(ptr)

  // initialize a new pointer which is pointing to nothing
  interface_ptr := TestPointers{pointer_type:"nil", pointer_value:"nil", pointer_dereferenced_value:"nil", pointer_address:"nil", pointer_methods:[]string{},
             pointer_exists:make(map[string]string)}
  callAddAttributes(interface_ptr, ptr)

  s := "hello"
  b := true
  var ar = []string {"alpha", "beta", "gamma"}

  var s_ptr *string
  var b_ptr *bool
  var ar_ptr *[]string

  s_ptr = &s
  callAddAttributes(interface_ptr, s_ptr)
  b_ptr = &b
  callAddAttributes(interface_ptr, b_ptr)
  ar_ptr = &ar
  callAddAttributes(interface_ptr, ar_ptr)
  // since we're not passing references anywhere - can we pass references above?
  callPrintAttributes(interface_ptr)
}
