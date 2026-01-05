# Importation des outils nécessaires pour traiter une catégorie
from scraper_utils import (
        extract_book_data, 
        get_books_urls_from_category,
        save_to_csv,
        DEFAULT_CATEGORY_URL
    )

def run_phase2(url=DEFAULT_CATEGORY_URL):
    """
    Extraction de tous les livres d'une catégorie.
    Parcourt la liste des URLs de livres, extrait les infos de chaque livre,
    et génère un fichier CSV nommé selon la catégorie.
    """
    
    print(f"\n--- Phase 2 : Extraction d'une catégorie ---")
    print(f"Cible : {url}")

    #Récupération de toutes les URLs des livres de la catégorie (gère la pagination)
    book_urls = get_books_urls_from_category(url)
    print(f"{len(book_urls)} livres trouvés. Extraction en cours...")
    
    #Boucle de scraping séquentielle sur chaque livre
    results = []
    for i, book_url in enumerate(book_urls, 1):
        # Affichage de la progression sur la même ligne
        print(f"  [{i}/{len(book_urls)}] Scraping livre...", end="\r")
        data = extract_book_data(book_url)
        if data:
            results.append(data)

    #Sauvegarde automatique dans un CSV au nom de la catégorie
    if results:
        # On extrait le nom de la catégorie pour le nom du fichier
        category_name = results[0]['category'].lower().replace(' ', '_')
        save_to_csv(results, f"{category_name}.csv")
        print(f"\n--- Fin de la Phase 2 : {len(results)} livres extraits pour {category_name} ---")
        
    return results # Retourne les données extraites 
