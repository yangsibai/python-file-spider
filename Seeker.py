# -*- coding: utf-8 -*-

import urllib2
import sqlite3
import util


class Seeker:
    def __init__(self):
        # self.url = options.url
        # self.file = options.file

        self.State_New = 0
        self.State_Seeked = 1
        self.State_Invalid = 2

        self.conn = sqlite3.connect("spider.db")

        self._create_table()
        if self._has_no_url():
            self._insert_url(util.get_start_url())


    def _create_table(self):
        c = self.conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS Page
                    (PageID INTEGER PRIMARY KEY AUTOINCREMENT,
                     URL TEXT, Title TEXT,
                     AddTime TEXT, SeekTime TEXT, State INTEGER )''')
        self.conn.commit()

    def _has_no_url(self):
        c = self.conn.cursor()
        c.execute('''SELECT * FROM Page LIMIT 1''')
        return c.fetchone() is None

    def _insert_url(self, url):
        c = self.conn.cursor()
        sql = """INSERT INTO Page
                      (URL, Title, AddTime, SeekTime, State)
                      VALUES (?, ?, ?, ?, ?)"""
        if isinstance(url, basestring):
            url = [url]
        to_insert = [item for item in url if self._url_not_exist(item)]
        if len(to_insert) > 0:
            p = []
            for item in to_insert:
                p.append((item, "", "", "", self.State_New))
            c.executemany(sql, p)
            self.conn.commit()

    def _url_not_exist(self, url):
        c = self.conn.cursor()
        c.execute('SELECT * FROM Page WHERE URL = ?', (url, ))
        return c.fetchone() is None

    def _has_seeked(self, page_id):
        c = self.conn.cursor()
        c.execute('UPDATE Page SET State = ? WHERE PageID = ?',
                  (self.State_Seeked, page_id))
        self.conn.commit()

    def _seek(self):
        c = self.conn.cursor()
        para = (self.State_New, )
        c.execute("SELECT * FROM Page WHERE State = ? LIMIT 1", para)
        row = c.fetchone()
        if row is not None:
            page_url = row[1]
            print "fetch", page_url
            html = urllib2.urlopen(page_url.encode("UTF-8")).read()
            urls = util.fetch_all_urls(html)
            self._insert_url(urls)
            self._has_seeked(row[0])
        else:
            raise Exception("no url to seek")

    def run(self):
        while True:
            self._seek()
