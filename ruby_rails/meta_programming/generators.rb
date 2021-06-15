# what is attr_accessor => https://stackoverflow.com/a/4371143
class Module
  # emulating the attr_accessor method - note: method_name is actually the name of instance variables, for convention, keep method_name = variable_name
  def dummy_attr_accessor( method_name )
    # to_sym converts a string to a symbol, eg, "bar" becomes :bar
    inst_variable_name = "@#{method_name}".to_sym
    # define_method - method of class Module which can be used to create methods dynamically (for the receiver) - takes method name and a block as parameters
    # the parameters of the block become the parameters of the new method
    define_method method_name do
      # initialize the newly created instance variable above, ie, def bar \n  @bar \n end
      # instance_variable_get fetches a particular instance variable
      instance_variable_get inst_variable_name
    end
    define_method "#{method_name}=" do |new_value|
      # equivalent to - def bar(new_value) \n  @bar = new_value \n end
      # instance_variable_set sets the variable for a particular instance variable
      instance_variable_set inst_variable_name, new_value
    end
  end
end

# this class is a child of Module class, and its instance variable "new_var" can be get/set now
class Foo
  dummy_attr_accessor("new_var")
end

f = Foo.new
puts "Nil" if !f.new_var
f.new_var = 42
puts f.new_var
