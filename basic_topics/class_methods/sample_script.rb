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
    p args[:driver] + ", " + args[:route]
  end

  def create_method
  end

  # remember, using &
  def method_missing method_name, *args, &block
  end
end

class MailTruck
  def print_route
    print_driver
    just_route
  end
end

module MailModule
end

obj = MailTruck.new("Modi", "Partial Hell to Hell")
obj.print_route
obj.fancy_function(driver: "God", route: "Hell to Heaven")
obj::fancy_function(route: "Hell to Heaven to Hell", driver: "Demon")
