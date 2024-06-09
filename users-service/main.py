from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import redis

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

redis_client = redis.StrictRedis(host='redis', port=6379, db=0)


class FavoriteRepository(BaseModel):
    user_id: str
    repo_id: int
    repo_name: str


@app.post("/favorites/")
def save_favorite_repository(favorite: FavoriteRepository):
    key = f"user:{favorite.user_id}:favorites"
    redis_client.sadd(key, favorite.repo_name)
    return {"message": "Repository saved as favorite"}


@app.get("/favorites/{user_id}")
def get_favorite_repositories(user_id: str):
    key = f"user:{user_id}:favorites"
    return redis_client.smembers(key)


@app.delete("/favorites/{user_id}/{repo_name}")
def delete_favorite_repository(user_id: str, repo_name: str):
    key = f"user:{user_id}:favorites"
    if redis_client.sismember(key, repo_name):
        redis_client.srem(key, repo_name)
        return {"message": "Repository removed from favorites"}
    else:
        raise HTTPException(status_code=404, detail="Repository not found in favorites")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
