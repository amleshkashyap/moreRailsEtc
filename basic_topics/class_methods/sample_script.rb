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

  alias just_route print_route

  def fancy_function(args)
    # commenting this throws an error in lmbd2 - showing the implicit conversion of nil to String when used in #{} while printing
    [:driver, :route].each { |k| args[k] = "NIL_VALUE" if args[k].nil? }

    lmbd1 = lambda { |hrs| p "#{args[:driver]} spent #{hrs.to_s} hours today on the route: #{args[:route]} for lambda1" }
    lmbd2 = ->(hrs) { p args[:driver] + " spent " + hrs.to_s + " hours today on the route: " + args[:route] + " for lambda2" rescue p "Some Argument Is Nil" }

    return lmbd1, lmbd2
  end

  def create_method
  end

  # remember, using &
  def method_missing method_name, *args, &block
  end
end

class MailTruck
  # using an alias to extend an existing function
  def print_route
    print_driver
    just_route
  end
end

module MailModule
end

obj = MailTruck.new("Modi", "Partial Hell to Hell")
obj.print_route
lambda11, lambda12 = obj.fancy_function(driver: "God", route: "Hell/Earth to Heaven")
lambda21, lambda22 = obj::fancy_function(route: "Earth to Hell", driver: "Demon")
lambda31, lambda32 = obj::fancy_function :driver => "Demon"
lambda41, lambda42 = obj.fancy_function :route => "Earth To Hell"
lambda11.call(5)
lambda12.call(5)
lambda21.call(2)
lambda22.call(2)
lambda31.call(4)
lambda32.call(4)
