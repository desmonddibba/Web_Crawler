from fastapi import FastAPI, Query
from pydantic import BaseModel
from lxml import html
from urllib.parse import urlparse, urldefrag
import requests
import datetime


app = FastAPI(title="Desmonds Crawler")


class ResponseDTO(BaseModel):
    domain: str
    pages: list[str]



def crawl(url, domain, visited_links):
    """
    Crawls a domain, collecting all internal links.
    Skips edge cases such as mailto: phonenumber and javascript links.
    Saves the collection of links in a json file named after domain with a timestamp.
    """
    
    url = urldefrag(url)[0]

    if url in visited_links:
        return
    visited_links.add(url)
    print(f"-> Crawling: {url}")

    try:
        response = requests.get(url, timeout=7)
        tree = html.fromstring(response.text)
        tree.make_links_absolute(url)
        links = tree.xpath("//a[@href]")
        
        for link in links:
            href = link.get("href")

            print(f"--> Parsing: {href}")
            parsed_href = urlparse(href)

            # Ensure same domain. Filter out other domains.
            if parsed_href.netloc and parsed_href.netloc != domain:
                continue

            # Filter out links without netloc. Such as mailto, phonenumber, javascript:
            if not parsed_href.netloc:
                continue
            
            crawl(href, domain, visited_links)
    except Exception as e:
        print(f"Error crawling {url}: {e}")






@app.get("/pages", response_model=ResponseDTO)
def get_pages(target: str = Query(..., description="Enter start URL")) -> ResponseDTO:
    domain = urlparse(target).netloc
    visited_links = set()

    crawl(url=target, domain=domain, visited_links=visited_links)
    response = ResponseDTO(domain=target, pages=sorted(visited_links))

    try: 
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"crawled_{domain}_{timestamp}.json"

        with open(filename, "w", encoding="utf-8") as f:
            f.write(response.model_dump_json(indent=2))

    except Exception as e:
        print(f"Error writing to Json file: {e}")

    return response