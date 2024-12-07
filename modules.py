import queue
import threading
from handler import get_author_gs 
from playwright.sync_api import sync_playwright
from author import Author

class QueueProcessor:
    def __init__(self):
        self.queue = queue.Queue()
        self.shutdown_event = threading.Event()
        self.worker_thread = threading.Thread(
            target=self.process_queue, daemon=True
        )
        self.worker_thread.start()

    def add(self, items):
        for item in items:
            self.queue.put(item)

    def process_queue(self):
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            context = browser.new_context()
            context.set_extra_http_headers({'User-Agent': USER_AGENT})
            page = context.new_page()

            while not self.shutdown_event.is_set():
                try:
                    next_author = self.queue.get(timeout=1)
                    if next_author is not None:
                        author = Author()
                        get_author_gs(next_author, author,  page)
                        # TODO : Pass the author data to AI
                        # TODO : REST API - DB
                        print(author.as_obj())
                    self.queue.task_done()
                except queue.Empty:
                    continue

            browser.close()

    def shutdown(self):
        self.shutdown_event.set()
        self.worker_thread.join()

USER_AGENT = (
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
    'AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/91.0.4472.124 Safari/537.36'
)

