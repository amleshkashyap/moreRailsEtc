class ObjectPrinter
  attr_reader :current_object
  @@unchangeable = "unchangeable".freeze

  class << self
    @class_inst_var = "Does Nothing"

    def print_inside_class(arg=@class_inst_var)
      p "Class instance variable is: #{arg}"
    end
  end

  def initialize
    self.setup_object(ObjectPrinter, 0)
  end

  def is_instance_object?
    not (@is_class || @is_module || @is_binding)
  end

  def setup_object(obj, level)
    @current = obj
    @is_class = (@current.class == Class)
    @is_module = (@current.class == Module)
    @is_binding = (@current.class == Binding)
    @superclass = @is_class ? @current.superclass : nil
    @ancestors = (@is_class || @is_module) ? @current.ancestors : []
    @verbosity = level
  end

  def print_object_details
    p "Object is of class: #{@current.class}, with parent: #{@superclass ? @superclass : 'None'}"
    p "Ancestors are: #{@ancestors}, and it is_a? #{@current.class.ancestors}"
  end

  # shared between instance and class objects
  def print_class_vars
    class_vars = @current.class_variables rescue class_vars = @current.class.class_variables
    p "Class Variables: #{class_vars}"
  end

  def print_class_methods_if_instance
    return if self.is_instance_object?
    methods = self.get_singleton_methods(@current.class)
    p "Class Methods For Instance Object: #{methods}"
  end

  def print_instance_methods_unless_instance
    return if !self.is_instance_object?
    methods = self.get_instance_methods rescue methods = self.get_instance_methods(@current.class)
    p "Instance Methods For Non-Instance Object: #{methods}"
  end

  # methods in the metaclass apart from the own methods - in this ruby, class methods == singleton methods of the class object
  def print_singleton_methods(own_methods)
    methods = self.get_singleton_methods - own_methods
    p "Singleton Methods: #{methods}"
  end

  def print_instance_vars
    instance_vars = self.is_instance_object? ? @current.instance_variables : @current.singleton_class.instance_variables
    p "Instance Variables: #{instance_vars}"
  end

  def print_methods
    own_methods = self.is_instance_object? ? (self.get_instance_methods(@current.class) rescue self.get_instance_methods) : self.get_singleton_methods
    p "Own Methods: #{own_methods}"
    if @verbosity > 0
      self.print_singleton_methods(own_methods)
      self.print_class_methods_if_instance
      self.print_instance_methods_unless_instance
    end
  end

  # shared between instance and class objects
  def print_constants
    constants = @current.constants rescue constants = @current.class.constants
    p "Constants: #{constants}"
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
# obj_printer_confuse = ObjectPrinter.new
# obj_printer.describe_object(obj_printer_confuse, 1)
# obj_printer.describe_object(ObjectPrinter, 1)
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
  obj_printer.describe_object(TOPLEVEL_BINDING)
end
