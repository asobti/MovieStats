MovieStats
==========

Dependencies
------------

- [anyjson](http://pypi.python.org/pypi/anyjson/0.2.0)
- [beautiful soup](http://www.crummy.com/software/BeautifulSoup/)
- [peewee](https://github.com/coleifer/peewee)
- [urllib2](http://docs.python.org/2/library/urllib2.html)


Create a 'config.ini' file in the same directory as imdb.py with the following contents

```
[database]
db = imdb
user = user_name
passwd = password
```

Replace user_name and password with your database credentials. 
Make sure a database called 'imdb' exists.