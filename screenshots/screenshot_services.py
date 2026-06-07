#!/usr/bin/env python3
"""Screenshot BeautyByYulis services page at multiple viewports."""
import asyncio
import os
from datetime import datetime
from playwright.async_api import async_playwright

VIEWPORTS = [
    (375, 812, "375x812"),
    (414, 896, "414x896"),
    (768, 1024, "768x1024"),
    (1440, 900, "1440x900"),
    (1920, 1080, "1920x1080"),
]

BASE_URL = "https://www.beautybyyulis.com"
PAGES = [
    ("/services/", "services-en"),
    ("/es/services/", "services-es"),
]

OUTPUT_DIR = os.path.expanduser("~/clients/beautybyyulis/website/screenshots/2026-06-07")

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        for page_slug, url_suffix in PAGES:
            for width, height, viewport_name in VIEWPORTS:
                page = await browser.new_page()
                await page.set_viewport_size({"width": width, "height": height})
                try:
                    await page.goto(f"{BASE_URL}{url_suffix}", wait_until="networkidle", timeout=15000)
                    await page.wait_for_timeout(2000)
                    vp_dir = os.path.join(OUTPUT_DIR, viewport_name)
                    os.makedirs(vp_dir, exist_ok=True)
                    filename = f"{page_slug}-{datetime.now().strftime('%H%M')}.png"
                    filepath = os.path.join(vp_dir, filename)
                    await page.screenshot(path=filepath, full_page=True)
                    print(f"OK {viewport_name} - {page_slug} -> {filepath}")
                except Exception as e:
                    print(f"ERR {viewport_name} - {page_slug} -> {e}")
                finally:
                    await page.close()
        await browser.close()

asyncio.run(main())
