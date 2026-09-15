import argparse,csv,json
from datetime import date

def validate_contract(contract):
    if not isinstance(contract,dict) or set(contract)-{'columns','min_rows'}:raise ValueError('Contrato inválido.')
    columns=contract.get('columns')
    if not isinstance(columns,dict) or not columns:raise ValueError('Contrato precisa de columns.')
    if type(contract.get('min_rows',0)) is not int or contract.get('min_rows',0)<0:raise ValueError('min_rows inválido.')
    for name,rules in columns.items():
        if not name or not isinstance(rules,dict) or set(rules)-{'required','unique','type','min'}:raise ValueError('Regra desconhecida.')
        if rules.get('type','string') not in ('string','integer','date'):raise ValueError('Tipo desconhecido.')
        for flag in ('required','unique'):
            if flag in rules and type(rules[flag]) is not bool:raise ValueError('Regra booleana inválida.')
        if 'min' in rules and (rules.get('type')!='integer' or type(rules['min']) is not int):raise ValueError('min exige tipo integer.')
    return columns

def validate(source,contract):
    columns=validate_contract(contract); errors=[]; seen={key:set() for key in columns};count=0
    def error(line,field,message):errors.append({'line':line,'field':field,'message':message})
    with open(source,encoding='utf-8-sig',newline='') as file:
        reader=csv.DictReader(file)
        if not reader.fieldnames or len(set(reader.fieldnames))!=len(reader.fieldnames) or set(reader.fieldnames)!=set(columns):
            return {'valid':False,'rows':0,'errors':[{'line':1,'field':'*','message':'Cabeçalho incompatível com contrato.'}]}
        for line,row in enumerate(reader,2):
            count+=1
            if None in row or any(value is None for value in row.values()):error(line,'*','Quantidade de colunas inválida.');continue
            for field,rules in columns.items():
                value=row[field].strip()
                if not value:
                    if rules.get('required'):error(line,field,'Campo obrigatório.')
                    continue
                if rules.get('unique'):
                    if value in seen[field]:error(line,field,'Valor duplicado.')
                    seen[field].add(value)
                try:
                    if rules.get('type')=='integer':
                        number=int(value)
                        if 'min' in rules and number<rules['min']:error(line,field,'Valor abaixo do mínimo.')
                    elif rules.get('type')=='date':date.fromisoformat(value)
                except ValueError:error(line,field,'Tipo ou formato inválido.')
    if count<contract.get('min_rows',0):error(1,'*','Quantidade de registros abaixo do mínimo.')
    return {'valid':not errors,'rows':count,'errors':errors}

def main():
    p=argparse.ArgumentParser(description='Validação CSV por contrato JSON');p.add_argument('source');p.add_argument('contract');args=p.parse_args()
    try:
        with open(args.contract,encoding='utf-8') as file:contract=json.load(file)
        result=validate(args.source,contract);print(json.dumps(result,ensure_ascii=False,indent=2));return 0 if result['valid'] else 1
    except (ValueError,OSError) as error:p.exit(2,f'Erro: {error}\n')
if __name__=='__main__':raise SystemExit(main())
