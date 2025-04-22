from fastapi import FastAPI, Query
from pydantic import BaseModel

app = FastAPI(title="Desmonds Crawler")


class ResponseDTO(BaseModel):
    domain: str
    pages: list[str]







@app.get("/pages", response_model=ResponseDTO)
def get_pages(target: str = Query(..., description="Enter start URL")) -> ResponseDTO:
    return ResponseDTO(domain=target, pages=[])