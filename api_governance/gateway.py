from typing import Dict, Optional
import logging
from fastapi import FastAPI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/health")
def health_check() -> Dict:
    return {"status": "ok"}

if __name__ == "__main__":
    app.run()