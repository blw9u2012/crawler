from HTMLParser import HTMLParser

# HTMLParser is subclassed the only method that we
# need to override is handle_starttag.


class HREFParser(HTMLParser):

    """
    Parser that extracts hrefs
    """
    hrefs = set()

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            dict_attrs = dict(attrs)
            if dict_attrs.get('href'):
                self.hrefs.add(dict_attrs['href'])
