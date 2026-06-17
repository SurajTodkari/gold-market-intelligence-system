from playwright.sync_api import sync_playwright

from shared.logging.logger import app_logger

from shared.resilience.retry import resilient_retry


@resilient_retry()
def open_calendar(page):

    response = page.goto(

        "https://www.forexfactory.com/calendar",

        wait_until="networkidle",

        timeout=60000
    )

    app_logger.info(

        f"Response Status: "
        f"{response.status if response else 'None'}"
    )


def run():

    with sync_playwright() as p:

        browser = p.chromium.launch(

            headless=False,

            args=[
                "--disable-blink-features=AutomationControlled"
            ]
        )

        context = browser.new_context(

            viewport={
                "width": 1920,
                "height": 1080
            },

            user_agent=(
                "Mozilla/5.0 "
                "(Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/136.0.0.0 "
                "Safari/537.36"
            )
        )

        page = context.new_page()

        open_calendar(page)

        page.wait_for_timeout(10000)

        app_logger.info(
            f"Current URL: {page.url}"
        )

        app_logger.info(
            f"Page Title: {page.title()}"
        )

        rows = page.query_selector_all("tr")

        app_logger.info(
            f"TR Count: {len(rows)}"
        )

        page.screenshot(

            path="forexfactory_debug.png",

            full_page=True
        )

        with open(

            "forexfactory_debug.html",

            "w",

            encoding="utf-8"

        ) as f:

            f.write(page.content())

        app_logger.info(
            "Debug artifacts generated"
        )

        input(
            "Press ENTER to close browser..."
        )

        browser.close()


if __name__ == "__main__":

    run()