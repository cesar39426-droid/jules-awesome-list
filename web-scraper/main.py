import requests
from bs4 import BeautifulSoup

def main():
    """
    Main function to scrape a website and print its title.
    """
    url = "http://example.com/"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes
        soup = BeautifulSoup(response.content, "html.parser")

        if soup.title:
            print(f"The title of the page is: {soup.title.string}")
        else:
            print("The page has no title.")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()