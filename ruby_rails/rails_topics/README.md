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

##### Query Interface
  * Methods based on returned response type -
    - `ActiveRecord::Relation` - also referred as `collection` or `relation` => ex, `where`, `group`, `order`, `select`, `joins`, `includes`
      - These don't contain an actual resulting row from the DB, but a query which can be fired to get the resulting rows.
    - `ActiveRecord::Object` - also referred as object, and containing an actual row from the DB => ex, `find`, `first`, `take`, `last`, `find_by` 
      - This type of object is also created when a new record has to be inserted to the DB - `new_record?` method is used to differentiate them.
    - `ActiveRecord::Result` - `select_all` - rarely used. Doesn't provide attribute methods after converting to `Array` using `to_a` (provides a regular ruby `Hash`)
    - `Array` of `ActiveRecord::Object` - `find_by_sql`
    - `Array` - `pluck`

  * Method Chaining - Multiple methods can be used one after the other.
    - All previous methods should return a `collection` - methods like `find` (returns `ActiveRecord::Object`) or `pluck` (returns `Array`) fire an actual query.
    - This is to simplify building complex queries before they're actually fired to get the results from the DB.

  * Scope - When building a query to be fired to DB (`collection`), we often have a set of (chained) methods - this can be considered a scope.
    - Some scopes can be defined during model definition if we already know what queries are going to be frequently fired. Scopes can be chained as well.
    - There are some overriding methods provided by `ActiveRecord` which allows one to modify a given scope (including complete elimination of certain methods).

  * `find` workflow -
    - Convert given method + params to SQL query
    - Fire query and get results from DB
    - Create ruby object for every resulting row
    - `after_find` and `after_initialize` callbacks

  * Common Query Methods -
    - `find`
      - `Model.find(10)` => `select * from models where (models.id = 10) limit 1`

    - `take`
      - `Model.take` => `select * from models limit 1`
      - `Model.take(3)` => `select * from models limit 3`

    - `first` - By default, finds the first record ordered by primary key. For an ordered `collection`, ordering is performed using the specified key.
      - `Model.first` => `select * from models order by models.id asc limit 1`
      - `Model.first(3)` => `select * from models order by models.id asc limit 3`
      - `Model.order(:some_attr).first` => `select * from models order by model.some_attr asc limit 1`

    - `last` - Same as `first`, but does everything with `desc`
      - `Model.last(2)` => `select * from models order by models.id desc limit 2`
      - `Model.order(:some_attr).last` => `select * from models order by model.some_attr desc limit 1`

    - `find_by` - Finds the first record matching the given conditions.
      - `Model.find_by(some_attr: 'some_value')` => `select * from models where (models.some_attr = 'some_value') limit 1`
      - This is equivalent to `Model.where(some_attr: 'some_value').take`
      - Doesn't have any order by, so results can be non-deterministic [as it finds and returns the first matching record only].

    - `where` - Conditions can be specified as a string, array or hash.
       - String based conditions which contain variables may be vulnerable to SQL injection as `ActiveRecord` uses the string as is.
       - `Model.where("some_attr = #{some_var} and another_attr = #{another_var}")` => `select * from models where (some_attr = <value1> and another_attr = <value2>)`
       <br/>

       - Array based conditions are safer, except when using `like` wildcards (%, _) - array arguments are escaped by `ActiveRecord`.
       - `Model.where("some_attr = ? and another_attr = ?", some_var, another_var)`
       - Another way to write array based conditions for more clarity - `Model.where("some_attr = :var1 and another_attr = :var2", { var1: some_var, var2: another_var })`
       - Proper use of `like` based condtions - `Model.where("some_attr like ?", Model.sanitize_sql_like(some_var) + %)`
       <br/>

       - Hash based conditions are provided for clarity purpose.
       - `Model.where(some_attr: 'some_value')` or `Model.where('some_attr' => 'some_value')` => `select * from models where (models.some_attr = 'some_value')`
       - `Model.where(created_at: (Time.now.midnight - 1.day)..Time.now.midnight)` => `select * from models where (models.created_at between '2022-01-01 00:00:00' and '2022-01-02 00:00:00')`
       - `Model.where(some_attr: [1, 2, 4])` => `select * from models where (models.some_attr in (1,2,4))`
       <br/>

       - `Model.where.not(some_attr: [1, 2, 4])` => `select * from models where (models.some_attr not in (1,2,4))`
       - For above queries, if `nil` is passed as the value to match, then all records which have a non-nil [SQL: NULL] value for that attribute will be returned.
       <br/>

       - `Model.where(some_attr: 'some_value').or(Model.where(another_attr: [1, 2, 3]))` => `select * from models where (models.some_attr = 'some_value' or models.another_attr in (1,2,3))`
       - Above is similar to - `Model.where("some_attr = 'some_value' or another_attr in (1,2,3)")` => `select * from models where (some_attr = 'some_value' or another_attr in (1,2,3))`
       <br/>

       - `Model.where(some_attr: 'some_value').where(another_attr: [1, 2, 3])` => `select * from models where (models.some_attr = 'some_value' and models.another_attr in (1,2,3))`
       - Above can be also written as - `Model.where(some_attr: 'some_value').and(Model.where(another_attr: [1, 2, 3]))`
       - Above two are similar to - `Model.where("some_attr = 'some_value' and another_attr in (1,2,3)")` => `select * from models where (some_attr = 'some_value' and another_attr in (1,2,3))`

    - `order` - Order the resulting rows via given conditions. Chaining in cur step will result in ordering the results of previous step.
       - `Model.order('some_attr')` and `Model.order('some_attr asc')` => `select * from models order by some_attr asc limit <some default>`
       - `Model.order(:some_attr)` and `Model.order(some_attr: :asc)` are same => `select * from models order by models.some_attr asc limit <some default>`
       - `Model.order(:some_attr).order(another_attr: :desc)` => `select * from models order by models.some_attr asc, models.another_attr desc limit <some default>`

    - `select` - Useful for selecting only specific columns from a table. There are 2 problems - (1) trying to access a field (except `id`) not specified in select will lead to exception, (2) since
      `id` method is required for associations to work, but it doesn't raise a missing attribute exception, so it can lead to unexpected results (what?)
       - `Model.select('some_attr')` => `select models.some_attr from models limit <some default>`
       - `Model.select('some_attr').first` => `select models.some_attr from models order by models.id asc limit 1`
       - `Model.select(:some_attr).distinct` => `select distinct models.some_attr from models limit <some default>`

    - `limit` and `offset` - For paginating the queries.
      - `Model.limit(5).offset(20)` => `select * from models limit 5 offset 20`

    - `group` - Groups the results according to a given attribute. See [this](https://stackoverflow.com/questions/164319/is-there-any-difference-between-group-by-and-distinct).
      - `Model.select(:some_attr).group(:some_attr)` => `select models.some_attr from models group by models.some_attr limit <some default>
      - Can be used to count unique values for a attribute as well.
      - `Model.group(:some_attr).count` => `select count(*) as count_all, models.some_attr as models_some_attr from models group by models.some_attr`

    - `having` -

    - `exists` - Use this when only existence has to be checked, rather than getting the record. Faster than getting the record. Supports `where` clause as well.

    - `pluck` - It is a faster alternative for converting the columns returned from `select` query into a ruby `Array` (skipping `ActiveRecord` object creation).
      - A DB query is performed as soon as `pluck` is encountered, and result is a ruby `Array`, so adding any subsequent clauses will result in error - they've to be added beforehand.
      - Works with multiple tables as well (`joins` and `includes`).
      - When used with `includes`, it performs eager loading, even though the result will contain columns from first model only (unlike `select`, which doesn't work with `includes`)

  * Locking - This is for ensuring atomic updates, prevents race conditions.
    - Optimistic Locking - Allows multiple users to make edits and assumes that the conflicts caused will be minimal (hence transactions won't have to be rolled back). `ActiveRecord::StaleObjectError`
      is thrown if another process (ie, user) has made changes to the record since it was opened. Optimistic locking can be enabled by adding the column `lock_version` - if an update request is
      made with a `lock_version` value lower than what is present in the DB, then the aforementioned exception is raised - the exception can be rescued and transaction can be rolled back or merged, etc.

    - Pessimistic Locking - Uses the locking mechanism provided by the underlying database - obtains an exclusive lock on the selected row, when used. Lock operations are wrapped inside a
      transaction to avoid deadlocks. `lock` can accept raw SQL arguments for different kinds of locking, eg, `LOCK IN SHARE MODE` to allow reads.

    - `lock` - Simple pessimistic locking of a row, user has to wrap it in transaction to prevent deadlocks.
      - `Model.lock.first`
      - `Model.transaction do; v_mod = Model.lock.first; v_mod.some_attr = 'some new value'; v_mod.save; end`
      <br/>
    - `with_lock` - Pessimistic locking along with starting a transaction.
      - `v_mod = Model.first; v_mod.with_lock do; v_mod.some_attr = 'some new value'; v_mod.save; end`

  * Less Used Methods-
    - Overriding conditions - Can be used to override the existing query. Actual purpose is unknown, but looks to be to simplify refactoring (ie, update existing query rather than rewrite).
      - `unscope` => Any condition can be removed from the query, eg, `Model.where(some_attr: [1,2,3]).order(:some_attr).unscope(:order)` will remove order condition.
      - `only` => Use this to tell the query to use any particular condition only.
      - `reselect` => Overrides the fields in any existing `select` statement.
      - `reorder` => Override the default ordering (which can be specified at model definition as well).
      - `reverse_order` => Reverses the existing ordering condition.
      - `rewhere` => Overrides any existing where condition.

    - `none` - Returns a chainable relation with no records, and any subsequent chaining will result in an empty relation. Fires no queries.
    - `readonly` - Used to explicitly disallow the modification of any returned records - raises an exception if we try to update such an object (via `save`/`destroy`/`update`).

  * Batch Finder Methods-
    - `find_each` - Gets the records matching given criterias, but in batches, and yields 1 record at a time from the resulting array. Works with objects as well as collection.
       - `Model.where(some_attr: 'some_value').find_each { |m| m.some_method }`
       - Parameters available for batch size, pagination and ignoring errors.

    - `find_in_batches` - Same as above, but yields the whole resulting array at once.

    - `in_batches`

    - `all.each` - Loads the complete set of results in a data structure - not suitable for use when the complete set can be huge.

  * Join methods -
    - `joins` - For inner joins and custom queries.

    - `left_outer_joins` - For left outer joins, ie, returning records even if any associated records aren't found.

  * Eager Loading - This is provided as a solution to the N+1 queries problem.
    - `includes` - All specified associations are loaded with minimum possible queries. Any number of associations can be specified for eager loading. Uses left inner join when `where` is given.
      - `Model.includes(:another_model)` => Fires 2 queries => `select * from models` and `select * from another_models where another_models.id in (some values)`
      - `Model.includes(:another_model, :third_model)`
      - `Model.includes(:another_model, { third_model: [ :fourth_model, :fifth_model ] }).find(1)` => Loads one model object, associated `another_model` objects, `third_model` objects corresponding to
        `another_model` object, and `fourth_model` and `fifth_model` objects associated with `third_model` object.
      <br/>

      - We can add a where condition to the eager loaded association, and that loads the objects using the left inner join operation (instead of multiple queries).
      - `Model.includes(:another_model).where(another_model: { some_attr: 'some_value' })` =>
        `select models.id as t0_r0, models.attr1 as t0_r1, ..., another_mod.id as t1_r0, another_mod.attr2 as t1_r1, ..., from models left outer join another_models another_mod on another_mod.id
          = models.another_model_id where (another_mod.some_attr = 'some_value')`
      <br/>

      - We can pass a string based query as well in the where clause, but then `references` has to be used at the end.
      - `Model.includes(:another_model).where("another_models.some_attr = 'some_value'").references(:another_model)`
      - NOTE: use of 's' for string vs hash queries when firing queries which reference tables. Table names have 's' at the end and so should the raw SQL queries (when using a table name).
      <br/>

      - Above operation can be done using `joins` query as well, but it performs an inner join which can return empty results when given conditions don't match - left inner join will always return
        at least the base table (ie, `models`).
      - Another caveat of includes => If an association is eager loaded as part of a join, any fields from custom `select` clause will not be present in the loaded models - this is to avoid the
        ambiguity of whether those fields should be on the parent object or child.

    - `preload` - Loads each specified association using one query per association just like `includes` - however, `where` clause can't be specified.

    - `eager_load` - Loads all specified associations using left outer join (always). Also, it possible to add `where` clause like the `includes` method. `includes` method is a hybrid of `preload`
      and `eager_load` based on whether or not `where` clause is provided.

  * Other Methods -
    - Dynamic Finders - ActiveRecord defines these (along with bang versions, which raises RecordNotFound error) for every attribute of a model, eg, `Model.find_by_some_attr()`.
    - `find_by_sql` - executes the SQL query as it is an returns an array of model objects like other finder methods.
    - `select_all` - `connection.select_all` is similar to `find_by_sql`. It returns the objects from DB without initializing (type - `ActiveRecord::Result`). Call `to_a` to get array of hashes.
      - res = `Model.connection.select_all('select * from models where some_attr = 'some_value')` -> `res.to_a.first` -> This is of type `Hash` with no methods for attributes.
    - `ids` - `pluck` all the id's for the relation using the primary key of the table (which need not be `id` always).
    - `count`, `average`, `minimum`, `maximum` and `sum` -
    - `explain` -
    - Enums -
    - Find Or Build Methods -

###### Advanced Queries/Associations

##### Active Support Core Extensions
  * Notes - Even the smallest required extensions can be loaded instead of the whole library, eg, `require "active_support/core_ext/hash/indifferent_access"`
  * General Methods -
    - `blank?` and `present?`
    - `try` -
    - `presence`
    - `duplicable?` - check if `dup` and `clone` would work on an object (sometimes, an object can undefine or raise exception for those methods, `duplicable?` doesn't work for them).
    - `acts_like?` - check if an object acts like some other class (if the method definition names are the same - return values can still be different so avoid using this).
    - `in?` -
    - `deep_dup` -
    - `class_eval` -
    - `to_param` -
    - `to_query` -
    - `with_options` -
    - `to_json` -
    - `instance_values` and `instance_variables` -
    - `suppress`, `silence_warnings`, `enable_warnings` -

  * Class and Module
    - `alias_attribute` -
    - `attr_internal` -
    - `mattr_accessor` -
    - `module_parent`, `module_parents`, `module_parent_name` -
    - `anonymous?` -
    - `delegate` -
    - `delegate_missing_to` -
    - `redefine_method` -
    <br/>

    - `class_attribute` -
    - `cattr_accessor` -
    - `subclasses` and `descendants` -

  * String, Regexp, Symbol
    - `html_safe` -
    - `downcase`, `gsub`, `chomp`, `strip`, `underscore`, `to_s`, `dup` -
    - `remove` -
    - `squish` -
    - `truncate`, `truncate_bytes` and `truncate_words` -
    - `inquiry` -
    - `starts_with?` and `ends_with?` -
    - `strip_heredoc` -
    - `indent` -
    - `at`, `from`, `to`, `first`, `last` -
    - `pluralize`, `singularize`, `camelize`, `underscore`, `titelize`, `dasherize`, `demodulize`, `deconstantize`, `parameterize`, `tableize`, `classify`, `constantize`, `humanize`, `foreign_key`
    - `to_date`, `to_time`, `to_datetime`
    <br/>

    - `multiline?` -
    <br/>

    - `starts_with?` and `ends_with?` -

  * Numeric, Integer and BigDecimal
    - `bytes`, `kilobytes`, ..., `exabytes` -
    - `seconds`, 'minutes`, 'hours`, `days`, `weeks`, `fortnights` -
    - `to_fs`
    <br/>

    - `multiple_of?` -
    - `ordinal` and `ordinalize` -
    - `months` and `years` -
    <br/>

    - `to_s` -

  * Arrays, Range
    - `from`, `to`, `including`, `excluding`, `first`, `second`, ..., `forty_two`
    - `extract` -
    - `extract_options` -
    - `to_sentence` - connectors can also be passed.
    - `to_fs` -
    - `to_xml` -
    - `wrap` -
    - `deep_dup` -
    - `in_groups_of` and `in_groups` -
    - `split` -
    <br/>

    - `to_s` -
    - `===` and `include?` -
    - `overlaps?` -

  * Hashes
    - `to_xml` -
    - `merge`, `reverse_merge`, `deep_merge` -
    - `reverse_update` -
    - `deep_dup` -
    - `except` -
    - `stringify_keys` -
    - `symbolize_keys` -
    - `to_options` -
    - `assert_valid_keys` -
    - `deep_transform_values` -
    - `slice` and `extract` -
    - `with_indifferent_access` - returns `ActiveSupport::HashWithIndifferentAccess`

  * Enumerable
    - `sum` -
    - `index_by` and `index_with` -
    - `many?` -
    - `exclude?` -
    - `including` and `excluding` -
    - `pluck` and `pick` -

  * Date, DateTime, Time
    - Date objects have the format `DD:MM:YY`
    - `current`, `today`, `tomorrow`, ..., `future?`, `on_weekend?`, etc -
    - `beginning_of_week`, `beginning_of_month`, `beginning_of_quarter`, `beginning_of_year`, `end_of_week`, ..., `end_of_year` -
    - `monday`, `sunday` -
    - `prev_week`, `next_week` -
    - `years_ago`, `months_ago`, `weeks_ago`, `years_since`, `months_since` -
    - `advance` and `change` - takes keys like `weeks`, `months`, etc
    - `beginning_of_minute`, `beginning_of_hour`, `beginning_of_day`, `end_of_minute`, `end_of_hour`, `end_of_day` - returns Time/DateTime types, uses the set timezone.
    - `ago` and `since` - returns Time/DateTime, takes arguments in seconds.
    <br/>

    - DateTime is subclass of Date so all methods are inherited, but the return values are DateTime (format - DD:MM:YY HH:MM:SS TZ). DateTime doesn't understand DST.
    - `beginning_of_hour` and `end_of_hour` are only implemented for DateTime (not for Date).
    - `seconds_since_midnight` -
    - `utc` and `utc?` -
    - `advance` and `change` - now they work with extra arguments.
    <br/>

    - Time takes DST into account. Return type is Time (for `since` and `ago`, returns type maybe DateTime). `:usec` option is supported in `change` method.
    - `all_day`, `all_week`, `all_month`, `all_quarter` and `all_year` - returns a range of Time.
    - `prev_day`, `prev_month`, `prev_quarter`, `prev_year`, `next_day`,..., `next_year` -

  * File Related -
    - `File#atomic_write` - Prevents any reader from seeing half written content.
    - `Pathname#existence` - Checks the existence of file and returns it if it exists, else null.

  * Errors -
    - NameError -
    - LoadError -


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
