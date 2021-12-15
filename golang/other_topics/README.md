### Testing

#### Unit Tests
  * Two effective methods for managing the growing complexity of programs - (a) routine peer review, (b) testing
  * The corner cases thought while programming are the ones that should be included in tests - missed corner cases is why peer review is required.
  * gotest -
    - Files within a package ending with \_test.go
    - Test, Benchmark and Examples - reported after execution by gotest
  * Testing - ex. func TestFunc(t \*testing.T) {} - name convention is mandatory, "t" holds results of test accessible via methods.
    - Write tests for reported bugs to verify it is the problem before fixing.
    - One testing strategy is to write the simplest and less efficient but correct implementation for a function and match the output with the actual implementation.
  * Randomized Testing -
    - If inputs have a pattern, generate random ones to test the functions.
    - 
  * Effective Testing Tips By Authors -
    - Define functions to avoid repetition.
    - It should have a good user interface - ie, the test messages and error messages should be clear.
    - Shouldn't explode on failure, and print clear description of the problem leading to the failure (of the test).
    - Maintaining the tests need not involve reading the source code when debugging the failure.
    - A test should not stop after a single failure and try to report several errors in a single run - how?? that's like compilation!!
    - Start with implementing the tests for concrete behaviours required, followed by functions and abstractions - avoid a library of abstract, generic tests.
  * Brittle Tests -
    - A program which fails when a new but valid input is passed is buggy. A test which fails unexpectedly when a change was made to its program is brittle.
    - Tests which check large output values which are prone to modification may be brittle - one way to avoid is to only check the relevant properties.
  * Profiling -
    - Basic: 3% of code needs optimization to generate real benefits.
