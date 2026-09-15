import argparse
import csv
from datetime import date
from decimal import Decimal, InvalidOperation
from html import escape
from pathlib import Path

def analyze(path):
    products, months, total, units, count = {}, {}, Decimal(0), 0, 0
    with open(path, encoding='utf-8-sig', newline='') as file:
        reader = csv.DictReader(file)
        if reader.fieldnames != ['date', 'product', 'quantity', 'unit_price']:
            raise ValueError('Cabeçalho esperado: date,product,quantity,unit_price')
        for line, row in enumerate(reader, 2):
            try:
                if None in row or any(value is None for value in row.values()):
                    raise ValueError()
                day = date.fromisoformat(row['date'])
                name = row['product'].strip()
                quantity = int(row['quantity'])
                price = Decimal(row['unit_price'])
                if not name or quantity <= 0 or not price.is_finite() or price < 0 or price != price.quantize(Decimal('.01')):
                    raise ValueError()
                amount = price * quantity
                products[name] = products.get(name, Decimal(0)) + amount
                month = day.strftime('%Y-%m')
                months[month] = months.get(month, Decimal(0)) + amount
                total += amount; units += quantity; count += 1
            except (ValueError, InvalidOperation):
                raise ValueError(f'Linha {line}: venda inválida.') from None
    return dict(total=total, units=units, count=count, products=products, months=months)

def render(data):
    maximum = max(data['products'].values(), default=Decimal(0)) or Decimal(1)
    rows = ''.join(f'<tr><td>{escape(name)}</td><td>R$ {value:.2f}</td><td><meter min="0" max="1" value="{value/maximum}"></meter></td></tr>' for name,value in sorted(data['products'].items(), key=lambda item: (-item[1],item[0])))
    months = ''.join(f'<li>{month}: R$ {value:.2f}</li>' for month,value in sorted(data['months'].items()))
    return f"""<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Sales Insights</title>
    <style>body{{font:17px system-ui;margin:40px auto;max-width:900px;padding:24px;background:#f1f5fa;color:#162a43}}section{{background:white;padding:24px;border-radius:16px;margin:18px 0}}table{{width:100%;border-collapse:collapse}}td,th{{padding:14px;text-align:left;border-bottom:1px solid #eee}}meter{{width:100%}}h1{{font-size:40px}}</style>
    <small>SALES INSIGHTS / RELATÓRIO LOCAL</small><h1>Vendas em perspectiva</h1><section><h2>R$ {data['total']:.2f}</h2><p>{data['units']} unidades · {data['count']} linhas de venda</p></section>
    <section><h2>Produtos por receita</h2><table><thead><tr><th>Produto</th><th>Receita</th><th>Proporção</th></tr></thead><tbody>{rows}</tbody></table></section><section><h2>Receita mensal</h2><ul>{months}</ul></section></html>"""

def main():
    p = argparse.ArgumentParser(description='Relatório HTML de vendas CSV')
    p.add_argument('csv'); p.add_argument('--output', default='report.html')
    args = p.parse_args()
    if Path(args.csv).resolve() == Path(args.output).resolve():
        p.exit(2, 'Entrada e saída devem ser arquivos diferentes.\n')
    try:
        data = analyze(args.csv)
        Path(args.output).write_text(render(data), encoding='utf-8')
        print(f'Relatório: {args.output} | Receita: R$ {data["total"]:.2f}')
    except (ValueError, OSError) as error:
        p.exit(2, f'Erro: {error}\n')

if __name__ == '__main__': main()
