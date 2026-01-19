import json
import aiofiles
import os

json_file = 'list_books.json'

async def save_book(book):
    try:
        async with aiofiles.open(json_file, 'r') as f:
            content = await f.read()
            datos = json.loads(content) if content.strip() else []
    except (FileNotFoundError, json.JSONDecodeError, ValueError):
        datos = []
    if isinstance(datos, list): datos.append(book)
    else: datos = [datos, book]
    async with aiofiles.open(json_file, 'w') as f:
        await f.write(json.dumps(datos, default=str, indent=4, ensure_ascii=False))


def read_book() -> list:
    with open(json_file, 'r', encoding='utf-8') as f:
        datos = json.load(f)
        if isinstance(datos, list):
            return datos 


async def delete_book_new(book: str):
    if not os.path.exists(json_file):
        return None
    
    async with aiofiles.open(json_file, 'r', encoding='utf-8') as f:
        content = await f.read()
        archivos = json.loads(content) if content.strip() else []
    
    if not isinstance(archivos, list):
        raise ValueError('El archivo debe contener una lista')
        
    if not any(str(item.get('id')) == book for item in archivos):
        print(f'ID {book} no encontrado')
        return None
        
    datos_filtrados = [item for item in archivos if str(item.get('id')) != book]
    
    async with aiofiles.open(json_file, 'w', encoding='utf-8') as f:
        await f.write(json.dumps(datos_filtrados, indent=4))
    return book


async def edit_book(book: str, u_book):
    if not os.path.exists(json_file):
        return None
    
    async with aiofiles.open(json_file, 'r', encoding='utf-8') as file:
        content = await file.read()
        files = json.loads(content) if content.strip() else []
        
    if not isinstance(files, list):
        raise ValueError('El archivo debe contener una lista')
    
    encontrado = False
    for i, item in enumerate(files):
        if str(item.get('id')) == book:
            files[i] = u_book  # ← REEMPLAZA el registro
            encontrado = True
            break
    
    if not encontrado:
        print(f'ID {book} no encontrado')
        return None
    
    async with aiofiles.open(json_file, 'w', encoding='utf-8') as file:
        await file.write(json.dumps(files, indent=4))
        
    return book
    
    