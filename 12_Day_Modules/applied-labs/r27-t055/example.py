"""R27-T055: Module boundary with CLI main guard and deterministic fixtures."""

REPEATABLE_FIXTURES = (0, 100, -40, 37)


def celsius_to_fahrenheit(celsius, *, event_sink=None, clock=None):
    """Convert Celsius temperature to Fahrenheit.

    Optionally inject an event_sink (storage list) and clock callable to record
    deterministic conversion events.
    """
    fahrenheit = (celsius * 9 / 5) + 32
    if isinstance(fahrenheit, float) and fahrenheit.is_integer():
        fahrenheit = int(fahrenheit)

    if event_sink is not None:
        timestamp = clock() if clock is not None else "2026-01-01T00:00:00Z"
        event_sink.append(
            {
                "celsius": celsius,
                "fahrenheit": fahrenheit,
                "timestamp": timestamp,
            }
        )

    return fahrenheit


def convert_batch(values, *, event_sink=None, clock=None):
    """Convert a sequence of Celsius temperatures with optional event injection."""
    return [
        celsius_to_fahrenheit(val, event_sink=event_sink, clock=clock)
        for val in values
    ]


def main(argv=None):
    """CLI entry point protected by the main guard."""
    import sys

    args = argv if argv is not None else sys.argv[1:]
    if args:
        for arg in args:
            c = float(arg)
            f = celsius_to_fahrenheit(c)
            print(f"{c}°C -> {f}°F")
    else:
        print(f"0°C -> {celsius_to_fahrenheit(0)}°F")
        print(f"100°C -> {celsius_to_fahrenheit(100)}°F")


if __name__ == "__main__":
    main()

