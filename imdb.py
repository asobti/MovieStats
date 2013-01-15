import urllib2
from bs4 import BeautifulSoup

class Movie :
	def __init__(self, id, title, year, ratings) :
		self.id = id
		self.title = title
		self.year = year
		self.ratings = ratings

	def __str__(self) :
		return (self.title + " " + self.year + " : " + str(self.ratings) + " ratings.").encode('utf-8')

class Imdb :
	def __init__(self, years) :
		# the years to scrape
		self.years = years

		# url that lists movies for a year sorted by num_votes (desc)
		self.baseUrl = "http://www.imdb.com/search/title?count=100&sort=num_votes&title_type=feature&year="

		# ignore movies with less that votingThreshold ratings
		self.votingThreshold = 5000	
		

	def begin(self) :
		page = self.scrapeYear(self.years[12])

		if page is not None :
			movies = self.parseYear(page)
			
			print 'Count: ' + str(len(movies))

			for movie in movies :
				print movie
				#pass


	'''
		Responsible for scraping all movies for the specified year that have 
		more than self.votingThreshold ratings
	'''
	def scrapeYear(self, year) :
		year = str(year)
		start = 1
		yearUrl = self.baseUrl + year + "&start="

		url = yearUrl + str(start)

		try :
			return urllib2.urlopen(url).read()
		except urllib2.HTTPError as e :
			return None

	def parseYear(self, page) :
		soup = BeautifulSoup(str(page))
		movies = []

		for span in soup.find_all('span', class_="wlb_wrapper") :			
			id = span['data-tconst']			
			span = span.next_sibling

			if len(span.string.strip()) == 0 :			
				span = span.next_sibling

			title = span.string
			span = span.next_sibling
			
			if len(span.string.strip()) == 0 :			
				span = span.next_sibling

			year = span.string

			ratings = int(soup.find('td', class_="sort_col").string.replace(',', ''))			

			movies.append(Movie(id, title, year, ratings))

			#break

		return movies


if __name__ == "__main__" :
	
	startYear = 2000
	endYear = 2012

	years = range(startYear, endYear + 1)
	imdb = Imdb(years)
	imdb.begin()