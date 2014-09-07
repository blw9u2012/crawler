crawler
=======


This is a multi-threaded web scraper. Most of the heavy lifting was done by Brice Leroy here: http://www.debrice.com/building-a-simple-crawler/. I thought it was a good choice to get started on learning about threading and concurrency in Python.

Decided to use SQLite as a cache. I know that SQLite doesn't scale well but this project is specifically for learning. Will probably end up trying to use Twisted or Gevent to see if crawling asynchronously is better that crawling "concurrently."


