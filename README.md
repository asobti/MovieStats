MovieStats
==========

Dependencies
------------

- [anyjson](http://pypi.python.org/pypi/anyjson/0.2.0)
- [beautiful soup](http://www.crummy.com/software/BeautifulSoup/)
- [peewee](https://github.com/coleifer/peewee)
- [urllib2](http://docs.python.org/2/library/urllib2.html)


Create a _config.ini_ file in the same directory as _imdb.py_ with the following contents

```
[database]
db = imdb
user = user_name
passwd = password
```

Replace *user_name* and _password_ with your database credentials. 
Make sure a database called _imdb_ exists.

Usage
-----

```
python imdb.py [--verbose] [--threshold=n] [--start=s] [--end=e]
```

Verbose mode prints copious logs to the console at every step of execution

--threshold is the minimum number of user votes a movie must have for it to be picked up. **Default value is 500**, so movies that have less than 500 votes get ignored.

--start is the starting year from which movies will be picked up. **Default value is 2000**.
--end is the ending year up to which movies will be picked up. **Default value is 2012**

Format for --start and --end is YYYY. Start and end year are inclusive.

It is inevitable that fetching data on a few movies will error out with a URLError exception. In my tests, this happens roughly once per ~1000 movies. However, when adding movies, the script first checks the database. If it finds a record for the movie already exists, it does not bother fetching it again. This means, that after having run the script once, if you run it a second time, it will blaze by the movies it had already fetched and fill in all those it missed in the last run.

At some point, I will edit the script to re-try failed requests a certain number of times before moving on, but until then, a second pass works great.
