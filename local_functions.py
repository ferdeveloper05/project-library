import json

json_file = 'list_books.json'

def save_book(book):
    list_books =[]
    with open(json_file, 'a', encoding='utf-8') as f:
        list_books.append(book)
        json.dump(list_books, f, indent=4, ensure_ascii=False, separators=(',',':'))
        
def read_book() -> list:
    with open(json_file, 'r', encoding='utf-8') as f:
        return json.load(f)
    
def delete_book(book: dict):
    with open(json_file, 'r', encoding='utf-8') as f:
        archivos = list(json.load(f))
        
        for dato in archivos:
            if dato['id'] == book['id']:
                archivos
        