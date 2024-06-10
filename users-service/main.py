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
    repo_id: str
    repo_name: str


@app.post("/favorites/")
def save_favorite_repository(favorite: FavoriteRepository):
    set_key = f"user:{favorite.user_id}:favorites_set"
    hash_key = f"user:{favorite.user_id}:favorites_hash"
    redis_client.sadd(set_key, favorite.repo_id)
    redis_client.hset(hash_key, mapping={favorite.repo_id: favorite.repo_name})
    return {"message": "Repository saved as favorite"}


@app.get("/favorites/{user_id}")
def get_favorite_repositories(user_id: str):
    set_key = f"user:{user_id}:favorites_set"
    hash_key = f"user:{user_id}:favorites_hash"
    repo_ids = redis_client.smembers(set_key)
    return [{"id": repo_id, "name": redis_client.hget(hash_key, repo_id)} for repo_id in repo_ids]


@app.delete("/favorites/{user_id}/{repo_id}")
def delete_favorite_repository(user_id: str, repo_id: str):
    set_key = f"user:{user_id}:favorites_set"
    hash_key = f"user:{user_id}:favorites_hash"
    if redis_client.sismember(set_key, repo_id):
        redis_client.srem(set_key, repo_id)
        redis_client.hdel(hash_key, repo_id)
        return {"message": "Repository removed from favorites"}
    else:
        raise HTTPException(status_code=404, detail="Repository not found in favorites")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
