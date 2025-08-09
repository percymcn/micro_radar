from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from .schemas import ScanResult, Trend, DeployRequest
from .tasks import scan_sources, validate_trends, build_mvp, launch_marketing
from .config import settings

app = FastAPI(title="Micro-Market Radar")

static_root = Path(settings.STORAGE_DIR)/"sites"
static_root.mkdir(parents=True, exist_ok=True)
app.mount("/", StaticFiles(directory=static_root, html=True), name="sites")

@app.get("/healthz")
def healthz():
    return {"ok": True}

@app.post("/scan", response_model=ScanResult)
def api_scan():
    blobs = scan_sources.apply().get()
    validated = validate_trends.apply(args=[blobs]).get()
    return ScanResult(items=[Trend(**v) for v in validated])

@app.post("/deploy")
def api_deploy(req: DeployRequest):
    t = req.trend.model_dump()
    meta = build_mvp.apply(args=[t]).get()
    launched = launch_marketing.apply(args=[t, meta]).get()
    return {"deployed": True, "meta": meta, "launched": launched}

@app.post("/run_cycle")
def api_run_cycle():
    blobs = scan_sources.apply().get()
    validated = validate_trends.apply(args=[blobs]).get()
    results=[]
    for v in validated:
        meta = build_mvp.apply(args=[v]).get()
        launched = launch_marketing.apply(args=[v, meta]).get()
        results.append({"trend": v["trend"], "url": launched["url"]})
    return JSONResponse(results)
