#!/usr/bin/python
# filename: run.py
import re
import time
import sqlite3
import threading
import pdb
from Queue import Queue
from crawler import Crawler
from CrawlerCache import CrawlerCache
from bs4 import BeautifulSoup

# Set global variables
num_crawler_threads = 3
max_num_searcher_threads = 3
feed_queue = Queue(maxsize=0)

# Define a function that each thread will run when start() is called


def worker_crawl(q):
    # pdb.set_trace()
    while not q.empty():
        site = q.get()
        print "Getting ready to crawl: " + site
        # crawler = Crawler(CrawlerCache(site[11:-4] + '.db'))
        crawler = Crawler(CrawlerCache('crawler.db'))
        print "Successfully created crawler for site: " + site + " with object: " + str(crawler)
        root_re = re.compile('^/$').match
        crawler.crawl(site, search_term=search, no_cache=root_re)
        print "Finished crawling site: ", site
        q.task_done()


def worker_search(site):
    # pdb.set_trace()
    with sqlite3.connect('crawler.db') as connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT * FROM sites WHERE domain LIKE ?", ('%{}%'.format(site), ))
        for row in cursor:
            soup = BeautifulSoup(row[2])
            if site == 'slickdeals':
                with open(site+".txt", 'w+') as f:
                    f.write(soup.findAll('div', attrs={"class": "dealblocktext"}))
            if site == 'woot':
                with open(site+".txt", 'w+') as f:
                    f.write(soup.findAll('div', attrs={"class": "info"}))
            if site == 'cowboom':
                with open(site+".txt", 'w+') as f:
                    f.write(soup.findAll('div', attrs={"class": "product-block"}))


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
            feed_queue.put(site)
            sites.append(site)

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
            worker = threading.Thread(target=worker_crawl, args=(feed_queue,))
        else:
            worker = threading.Thread(target=worker_crawl, args=(feed_queue,))
        worker.setDaemon = True
        worker.start()
    feed_queue.join()
    end = time.clock() - start
    print "Time it took to finish: {0} seconds".format(end)
    print "All threads have finished. Finished crawling sites."

    print "Starting to search through sites."
    # pdb.set_trace()
    for x in range(len(sites)):

        num_threads = threading.active_count()
        if threading.active_count() < max_num_searcher_threads:
            worker = threading.Thread(
                target=worker_search, args=(sites[x][11:-4],))
            worker.setDaemon = True
            worker.start()
        else:
            print "Reached max number of threads. Be patient"
