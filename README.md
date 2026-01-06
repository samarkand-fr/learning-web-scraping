# 📚 Books to Scrape  - Système de Surveillance des Prix

Ce projet est un outil de web scraping développé en Python pour extraire des données du site [Books to Scrape](http://books.toscrape.com/). Il a été conçu de manière modulaire pour couvrir différents besoins, de l'extraction d'un livre unique à la récupération complète du catalogue avec images.

## Architecture du Projet

Le projet est modulaire, avec une orchestration centrale assurée par main.py.
Les responsabilités sont séparées par phase, et les fonctions communes sont mutualisées dans un module utilitaire afin de respecter le principe DRY "Don't Repeat Yourself".

- **`main.py`** : Le point d'entrée principal. Il propose un menu interactif pour lancer les différentes phases.
- **`scraper_utils.py`** : Contient toute la logique technique (extraction, pagination, sauvegarde CSV, téléchargement d'images) et les constantes globales.
- **`phase1.py` à `phase4.py`** :  Scripts indépendants contenant la logique propre à chaque phase et qui utilisent les fonctions de `scraper_utils.py`.

## Installation

1. **Clonez le repository** :
   ```bash
   git clone https://github.com/samarkand-fr/learning-web-scraping
   cd ./learning-web-scraping/
   ```

2. **Créez un environnement virtuel** :
   ```bash
   python -m venv venv
   ```

3. **Activez l'environnement virtuel** :
   - **Sur Mac/Linux** :
     ```bash
     source venv/bin/activate
     ```
   - **Sur Windows** :
     ```bash
     venv\Scripts\activate
     ```

4. **Installez les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```

## Utilisation (Recommandé)

Lancez simplement le script principal pour accéder au menu interactif :

```bash
python main.py
```

Le menu vous proposera 4 options :
1. **Phase 1** : Extraire les données d'un livre spécifique (ex: 'wuthering heights').
2. **Phase 2** : Extraire tous les livres d'une catégorie choisie (ex: 'food and drink').
3. **Phase 3** : Extraire l'intégralité du catalogue (toutes les livres) dans des fichiers CSV par catégorie.
4. **Phase 4** : Extraire et télécharger l'ensemble des images du site.

## Résultats

Toutes les données générées sont centralisées dans le dossier **`scraped_data/`** (ignoré par Git) :

- **Fichiers CSV** : Sauvegardés dans `scraped_data/csv/` (un fichier par catégorie).
- **Images** : Enregistrées dans `scraped_data/images/`, classées par sous-dossiers de catégorie.

## Dépendances
- `requests` : Pour effectuer les requêtes HTTP.
- `beautifulsoup4` : Pour analyser le code HTML des pages.
