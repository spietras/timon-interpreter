# timon-interpreter
Python-based interpreter for simple time-oriented language called Timon ⏰

## Requirements
- Python >= 3.6

## Usage

Run from cmd from top directory:

```
python3 -m timoninterpreter [-stage {lexer, parser, execution}] PATH_TO_SCRIPT
```

Sample scripts can be found in ```tests/acceptance/scripts/```.

By passing ```-stage``` argument execution can be stopped at certain stage and output from that stage will be shown.
Default stage is ```execution```.

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
