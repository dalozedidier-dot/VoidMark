# VoidMark

Prototype v0.1 du module VoidMark.

## Installation

```
pip install -r requirements-dev.txt
```

## Lancement

```
echo '{"test": "block1"}' > test.json
python src/void_mark.py test.json --vault-dir vault_test
```

### Paramètres

- `--vault-dir <dir>` : répertoire de stockage du vault (créé si absent).  
  Exemple : `vault_test`.

## Objectif

Marquer un bloc de données dans un vault local, sans interprétation.
