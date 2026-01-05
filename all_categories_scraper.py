# Importation des outils pour extraire tout le site (CSV uniquement)
from scraper_utils import ( 
        extract_book_data,
        get_books_urls_from_category, 
        get_all_categories_links, 
        save_to_csv,
        BASE_URL
    )

def run_phase3():
    """
    Extraction de TOUTES les données CSV de tout le site.
    Parcourt chaque catégorie du site, et pour chacune, extrait tous les livres.
    """

    print("\n--- Phase 3 : Extraction de tout le site (Toutes les catégories) ---")
    total_books = 0 # Compteur simple pour le total des livres extraits

    # On récupère la liste de toutes les catégories présentes sur la page d'accueil 
    categories = get_all_categories_links(BASE_URL)
    print(f"{len(categories)} catégories trouvées.")
    
    # On traite chaque catégorie l'une après l'autre (boucle externe)
    for category in categories:
        print(f"\nTraitement de la catégorie : {category['name']}...")

        # Récupération des livres de la catégorie actuelle
        book_urls = get_books_urls_from_category(category['url'])

        # Extraction des données de chaque livre (boucle interne)
        results = []
        for i, url in enumerate(book_urls, 1):
            # Affichage de la progression sur la même ligne
            print(f"  [{i}/{len(book_urls)}] Extraction livre...", end="\r")
            data = extract_book_data(url)
            if data:
                results.append(data)

        # Sauvegarde immédiate du fichier CSV pour cette catégorie
        if results:
            count = len(results)
            total_books += count
            filename = f"{category['name'].lower().replace(' ', '_')}.csv"
            save_to_csv(results, filename)
            print(f"\n  {count} livres extraits et sauvegardés dans {filename}")
            
    print(f"\n--- Fin de la Phase 3 : {total_books} livres extraits au total ---")
    return total_books # return nombre de livres extraits au total