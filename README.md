# kestra-sales-etl

![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=flat-square&logo=python&logoColor=white)
![DuckDB](https://img.shields.io/badge/DuckDB-1.5-FFF000?style=flat-square&logo=duckdb&logoColor=black)
![Pandas](https://img.shields.io/badge/Pandas-3.0-150458?style=flat-square&logo=pandas&logoColor=white)
![Polars](https://img.shields.io/badge/Polars-1.44-CD792C?style=flat-square&logo=polars&logoColor=white)
![PyArrow](https://img.shields.io/badge/PyArrow-25.0-blue?style=flat-square)
![openpyxl](https://img.shields.io/badge/openpyxl-3.1-217346?style=flat-square&logo=microsoftexcel&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-notebook-F37626?style=flat-square&logo=jupyter&logoColor=white)
![Kestra](https://img.shields.io/badge/Kestra-orchestration-8405FE?style=flat-square&logo=kestra&logoColor=white)
![Docker Compose](https://img.shields.io/badge/Docker%20Compose-services-2496ED?style=flat-square&logo=docker&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18-4169E1?style=flat-square&logo=postgresql&logoColor=white)
![uv](https://img.shields.io/badge/uv-package%20manager-DE5FE9?style=flat-square)

Pipeline data d'analyse des ventes d'un caviste : croisement d'un export **ERP** (catalogue produit) avec les ventes du site **e-commerce**, calcul du chiffre d'affaires, et détection des vins **premium** par score statistique (z-score). Le pipeline est développé et validé en local sous forme de scripts Python, avant orchestration via **Kestra**.

## Contexte métier

Un caviste dispose de trois sources de données disjointes :
- un **ERP** avec le catalogue produit et les prix,
- un site **e-commerce** avec les ventes,
- une table de **liaison** faisant correspondre les identifiants produit ERP ↔ web.

L'objectif est de fournir au service métier :
1. le **chiffre d'affaires** total et par produit,
2. la liste des vins classés **premium** vs **ordinaires**, sur la base d'un écart significatif de prix (z-score > 2).

Chaque étape du pipeline embarque ses propres tests de cohérence (volumétrie, doublons, valeurs manquantes, CA attendu) qui comparent le résultat calculé aux chiffres de référence fournis par le métier, afin de garantir la fiabilité de la chaîne de bout en bout.

## Structure du projet

```
kestra-sales-etl/
├── data/                       # Sources brutes (xlsx), non versionnées en usage réel
│   ├── Fichier_erp.xlsx        # Catalogue produit ERP
│   ├── Fichier_web.xlsx        # Export des ventes du site web
│   └── fichier_liaison.xlsx    # Table de correspondance product_id ↔ sku
│
├── scripts/                    # Pipeline ETL, étape par étape
│   ├── sql_nettoyage.py        # Étape 1 — nettoyage & dédoublonnage
│   ├── sql_jointure.py         # Étape 2 — jointure ERP / liaison / web
│   ├── sql_ca.py               # Étape 3 — calcul du chiffre d'affaires
│   ├── py_zscore.py            # Étape 4 — z-score & classification premium
│   └── py_export.py            # Étape 5 — export des livrables finaux
│
├── export/                     # Résultats intermédiaires entre chaque étape (CSV)
│   ├── erp_s1.csv / web_s1.csv / liaison_s1.csv
│   ├── fusion_s2.csv
│   ├── ca_pro_s3.csv / ca_tot_s3.csv
│   └── vins_premiums.csv / vins_ordinaires.csv
│
├── livrables/                  # Livrables finaux destinés au métier
│   ├── rapport_bottleneck.xlsx     # Classeur Excel multi-feuilles (CA produit / CA total)
│   ├── liste_vins_premiums.csv
│   └── liste_vins_ordinaires.csv
│
├── notebooks/                  # Exploration & profiling des données sources
│   ├── profiling.ipynb
│   └── profiling_p10_raw.xlsx
│
├── kestra/                     # Orchestration (à venir)
│   └── docker-compose.yml      # Stack Kestra (standalone) + PostgreSQL
│
├── pyproject.toml              # Dépendances du projet (géré avec uv)
├── uv.lock
└── .python-version             # Python 3.13
```

## Pipeline ETL

Le pipeline est découpé en 5 scripts séquentiels, chacun consommant les exports du précédent et produisant les siens dans `export/`. Chaque script est exécutable indépendamment et embarque ses propres vérifications (`assert`) qui interrompent le pipeline en cas d'incohérence.

| # | Script | Entrées | Rôle | Sorties |
|---|--------|---------|------|---------|
| 1 | [`sql_nettoyage.py`](scripts/sql_nettoyage.py) | `data/*.xlsx` | Chargement des sources Excel dans DuckDB, suppression des colonnes 100% vides, filtrage des clés nulles, dédoublonnage (ERP, web, liaison) | `erp_s1.csv`, `web_s1.csv`, `liaison_s1.csv` |
| 2 | [`sql_jointure.py`](scripts/sql_jointure.py) | exports étape 1 | Jointure SQL `erp → liaison → web` (`INNER JOIN`) pour reconstituer une table produit/vente unifiée | `fusion_s2.csv` |
| 3 | [`sql_ca.py`](scripts/sql_ca.py) | `fusion_s2.csv` | Calcul du CA par produit (`price × total_sales`) et du CA total | `ca_pro_s3.csv`, `ca_tot_s3.csv` |
| 4 | [`py_zscore.py`](scripts/py_zscore.py) | `fusion_s2.csv` | Calcul du z-score sur le prix, classification vins premium (`z-score > 2`) / ordinaires | `vins_premiums.csv`, `vins_ordinaires.csv` |
| 5 | [`py_export.py`](scripts/py_export.py) | exports étapes 3 & 4 | Génération des livrables finaux : classeur Excel multi-feuilles + CSV | `rapport_bottleneck.xlsx`, `liste_vins_premiums.csv`, `liste_vins_ordinaires.csv` |

**Stack technique par étape** : les transformations relationnelles (nettoyage, jointures, agrégations) sont réalisées en SQL via **DuckDB**, moteur analytique embarqué performant sur fichiers plats, avec **pandas** en interface d'E/S (lecture Excel, registre DuckDB). Le calcul du z-score et les exports finaux restent en pandas pur.

### Résultats de référence (jeu de données actuel)

- ERP nettoyé : **825** lignes
- Web nettoyé : **714** lignes
- Table fusionnée : **714** lignes
- Chiffre d'affaires total : **70 568,60 €**
- Vins premium détectés (z-score > 2) : **30**
- Vins ordinaires : **684**

## Installation & exécution

Le projet utilise [uv](https://docs.astral.sh/uv/) comme gestionnaire de dépendances et d'environnement Python.

```bash
# Installer les dépendances (crée automatiquement le .venv)
uv sync

# Exécuter le pipeline dans l'ordre
uv run scripts/sql_nettoyage.py
uv run scripts/sql_jointure.py
uv run scripts/sql_ca.py
uv run scripts/py_zscore.py
uv run scripts/py_export.py
```

Chaque script affiche en console les contrôles de cohérence effectués (volumétrie, doublons, unicité des clés, CA, classification) avant de produire ses fichiers de sortie.

### Dépendances principales

- **duckdb** — moteur SQL analytique embarqué, utilisé pour le nettoyage et les jointures
- **pandas** — manipulation de données et interface avec DuckDB
- **polars** / **pyarrow** — disponibles pour les traitements columnaires
- **openpyxl** / **fastexcel** — lecture/écriture des fichiers Excel sources et livrables
- **ipykernel** — exécution des notebooks de profiling

## Orchestration Kestra

> Section à compléter.

Un socle Docker Compose est disponible dans [`kestra/docker-compose.yml`](kestra/docker-compose.yml) : il déploie un serveur **Kestra** (mode standalone) adossé à une base **PostgreSQL 18** (repository, queue) et monte le dossier `data/` du projet dans le conteneur Kestra.

```bash
cd kestra
docker compose up -d
```

L'interface Kestra est ensuite accessible sur [http://localhost:8080](http://localhost:8080).

*(Flows Kestra, planification et orchestration des 5 étapes du pipeline à documenter ici une fois développés.)*

