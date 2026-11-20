import threading
import unittest
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from playwright.sync_api import (
    Browser,
    BrowserContext,
    Page,
    Playwright,
    expect,
    sync_playwright,
)

BUILD = Path(__file__).resolve().parents[1] / "build"


class BrowserTest(unittest.TestCase):
    server: ThreadingHTTPServer
    thread: threading.Thread
    playwright: Playwright
    browser: Browser
    context: BrowserContext
    page: Page

    @classmethod
    def setUpClass(cls) -> None:
        if not (BUILD / "site/index.html").is_file():
            raise RuntimeError("Build the site before running browser tests.")
        # Serve from a subdirectory to match a GitHub project Pages URL.
        cls.server = ThreadingHTTPServer(
            ("127.0.0.1", 0), partial(SimpleHTTPRequestHandler, directory=BUILD)
        )
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.addClassCleanup(cls.server.server_close)
        cls.addClassCleanup(cls.thread.join, 5)
        cls.addClassCleanup(cls.server.shutdown)
        cls.playwright = sync_playwright().start()
        cls.addClassCleanup(cls.playwright.stop)
        cls.browser = cls.playwright.chromium.launch()
        cls.addClassCleanup(cls.browser.close)

    def setUp(self) -> None:
        self.context = self.browser.new_context()
        self.addCleanup(self.context.close)
        self.page = self.context.new_page()
        self.base_url = f"http://127.0.0.1:{self.server.server_port}/site/"

    def test_steps_plays_and_applies_complex_bounds(self) -> None:
        self.page.goto(self.base_url)
        start = self.page.get_by_role("button", name="Start", exact=True)
        expect(start).to_be_enabled(timeout=45_000)
        step = self.page.get_by_role("button", name="Step", exact=True)
        dark = self.page.locator("#dark")
        count = self.page.locator("#iteration")
        plot = self.page.locator("#sky")
        initial = plot.evaluate("(canvas) => canvas.toDataURL()")
        step.click()
        expect(count).to_have_text("1")
        expect(dark).to_have_text("0")
        step.click()
        expect(count).to_have_text("2")
        expect(dark).not_to_have_text("0")
        self.assertNotEqual(plot.evaluate("(canvas) => canvas.toDataURL()"), initial)
        self.page.get_by_role("button", name="Resume").click()
        expect(count).not_to_have_text("2")
        self.page.get_by_role("button", name="Pause").click()

        minimum = self.page.get_by_label("Min real")
        minimum.fill("3")
        minimum.press("Tab")
        expect(self.page.get_by_role("alert")).to_contain_text("increasing")
        minimum.fill("-0.8")
        minimum.press("Tab")
        expect(start).to_be_enabled()
        expect(count).to_have_text("0")
        expect(self.page.get_by_role("alert")).to_be_hidden()
        self.page.set_viewport_size({"width": 390, "height": 844})
        self.assertTrue(
            self.page.evaluate("document.documentElement.scrollWidth <= innerWidth")
        )

    def test_runtime_failure_shows_retry(self) -> None:
        self.page.route("**/vendor/pyodide.js", lambda route: route.abort())
        self.page.goto(self.base_url)
        expect(self.page.get_by_role("alert")).to_contain_text("Python could not load")
        expect(
            self.page.get_by_role("button", name="Reload", exact=True)
        ).to_be_visible()
