from scraper_utils import ( 
        extract_book_data,
        get_books_urls_from_category, 
        get_all_categories_links, 
        save_to_csv,
        BASE_URL
    )

def run_phase3():
    """Phase 3 : Extraction de TOUTES les données (CSV) du site."""

    print("\n--- Phase 3 : Extraction de tout le site (Toutes les catégories) ---")
    categories = get_all_categories_links(BASE_URL)
    print(f"{len(categories)} catégories trouvées.")
    
    for category in categories:
        print(f"\nTraitement de la catégorie : {category['name']}...")
        book_urls = get_books_urls_from_category(category['url'])
        
        results = []
        for i, url in enumerate(book_urls, 1):
            print(f"  [{i}/{len(book_urls)}] Extraction livre...", end="\r")
            data = extract_book_data(url)
            if data:
                results.append(data)
        
        if results:
            filename = f"{category['name'].lower().replace(' ', '_')}.csv"
            save_to_csv(results, filename)
            print(f"\n  Données sauvegardées dans {filename}")