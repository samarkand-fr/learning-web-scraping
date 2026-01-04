from scraper_utils import (
    extract_book_data, 
    get_books_urls_from_category, 
    get_all_categories_links, 
    save_to_csv, 
)

# Configuration des cibles par défaut
DEFAULT_BOOK_URL = "http://books.toscrape.com/catalogue/wuthering-heights_307/index.html"
DEFAULT_CATEGORY_URL = "https://books.toscrape.com/catalogue/category/books/food-and-drink_33/index.html"
BASE_URL = "http://books.toscrape.com/"

def phase_1(url=DEFAULT_BOOK_URL):
    print("\n--- Phase 1 : Extraction d'un seul livre ---")
    print(f"Cible : {url}")
    data = extract_book_data(url)
    if data:
        save_to_csv([data], "book.csv")
        print(f"Succès ! Livre '{data['title']}' sauvegardé dans book.csv")

def phase_2(url=DEFAULT_CATEGORY_URL):
    print("\n--- Phase 2 : Extraction d'une catégorie ---")
    print(f"Cible : {url}")
    book_urls = get_books_urls_from_category(url)
    print(f"{len(book_urls)} livres trouvés. Extraction en cours...")
    
    results = []
    for i, book_url in enumerate(book_urls, 1):
        print(f"  [{i}/{len(book_urls)}] Scriping...", end="\r")
        data = extract_book_data(book_url)
        if data:
            results.append(data)
    
    if results:
        category_name = results[0]['category'].lower().replace(' ', '_')
        save_to_csv(results, f"{category_name}.csv")
        print(f"\nTerminé ! Données sauvegardées dans {category_name}.csv")

def phase_3():
    mode = "Phase 4" if download_images else "Phase 3"
    print(f"\n--- {mode} : Extraction de tout le site ---")
    
   
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
            print(f"\n  Fini ! Données sauvegardées dans {filename}")

def main():
    # Extraction des noms pour l'affichage dynamique
    book_name = DEFAULT_BOOK_URL.split('/')[-2].replace('-', ' ').title()
    category_name = DEFAULT_CATEGORY_URL.split('/')[-2].split('_')[0].title()

    while True:
        print("\n=== Système de surveillance des prix Books Online ===")
        print(f"1. Phase 1 : Extraire le livre '{book_name}'")
        print(f"2. Phase 2 : Extraire la catégorie '{category_name}'")
        print(f"3. Phase 3 : Extraire tout le site (Toutes les catégories)")
        print("q. Quitter")
        
        choice = input("\nChoisissez une option : ").strip().lower()
        
        if choice == '1':
            phase_1(DEFAULT_BOOK_URL)
        elif choice == '2':
            phase_2(DEFAULT_CATEGORY_URL)
        elif choice == '3':
            phase_3()
        elif choice == 'q':
            print("no more scraping =====!")
            break
        else:
            print("Option invalide.")

if __name__ == "__main__":
    main()
