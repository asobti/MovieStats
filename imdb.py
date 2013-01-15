import urllib2
import sys
from bs4 import BeautifulSoup

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

class Movie :
	def __init__(self, id, title, year, ratings) :
		self.id = id
		self.title = title
		self.year = year
		self.ratings = ratings

	def __str__(self) :
		return (self.title + " " + self.year + " : " + str(self.ratings) + " ratings.").encode('utf-8')

class Imdb :
	def __init__(self, years, threshold, log) :
		# logger instance
		self.log = log

		# the years to scrape
		self.years = years

		# url that lists movies for a year sorted by num_votes (desc)
		self.baseUrl = "http://www.imdb.com/search/title?count=100&sort=num_votes&title_type=feature&year="

		# ignore movies with less that votingThreshold ratings
		self.votingThreshold = threshold

		# number of movies shown per page. Used to increment value of start
		self.count = 100

		# collection of movies
		self.movies = []
		
	'''
		Begin the process of scraping, parsing for the years supplied in the constructor
	'''
	def begin(self) :
		self.scrapeYear(self.years[12])
		print 'Total movies picked up: ' + str(len(self.movies))

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
				
			except urllib2.HTTPError as e :
				self.log.error(e)
			except :
				self.log.error('Error encountered')

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
			el = el.next_sibling

			if len(el.string.strip()) == 0 :			
				el = el.next_sibling

			title = el.string
			el = el.next_sibling
			
			if len(el.string.strip()) == 0 :			
				el = el.next_sibling

			year = el.string
			
			el = el.parent.next_sibling

			if len(el.string.strip()) == 0 :
				el = el.next_sibling

			ratings = int(el.string.replace(',', ''))
			
			if ratings < self.votingThreshold :
				return False

			self.movies.append(Movie(id, title, year, ratings))			
			
		self.log.log('Movie count : ' + str(len(self.movies)))
		self.log.newline()
		return True


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
	imdb = Imdb(years, threshold, log)
	imdb.begin()