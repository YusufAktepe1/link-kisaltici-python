"""LinkKısaltıcı - FastAPI uygulaması."""
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, PlainTextResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app import database, tracking
from app.codes import generate_unique_code

templates = Jinja2Templates(directory=Path(__file__).parent / "templates")


def format_date(value: str) -> str:
    """'2026-11-25 14:30:00' -> '25.11.2026 14:30' (eski formattaki kayıtlar olduğu gibi gösterilir)"""
    try:
        return datetime.strptime(value, database.DATE_FORMAT).strftime("%d.%m.%Y %H:%M")
    except ValueError:
        return value


templates.env.filters["tarih"] = format_date


@asynccontextmanager
async def lifespan(app: FastAPI):
    database.init_db()  # uygulama açılırken tabloları oluştur
    yield


app = FastAPI(title="LinkKısaltıcı", lifespan=lifespan)


def is_valid_url(url: str) -> bool:
    parts = urlparse(url)
    return parts.scheme in ("http", "https") and bool(parts.netloc)


def render_home(request: Request, status_code: int = 200, **extra):
    context = {"links": database.recent_links(), **extra}
    return templates.TemplateResponse(request, "index.html", context, status_code=status_code)


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return render_home(request)


@app.post("/", response_class=HTMLResponse)
def shorten(request: Request, url: str = Form("")):
    url = url.strip()
    if not is_valid_url(url):
        return render_home(
            request,
            status_code=400,
            error="Geçerli bir link girin (https:// ile başlamalı).",
            url=url,
        )

    code = generate_unique_code()
    database.add_link(code, url)
    return render_home(request, short_url=f"{request.base_url}{code}", short_code=code)


@app.get("/stats/{code}", response_class=HTMLResponse)
def stats(request: Request, code: str):
    """Bir kısa linkin tıklama istatistikleri."""
    link = database.get_link(code)
    if link is None:
        return PlainTextResponse("Bu kısa link bulunamadı.", status_code=404)

    context = {
        "link": link,
        "short_url": f"{request.base_url}{code}",
        "stats": database.click_stats(link["id"]),
    }
    return templates.TemplateResponse(request, "stats.html", context)


@app.get("/{code}")
def follow(request: Request, code: str):
    """Kısa linke gelen ziyaretçiyi kaydeder ve asıl adrese yönlendirir."""
    device, browser, os = tracking.parse_user_agent(request.headers.get("user-agent", ""))
    referrer = tracking.parse_referrer(request.headers.get("referer"))

    url = database.register_click(code, device, browser, os, referrer)
    if url is None:
        return PlainTextResponse("Bu kısa link bulunamadı.", status_code=404)
    return RedirectResponse(url, status_code=302)
