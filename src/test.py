RELEASE_PAGE_HTML = """
<ol class="c-release-list">
    <li>
        <strong>
            <a href="/releases/123">Firefox 123</a>
        </strong>
        <ol>
            <li><a href="/releases/123.1">Firefox 123.1</a></li>
        </ol>
    </li>
</ol>
"""

SECURITY_PAGE_HTML = """
<a href="https://example.com/CVE-1234">CVE-1234</a>
<a href="https://example.com/CVE-5678">CVE-5678</a>
"""

@responses.activate
def test_release_data_extraction():
    url = "https://www.mozilla.org/en-US/firefox/releases/"
    responses.add(responses.GET, url, body=RELEASE_PAGE_HTML, status=200)

    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    data = []
    for release in soup.select("ol.c-release-list > li"):
        main_version = release.find("strong").text.strip()
        main_link = "https://www.mozilla.org" + \
            release.find("strong").find("a")["href"].strip()
        data.append((main_version, main_link))

        for sub_release in release.select("ol > li > a"):
            sub_version = sub_release.text.strip()
            sub_link = "https://www.mozilla.org" + sub_release["href"].strip()
            data.append((sub_version, sub_link))

    assert len(data) == 2
    assert data[0] == ("Firefox 123", "https://www.mozilla.org/releases/123")
    assert data[1] == (
        "Firefox 123.1", "https://www.mozilla.org/releases/123.1")


def test_database_insertion(setup_in_memory_db):
    conn = setup_in_memory_db
    cursor = conn.cursor()

    data = [("Firefox 123", "https://www.mozilla.org/releases/123")]
    cursor.executemany(
        "INSERT INTO releases (version, link) VALUES (?, ?)", data)
    conn.commit()

    cursor.execute("SELECT version, link FROM releases")
    records = cursor.fetchall()
    assert len(records) == 1
    assert records[0] == (
        "Firefox 123", "https://www.mozilla.org/releases/123")


@responses.activate
def test_cve_extraction():
    url = "https://example.com/security"
    responses.add(responses.GET, url, body=SECURITY_PAGE_HTML, status=200)

    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    cve_ids = [link.text for link in soup.find_all("a") if "CVE-" in link.text]

    assert len(cve_ids) == 2
    assert cve_ids == ["CVE-1234", "CVE-5678"]

def test_invalid_url():
    with pytest.raises(requests.exceptions.RequestException):
        requests.get("https://invalid-url.example")

@responses.activate
def test_empty_response():
    responses.add(responses.GET, "https://www.mozilla.org/en-US/firefox/releases/", body="", status=200)

    response = requests.get("https://www.mozilla.org/en-US/firefox/releases/")
    assert response.text == ""

def test_sql_injection(setup_in_memory_db):
    conn = setup_in_memory_db
    cursor = conn.cursor()

    malicious_input = ("'; DROP TABLE releases;--", "https://example.com")
    cursor.execute("INSERT INTO releases (version, link) VALUES (?, ?)", malicious_input)
    conn.commit()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='releases'")
    assert cursor.fetchone() is not None