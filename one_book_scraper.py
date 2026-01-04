from scraper_utils import (
        extract_book_data,
        save_to_csv,
        DEFAULT_BOOK_URL
    )

def run_phase1(url=DEFAULT_BOOK_URL):
    """Phase 1 : Extraction d'un seul livre."""
    
    print(f"\n--- Phase 1 : Extraction d'un seul livre ---")
    print(f"Cible: {url}")
    data = extract_book_data(url)
    if data:
        save_to_csv([data], "book.csv")
        print(f"Succès ! Livre '{data['title']}' sauvegardé dans book.csv")
    return data