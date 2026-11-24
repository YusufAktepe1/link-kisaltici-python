"""Tıklayan ziyaretçinin cihaz, tarayıcı ve geldiği site bilgisini çıkarır."""
from urllib.parse import urlparse

from user_agents import parse

DIRECT = "Doğrudan"  # Referer bilgisi yoksa (link adres çubuğuna yazıldıysa, uygulamadan açıldıysa vb.)


def parse_user_agent(user_agent: str) -> tuple[str, str, str]:
    """User-Agent metninden (cihaz, tarayıcı, işletim sistemi) döndürür."""
    ua = parse(user_agent or "")

    if ua.is_bot:
        device = "Bot"
    elif ua.is_mobile:
        device = "Mobil"
    elif ua.is_tablet:
        device = "Tablet"
    elif ua.is_pc:
        device = "Masaüstü"
    else:
        device = "Bilinmiyor"

    browser = ua.browser.family if ua.browser.family != "Other" else "Bilinmiyor"
    os = ua.os.family if ua.os.family != "Other" else "Bilinmiyor"
    return device, browser, os


def parse_referrer(referrer: str | None) -> str:
    """'https://www.google.com/search?q=...' -> 'google.com'"""
    if not referrer:
        return DIRECT
    host = urlparse(referrer).netloc.lower()
    if host.startswith("www."):
        host = host[4:]
    return host or DIRECT
