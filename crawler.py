# -*- coding: utf-8 -*-
# filename: crawler.py
import pdb
import urllib2
from HREFParser import HREFParser
from urlparse import urlparse


def get_local_links(html, domain):
    """
    Read through HTML content and returns a tuple of links
    internal to the given domain
    """

    # Initialize a set of links
    href_links = set()
    parser = HREFParser()
    parser.feed(html)

    for href in parser.hrefs.copy():
        u_parse = urlparse(href)
        try:
            if href.startswith('/'):
            # purposefully using path, no query, no hash
                href_links.add(u_parse.path)
            else:
                # only keep the local urls
                if u_parse.netloc == domain:
                    href_links.add(u_parse.path)
        except Exception, e:
            raise e

    return href_links


class Crawler(object):

    def __init__(self, cache=None, depth=2, search_term=None):
        """
        depth: how many time it will bounce from page one (optional)
        cache: a basic cache controller (optional)
        """
        self.depth = depth
        self.content = {}
        self.cache = cache
        self.search_term = search_term

    def crawl(self, url, no_cache=None):
        """
        url: where we start crawling, should be a complete URL like
        'http://www.intel.com/news/'
        search_term: the term the user is searching for should they opt to.
        no_cache: function returning True if the url should be refreshed
        """
        u_parse = urlparse(url)
        self.domain = u_parse.netloc
        self.content[self.domain] = {}
        self.scheme = u_parse.scheme
        self.no_cache = no_cache
        self._crawl([u_parse.path], self.depth)

    def set(self, url, html):
        self.content[self.domain][url] = html
        if self.is_cacheable(url):
            self.cache.set(self.domain, url, html)

    def get(self, url):
        # pdb.set_trace()
        page = None
        if self.is_cacheable(url):
            page = self.cache.get(self.domain, url)
        if page is None:
            # Check for the search term...
            page = self.curl(url)
        else:
            print "cached url... [%s] %s" % (self.domain, url)
        return page

    def is_cacheable(self, url):
        return self.cache and self.no_cache \
            and not self.no_cache(url)

    def _crawl(self, urls, max_depth):
        """
        Recursively crawl a site given the max depth.
        """
        n_urls = set()
        if max_depth:
            for url in urls:
                # do not crawl twice the same page
                # if the domain is not a key in the content dictionary
                if url not in self.content:
                    html = self.get(url)
                    if html is not None:
                        self.set(url, html)
                    else:
                        pass
                    n_urls = n_urls.union(get_local_links(html, self.domain))
            self._crawl(n_urls, max_depth - 1)

    def curl(self, url):
        """
        return content at url.
        return empty string if response raise an HTTPError (not found, 500...)
        """
        try:
            print "retrieving url... [%s] %s" % (self.domain, url)
            req = urllib2.Request(
                '%s://%s%s' % (self.scheme, self.domain, url))
            response = urllib2.urlopen(req)
            content = response.read().decode('ascii', 'ignore')
            # Return everything
            if self.search_term is None:
                return content

            # Return only search term items..
            elif self.search_term is not None and self.search_term in content:
                return content

            else:
                return
        except urllib2.HTTPError, e:
            print "error [%s] %s: %s" % (self.domain, url, e)
            return ''
