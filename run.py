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
    while not q.empty():
        site = q.get()
        print "Getting ready to crawl: " + site
        # crawler = Crawler(CrawlerCache(site[11:-4] + '.db'))
        crawler = Crawler(CrawlerCache('crawler.db'))
        print "Successfully created crawler for site: " + site + " with object: " + str(crawler)

        # Crawl the site
        root_re = re.compile('^/$').match
        crawler.crawl(site, root_re)
        print "Finished crawling site: ", site
        q.task_done()


def worker_search(site):
    # pdb.set_trace()
    with sqlite3.connect('crawler.db') as connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT * FROM sites WHERE domain LIKE ?", ('%{}%'.format(site), ))
        for row in cursor:
            if 'xbox' in row[1] or 'ps4' in row[1]:
                print row

if __name__ == "__main__":
    root_re = re.compile('^/$').match
    # Adding the sites manually to the queue is done for the sake of
    # simplicity. The queue is a FIFO queue.
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
    # Create the worker threads, feed them the worker function and the queue
    start = time.clock()
    for x in range(len(sites)):
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
        if threading.active_count() < max_num_searcher_threads:
            worker = threading.Thread(
                target=worker_search, args=(sites[x][11:-4],))
            worker.setDaemon = True
            worker.start()
        else:
            print "Reached max number of threads. Be patient"
