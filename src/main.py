from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/api/v1/supply-chain/recommendations")
async def get_recommendations():
    pass


handler = Mangum(app)
