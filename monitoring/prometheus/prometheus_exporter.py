from http.server import (
    BaseHTTPRequestHandler,
    HTTPServer
)

from monitoring.metrics.metrics_collector import (
    metrics_collector
)

from shared.logging.logger import app_logger


# -----------------------------------
# Prometheus Metrics Handler
# -----------------------------------

class MetricsHandler(

    BaseHTTPRequestHandler
):

    def do_GET(self):

        if self.path != "/metrics":

            self.send_response(404)

            self.end_headers()

            return

        metrics = (

            metrics_collector
            .get_all_metrics()
        )

        response = ""

        for key, value in metrics.items():

            response += (

                f"{key} {value}\n"
            )

        self.send_response(200)

        self.send_header(

            "Content-Type",

            "text/plain"
        )

        self.end_headers()

        self.wfile.write(

            response.encode()
        )


# -----------------------------------
# Exporter Startup
# -----------------------------------

def start_exporter():

    server = HTTPServer(

        ("0.0.0.0", 8000),

        MetricsHandler
    )

    app_logger.info(

        "Prometheus Exporter Started "
        "on Port 8000"
    )

    server.serve_forever()


# -----------------------------------
# Main
# -----------------------------------

if __name__ == "__main__":

    start_exporter()