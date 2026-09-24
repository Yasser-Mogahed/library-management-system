"""Notifiers are injected into Library (dependency injection, loose coupling)."""
from abc import ABC, abstractmethod


class Notifier(ABC):
    """Interface-like abstract class: Library only depends on this."""

    @abstractmethod
    def send(self, recipient_email: str, message: str) -> None:
        ...


class ConsoleNotifier(Notifier):
    def send(self, recipient_email: str, message: str) -> None:
        print(f"  -> notification to {recipient_email}: {message}")


class SilentNotifier(Notifier):
    """Does nothing. Useful for tests."""

    def send(self, recipient_email: str, message: str) -> None:
        pass
