# -*- coding: utf-8 -*-

import sqlite3


class Downloader:
    def __init__(self):
        self.conn = sqlite3.connect("spider.db")
        c = self.conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS File
                     (FileID INTEGER PRIMARY KEY AUTOINCREMENT,
                     PageID INTEGER, AddTime TEXT, DownloadTime TEXT,
                     Size INTEGER, State INTEGER)''')
        self.conn.commit()

