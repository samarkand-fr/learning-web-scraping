from scraper_utils import (
        extract_book_data, 
        get_books_urls_from_category,
        save_to_csv,
        DEFAULT_CATEGORY_URL
    )
    
def run_phase2(url=DEFAULT_CATEGORY_URL):
    """Phase 2 : Extraction d'une catégorie complète."""
    
    print(f"\n--- Phase 2 : Extraction d'une catégorie ---")
    print(f"Cible : {url}")
    book_urls = get_books_urls_from_category(url)
    print(f"{len(book_urls)} livres trouvés. Extraction en cours...")
    
    results = []
    for i, book_url in enumerate(book_urls, 1):
        print(f"  [{i}/{len(book_urls)}] Scraping livre...", end="\r")
        data = extract_book_data(book_url)
        if data:
            results.append(data)
    
    if results:
        category_name = results[0]['category'].lower().replace(' ', '_')
        save_to_csv(results, f"{category_name}.csv")
        print(f"\nTerminé ! Données sauvegardées pour la catégorie {category_name}")
    return results
