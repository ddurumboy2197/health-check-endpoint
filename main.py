from fastapi import FastAPI, Response
from pydantic import BaseModel
import uvicorn
import redis
from sqlalchemy import create_engine

app = FastAPI()

# Redis uchun kloning
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# Database uchun kloning
engine = create_engine('sqlite:///database.db')

class HealthCheck(BaseModel):
    status: str

@app.get("/health-check")
async def health_check():
    try:
        # Redis status
        redis_status = redis_client.ping()
        if redis_status:
            redis_status = "Redis is working"
        else:
            redis_status = "Redis is not working"
        
        # Database status
        engine.execute("SELECT 1")
        database_status = "Database is working"
        
        return HealthCheck(status=f"Redis: {redis_status}, Database: {database_status}")
    except Exception as e:
        return HealthCheck(status=f"Error: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

Kodni ishga tushirish uchun quyidagilarni amalga oshiring:

1. `redis` va `sqlalchemy` kutubxonalarni o'rnatib oling.
2. `sqlite:///database.db` deb atalgan SQLite bazasini yaratib oling.
3. `localhost` hostga `6379` portda Redis serverni ishga tushiring.
4. Kodni `main.py` deb nomlangan faylga saqlab oling.
5. `uvicorn` ni ishga tushiring: `uvicorn main:app --host 0.0.0.0 --port 8000`
