from typing import Dict, Optional
import logging
from prometheus_client import start_http_server, Gauge
from fastapi import FastAPI, HTTPException
from fastapi.middleware.gzip import GZipMiddleware

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="API Monitor")
app.add_middleware(GZipMiddleware)

class APIEndpointMetrics:
    def __init__(self):
        self.endpoints: Dict[str, Dict] = {}
        
    def record_request(self, endpoint: str, status_code: int, duration: float) -> None:
        if endpoint not in self.endpoints:
            self.endpoints[endpoint] = {"success": 0, "failure": 0, "latency_sum": 0.0}
        self.endpoints[endpoint]["success" if status_code < 400 else "failure"] += 1
        self.endpoints[endpoint]["latency_sum"] += duration
        
    def get_metrics(self) -> Dict:
        return {
            endpoint: {
                "success_rate": success / (success + failure),
                "avg_latency": latency_sum / (success + failure)
            }
            for endpoint, metrics in self.endpoints.items()
            if (success := metrics["success"]) + (failure := metrics["failure"]) > 0
        }

metrics = APIEndpointMetrics()

@app.get("/metrics")
def get_metrics() -> Dict:
    try:
        return metrics.get_metrics()
    except Exception as e:
        logger.error(f"Error retrieving metrics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    start_http_server(8000)