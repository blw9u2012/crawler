#!/usr/bin/python
# filename: run.py
import re
import time
import sqlite3
import threading
import pdb
import requests
from Queue import Queue
from crawler import Crawler
from CrawlerCache import CrawlerCache
from bs4 import BeautifulSoup

# Set global variables
num_crawler_threads = 3
max_num_searcher_threads = 3
feed_queue = Queue(maxsize=0)

# Define a function that each thread will run when start() is called


def worker_crawl(q, search):
    # pdb.set_trace()
    while not q.empty():
        site = q.get()
        print "Getting ready to crawl: " + site
        crawler = Crawler(CrawlerCache('crawler.db'), search_term=search)
        print "Successfully created crawler for site: " + site + " with object: " + str(crawler)
        root_re = re.compile('^/$').match
        crawler.crawl(site, no_cache=root_re)
        print "Finished crawling site: ", site
        q.task_done()


def check_site(site):
    try:
        response = requests.get(site)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.MissingSchema:
        print "Missing schema for site. Did you mean http://{}".format(site)


if __name__ == "__main__":
    # Adding the sites manually to the queue is done for the sake of
    # simplicity. The queue is a FIFO queue by default.
    sites = []
    get_sites = True
    print "Please enter sites one at a time. When finished enter 'done'"
    while get_sites:
        site = raw_input("@> ")
        if site.lower() == "done":
            get_sites = False
            print "Finished entering sites"
        else:
            # Check to see if site is valid here...
            if check_site(site):
                feed_queue.put(site)
                sites.append(site)
            else:
                "Please enter a valid url"
                continue

    # Search
    custom_search = False
    search = ""
    response = raw_input("Would you like to search for something? (y/n): ")
    # pdb.set_trace()
    if 'y' in response.lower():
        custom_search = True
        search = raw_input("What would like to search for? ")
    else:
        print "Not searching for anything."

    # Create the worker threads, feed them the worker function and the queue
    start = time.clock()
    for x in range(len(sites)):
        if custom_search:
            worker = threading.Thread(target=worker_crawl, args=(feed_queue,search,))
        else:
            worker = threading.Thread(target=worker_crawl, args=(feed_queue,search,))
        worker.setDaemon = True
        worker.start()
    feed_queue.join()
    end = time.clock() - start
    print "Time it took to finish: {0} seconds".format(end)
    print "All threads have finished. Finished crawling sites."