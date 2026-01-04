from scraper_utils import extract_book_data, get_books_urls_from_category, get_all_categories_links, save_to_csv, download_image
import os

BASE_URL = "http://books.toscrape.com/"
def run_phase4():
    """Phase 4 : Téléchargement de TOUTES les images du site uniquement."""
    print("\n--- Phase 4 : Téléchargement de toutes les images du site ---")
    images_dir = os.path.join("scraped_data", "images")
    if not os.path.exists(images_dir):
        os.makedirs(images_dir)

    categories = get_all_categories_links(BASE_URL)
    print(f"{len(categories)} catégories trouvées.")
    
    for category in categories:
        print(f"\nTéléchargement images : {category['name']}...")
        book_urls = get_books_urls_from_category(category['url'])
        
        for i, url in enumerate(book_urls, 1):
            print(f"  [{i}/{len(book_urls)}] Téléchargement...", end="\r")
            data = extract_book_data(url)
            if data:
                download_image(data['image_url'], data['category'], data['universal_product_code'])
        print(f"\n  Images terminées pour {category['name']}")

