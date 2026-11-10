# R27-T055: Module boundary and deterministic temperature conversion

`celsius_to_fahrenheit(celsius)` converts temperatures from Celsius to Fahrenheit.

## Contract and Architecture

- **Importable Module**: When imported, the module prints nothing and never reads user input.
- **Main Guard**: The CLI is protected by `if __name__ == "__main__":` to allow script execution without side effects on import.
- **Fixtures**:
  - `0°C -> 32°F`
  - `100°C -> 212°F`
- **Deterministic Injection**: Supports optional dependency injection for event storage (`event_sink`) and time (`clock`), ensuring two isolated runs produce identical results.

## Run the tests

From the repository root:

    python3 -m unittest discover -s 12_Day_Modules/applied-labs/r27-t055 -p "test_*.py"
