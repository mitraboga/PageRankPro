import json
import logging

from pagerankpro.observability import JsonFormatter, init_error_monitoring


def test_json_formatter_outputs_machine_readable_log() -> None:
    record = logging.LogRecord(
        name="pagerankpro.test",
        level=logging.INFO,
        pathname=__file__,
        lineno=10,
        msg="example_event",
        args=(),
        exc_info=None,
    )
    record.service = "test-service"

    payload = json.loads(JsonFormatter().format(record))

    assert payload["level"] == "INFO"
    assert payload["message"] == "example_event"
    assert payload["service"] == "test-service"
    assert "timestamp" in payload


def test_error_monitoring_is_disabled_without_dsn(monkeypatch) -> None:
    monkeypatch.delenv("SENTRY_DSN", raising=False)

    assert init_error_monitoring() is False
