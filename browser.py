from playwright.sync_api import sync_playwright

USER_AGENT = (
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
    'AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/91.0.4472.124 Safari/537.36'
)

class Playwright:
    def __init__(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=True)

    def close_browser(self):
        self.browser.close()
        self.playwright.stop()

    def create_page_with_context(self):
        context = self.browser.new_context()
        context.set_extra_http_headers({'User-Agent': USER_AGENT})
        return context.new_page()
