import argparse
from collections import Counter
import math
from pathlib import Path
import re
import sqlite3
import unicodedata

def tokens(text):
    normalized = ''.join(c for c in unicodedata.normalize('NFKD', text.lower()) if not unicodedata.combining(c))
    return re.findall(r'[a-z0-9]+', normalized)

def connect(path):
    db = sqlite3.connect(path)
    db.executescript('CREATE TABLE IF NOT EXISTS docs(id INTEGER PRIMARY KEY,path TEXT,text TEXT); CREATE TABLE IF NOT EXISTS terms(term TEXT,doc INTEGER,freq INTEGER,PRIMARY KEY(term,doc));')
    return db

def index(folder, db_path):
    folder = Path(folder)
    if not folder.is_dir(): raise ValueError('Pasta não encontrada.')
    documents = []
    for path in sorted(folder.rglob('*')):
        if path.is_symlink() or not path.is_file() or path.suffix.lower() not in ('.txt','.md'): continue
        if any(parent.is_symlink() for parent in path.parents): continue
        if path.stat().st_size > 2_000_000: raise ValueError(f'Arquivo acima de 2 MB: {path.name}')
        documents.append((str(path.relative_to(folder)), path.read_text(encoding='utf-8')))
    db = connect(db_path)
    try:
        with db:
            db.execute('DELETE FROM terms'); db.execute('DELETE FROM docs')
            for path,text in documents:
                id = db.execute('INSERT INTO docs(path,text) VALUES(?,?)',(path,text)).lastrowid
                db.executemany('INSERT INTO terms VALUES(?,?,?)', [(word,id,freq) for word,freq in Counter(tokens(text)).items()])
    finally: db.close()
    return len(documents)

def search(query, db_path, limit=5):
    if not Path(db_path).is_file(): raise ValueError('Crie o índice primeiro.')
    db = connect(db_path)
    try:
        count = db.execute('SELECT count(*) FROM docs').fetchone()[0]
        scores = Counter()
        for term in set(tokens(query)):
            matches = db.execute('SELECT doc,freq FROM terms WHERE term=?',(term,)).fetchall()
            idf = math.log((1+count)/(1+len(matches))) + 1
            for id,freq in matches: scores[id] += (1+math.log(freq))*idf
        result = []
        for id,score in sorted(scores.items(), key=lambda item: (-item[1],item[0]))[:limit]:
            path,text = db.execute('SELECT path,text FROM docs WHERE id=?',(id,)).fetchone()
            result.append(dict(path=path,score=round(score,4),snippet=' '.join(text.split())[:180]))
        return result
    finally: db.close()

def main():
    p=argparse.ArgumentParser(description='Busca local TF-IDF')
    sub=p.add_subparsers(dest='command',required=True)
    for command in ('index','search'):
        child=sub.add_parser(command); child.add_argument('value'); child.add_argument('--db',default='search.db')
    args=p.parse_args()
    try:
        if args.command=='index': print(f'{index(args.value,args.db)} documentos indexados.')
        else:
            result=search(args.value,args.db)
            for row in result: print(f'{row["path"]} | score {row["score"]}\n  {row["snippet"]}')
            if not result: print('Nenhum resultado.')
    except (ValueError,OSError,UnicodeError) as error: p.exit(2,f'Erro: {error}\n')

if __name__=='__main__': main()
