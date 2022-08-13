class Item
  attr_reader :item_name, :quantity, :supplier_name, :price

  def initialize(item_name, quantity, supplier_name, price)
    @item_name = item_name
    @quantity = quantity
    @supplier_name = supplier_name
    @price = price
  end 
  
  def compare_others(other_item)
    @item_name == other_item.item_name && @quantity == other_item.quantity && @supplier_name == other_item.supplier_name && @price == other_item.price
  end
  
  def ==(other_item)
    @item_name == other_item.item_name && @quantity == other_item.quantity && @supplier_name == other_item.supplier_name && @price == other_item.price
  end
  
  def eql?(other_item)
    # ==(other_item)    # doesn't work
    # compare_others(other_item)
    # self.==(other_item)   # works as well
  end
  
  def hash
    @item_name.hash ^ @quantity.hash ^ @supplier_name.hash ^ + @price.hash
  end
end

items = [Item.new("a", 1, "b", 2), Item.new("a", 1, "b", 2), Item.new("c", 2, "b", 2), Item.new("a", 1, "b", 2)]
# uniq somehow utilizes ==, eql? and hash methods defined somewhere up the hierarchy to perform comparisons
p items.uniq
