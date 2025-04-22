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


def crawl(url:str, domain:str, visited_links:set[str], max_depth:int, depth:int = 0) -> None:
    """
    Crawls a domain, collecting all internal links found in the visited_links set.
    Skips edge cases such as mailto:, phone numbers, and JavaScript links.
    """
    url = urldefrag(url)[0]
    if url in visited_links or depth > max_depth:
        return
    
    visited_links.add(url)
    print(f"--> Depth: {depth} : Crawling: {url}")
    try:
        response = requests.get(url, timeout=7)
        tree = html.fromstring(response.text)
        tree.make_links_absolute(url)
        links = tree.xpath("//a[@href]")
        
        for link in links:
            href = link.get("href")

            print(f"--> Depth: {depth} : Parsing: {href}")
            parsed_href = urlparse(href)

            # Ensure same domain. Filter out other domains.
            if parsed_href.netloc and parsed_href.netloc != domain:
                continue

            # Filter out links without netloc. Such as mailto, phonenumber, javascript:
            if not parsed_href.netloc:
                continue
            
            crawl(url=href, domain=domain, visited_links=visited_links, max_depth=max_depth, depth=depth+1)

    except Exception as e:
        print(f"Error crawling {url}: {e}")



@app.get("/pages", response_model=ResponseDTO)
def get_pages(
    target: str = Query(..., description="Enter start URL"),
    max_depth: int = Query(5, description="Optional crawl depth limit")
    ) -> ResponseDTO:
    """
    GET /pages?target=<url>&max_depth=<int>

    Crawls a domain, returning all internal links found.
    Writes the results to a timestamped JSON file.
    """ 
    domain = urlparse(target).netloc
    visited_links = set()

    crawl(url=target, domain=domain, visited_links=visited_links, max_depth=max_depth)
    response = ResponseDTO(domain=target, pages=sorted(visited_links))

    # Write response to Json file marked named after domain + timestamp 
    try: 
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"crawled_{domain}_{timestamp}.json"

        with open(filename, "w", encoding="utf-8") as f:
            f.write(response.model_dump_json(indent=2))
    except Exception as e:
        print(f"Error writing to Json file: {e}")

    return response