import argparse,csv,json,sqlite3
from datetime import date
from decimal import Decimal,InvalidOperation

def extract(path):
    records=[]; seen=set()
    with open(path,encoding='utf-8-sig',newline='') as file:
        reader=csv.DictReader(file)
        if reader.fieldnames!=['order_id','date','customer','amount']:
            raise ValueError('Cabeçalho esperado: order_id,date,customer,amount')
        for line,row in enumerate(reader,2):
            try:
                if None in row or any(v is None for v in row.values()):raise ValueError()
                key=row['order_id'].strip(); customer=row['customer'].strip()
                day=date.fromisoformat(row['date']).isoformat();amount=Decimal(row['amount'])
                if not key or not customer or key in seen or not amount.is_finite() or amount<0:raise ValueError()
                cents=amount*100
                if cents!=cents.to_integral_value() or cents>9223372036854775807:raise ValueError()
                seen.add(key);records.append((key,day,customer,int(cents)))
            except (ValueError,InvalidOperation):raise ValueError(f'Linha {line}: registro inválido ou ID duplicado.') from None
    return records

def run(source,database):
    records=extract(source)
    db=sqlite3.connect(database)
    try:
        db.executescript('CREATE TABLE IF NOT EXISTS orders(order_id TEXT PRIMARY KEY,date TEXT,customer TEXT,amount_cents INTEGER); CREATE TABLE IF NOT EXISTS runs(id INTEGER PRIMARY KEY,source TEXT,inserted INTEGER,skipped INTEGER,created TEXT DEFAULT CURRENT_TIMESTAMP);')
        inserted=skipped=0
        with db:
            db.execute('BEGIN IMMEDIATE')
            for record in records:
                existing=db.execute('SELECT * FROM orders WHERE order_id=?',(record[0],)).fetchone()
                if existing:
                    if existing!=record:raise ValueError(f'ID {record[0]} já existe com conteúdo diferente.')
                    skipped+=1
                else:
                    db.execute('INSERT INTO orders VALUES(?,?,?,?)',record);inserted+=1
            db.execute('INSERT INTO runs(source,inserted,skipped) VALUES(?,?,?)',(str(source),inserted,skipped))
        return {'inserted':inserted,'skipped':skipped,'total_cents':db.execute('SELECT COALESCE(sum(amount_cents),0) FROM orders').fetchone()[0]}
    finally:db.close()

def main():
    p=argparse.ArgumentParser(description='Pipeline CSV para data warehouse SQLite');p.add_argument('source');p.add_argument('--db',default='warehouse.db');args=p.parse_args()
    try:print(json.dumps(run(args.source,args.db),indent=2))
    except (ValueError,OSError,sqlite3.Error) as error:p.exit(2,f'Erro: {error}\n')
if __name__=='__main__':main()
