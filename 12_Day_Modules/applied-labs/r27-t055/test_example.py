import io
import sys
import unittest
from unittest.mock import patch

from example import (
    REPEATABLE_FIXTURES,
    celsius_to_fahrenheit,
    convert_batch,
    main,
)


class TestTemperatureModule(unittest.TestCase):
    def test_celsius_to_fahrenheit_fixtures(self):
        self.assertEqual(celsius_to_fahrenheit(0), 32)
        self.assertEqual(celsius_to_fahrenheit(100), 212)

    def test_two_isolated_runs_agree(self):
        def fixed_clock():
            return "2026-01-01T12:00:00Z"

        sink_run1 = []
        sink_run2 = []

        result_run1 = convert_batch(
            REPEATABLE_FIXTURES, event_sink=sink_run1, clock=fixed_clock
        )
        result_run2 = convert_batch(
            REPEATABLE_FIXTURES, event_sink=sink_run2, clock=fixed_clock
        )

        # Both runs produce identical outputs and identical event logs
        self.assertEqual(result_run1, result_run2)
        self.assertEqual(sink_run1, sink_run2)
        self.assertEqual(result_run1, [32, 212, -40, 98.6])

    def test_import_prints_nothing_and_never_reads_input(self):
        stdout_buf = io.StringIO()
        with patch("sys.stdout", stdout_buf), patch(
            "builtins.input", side_effect=AssertionError("input() was called")
        ):
            # Re-import to guarantee no output on import
            if "example" in sys.modules:
                del sys.modules["example"]
            import example  # noqa: F401

            self.assertEqual(stdout_buf.getvalue(), "")

    def test_cli_main_guard(self):
        stdout_buf = io.StringIO()
        with patch("sys.stdout", stdout_buf):
            main(["0", "100"])

        output = stdout_buf.getvalue().strip().splitlines()
        self.assertEqual(output, ["0.0°C -> 32°F", "100.0°C -> 212°F"])


if __name__ == "__main__":
    unittest.main()

