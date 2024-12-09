import requests
from bs4 import BeautifulSoup


class WebPageParser:
    def __init__(self, url):
        self.url = url
        self.response = None
        self.soup = None

    def fetch_page(self):
        """
        Fetch the webpage content and store the response.
        """
        try:
            self.response = requests.get(self.url)
            self.response.raise_for_status()
            return self.response.text
        except requests.exceptions.RequestException as e:
            print(f"Error fetching the page: {e}")
            return None

    def parse_page(self):
        """
        Parse the fetched webpage using BeautifulSoup.
        """
        if self.response is None:
            return None
        self.soup = BeautifulSoup(self.response.content, 'html.parser')
        return self.soup

    def find_links_by_keyword(self, keyword):
        """
        Find all links containing a specific keyword in the anchor text.
        """
        if self.soup is None:
            return []

        anchors = self.soup.find_all('a', string=lambda text: text and keyword.lower() in text.lower())
        return [anchor['href'] for anchor in anchors if 'href' in anchor.attrs]

    def get_page_title(self):
        """
        Get the title of the page.
        """
        if self.soup is None:
            return None
        title = self.soup.title
        return title.get_text() if title else 'No title found'

    def get_response(self):
        """
        Return the response object (can be useful for status codes, headers, etc.).
        """
        return self.response


url = 'https://example.com'
parser = WebPageParser(url)

parser.fetch_page()
parser.parse_page()

links = parser.find_links_by_keyword('security')
print("Links containing 'security':", links)

title = parser.get_page_title()
print("Page title:", title)
