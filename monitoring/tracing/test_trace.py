from monitoring.tracing.request_tracer import (
    create_trace,
    add_stage
)

from monitoring.tracing.trace_manager import (
    log_trace
)

trace = create_trace(
    "TEST-EVENT-001"
)

add_stage(
    trace,
    "SCRAPER"
)

add_stage(
    trace,
    "KAFKA"
)

add_stage(
    trace,
    "VALIDATION"
)

add_stage(
    trace,
    "PERSISTENCE"
)

log_trace(trace)