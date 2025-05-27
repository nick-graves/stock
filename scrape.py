from duckduckgo_search import DDGS
import requests
from bs4 import BeautifulSoup

def get_top_urls(query, max_results=5):
    urls = []
    with DDGS() as ddgs:
        for result in ddgs.text(query):
            if "href" in result:
                urls.append(result["href"])
            elif "url" in result:
                urls.append(result["url"])
            if len(urls) >= max_results:
                break
    return urls

def extract_text_from_url(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        # Remove scripts, styles, etc.
        for tag in soup(["script", "style", "noscript", "footer", "header"]):
            tag.decompose()

        text = soup.get_text(separator="\n", strip=True)
        return text
    except Exception as e:
        return f"[Failed to extract from {url}]: {e}"

def get_combined_web_text(query, max_sites=5):
    print(f"\nSearching for: {query}")
    urls = get_top_urls(query, max_sites)
    all_text = ""
    for url in urls:
        print(f"Scraping: {url}")
        page_text = extract_text_from_url(url)
        all_text += f"\n--- {url} ---\n" + page_text + "\n\n"
    return all_text


'''
# Example usage
if __name__ == "__main__":
    combined = get_combined_web_text("VanEck Uranium and Nuclear ETF summary")
    print(combined[:10000])

'''