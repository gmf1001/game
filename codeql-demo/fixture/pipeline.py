from source import fixture_source
from transform import pass_through


def build_value():
    return pass_through(fixture_source())
