### General
  * includes, join -
    1. join performs an inner join between tables based on the specified second table - eg, Articles.join(:user) => returns articles + users where user\_id of every
       article is non-null.
    2. join doesn't load the resulting rows to memory so if reusing the result, it'll fire a DB query again.
    3. includes performs a left outer join between tables - eg, Articles.join(:user) => returns all articles and fills up null if user\_id is null.
    4. includes stores both resulting rows in the memory.
  * pluck, collect, \<fields\> - Rails 4+
    1. Use .ids if need only id fields (eg, Article.user\_ids) - can do Article.collect(&:user\_id), Article.pluck(:user\_id)
    2. Use .pluck if need more than one fields (eg, Article.pluck(:user\_id, :created\_at)
    3. Use .collect if need all fields (eg, Article.collect)
