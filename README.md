# Web Crawler

Crawls a domain, collecting all internal links and writes them to a timestamped json file.
Skips edge cases such as mailto:, phone numbers, and JavaScript links.
Has an optional max_depth parameter to limit crawl depth (default set to 5).

# Tech stack:
* Python 3.12
* FastAPI
* Uvicorn
* Pydantic
* lxml
* Requests

# Installation
1. Clone repo
2. Install requirements from requirements.txt
3. Start API with: uvicorn main:app
4. Example endpoint: /pages?target=https://example.com&max_depth=3
5. Or navigate to http://localhost:port/docs for Swagger UI
6. Result will be written to disc as json file: crawled_domain_timestamp.json


Example output:
{
  domain: "https://example.com",
  pages: [
    "https://example.com/",
    "https://example.com/contact.html"
  ]
}
