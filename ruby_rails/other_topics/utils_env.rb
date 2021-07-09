class ObjectPrinter
  attr_reader :current_object
  @@unchangeable = "unchangeable".freeze

  class << self
    @class_inst_var = "Does Nothing"
    # uncomment this to act like Binding class with no new method
    # undef :new

    def print_inside_class(arg=@class_inst_var)
      p "Class instance variable is: #{arg}"
    end
  end

  def initialize
    self.setup_object(ObjectPrinter, 0)
  end

  def is_instance_object?
    # metaclass of an instance object doesn't have a superclass in concept, but in this Ruby, it's the class of the instance object - class has :new method
    @current.class.methods.include?(:new) && (@current.singleton_class.superclass == @current.class)
  end

  def setup_object(obj, level)
    @current = obj
    @is_class = (@current.class == Class)
    @is_module = (@current.class == Module)
    @is_unknown = !(self.is_instance_object? || @is_class || @is_module)
    @superclass = @current.respond_to?(:superclass) ? @current.superclass : nil
    @ancestors = @current.respond_to?(:ancestors) ? @current.ancestors : []
    @verbosity = level
  end

  def print_object_details
    p "Object Is Of Class: #{@current.class}, With Parent: #{@superclass ? @superclass : 'None'}"
    p "Ancestors Are: #{@ancestors}, And It is_a? #{@current.class.ancestors}"
  end

  # shared between instance and class objects
  def print_class_vars
    begin
      class_vars = self.is_instance_object? ? @current.class.class_variables : @current.class_variables
      p "Class Variables: #{class_vars}, For Class: #{@current.class}"
    rescue
      p "Expected Class Variables Not Found For This Object Of Class: #{@current.class}"
    end
  end

  def print_class_methods_if_instance
    return unless self.is_instance_object?
    methods = self.get_singleton_methods(@current.class)
    p "Class Methods For Instance Object: #{methods}"
  end

  def print_instance_methods_unless_instance
    return if self.is_instance_object?
    begin
      methods = self.get_instance_methods
      p "Instance Methods For Non-Instance Object: #{methods}, Of Class: #{@current.class}"
    rescue
      p "Expected Instance Methods Not Found For Non-Instance Object Of Class: #{@current.class}"
    end
  end

  # methods in the metaclass apart from the own methods - in this ruby, class methods == singleton methods of the class object
  def print_singleton_methods(own_methods)
    methods = self.get_singleton_methods - own_methods
    p "Singleton Methods: #{methods}"
  end

  # relies on the assumption that for all non-class instance objects, instance variables are present in its singleton_class
  def print_instance_vars
    begin
      instance_vars = self.is_instance_object? ? @current.instance_variables : @current.singleton_class.instance_variables
      p "Instance Variables: #{instance_vars}"
    rescue
      p "Expected Instance Variables Not Found For This Object Of Class: #{@current.class}"
    end
  end

  def print_methods
    begin
      own_methods = self.is_instance_object? ? self.get_instance_methods(@current.class) : self.get_singleton_methods
      p "Own Methods: #{own_methods}"
    rescue
      p "No Expected Own Methods For This Object Of Class: #{@current.class}"
      own_methods = []
    end
    if @verbosity > 0
      self.print_singleton_methods(own_methods)
      self.print_class_methods_if_instance
      self.print_instance_methods_unless_instance
    end
  end

  # shared between instance and class objects
  def print_constants
    begin
      constants = self.is_instance_object? ? @current.class.constants : @current.constants
      p "Constants: #{constants}"
    rescue
      p "No Expected Constants For This Object Of Class: #{@current.class}"
    end
  end

  def describe_object(obj, level=0)
    puts ""
    self.setup_object(obj, level)
    self.print_object_details
    self.print_class_vars
    self.print_instance_vars
    self.print_methods
    self.print_constants
  end

  INSTANCE_EXIT = :dup
  SINGLETON_EXIT = :new

  private

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
      if meth == exit_at
        break
      else
        methods.push(meth)
      end
    end
    methods
  end

end


obj_printer = ObjectPrinter.new
obj_printer_confuse = ObjectPrinter.new
obj_printer.describe_object(obj_printer_confuse, 1)
obj_printer.describe_object(ObjectPrinter, 1)
# exit

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
  p "Bindings are: "
  obj_printer.describe_object(TOPLEVEL_BINDING, 1)
end
