import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs, urlencode
import argparse
import random

def crawl_and_find_get_params(url):
    """
    Crawl the given URL and extract all GET parameters from the links on the page.
    """
    try:
        # Fetch the content of the page
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Set to store unique URLs with GET parameters
        urls_with_get_params = set()

        # Iterate over all <a> tags
        for a_tag in soup.find_all("a", href=True):
            href = a_tag['href']
            # Combine relative links with the base URL
            full_url = urljoin(url, href)
            parsed_url = urlparse(full_url)
            # Check if the URL contains GET parameters
            if parsed_url.query:
                urls_with_get_params.add(full_url)

        return urls_with_get_params
    except Exception as e:
        print(f"Error crawling the page: {e}")
        return set()

def extract_get_params(urls):
    """
    Extract and display GET parameters from a list of URLs.
    """
    for url in urls:
        parsed_url = urlparse(url)
        params = parse_qs(parsed_url.query)
        print(f"URL: {url}")
        for param, values in params.items():
            print(f"  - Parameter: {param}, Value(s): {values}")

def test_reflections(urls):
    """
    Test if GET parameters in the URL are reflected in the page.
    """
    for url in urls:
        parsed_url = urlparse(url)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
        params = parse_qs(parsed_url.query)

        if not params:
            print(f"No GET parameters found in: {url}")
            return

        for param, values in params.items():
            unique_value = f"test_{param}_{random.randint(1000, 9999)}"
            test_params = {key: (unique_value if key == param else value[0]) for key, value in params.items()}
            test_url = f"{base_url}?{urlencode(test_params)}"
            
            try:
                response = requests.get(test_url)
                if unique_value in response.text:
                    print(f"[!] Parameter '{param}' is reflected on the page.")
                    print(f"Tested URL: {test_url}")
                else:
                    print(f"[ ] Parameter '{param}' is not reflected.")
            except Exception as e:
                print(f"Error testing {test_url}: {e}")


def main():
    parser = argparse.ArgumentParser(description="A script for finding potential parameters to XSS.")
    parser.add_argument("--reflected", action="store_true", help="Enable reflection test.")
    args = parser.parse_args()

    target_url = input("Enter target URL: ")
    print(f"Crawling {target_url} for GET parameters...")

    urls_with_params = crawl_and_find_get_params(target_url)
    if urls_with_params:
        if args.reflected:
            print("\nFound URLs with GET parameters that are reflected:")
            test_reflections(urls_with_params)
        else:
            print("\nFound URLs with GET parameters:")
            extract_get_params(urls_with_params)
       
    else:
        print("No GET parameters found.")

if __name__ == "__main__":
    main()
