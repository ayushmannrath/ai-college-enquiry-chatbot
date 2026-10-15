"""Run on your own machine to auto-capture screenshots into ../screenshots.
1) pip install -r requirements.txt && playwright install chromium
2) streamlit run app.py        (leave running)
3) python capture_screenshots.py"""
import os
from playwright.sync_api import sync_playwright

OUT = os.path.join(os.path.dirname(__file__), "..", "screenshots")
os.makedirs(OUT, exist_ok=True)
QUERIES = ["What courses do you offer?", "How do I apply for admission?",
           "What are the fees?", "Do you provide scholarships?", "xyzabc random nonsense"]
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1400, "height": 900})
    pg.goto("http://localhost:8501"); pg.wait_for_selector("input")
    pg.screenshot(path=f"{OUT}/01_home.png")
    for i, q in enumerate(QUERIES, 2):
        box = pg.get_by_label("Type your question:")
        box.fill(q); pg.get_by_role("button", name="Send").click()
        pg.wait_for_timeout(1500)
        pg.screenshot(path=f"{OUT}/{i:02d}_query.png", full_page=True)
    b.close()
print("Saved to", os.path.abspath(OUT))
