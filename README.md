# timon-interpreter
Python based interpreter for simple date oriented language

## Requirements:
- Python >= 3.6

## Usage:

Run from cmd from top directory:

```
python3 -m timoninterpreter PATH_TO_SCRIPT
```

Sample scripts can be found in ```tests/acceptance/scripts/```

## Tests

Running acceptance tests (with sample scripts):

```
python3 -m unittest discover tests/acceptance
```

Running unit tests:

```
python3 -m unittest discover tests/unit
```

## Grammar

Timon language grammar can be found in ```docs/grammar.ebnf```