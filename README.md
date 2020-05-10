# timon-interpreter
Python-based interpreter for simple time-oriented language called Timon ⏰

## Requirements:
- Python >= 3.6

## Usage:

Run from cmd from top directory:

```
python3 -m timoninterpreter [-stage {lexer, parser}] PATH_TO_SCRIPT
```

Sample scripts can be found in ```tests/acceptance/scripts/```.

By passing ```-stage``` argument execution can be stopped at certain stages and output from final stage will be shown.

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

Timon language grammar can be found in ```docs/grammar.ebnf```.
