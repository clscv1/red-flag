"""Red flag detector powered by Jev."""

from jev_experiment.detector import analyze

__all__ = ["analyze"]


def main() -> None:
    from jev_experiment.server import main as run_server

    run_server()
