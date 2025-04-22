from fastapi import FastAPI


app = FastAPI(title="Desmonds Crawler")




@app.get("/pages")
def get_pages(target: str):
    pass