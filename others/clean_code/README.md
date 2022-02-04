#### Trivia
  * Code should be short, intuitive and shouldn't put too much pressure on the reader.
  * Clean code is about how to write code (within a package), clean architecture is about writing where to write which code (within a repo).
  * This is a subjective topic - eg, python's strftime(), 
    - Every language has it's own guidelines.
    - However, clearly bad practices are not good at all.

#### Places For Improvement
  * Names - variables, functions, classes
  * Structure and Comments - formatting, good/bad comments
  * Functions - length, parameters
  * Conditionals, Errors - deep nesting, missing error handling
  * Classes, DS - differentiating between classes and DS, huge classes almost like libraries

#### Naming
  * Variables - noun + adjective - as short with most details
    - Object - value + detail - without redundancy - ex. user (good) vs userData (redundant) vs customer (specific user, best)
    - Scalars - value + detail - without redundancy
    - Boolean - ex. isValid, loggedIn vs isLoggedIn (former is obvious and sufficient)
  * Functions - verb + adjective
    - Performs some operation - ex. getUser(), getUserByEmail()
    - Returns a boolean - ex. isValid(), emailIsValid()
    - Bad names - ex. process(), handle(), using validate() for save() operation
    - Okay names - ex. save(), storeData() - good names - saveUser(), user.save()
  * Class - noun + noun
    - Describe object without redundancy and redundant suffixes
    - Ex. DataStorage (bad), DatabaseManager (ok) vs Database (good)
    - Ex. DatabaseManager or DatabaseUtil can be an ok name for a class if it has only static methods - so in the code, it would not look unintuitive.
  * Casing - snake (is\_valid - eg, Python), camel (isValid - eg, JS), pascal (IsValid - eg, class names), kebab (is-valid - eg, HTML)
  * Exceptions -
    - 
  * Bad -
    - Using slang
    - Unclear abbreviations
    - Disinformation
    - Similar method names within a class which do different things
    - Inconsistent names - eg, using fetch, get, and retrieve in different contexts - use one

#### Functions
  * DRY
  * Input/Output Params - sending maps as inputs
  * Methods are better - 

#### Error Handling
