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