$SomeGlobal = "Random String"
class LoadedClass

  def initialize(str)
    @var = str
  end

  def load_method(str)
    p "Load method with string: #{str} with constant: #{Cnst} and instance var: #{@var}"
  end

  Cnst = "Constant"
end

ld_cls_old = LoadedClass.new("Old Variable")
ld_cls_new = LoadedClass.new("New Variable")

ld_cls_old.load_method("From Old Object")
ld_cls_new.load_method("From New Object")

p "Some Global: #{$SomeGlobal}"
p "Other Global Before: #{$OtherGlobal}"
$OtherGlobal = "Other Random String"
p "Other Global After: #{$OtherGlobal}"
