if __name__ == "__main__":
    import sys
    sys.path.append('code')
    from menuitem import MenuItem
else:
    from code.menuitem import MenuItem


def clean_price(price:str) -> float:
    # remove dollar sign
    price = price.replace("$", "")
    # remove any commas
    price = price.replace(",", "")
    # convert to float
    return float(price)

def clean_scraped_text(scraped_text: str) -> list[str]:
    # Splits the whole text into a list of lines, cutting at every newline characer (\n) and items is a list where each line is a seperate string
    items = scraped_text.split("\n")
    # Creates an empty list called "cleaned"
    cleaned = []
    # Loops through each line(item) one by one from items
    for item in items:
    # if the itme is exactly one of these ["GS", "V", "S","P"], then continue by skiping this item and goes to the next one.
        if item in ["GS", "V", "S","P"]:
            continue
    # if the item starts with "NEW", continue by skipping it
        if item.startswith("NEW"):
            continue
    # item.strip() removes any spaces before/after the text. If the line becomes empty (length 0), skip it beacuase this will proteect me from adding blank line
        if len(item.strip()) == 0:
            continue
    # If the item passed all the check, it is a goof item. Add it to the clearned list
        cleaned.append(item)
    
    return cleaned

def extract_menu_item(title:str, scraped_text: str) -> MenuItem:
    # Cleans the scraped text using the fuction that I wrote earlier
    cleaned_items = clean_scraped_text(scraped_text)
    # Creates a new MenuItem object
    item = MenuItem(category=title, name="", price=0.0, description="")
    # Sets the first line of clearned_items as the name of the item
    item.name = cleaned_items[0]
    # Takes the second line of cleaned_items and cleans it using clean_price() and save it as the price
    item.price = clean_price(cleaned_items[1])
    # check if there is a third line in cleaned_items
    if len(cleaned_items) > 2:
    # Sets the third line as the description
        item.description = cleaned_items[2]
    else:
        item.description = "No descripion avalibale."
    return item



if __name__=='__main__':
     test_items = [
        '''
NEW!

Tully Tots

$11.79

Made from scratch with shredded potatoes, cheddar-jack cheese and Romano cheese all rolled up and deep-fried. Served with a spicy cheese sauce.
        ''',

        '''Super Nachos

$15.49
GS

Tortilla chips topped with a mix of spicy beef and refried beans, nacho cheese sauce, olives, pico de gallo, jalapeños, scallions and shredded lettuce. Sour cream and salsa on the side. Add guacamole $2.39

        ''',
        '''Veggie Quesadilla

$11.99
V

A flour tortilla packed with cheese, tomatoes, jalapeños, black olives and scallions. Served with sour cream and pico de gallo.
Add chicken $2.99 | Add guacamole $2.39
''',
'''Kid's Burger & Fries

$6.99
'''

    ]
title = "TEST"
for scraped_text in test_items:
    item = extract_menu_item(title, scraped_text)
    print(item)
