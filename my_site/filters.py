# filters.py

def clean_title(title):
    title = title.replace(' ', '-').replace('(', '').replace(')', '').replace(':', '').replace(',', '')
    return title
