from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from .config import settings

env = Environment(loader=FileSystemLoader((Path(__file__).parent / "templates")))

def build_static_landing(slug: str, title: str, checkout_url: str|None) -> str:
    out_dir = Path(settings.STORAGE_DIR)/"sites"/slug
    out_dir.mkdir(parents=True, exist_ok=True)
    html = env.get_template("landing.html.j2").render(
        title=title,
        checkout_url=checkout_url or settings.STRIPE_CHECKOUT_LINK
    )
    (out_dir/"index.html").write_text(html, encoding="utf-8")
    return str(out_dir)
