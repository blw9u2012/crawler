#!/usr/bin/python
# filename: run.py
import re
import time
from Queue import Queue
from threading import Thread
from crawler import Crawler
from CrawlerCache import CrawlerCache

# Set global variables
num_threads = 3
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

if __name__ == "__main__":
    root_re = re.compile('^/$').match
    # Adding the sites manually to the queue is done for the sake of
    # simplicity. The queue is a FIFO queue.
    get_sites = True
    print "Please enter sites one at a time. When finished enter 'done'"
    while get_sites:
        site = raw_input("@> ")
        if site.lower() == "done":
            get_sites = False
            print "Finished entering sites"
        else:
            feed_queue.put(site)

    # Create the worker threads, feed them the worker function and the queue
    start = time.clock()
    for x in range(num_threads):
        worker = Thread(target=worker_crawl, args=(feed_queue,))
        worker.setDaemon = True
        worker.start()
    feed_queue.join()
    end = time.clock() - start
    print "Time it took to finish: {0} seconds".format(end)
    print "All threads have finished. Finished crawling sites."
