

from utils_scraper import extract_book_data, get_books_urls_from_category, save_to_csv

def run_phase2():
    """
    Phase 2 : Extrait les données de tous les livres d'une catégorie spécifique.
    Gère la pagination et enregistre les résultats dans un CSV nommé selon la catégorie.
    """
    url = "https://books.toscrape.com/catalogue/category/books/food-and-drink_33/index.html"
    
    # Récupération de tous les liens de livres de la catégorie
    book_urls = get_books_urls_from_category(url)
    
    # Extraction des détails pour chaque livre
    category_books = []
    for book_url in book_urls:
        data = extract_book_data(book_url)
        if data:
            category_books.append(data)
    
    # Sauvegarde dans un fichier CSV au nom de la catégorie
    if category_books:
        category_name = category_books[0]['category'].lower().replace(' ', '_')
        save_to_csv(category_books, f"{category_name}.csv")

if __name__ == "__main__":
    run_phase2()
