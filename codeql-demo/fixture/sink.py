from pipeline import build_value

_observed_values = []


def fixture_sink(value):
    """Record the value in memory; this demo performs no external side effects."""
    _observed_values.append(value)


def run_fixture():
    fixture_sink(build_value())


def observed_values():
    return list(_observed_values)
