import requests
from bs4 import BeautifulSoup
import sqlite3

from WebPageParser import WebPageParser

url = "https://www.mozilla.org/en-US/firefox/releases/"

conn = sqlite3.connect("firefox_releases.db")

cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS vuln (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        version TEXT,
        vul TEXT,
        link TEXT
    )
""")

query = "SELECT version, link  FROM releases limit 2;"

cursor.execute(query)

records = cursor.fetchall()

for record in records:
    version, link = record
    print(f"Processing record: ID={version}, Name={link}")
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
        print(datem)
        cursor.executemany("INSERT INTO vuln (version, vul, link) VALUES (?, ?, ?)", datem)

        print("CVE IDs:", cve_ids)

    data = []

conn.commit()
cursor.close()
conn.close()
