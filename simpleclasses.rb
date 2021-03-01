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
m.instance_variable_set( "@speed", 45 )
puts m.class
puts "    \n"
# p xyz = puts xyz.inspect
p m.instance_variables
puts "    \n"
# only one instance of MailTruck has an extra instance variable
p MailTruck.new("Kumar", []).instance_variables
puts "    \n"
meths = m.methods
# p meths
m.print_driver
m.print_route
m.print_speed
