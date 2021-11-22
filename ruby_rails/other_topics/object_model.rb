$verbose_level = 0
# assumes every object will have :class and :methods defined for sure
class ObjectPrinter
  attr_reader :current_object
  @@unchangeable = "unchangeable".freeze

  class << self
    @class_inst_var = "Does Nothing"
    # uncomment this to act like Binding class with no new method
    # undef :new

    def print_inside_class(arg=@class_inst_var)
      p "  Class instance variable is: #{arg}"
    end
  end

  def initialize
    self.setup_object(ObjectPrinter, 0)
  end

  def is_instance_object?
    # if it can not be created using :new method, then it's not an instance_object
    (not @is_class) && (not @is_module) && @current.class.methods.include?(:new)
  end

  def is_really_allocated?
    @is_allocated && @current.class.methods.include?(:allocate)
  end

  # 4.respond_to?(:singleton_class) returns true, but 4.singleton_class throws an error
  def has_metaclass?
    begin
      @current.singleton_class
      return true
    rescue
      return false
    end
  end

  def has_superclass?
    begin
      @current.superclass
      return true
    rescue
      return false
    end
  end

  def has_ancestors?
    begin
      @current.ancestors
      return true
    rescue
      return false
    end
  end

  def setup_object(obj, level)
    @current = obj
    @is_class = (@current.class == Class)
    @is_module = (@current.class == Module)
    @is_allocated = !(self.is_instance_object? || @is_class || @is_module)
    @superclass = self.has_superclass? ? @current.superclass : nil
    @metaclass = self.has_metaclass? ? @current.singleton_class : nil
    @ancestors = self.has_ancestors? ? @current.ancestors : []
    @verbosity = level
  end

  def print_object_details
    p "Object Is Of Class: #{@current.class}, With Parent: #{@superclass ? @superclass : 'None'}"
    p "  Ancestors Are: #{@ancestors}, And It is_a? #{@current.class.ancestors}"
    p "  Type of object: Class #{@is_class}, Module: #{@is_module}, Instance Obj: #{self.is_instance_object?}, Allocated: #{@is_allocated}, Purely Memory, No Metaclass: #{!self.has_metaclass?}, Is Really Via :allocate: #{self.is_really_allocated?}"
  end

  # shared between instance and class objects
  def print_class_vars
    if (@is_class || @is_module)
      begin
        class_vars = @current.class_variables
        p "  Class Variables: #{class_vars}, For Class: #{@current.class}"
      rescue
        p "  class_variables Not Defined For This Class Object Of Class: #{@current.class}"
      end
    else
      begin
        class_vars = @current.class.class_variables
        p "  Class Variables: #{class_vars}, For Class: #{@current.class}"
      rescue
        p "  class_variables Not Defined For The Class Of This Object Of Class: #{@current.class}, Allocated: #{@is_allocated}"
      end
    end
  end

  def print_class_methods_if_instance_or_allocated
    return unless (self.is_instance_object? || @is_allocated)
    begin
      methods = self.get_singleton_methods(@current.class)
      p "  Class Methods For Instance Object: #{methods}"
    rescue
      p "  singleton_methods Not Defined For Class Of This Instance Object Of Class: #{@current.class}, Allocated: #{@is_allocated}"
    end
  end

  def print_instance_methods_unless_instance
    return if (self.is_instance_object? || @is_allocated)
    begin
      methods = self.get_instance_methods
      p "  Instance Methods For Non-Instance Object: #{methods}, Of Class: #{@current.class}"
    rescue
      p "  instance_methods Not Defined For Non-Instance Object Of Class: #{@current.class}"
    end
  end

  # methods in the metaclass apart from the own methods - in this ruby, class methods == singleton methods of the class object
  def print_singleton_methods(own_methods)
    begin
      methods = self.get_singleton_methods - own_methods
      p "  Singleton Methods: #{methods}"
    rescue
      p "  singleton_methods Not Defined For This Object Of Class: #{@current.class}, Allocated: #{@is_allocated}"
      methods = []
    end
    return methods
  end

  # relies on the assumption that for all non-class instance objects, instance variables are present in its metaclass
  def print_instance_vars
    if (@is_class || @is_module)
      begin
        if @metaclass
          instance_vars = @metaclass.instance_variables
          p "  Instance Variables: #{instance_vars}"
        else
          p "  No Instance Variables Because No Metaclass For Non-Instance Object With Class: #{@current.class}"
        end
      rescue
        p "  instance_variables Not Defined For Singleton Class Of This Non-Instance Object Of Class: #{@current.class}"
      end
    else
      begin
        instance_vars = @current.instance_variables
        p "  Instance Variables: #{instance_vars}"
      rescue
        p "  instance_variables Not Defined For This Instance Object Of Class: #{@current.class}, Allocated: #{@is_allocated}"
      end
    end
  end

  def print_own_methods
    if (@is_class || @is_module)
      begin
        # any methods defined manually while writing the definition in the code rather than created at runtime (but includes runtime for class/module)
        own_methods = self.get_singleton_methods
        p "  Own Methods: #{own_methods}"
      rescue
        p "  singleton_methods Not Defined For This Non-Instance Object Of Class: #{@current.class}, Methods: #{self.get_all_methods}"
        own_methods = []
      end
    else
      begin
        # any methods defined manually while writing the definition in the code rather than created at runtime (but includes runtime for class/module)
        own_methods = self.get_instance_methods(@current.class)
        p "  Own Methods: #{own_methods}"
      rescue
        p "  instance_methods Not Defined For Class Of This Non-Instance Object Of Class: #{@current.class}, Allocated: #{@is_allocated}, Methods: #{self.get_all_methods}"
        own_methods = []
      end
    end
    if @verbosity > 0
      # any singleton methods apart from the own methods, defined manually
      singleton_methods = self.print_singleton_methods(own_methods)
      # for any instance kind of objects, its class methods defined manually
      self.print_class_methods_if_instance_or_allocated
      # for any class/module, its instance methods defined manually
      self.print_instance_methods_unless_instance
      if @verbosity > 1
        # any inherited methods of the object
        self.print_inherited_methods(own_methods, singleton_methods)
      end
    end
  end

  def print_inherited_methods(own_methods, singleton_methods)
    inherited_methods = @current.methods - own_methods - singleton_methods
    p "    Inherited Methods: #{inherited_methods}"
  end

  # shared between instance and class objects
  def print_constants
    if (@is_class || @is_module)
      begin
        constants = @current.constants
        p "  Constants Are: #{constants}"
      rescue
        p "  constants Not Defined For This Non-Instance Object Of Class: #{@current.class}"
      end
    else
      begin
        constants = @current.class.constants
        p "  Constants Are: #{constants}"
      rescue
        p "  constants Not Defined For Class Of This Instance Object Of Class: #{@current.class}, Allocated: #{@is_allocated}"
      end
    end
  end

  def describe_object(obj, level=$verbose_level)
    puts ""
    self.setup_object(obj, level)
    self.print_object_details
    self.print_class_vars
    self.print_instance_vars
    # methods defined manually for the object - by its class, or metaclass
    self.print_own_methods
    self.print_constants
    puts ""
  end

  INSTANCE_EXIT = :dup
  SINGLETON_EXIT = [:new, :allocate]
  ALL_EXIT = [:dup, :new, :allocate]

  private

  def get_all_methods(object=@current, exit_at=ALL_EXIT)
    methods = []
    object.methods.each do |meth|
      if exit_at.include?(meth)
        break
      else
        methods.push(meth)
      end
    end
    methods
  end

  def get_instance_methods(object=@current, exit_at=INSTANCE_EXIT)
    methods = []
    object.instance_methods.each do |meth|
      if meth == exit_at
        break
      else
        methods.push(meth)
      end
    end
    methods
  end

  def get_singleton_methods(object=@current, exit_at=SINGLETON_EXIT)
    methods = []
    object.singleton_methods.each do |meth|
      if exit_at.include?(meth)
        break
      else
        methods.push(meth)
      end
    end
    methods
  end

end


obj_printer = ObjectPrinter.new

# convert a symbol to a string, and then string to a constant - prints the Modules loaded
p Module.constants.sort.select { |x| eval(x.to_s).instance_of?(Module) }
puts ""

p Module.constants.sort.select { |x| c = eval(x.to_s); c.is_a?(Class) && (not c.ancestors.include?(Exception)) }
puts ""

# print Exception constants
p Module.constants.sort.select { |x| c = eval(x.to_s); c.is_a?(Class) && c.ancestors.include?(Exception) }
puts ""


begin
  p RandomConstantForError
rescue
  p "Error thrown, message: #{$!.message}, backtrace: #{$!.backtrace}"; puts ""
  p "In Process: #{$$}, arguments: #{ARGV}, last successful process: #{$?}, #{RUBY_VERSION}"; puts "";
end

def some_global_function
end

# now check some objects
# Global Constants
obj_printer.describe_object(ARGV)    # instance of Array
obj_printer.describe_object(RUBY_VERSION)    # instance of String
obj_printer.describe_object($$)    # Process ID - class Integer, allocated
obj_printer.describe_object($!)    # Global Exception object - it's a nilclass, allocated
obj_printer.describe_object($*)    # Global Exception bakctrace - instance of Array
obj_printer.describe_object(TOPLEVEL_BINDING)    # allocated Binding object
# Literals
obj_printer.describe_object(nil)    # allocated NilClass object
obj_printer.describe_object("string")    # instance of String
obj_printer.describe_object(0)    # allocated Integer object
obj_printer.describe_object(true)    # allocated TrueClass object
# Class Objects
obj_printer.describe_object(NilClass)
obj_printer.describe_object(File)
obj_printer.describe_object(ObjectPrinter)
obj_printer.describe_object(BasicObject)
obj_printer.describe_object(Object)
obj_printer.describe_object(Module)
obj_printer.describe_object(Class)
obj_printer.describe_object(Struct)
obj_printer.describe_object(Method)
obj_printer.describe_object(Symbol)
# Module Objects
obj_printer.describe_object(Kernel)
obj_printer.describe_object(Module.new)
# Lambdas
obj_printer.describe_object(lambda {|x| p x})
# Method Objects
obj_printer.describe_object(Kernel.method(:some_global_function))    # allocated Method object
obj_printer.describe_object(obj_printer.method(:print_constants))    # allocated Method object
obj_printer.describe_object(some_global_function)    # an undefined local variable is treated as nil - because it's evaluated as an expression returning nil
obj_printer.describe_object(:some_global_function)   # an uninitialized symbol
# Literals
obj_printer.describe_object(nil)    # allocated NilClass object
obj_printer.describe_object("string")    # instance of String
obj_printer.describe_object(5)    # allocated Integer object
obj_printer.describe_object(true)    # allocated TrueClass object
# Instance Objects
obj_printer_confuse = ObjectPrinter.new
obj_printer.describe_object(obj_printer_confuse)
