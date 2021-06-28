class MailTruck
  # can directly read/write to the instance variables using attr_accessor
  attr_accessor :driver, :route, :abcd

  def initialize( driver, route )
    @driver, @route = driver, route
  end

  def print_driver
    p @driver
  end

  def print_route
    p @route
  end

  alias just_route print_route

  def fancy_function(args)
    # commenting this throws an error in lmbd2 - showing the implicit conversion of nil to String when used in #{} while printing
    # so no need to pass all hash keys at invokation for hash arguments - if nil is handled.
    [:driver, :route].each { |k| args[k] = "NIL_VALUE" if args[k].nil? }

    lmbd1 = lambda { |hrs| p "#{args[:driver]} spent #{hrs.to_s} hours today on the route: #{args[:route]} for lambda1" }
    lmbd2 = ->(hrs) { p args[:driver] + " spent " + hrs.to_s + " hours today on the route: " + args[:route] + " for lambda2" rescue p "Some Argument Is Nil" }

    return lmbd1, lmbd2
  end

#  def create_method
#  end

   # for missing methods
  def method_missing method_name, *args, &block
    p "You've called a missing method - #{method_name}"
    raise Exception.new("Non-Existing Method")
  end

  def override_one(value)
    @driver = value
    p "Parent Class Override One: #{@driver}"
  end

  def override_two=(value)
    @driver = value
    p "Parent Class Override Two: #{@driver}"
  end
end

class MailTruck
  # using an alias to extend an existing function
  def print_route
    print_driver
    just_route
  end
end

class MailTruckKid < MailTruck
  undef print_route

  def override_one(value)
    @driver = value
    p "Child Class Override One: #{@driver}"
  end

  def override_two=(value)
    @driver = value
    p "Child Class Override Two: #{@driver}"
  end

  def call_overridden_methods_one(value)
    override_one(value)     # no problems when no assignment operator
    p "Called the first method"
    self.override_one(value)
    p "Called the second method"
  end

  def call_overridden_methods_two(value)
    override_two=(value)    # this seems to be considered as an assignment
    p "Called the first method"
    override_two = value    # this is definitely considered as an assignment
    p "Called the second method"
    self.override_two=(value)
    p "Called the third method"
    self.override_two = value
  end

  def driver_n
#    "#{self.driver} name"
    MailTruck.new("random", "random")
  end

  def some_method(value)
    self.abcd = self.driver_n, value # by laws of parallel assignment, creates an array
#    p self.abcd
  end

  def some_method_access
    self.abcd(self.driver_n)
  end

  def find_method
    p method(:some_method_access)
  end
end

module MailModule
end

# see the aliasing at work
obj = MailTruck.new("Modi", "Partial Hell to Hell")
p "parent route print: "
obj.print_route
puts ""

# remove the parents properties from child
obj_kid = MailTruckKid.new("Modi's Nephew", "Partial Hell To Hell")
p "child route print: "
begin
  obj_kid.print_route
rescue Exception => ex
  p "Something went wrong: " + ex.to_s
end
puts ""

p "child just route print: "
obj_kid.just_route
puts ""
p "child driver print: "
obj_kid.print_driver
puts ""

# Define some lambdas
lambda11,lambda12 = obj.fancy_function(driver: "God", route: "Hell/Earth to Heaven")
lambda21,lambda22 = obj::fancy_function(route: "Earth to Hell", driver: "Demon")
lambda31,lambda32 = obj::fancy_function :driver => "Demon"
lambda41,lambda42 = obj.fancy_function :route => "Earth To Hell"
# call these lambdas
lambda11.call(5); lambda21.call(2); lambda31.call(4); lambda41.call(8)
puts ""
lambda12.call(5); lambda22.call(2); lambda32.call(4); lambda42.call(8)
puts ""

# 
meth_details = obj.method('fancy_function')
p meth_details
puts ""

# Encoding objects don't have these methods
p Encoding.locale_charmap
p Encoding.default_external
puts ""

# Overridden methods for non predefined methods
obj_kid.call_overridden_methods_one("Some Guy One")
puts ""
obj_kid.call_overridden_methods_two("Some Guy Two")
puts ""

p obj_kid.some_method("val")
p obj_kid.driver_n
p obj_kid.abcd
# p obj_kid.some_method_access
puts ""


# utilizing similar methods across classes - blank/present are part of Rails, not Ruby
p "Array empty, nil, length, size: #{Array.new.empty?}, #{Array.new.nil?}, #{Array.new.length}, #{Array.new.size}"
p "String empty, nil, length, size: #{String.new("").empty?}, #{String.new("").nil?}, #{String.new("").length}, #{String.new("").size}"
p "Hash empty, nil, length, size: #{Hash.new.empty?}, #{Hash.new.nil?}, #{Hash.new.length} #{Hash.new.size}"
p "Boolean nil: #{false.nil?}"
p "Numeric nil: #{Numeric.new.nil?}"
p "Regex nil: #{Regexp.new(//).nil?}"
puts ""

# what exactly is happening? checking substring?
str_v = "^abcdefgh"
p "yes" if str_v["efg"]
p "yes" if str_v["eg"]
a = 5 if str_v == 'a'
p "#{a.nil?}, #{a}, #{nil}" # a doesn't exist yet, still no error
puts ""

# Hash has an initialize_copy method defined already
hash_a = {:a => 4, :b => 5}
hash_b = hash_a.clone
hash_c = hash_a.dup
hash_d = hash_a
p "Hash a: #{hash_a}"
p "Hash b: #{hash_b}"
p "Hash c: #{hash_c}"
p "Hash d: #{hash_d}"
hash_a.delete(:a)
hash_a.delete(:b)
p "Hash a: #{hash_a}"
p "Hash b: #{hash_b}"
p "Hash c: #{hash_c}"
p "Hash d: #{hash_d}"
puts ""

# << is an in-place operator, + isn't
Const, ConstCopy = ["a", "b"], ["a", "b"]
Const1 = [ Const << 'c' ]
p "Check if adding via << to a constant: original value - #{ConstCopy}, new array #{Const1}, new value of original const #{Const}"
ConstCopy1 = Const.clone
Const2 = [ Const + ['d'] ]
p "Check if adding via + to a contant: original value - #{ConstCopy1}, new array #{Const2}, new value of original const #{Const}"
puts ""

pp = instance_eval("15 % 10")
p pp
