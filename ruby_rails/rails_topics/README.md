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


### Rails Libraries

#### Rack
##### Basic
  * Rack contains a lot of boilerplate code which every web server should ideally have already, instead of having to write them -
    - Rack::Request - Query parsing, multipart handling
    - Rack::Response - cookie handling, providing API to returning standard responses [status, header, body]
    - Rack::ShowExceptions - captures all exceptions
    - Rack::CommonLogger - apache style logs
    - Rack::URLMap - redirects to a different rack application, eg, a router
    - Rack::Deflater - compressing responses with gzip
    - Rack::Files - for serving static files
    - Rack::Head - return empty body for head requests
    - Rack::Lock - serialize requests using mutex (sets env["rack.multithread"] = false by default)
    - Rack::Runtime - includes response header which contains the time taken to serve the request (x-runtime)
    - Rack::ConditionalGet - returning not modified responses when it hasn't changed
    - ContentType, ContentLength and Logger
    - Rack::Recursive - for internal redirects
    - Rack::TempfileReaper - removing temp files created during a request
    - [Official Doc](https://github.com/rack/rack#available-middleware-shipped-with-rack)
  * Other features -
    - Possibility to run several web apps inside a single server - how?
    - Easy testing
    - Adding any other middleware as required
    - Supported by many servers - puma, phusion passenger, etc -

##### Rails On Rack
  * Rack compliant web servers need to use Rails.application object to serve a rails application.
  * Rack applications can be inserted into a rails application as either a middleware or as part of a route [see match/mount] as well.
  * bin/rails server creates Rack::Server object and starts the web server [rails server inherits from Rack::Server]
    - We usually start rails server using `rails s` or `rails server` command.
    - We can add `run Rails.application` to config.ru and start the server using `rackup config.ru` as well.
    - [rails s vs rackup](https://stackoverflow.com/a/9383491)
  * Middlewares are loaded once and one needs to restart the server for changes to reflect.
  * ActionDispatch
    - Middleware stack can be configured using `config.middleware`, with methods like `use`, `insert_before` and `insert_after`
    - These are similar to rack middlewares, and added by rails (optimized for rails) - has similar features ([list](https://guides.rubyonrails.org/rails_on_rack.html#internal-middleware-stack))

#### ActiveRecord
##### Basic
  * There are 2 types of ActiveRecord objects, one is present in the DB and another which is not in DB (eg, created via new method or a destroyed object. check via `new_record?` method)
  * Basic CRUD operations with naming conventions.
  * [Official Doc](https://guides.rubyonrails.org/active_record_basics.html)
  * Validations - create, save and update methods use validation before committing to the DB
    - bang versions of `create`, `save`, `update` will raise an exception at failure.
    - all other methods (eg, `insert`, `insert_all`, `upsert`, `update_all`, `update_attributes` will skip validation.
    - however, a `valid?` and `invalid?` method is provided to check if an object is valid if above methods have to be used.
    - inbuilt validations -
    - errors - `valid?` and `invalid?` methods attaches `errors` (ActiveRecord::Error type) object to the ActiveRecord object.
      - it provides an API to find out all errors for a record for specific attributes etc.
    - [Official Doc](https://guides.rubyonrails.org/active_record_validations.html)
  * Callbacks -
    - These methods trigger callbacks - `create`, `destroy`, `destroy_all`, `destroy_by`, `save`, `update`, `update_attribute`, `valid?`, `toggle`, `touch`
    - `after_find` callback triggered for these methods - `all`, `first`, `find`, `find_by`, `find_by_*`, `find_by_sql`, `last`
    - Other methods don't trigger callbacks, eg, `insert`, `delete_all`, `delete_by`, `update_all`, `upsert`, etc.
    - For DB transactions - `after_commit` and `after_rollback` wait for the actual DB commit/rollback to happen.
      - These are not part of the actual transaction. `save` and `destroy` methods are always wrapped inside a transaction.
      - [More on ActiveRecord transactions](https://api.rubyonrails.org/classes/ActiveRecord/Transactions/ClassMethods.html)
      - When using aliases for these method, the last defined method will be executed.
    - [Official Doc](https://guides.rubyonrails.org/active_record_callbacks.html)
  * Migrations -

##### Associations
  * Associations are there to simplify some operations for related models.
    - Eg, when creating a model object which should have a key to another model object becomes easier. Deleting related model objects are simplified.
    -

#####


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
