// Source: https://www.youtube.com/watch?v=NH1Tta7purM

// Ex-1-Avoid
if (checkForErrorA())
    handleErrorA();
else if (checkForErrorB())
    handleErrorB();
else if (checkForErrorC())
    handleErrorC();
else
    doSomethingUseful();

// Ex-1-Suggested
// this helps the hardware branch predictor - compiler does some conversions but branch predictors are the last level decision makers.
// Hardware is fast at determining if an integer is zero or not.
int64_t errorFlags;
if (!errorFlags)
    doSomethingUseful();
else
    HandleError(errorFlags);

// Ex-2 - Avoid using virtual functions
// Virtual functions are widely used - declare in base class, define in derived class
// However, if all derived classes are known, then we can have if-else to handle it based on some external configuration
// Virtual functions would obviously slow down the program because the decision making for which function to execute is done at runtime
// The if-else has to be put into a factory and instantiated at the beginning of the program [chooses based on configuration].
// Use a template to make this decision - that's the factory part.
