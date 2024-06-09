from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI()

# Configure CORS
origins = [
    "http://localhost:3000",  # Add the origin of your frontend here
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GITHUB_API_URL = "https://api.github.com/search/repositories"


@app.get("/top-repositories/")
async def get_top_repositories():
    params = {
        "q": "stars:>1",
        "sort": "stars",
        "order": "desc"
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(GITHUB_API_URL, params=params)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Error fetching data from GitHub")

        response_items: list[dict[str, Any]] = []
        for item in response.json()["items"]:
            response_item = {
                "name": item["name"],
                "stargazers_count": item["stargazers_count"],
                "id": item["id"],
                "url": item["url"]}
            response_items.append(response_item)

        return response_items


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=80)
