import celery
from .config import settings
from .scrapers import producthunt, reddit, tiktok_roundups, etsy, ebay
from . import pipeline, mvp_builder, marketing

celery_app = celery.Celery("micro_radar", broker=settings.REDIS_URL, backend=settings.REDIS_URL)

@celery_app.task
def scan_sources() -> list[dict]:
    blobs=[]
    for mod in (producthunt, reddit, tiktok_roundups, etsy, ebay):
        try:
            blobs += mod.fetch()
        except Exception as e:
            print("scan error", getattr(mod, "__name__", "mod"), e)
    return blobs

@celery_app.task
def validate_trends(blobs: list[dict]):
    candidates = pipeline.heuristics(blobs)
    val = pipeline.validate_with_google_trends(candidates)
    return [c.model_dump() for c in val]

@celery_app.task
def build_mvp(t: dict):
    slug = t["trend"].lower().replace(" ","-")[:50]
    site_dir = mvp_builder.build_static_landing(slug, t["trend"], t.get("meta",{}).get("checkout_url"))
    return {"slug": slug, "dir": site_dir}

@celery_app.task
def launch_marketing(t: dict, deploy_meta: dict):
    url = f"{settings.LANDING_HOST}/{deploy_meta['slug']}/"
    marketing.post_to_x(f"Launching: {t['trend']} — {url}")
    marketing.post_to_telegram(f"Launching: {t['trend']} — {url}")
    return {"url": url}
