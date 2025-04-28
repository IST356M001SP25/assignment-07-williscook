import re
from playwright.sync_api import Playwright, sync_playwright
from menuitemextractor import extract_menu_item
from menuitem import MenuItem
import pandas as pd

def tullyscraper(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.tullysgoodtimes.com/menus/")
    
    # Create an empty list to store all the extracted menu items
    extracted_items = []
    # Fins all <h3> element with the class 'foodmenu_menu-selector-title' and each title represents a menu section
    for title in page.query_selector_all("h3.foodmenu_menu-selector-title"):
    # Gets the text from that title
        title_text = title.inner_text()
        print("MENU SECTION:", title_text)
    # First moves to the next element, then again to the next after that so it is navigating the HTML strcuture to reach the container that holds the menu items related to that section.
        row = title.query_selector("~ *").query_selector("~ *")
    # Find all menu items inside that container ("div.foodmenu_menu-itme")
        for item in row.query_selector_all("div.foodmenu_menu-item"):
    # Gets the text of the text of each menu itme
            item_text = item.inner_text()
    # Proocess the section title and item next
            extracted_item = extract_menu_item(title_text, item_text)
            print(f" MENU ITEM: {extracted_item.name}")
    # Adds the extracted item to the list, converting it to a dictionary (key-value pairs) first
            extracted_items.append(extracted_item.to_dict())
    
    #Turns the list of dictionaries into a Pandas DataFrame
    df = pd.DataFrame(extracted_items)
    # Saves the DataFrame to a CSV file and do not add row numbers to the CSV
    df.to_csv("cache/tullys_menu.csv", index=False)

    context.close()
    browser.close()


with sync_playwright() as playwright:
    tullyscraper(playwright)
