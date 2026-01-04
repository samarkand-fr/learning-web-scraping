import os
import sys
from scraper_utils import (
    get_all_categories_links, 
    DEFAULT_BOOK_URL,
    DEFAULT_CATEGORY_URL,
    BASE_URL
)
from one_book_scraper import run_phase1
from category_books_scraper import run_phase2
from all_categories_scraper import run_phase3
from scraper_images import run_phase4

def main():
    # Extraction des noms pour l'affichage dynamique
    book_name = DEFAULT_BOOK_URL.split('/')[-2].replace('-', ' ').title()
    cat_name = DEFAULT_CATEGORY_URL.split('/')[-2].split('_')[0].title()

    while True:
        print("\n=== Système de surveillance des prix Books Online ===")
        print(f"1. Phase 1 : Extraire le livre '{book_name}'")
        print(f"2. Phase 2 : Extraire la catégorie '{cat_name}'")
        print(f"3. Phase 3 : Extraire TOUTES les catégories (CSV uniquement)")
        print(f"4. Phase 4 : Télécharger TOUTES les images")
        print("q. Quitter")
        
        choice = input("\nChoisissez une option : ").strip().lower()
        
        if choice == '1':
            run_phase1(DEFAULT_BOOK_URL)
        elif choice == '2':
            run_phase2(DEFAULT_CATEGORY_URL)
        elif choice == '3':
            run_phase3()
        elif choice == '4':
            run_phase4()
        elif choice == 'q':
            print("no more scraping =====!")
            break
        else:
            print("Option invalide.")

if __name__ == "__main__":
    main()
