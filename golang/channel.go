// code is taken verbatim from this SO answer - https://stackoverflow.com/a/39831976
package main

import ("fmt"; "time")

func main() {
  messages := make(chan int)
  go func() {
    time.Sleep(time.Second * 3)
    messages <- 1
  }()
  go func() {
    time.Sleep(time.Second * 2)
    messages <- 2
  }()
  go func() {
    time.Sleep(time.Second * 1)
    messages <- 3
  }()
  go func() {
    for i := range messages {
      fmt.Println(i)
    }
  }()
  go func() {
    time.Sleep(time.Second * 1)
    messages <- 4
  }()
  go func() {
    time.Sleep(time.Second * 1)
    messages <- 5
  }()
  time.Sleep(time.Second * 5)
}

