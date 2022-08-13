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


### Application Performance
  * [Perf Optimization](https://pawelurbanek.com/optimize-rails-performance)
  * [N+1 Query Problem](https://dev.to/junko911/rails-n-1-queries-and-eager-loading-10eh)
    - When a record is loaded from database, its related records are often used immediately after that for other computations/rendering.
    - This can lead to multiple database calls, one per usage of related record, and can go undetected - code would look simple.
    - To reduce the extra queries t requires pre-loading the expected related records along with the main record [using includes command above].
    - [Post](https://pawelurbanek.com/rails-n-1-queries)
  * [Tool Examples](https://nascenia.com/10-ways-and-tools-to-measure-performance-of-your-rails-application/)
  * [More Tips](https://programmingzen.com/top-10-ruby-on-rails-performance-tips/) [Article From 2007]
    1. Optimize ruby code
       - Builtin classes/methods
       - Regular expression rather than loop based string processing
       - Avoid abstraction and elegance (assembly code is the fastest and least elegant) - eg, avoid using define\_method and yield.
       - Refactor loops
       - Avoid hashes if possible - use variables for keys [or at least frequently accessed keys]
       - Avoid nested if/unless - use operators
    2. Caching
    3. Database features beyond ActiveRecord - direct communication if possible
    4. Avoid abstract methods for SQL queries -
       - Using limits and offsets
       - Fetch only limited fields [which are required]
       - Eager loading
       - At any cost, avoid dynamic finders like find\_by as they are very expensive - eg, even find_by_id is 2x slower than find. Use where instead.
       - Can use Model.find\_by\_sql(<full sql query>) as well as where.
    5. Group operations in transactions -
       - ActiveRecord makes creation/update of records as a transaction - better to group many, if possible.
    6. Controllers
    7. HTML for views
    8. Logging - avoid logging unnecessary information - logging is expensive.
    9. Patch garbage collection module of ruby - https://rubyforge.org/projects/railsbench/
