# VoidMark

Prototype v0.1 du module VoidMark.

## Installation
pip install -r requirements-dev.txt

## Lancement
echo '{"test": "block1"}' > test.json
python src/void_mark.py test.json --vault-dir vault_test

## Objectif
Maintenir une chaîne de blocs hashée (append-only) pour rendre les artefacts vérifiables.
