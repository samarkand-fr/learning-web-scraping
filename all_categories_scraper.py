from utils_scraper import extract_book_data, get_books_urls_from_category, get_all_categories_links, save_to_csv

BASE_URL = "http://books.toscrape.com/"

def run_phase3():
    """
    Phase 3 : Scrape l'ensemble du site en itérant sur toutes les catégories.
    Crée un fichier CSV distinct pour chaque catégorie trouvée.
    """
    # Récupération de tous les liens de catégories du site
    categories = get_all_categories_links(BASE_URL)
    
    for category in categories:
        # Récupération de toutes les URLs de livres pour la catégorie courante
        book_urls = get_books_urls_from_category(category['url'])
        
        category_data = []
        for url in book_urls:
            data = extract_book_data(url)
            if data:
                category_data.append(data)
            
        # Sauvegarde des données de la catégorie dans son propre fichier CSV
        if category_data:
            filename = f"{category['name'].lower().replace(' ', '_')}.csv"
            save_to_csv(category_data, filename)

if __name__ == "__main__":
    run_phase3()
