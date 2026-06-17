
from inspect import trace

from playwright.sync_api import sync_playwright
from datetime import datetime, UTC

from kafka import KafkaProducer

from monitoring.tracing.request_tracer import (
    create_trace,
    add_stage
)

from shared.logging.logger import app_logger
from shared.resilience.retry import resilient_retry

import json


# -----------------------------------
# Kafka Producer
# -----------------------------------

producer = KafkaProducer(

    bootstrap_servers="127.0.0.1:9092",

    value_serializer=lambda v:
    json.dumps(v, default=str).encode("utf-8"),

    retries=5,

    acks="all"
)

KAFKA_TOPIC = "topic.raw.ingestion"


# -----------------------------------
# Retry Protected Navigation
# -----------------------------------

@resilient_retry()
def open_calendar(page):

    response = page.goto(

        "https://www.forexfactory.com/calendar",

        wait_until="domcontentloaded",

        timeout=60000
    )

    app_logger.info(

        f"Response Status: "
        f"{response.status if response else 'None'}"
    )


# -----------------------------------
# Main Scraper
# -----------------------------------

def run_scraper():

    try:

        app_logger.info(
            "Starting Forex Factory scraper..."
        )

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

            page.wait_for_timeout(5000)

            app_logger.info(
                f"Current URL: {page.url}"
            )

            app_logger.info(
                f"Page Title: {page.title()}"
            )

            # -----------------------------------
            # Extract Events
            # -----------------------------------

            events = page.locator(
                "tr.calendar__row"
            ).all()

            app_logger.info(

                f"Total Event Rows Found: "
                f"{len(events)}"
            )

            published_count = 0

            for row in events:

                try:

                    event_id = row.get_attribute(
                        "data-event-id"
                    )

                    if not event_id:
                        continue

                    title = row.locator(
                        ".calendar__event-title"
                    ).inner_text().strip()

                    currency = row.locator(
                        ".calendar__currency"
                    ).inner_text().strip()

                    time_value = row.locator(
                        ".calendar__time"
                    ).inner_text().strip()

                    actual = row.locator(
                        ".calendar__actual"
                    ).inner_text().strip()

                    forecast = row.locator(
                        ".calendar__forecast"
                    ).inner_text().strip()

                    previous = row.locator(
                        ".calendar__previous"
                    ).inner_text().strip()

                    impact = "UNKNOWN"

                    try:

                        impact_class = row.locator(
                            ".calendar__impact span"
                        ).get_attribute("class")

                        if impact_class:

                            if "red" in impact_class:

                                impact = "HIGH"

                            elif "ora" in impact_class:

                                impact = "MEDIUM"

                            elif "yel" in impact_class:

                                impact = "LOW"

                    except Exception:

                        pass

                    trace = create_trace(
                         str(event_id)
                    )

                    add_stage(
                          trace,
                         "SCRAPER"
                    )

                    event_data = {

                      "trace": trace,

                      "source_event_id":
                       str(event_id),

                      "source":
                      "ForexFactory",

                      "event_name":
                       title,

                      "country":
                       currency,

                      "currency":
                       currency,

                      "impact":
                       impact,

                      "actual":
                       actual,

                      "forecast":
                       forecast,

                      "previous":
                       previous,

                      "source_event_date":
                       datetime.now(
                       UTC
                       ).strftime("%Y-%m-%d"),

                      "source_event_time":
                       time_value,

                      "published_at":
                       datetime.now(
                       UTC
                       ).isoformat(),

                      "ingested_at":
                       datetime.now(
                       UTC
                       ).isoformat()
                    }

                    producer.send(

                        KAFKA_TOPIC,

                        event_data
                    )

                    published_count += 1

                    app_logger.info(

                     f"Published Event | "
                     f"ID={event_id} | "
                     f"NAME={title} | "
                     f"ACTUAL={actual} | "
                     f"FORECAST={forecast} | "
                     f"PREVIOUS={previous}" 
                   )
                except Exception as e:

                    app_logger.error(

                        f"Failed To Process Event | "
                        f"{e}"
                    )

            producer.flush()

            app_logger.info(

                f"Published "
                f"{published_count} events"
            )

    except Exception as e:

        app_logger.error(

            f"Fatal Scraper Error: "
            f"{e}"
        )

    finally:

        app_logger.info(
            "Forex Factory scraper finished"
        )


if __name__ == "__main__":

    run_scraper()

