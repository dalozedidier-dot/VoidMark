DD-Vault Prototype v0.1

Objectif
Stocker des artefacts (JSON) de façon immuable et chaînée par hash.
Chaque nouvel artefact crée un bloc lié au bloc précédent.
Toute modification rétroactive casse la chaîne.

Contenu
- dd_vault.py : script principal

Prérequis
- Python 3.9+

Usage
1) Vaultiser un JSON
   python dd_vault.py results/graph_report.json --vault-dir my_vault

Sorties
- my_vault/vault_chain.json : chaîne de blocs
- my_vault/block_<index>_artifact.json : copie de l'artefact original

Notes
- Option --vault-dir (canonique). Alias compat: --vault_dir.
- Le champ data_summary est un résumé descriptif court.
- La sécurité est celle d'un hash en chaîne (tamper-evident), pas un consensus distribué.

Prochaines étapes envisagées
- Merkle tree pour vérification partielle
- Stockage IPFS ou dossier distribué
- Vérificateur externe de chaîne
