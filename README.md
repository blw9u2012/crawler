crawler
=======


This is a multi-threaded web scraper. Most of the heavy lifting was done by Brice Leroy here: http://www.debrice.com/building-a-simple-crawler/. I thought it was a good choice to get started on learning about threading and concurrency in Python.

### Knowing Your Data
Originally I thought I would be able to pull all of the html markup and from that pull the specific data that I wanted without knowing the structure of the html page this proved to be very difficult. For example, I wanted to scrape the site [slickdeals](http://www.slickdeals.net) and only extract data specific to an Xbox or PS4 (because I refuse to pay $400 for either lol). I assumed that the content I would be looking for would be in a `div` but other than that there were no other assumptions that I could make (such as the class name or any other attributes that would indicate the `div` contained a deal item) that would allow me to automatically extract the content I was looking for. Given that conclusion, I decided to feed the scraper the structure of the specific content I was looking for using BeautifulSoup instead of trying to figure out the structure while scraping the site. Because I decided to go this way, to extract specific data you should know the way this data is structured in the html page before scraping it.

### SQLite as a Cache
Decided to use SQLite as a cache. I know that SQLite doesn't scale well but this project is specifically for learning. Will probably end up trying to use Twisted or Gevent to see if crawling asynchronously is better that crawling "concurrently." Also looking to experiment with NoSQL database specifically Mongo.
