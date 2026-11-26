"""Screenshot a URL at 1440 and 390, report overflow, console errors and failed requests.
Usage: python shoot.py <url> <out_prefix>
"""
import sys
from playwright.sync_api import sync_playwright

url, out = sys.argv[1], sys.argv[2]
with sync_playwright() as p:
    b = p.chromium.launch(args=["--mute-audio"])
    for w, h in [(1440, 900), (390, 844)]:
        ctx = b.new_context(viewport={"width": w, "height": h}, device_scale_factor=1)
        pg = ctx.new_page()
        errs, fails = [], []
        pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.on("requestfailed", lambda r: fails.append(r.url))
        pg.on("response", lambda r: fails.append(f"{r.status} {r.url}") if r.status >= 400 else None)
        pg.goto(url, wait_until="networkidle")
        pg.wait_for_timeout(3200)
        ov = pg.evaluate("""() => {
          const W = document.documentElement.clientWidth;
          const bad = [...document.querySelectorAll('body *')].filter(e => {const r = e.getBoundingClientRect(); return r.right > W + 1 && r.width > 0;}).slice(0, 8).map(e => e.tagName + '.' + e.className);
          return {scrollW: document.documentElement.scrollWidth, W, bad};
        }""")
        pg.screenshot(path=f"{out}_{w}.png")
        pg.screenshot(path=f"{out}_{w}_full.png", full_page=True)
        print(w, "overflow:", ov, "console errors:", errs, "failed:", fails)
        ctx.close()
    b.close()
