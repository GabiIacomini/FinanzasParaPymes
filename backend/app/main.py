from fastapi import FastAPI

app = FastAPI(title="Financial Planner API")


@app.get("/api/health")
def read_root():
    return {"status": "ok"}
