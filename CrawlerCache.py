import sqlite3
import threading


class CrawlerCache(object):

    """
    Crawler data caching per relative URL and domain.
    """

    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        c = self.conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS sites
            (domain text, url text, content text)''')
        self.conn.commit()
        self.cursor = self.conn.cursor()

    def set(self, domain, url, data):
        """
        store the content for a given domain and relative url
        """
        lock = threading.Lock()
        lock.acquire()
        try:
            self.cursor.execute("INSERT INTO sites VALUES (?,?,?)", (domain, url, data))
            self.conn.commit()
        finally:
            lock.release()

    def get(self, domain, url):
        """
        return the content for a given domain and relative url
        """
        self.cursor.execute("SELECT content FROM sites WHERE domain=? and url=?",
                            (domain, url))
        row = self.cursor.fetchone()
        if row:
            return row[0]

    def get_urls(self, domain):
        """
        return all the URLS within a domain
        """
        self.cursor.execute("SELECT url FROM sites WHERE domain=?", (domain,))
        # could use fetchone and yield but I want to release
        # my cursor after the call. I could have create a new cursor tho.
        # ...Oh well
        return [row[0] for row in self.cursor.fetchall()]
