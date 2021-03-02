class MailTruck
  # can directly read/write to the instance variables using attr_accessor
  attr_accessor :driver, :route
  def initialize( driver, route )
    @driver, @route = driver, route
  end

  def print_driver
    p @driver
  end

  def print_route
    p @route
  end

  def create_method
  end

  # remember, using &
  def method_missing method_name, *args, &block
    
  end
end

module MailModule
end

begin
  print MailTruck.class, " ", MailTruck.superclass, " ", Class.class, " ", Class.superclass, "\n"
  print MailModule.class, " ", Module.class, " ", Module.superclass, "\n"	# , " ", MailModule.superclass
rescue Exception => ex
  print "Error Raised: ", ex.message, "\n"
end

m = MailTruck.new( "Harold", ['12 Corrigan Way', '23 Antler Ave'] )
m.instance_variable_set( "@speed", 5 )
puts m.instance_variable_get("@speed")
puts m.class
puts "    \n"
# only one instance of MailTruck has an extra instance variable
n = MailTruck.new("Jinping", ["India", "Pakistan"])
# p xyz = puts xyz.inspect
p m.instance_variables
p n.instance_variables
puts "    \n"
meths = m.methods
# p meths
m.print_driver
m.print_route
# m.print_speed
puts "   \n"
puts "Nil-0" if !m.speed(10)
puts "Nil-1" if !m.speed
# instance_eval can be used to define methods for an existing instance variable as well
m.instance_eval do
  def speed(value)
    @speed = value
  end
end
puts "    \n"
puts m.instance_variable_get("@speed")
puts m.speed(15)
puts m.instance_variable_get("@speed")

puts "    \n"
puts "Nil-2" if !m.avg_speed(20)
puts "Nil-3" if !m.avg_speed
# trying to define a new instance variable using class_eval - it obviously won't work
m.class_eval do
  def avg_speed(value)
    @avg_speed = value
  end
end
puts "    \n"
puts "Nil-4" if !m.avg_speed(25)
puts "Nil-5" if !m.instance_variable_get("@avg_speed")

puts "    \n"
p m.instance_variables
p n.instance_variables
puts "Nil-6" if !n.avg_speed(30)
puts "Nil-7" if !n.instance_variable_get("@avg_speed")

m.instance_eval do
  def avg_speed(value)
    @avg_speed = value
  end
end
puts "    \n"
puts "Nil-8" if !m.avg_speed(30)
puts "Nil-9" if !m.instance_variable_get("@avg_speed")
# use class_eval to define methods for an existing instance variable for a particular object which doesn't exist for other instances
MailTruck.class_eval do
  def avg_speed(value)
    @avg_speed = value
  end
end

puts "    \n"
puts m.avg_speed(40)
puts m.instance_variable_get("@avg_speed")
puts "    \n"
puts n.avg_speed(45)
puts n.instance_variable_get("@avg_speed")
puts "    \n"
p m.instance_variables
p n.instance_variables

# use class_eval to define methods for an non-existing instance variable
MailTruck.class_eval do
  def new_avg_speed(value)
    @new_avg_speed = value
  end
end

puts "    \n"
puts m.new_avg_speed(50)
puts m.instance_variable_get("@new_avg_speed")
puts "    \n"
puts n.new_avg_speed(55)
puts n.instance_variable_get("@new_avg_speed")
puts "    \n"
p m.instance_variables
p n.instance_variables
