require 'singleton'
require 'fileutils'

#################################################
class Option
  # this class has a 'Prototype' based and normal 'Factory' for object creation, stuffed as a nested class
  attr_accessor :name, :numargs, :flag, :alias_
  attr_writer :args, :description, :default

  def initialize(name="", flag="", alias_="", numargs=0, args=[], description="", default="", type="")
    @name = name
    @flag = flag
    @alias_ = alias_
    @numargs = numargs + 1
    @args = args
    @description = description
    @default = default
    @type = type
  end

  def add_tab
    "\t"
  end

  def show
    puts "    #{@flag}, #{self.add_tab} #{@alias_}, #{self.add_tab} #{@description}"
  end

  class OptionFactory
    @@option = Option.new("", "", "", 0, [], "", "", "general")
    @@step_option = Option.new("", "", "", 1, [], "", "", "step")

    def self.new_option(opts)
      option = @@option.clone
      option.name = opts[:name]
      option.flag = opts[:flag]
      option.alias_ = opts[:alias_]
      option.description = opts[:description]
      AllOptions.instance.add_option(option)
      return option
    end

    def self.new_step_option(opts)
      option = @@step_option.clone
      option.name = opts[:name]
      option.flag = opts[:flag]
      option.alias_ = opts[:alias_]
      option.description = opts[:description]
      option.numargs = opts[:numargs] + 1
      option.args = opts[:args]
      AllOptions.instance.add_option(option)
      return option
    end

    def self.remove_option(option)
      AllOptions.instance.remove_option(option.name)
    end
  end
end

#################################################
class AllOptions
  include Singleton
  @@options = []

  def add_option(option)
    @@options.push(option)
  end

  def remove_option(option_name)
    @@options.delete_if { |opt| opt.name == option_name }
  end

  def find_option(option_flag)
    return @@options.select { |opt| (opt.flag == option_flag) or (opt.alias_ == option_flag) }.first
  end

  def show
    if @@options.length > 0
      @@options.each { |opt| opt.show() }
    else
      p @@options
    end
  end
end

#################################################
class SupportedSteps
  # enum of steps in a job
  CREATE = "create_dir"
  COPY = "copy"
  MOVE = "move"
  CUSTOM = "custom"
  HELP = "help"
end

#################################################
class Step
  def validate_arglength(args, option)
    if args.length != option.numargs
      raise "Invalid Number of Arguments"
    end
  end

  def validate(args)
  end

  def execute(args)
  end

  def run(args, option)
    self.validate_arglength(args, option)
    self.validate(args)
    self.execute(args)
  end
end

#################################################
class CreateStep < Step
  def validate(args)
    raise "Given directory already exists" if File.exist?(args[1])
    true
  end

  def execute(args)
    FileUtils.mkdir(args[1])
  end
end

#################################################
class CopyStep < Step
  def validate(args)
    raise "Source file is missing" unless File.exist?(args[1])
    raise "Destination file/directory is missing" unless File.exist?(args[2])
    true
  end

  def execute(args)
    FileUtils.cp(args[1], args[2])
  end
end

#################################################
class RenameStep < Step
  # this shall be a demonstration of Command pattern with invoke/undo/redo - deleted files can't have undo
end

#################################################
class SupportedCombiners
  LINEAR = "Linear"
end

#################################################
class Job
  # a job is built from a supported combination of steps
  # eg, Linear - create a file in a directory - create the directory -> create the file
end

#################################################
class JobBuilder
end

#################################################
# This class breaks all kinds of design patterns
class SupportedOptions
  def self.create_options
    # --help, -h
    Option::OptionFactory.new_option(name: "help", flag: "--help", alias_: "-h", description: "Display the help menu")
    # --mkdir, --mk
    Option::OptionFactory.new_step_option(
        name: "create_dir", flag: "--mkdir", alias_: "--mk", numargs: 1, args: ["Destination directory"], description: "Create a directory"
    )
    # --cp, --c
    Option::OptionFactory.new_step_option(
        name: "copy_file", flag: "--cp", alias_: "--c", numargs: 2, args: ["Source file", "Destination file/directory"], description: "Copy a file"
    )
    # --job, --j
    Option::OptionFactory.new_option(name: "job", flag: "--job", alias_: "--j", description: "Create a job")
  end

  def self.run(opt, args)
    case opt.name
    when "job"
      raise "Not Supported" 
    when "copy_file"
      copy_step = CopyStep.new
      copy_step.run(args, opt)
    when "create_dir"
      create_step = CreateStep.new
      create_step.run(args, opt)
    when "help"
      AllOptions.instance.show()
    else
      raise StandardError
    end
  end
end

#################################################
BEGIN {
  if ARGV[0] == nil
    puts "no flag provided, displaying help menu"
  end
}

#################################################
class ScriptExecutor
  def self.main
    opts = AllOptions.instance
    SupportedOptions.create_options()

    if ARGV[0] == nil
      opts.show()
    else
      puts "Arguments: #{ARGV.join(', ')}"
      begin
	opt = opts.find_option(ARGV[0])
        SupportedOptions.run(opt, ARGV)
	puts "Successfully Executed: #{opt.name} with arguments #{ARGV.join(', ')}" unless opt.name == "help"
      rescue Exception => e
        puts "Invalid Arguments: #{e.message}"
      end
    end
  end

end

ScriptExecutor.main()
