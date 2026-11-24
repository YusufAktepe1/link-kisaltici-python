"""LinkKısaltıcı - FastAPI uygulaması."""
from contextlib import asynccontextmanager
from pathlib import Path
from urllib.parse import urlparse

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, PlainTextResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app import database
from app.codes import generate_unique_code

templates = Jinja2Templates(directory=Path(__file__).parent / "templates")


@asynccontextmanager
async def lifespan(app: FastAPI):
    database.init_db()  # uygulama açılırken tabloyu oluştur
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
    return render_home(request, short_url=f"{request.base_url}{code}")


@app.get("/{code}")
def follow(code: str):
    """Kısa linke gelen ziyaretçiyi asıl adrese yönlendirir."""
    url = database.register_click(code)
    if url is None:
        return PlainTextResponse("Bu kısa link bulunamadı.", status_code=404)
    return RedirectResponse(url, status_code=302)
