import urllib2
import sys
import peewee
import anyjson

from bs4 import BeautifulSoup
from datetime import datetime
from ConfigParser import SafeConfigParser

# db handle
# there has to be a way to do this without putting it 
# in the global namespace
db = peewee.MySQLDatabase(None)

class Logger :
	def __init__(self, verbose) :
		self.verbose = verbose

	def log(self, msg) :
		if (self.verbose) :
			print msg

	# prints error even if verbose = False
	def error(self, err) :
		print err

	def newline(self) :
		if (self.verbose) :
			print ''

class Movie(peewee.Model) :
	id 			= peewee.CharField(primary_key=True, unique=True)
	title 		= peewee.CharField()
	year 		= peewee.IntegerField()
	rated 		= peewee.CharField()
	released 	= peewee.DateField(null=True)
	runtime		= peewee.FloatField(null=True)
	poster		= peewee.CharField()
	rating 		= peewee.FloatField()
	votes 		= peewee.IntegerField()	

	class Meta :
		database = db	

class Imdb :
	def __init__(self, years, threshold, log) :
		# logger instance
		self.log = log

		# the years to scrape
		self.years = years

		# url that lists movies for a year sorted by num_votes (desc)
		self.baseUrl = "http://www.imdb.com/search/title?count=100&sort=num_votes&title_type=feature&year="

		# omdb api url
		self.omdbUrl = "http://www.omdbapi.com/?i="

		# ignore movies with less that votingThreshold ratings
		self.votingThreshold = threshold

		# number of movies shown per page. Used to increment value of start
		self.count = 100

		# collection of movies
		self.movies = 0

		# create table
		Movie.create_table(fail_silently=True)

		
	'''
		Begin the process of scraping, parsing for the years supplied in the constructor
	'''
	def begin(self) :

		for year in self.years :
			self.scrapeYear(year)

		# self.scrapeYear(self.years[2])
		print 'Total movies saved: ' + str(self.movies)

	'''
		Responsible for scraping all movies for the specified year that have 
		more than self.votingThreshold ratings
	'''
	def scrapeYear(self, year) :
		year = str(year)
		start = 1
		yearUrl = self.baseUrl + year + "&start="		

		continueScraping = True

		while continueScraping :
			self.log.log('[' + str(year) + '] Start = ' + str(start))

			url = yearUrl + str(start)

			try :
				self.log.log('Starting scrape...')
				page = urllib2.urlopen(url).read()

				self.log.log('Starting parse...')
				continueScraping = self.parsePage(page)
				
				start += self.count
			
			except urllib2.URLError as e :
				self.log.error(e)
			except Exception as e :
				self.log.error('Error encountered')
				self.log.error(e)
			
	'''
		Parse a page of movies and append Movie items
		into self.movie
		Returns True if parsing should continue, else False
		Based on self.votingThreshold
	'''
	def parsePage(self, page) :
		# TO-DO: handle soup creation errors
		soup = BeautifulSoup(str(page))
		
		for el in soup.find_all('span', class_="wlb_wrapper") :
			id = el['data-tconst']
			info = self.getMovieInfo(id)

			if info is not None :
				# special case because omdb is outdated
				if "N/A" in info['imdbVotes'] :
					info['imdbVotes'] = '9,999'

				if "N/A" in info['imdbRating'] :
					info['imdbRating'] = '0.0'
				# end of special case handling

				if int(info['imdbVotes'].replace(',', '')) < self.votingThreshold :
					# we have reached the threshold. Time to exit
					return False
				else :
					movie = self.createModel(info)
					movie.save()
					self.movies += 1
					self.log.log('Saved movie ' + movie.title)

		return True

	def getMovieInfo(self, id) :
		url = self.omdbUrl + str(id)

		try :
			infoStr = urllib2.urlopen(url).read()
			infoObj = anyjson.deserialize(infoStr)
			
			return infoObj

		except urllib2.URLError as e:
			self.log.log("Error at url " + url)
			self.log.log(e)
			return None

	def createModel(self, info) :
		id = info['imdbID']
		title = info['Title']
		year = int(info['Year'])
		rated = info['Rated']

		try :
			released = datetime.strptime(info['Released'], "%d %b %Y").date()
		except ValueError :
			released = None

		runtime = 0.0 if "N/A" in info['Runtime'] else float(info['Runtime'].replace('h','.').replace('min','').replace(' ',''))
		poster = info['Poster']
		rating = float(info['imdbRating'])
		votes = int(info['imdbVotes'].replace(',',''))

		return Movie.create(id=id, title=title, year=year, rated=rated, released=released, runtime=runtime, poster=poster, rating=rating, votes=votes)


if __name__ == "__main__" :
	
	# defaults
	verbose = False
	threshold = 500

	# read-in command line args
	for arg in sys.argv[1:] :
		if str(arg).lower() == '--verbose' or str(arg).lower() == '-v' :
			verbose = True
		if str(arg).lower().startswith("--threshold=") :
			threshString = str(arg).lower().replace("--threshold=", "")
			try :
				threshold = int(threshString)
			except :
				print 'Invalid value for threshold'
				sys.exit(1)

	# logger instance
	log = Logger(verbose)

	startYear = 2000
	endYear = 2012

	years = range(startYear, endYear + 1)	

	# init the db
	parser = SafeConfigParser()
	parser.read('config.ini')

	dbname = parser.get('database', 'db')
	user = parser.get('database', 'user')
	passwd = parser.get('database', 'passwd')

	db.init(dbname, user=user, passwd=passwd)

	imdb = Imdb(years, threshold, log)
	imdb.begin()