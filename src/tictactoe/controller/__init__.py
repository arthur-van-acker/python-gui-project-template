"""Controller scaffolding that documents telemetry/logging hooks."""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass, field
from typing import Any, Callable, Mapping, MutableMapping

TelemetryHook = Callable[["TelemetryEvent"], None]
ErrorHook = Callable[[Exception, "TelemetryEvent"], None]


@dataclass(frozen=True)
class TelemetryEvent:
    """Structured payload emitted by controller and UI surfaces."""

    channel: str
    action: str
    payload: Mapping[str, Any] = field(default_factory=dict)


@dataclass
class ControllerHooks:
    """Optional callbacks that capture controller telemetry."""

    view: TelemetryHook | None = None
    domain: TelemetryHook | None = None
    error: ErrorHook | None = None

    def emit(self, channel: str, action: str, **payload: Any) -> TelemetryEvent:
        """Trigger the hook registered for the supplied channel."""

        payload_dict: MutableMapping[str, Any] = dict(payload)
        event = TelemetryEvent(channel=channel, action=action, payload=payload_dict)
        hook = self._hook_for(channel)
        if not hook:
            return event
        try:
            hook(event)
        except Exception as exc:  # pragma: no cover - defensive guardrail
            self._handle_error(exc, event)
        return event

    def emit_error(self, exc: Exception, *, action: str, **payload: Any) -> TelemetryEvent:
        """Forward controller failures to the error hook (if any)."""

        payload_dict: MutableMapping[str, Any] = dict(payload)
        event = TelemetryEvent(channel="error", action=action, payload=payload_dict)
        if self.error:
            try:
                self.error(exc, event)
            except Exception:  # pragma: no cover - defensive guardrail
                logging.getLogger("tictactoe.controller").debug(
                    "Error hook raised while handling %s.%s",
                    event.channel,
                    event.action,
                    exc_info=True,
                )
            return event

        logging.getLogger("tictactoe.controller").debug(
            "Unhandled controller error during %s",
            action,
            exc_info=exc,
        )
        return event

    def _hook_for(self, channel: str) -> TelemetryHook | None:
        if channel == "view":
            return self.view
        if channel == "domain":
            return self.domain
        return None

    def _handle_error(self, exc: Exception, event: TelemetryEvent) -> None:
        if self.error:
            try:
                self.error(exc, event)
            except Exception:  # pragma: no cover - defensive guardrail
                logging.getLogger("tictactoe.controller").debug(
                    "Controller error hook raised while handling %s.%s",
                    event.channel,
                    event.action,
                    exc_info=True,
                )
            return

        logging.getLogger("tictactoe.controller").debug(
            "Controller hook raised during %s.%s",
            event.channel,
            event.action,
            exc_info=exc,
        )


def logging_hooks(
    logger: logging.Logger | None = None,
    *,
    level: int = logging.INFO,
) -> ControllerHooks:
    """Return hooks that emit telemetry through the stdlib logging module."""

    target_logger = logger or logging.getLogger("tictactoe.controller")

    def _log(event: TelemetryEvent) -> None:
        target_logger.log(
            level,
            "controller.%s.%s payload=%s",
            event.channel,
            event.action,
            dict(event.payload),
        )

    def _log_error(exc: Exception, event: TelemetryEvent) -> None:
        target_logger.error(
            "controller.%s.%s failed payload=%s",
            event.channel,
            event.action,
            dict(event.payload),
            exc_info=exc,
        )

    return ControllerHooks(view=_log, domain=_log, error=_log_error)


GLOBAL_TELEMETRY_ENV_VAR = "TICTACTOE_LOGGING"


def telemetry_logging_requested(*aliases: str) -> bool:
    """Return True when any telemetry env flag (global or alias) is truthy."""

    candidates = (GLOBAL_TELEMETRY_ENV_VAR, *aliases)
    for name in candidates:
        if not name:
            continue
        value = os.environ.get(name, "")
        if value.strip().lower() in {"1", "true", "yes", "on"}:
            return True
    return False


__all__ = [
    "ControllerHooks",
    "TelemetryEvent",
    "TelemetryHook",
    "GLOBAL_TELEMETRY_ENV_VAR",
    "logging_hooks",
    "telemetry_logging_requested",
]
