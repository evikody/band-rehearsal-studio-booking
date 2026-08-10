from fastapi import FastAPI

from app.api.routes import studio

app = FastAPI(title="Rehearsal Studio Booking API")

app.include_router(studio.router)


@app.get("/health")
def health():
    return {"status": "ok"}
