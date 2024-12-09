import requests
from bs4 import BeautifulSoup
import sqlite3
import time

SQLITE_FIREFOX_DB = "firefox_releases.db"
attempts = 0
MAX_ATTEMPTS = 3
SLEEP_DURATION = 5

data = []

conn = None
cursor = None
records = None
try:
    conn = sqlite3.connect(SQLITE_FIREFOX_DB)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS releases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            version TEXT,
            link TEXT,
            release_link TEXT
        )
    """)

    cursor.executemany("INSERT INTO releases (version, link) VALUES (?, ?)", data)

    conn.commit()
    conn.close()

    conn = sqlite3.connect(SQLITE_FIREFOX_DB)

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vuln (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            version TEXT,
            vul TEXT,
            link TEXT
        )
    """)

    query = "SELECT version, link  FROM releases limit 20;"
    cursor.execute(query)
    records = cursor.fetchall()
except:
    print("Failed to connect to DB.")
    exit(1)

for record in records:
    version, link = record
    response = requests.get(link)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    anchors = soup.find_all('a', string=lambda text: text and 'security' in text.lower())
    for anchor in anchors:
        response = requests.get(anchor['href'])
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        cve_ids = []
        datem = []
        download_link = "https://ftp.mozilla.org/pub/firefox/releases/" + version + "/linux-x86_64/en-US/firefox-" + version + ".tar.bz2"
        for link in soup.find_all("a"):
            if "CVE-" in link.text:
                cve_ids.append(link.text)
        res = ' '.join(cve_ids)

        datem.append((version, res, download_link))
        cursor.executemany("INSERT INTO vuln (version, vul, link) VALUES (?, ?, ?)", datem)

        print("Version:", version, "\nCVE IDs:", cve_ids, "\nDownload: " + download_link)

    data = []

conn.commit()
cursor.close()
conn.close()