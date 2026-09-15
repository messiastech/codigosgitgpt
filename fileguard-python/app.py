import argparse
import hashlib
import json
from pathlib import Path
import re

def scan(folder):
    root=Path(folder).resolve()
    if not root.is_dir(): raise ValueError('Pasta não encontrada.')
    files={}
    for path in sorted(root.rglob('*')):
        if path.is_symlink() or any(parent.is_symlink() for parent in path.parents) or not path.is_file(): continue
        digest=hashlib.sha256()
        with path.open('rb') as file:
            for chunk in iter(lambda:file.read(1024*1024),b''): digest.update(chunk)
        files[path.relative_to(root).as_posix()]=digest.hexdigest()
    return files

def check_location(folder, manifest):
    if Path(manifest).resolve().is_relative_to(Path(folder).resolve()):
        raise ValueError('Salve o inventário fora da pasta monitorada.')

def snapshot(folder, manifest):
    check_location(folder,manifest)
    data={'version':1,'algorithm':'sha256','files':scan(folder)}
    # Exclusive creation prevents accidental overwrite of an existing baseline.
    with open(manifest,'x',encoding='utf-8') as file: json.dump(data,file,indent=2,ensure_ascii=False)
    return len(data['files'])

def verify(folder,manifest):
    check_location(folder,manifest)
    data=json.loads(Path(manifest).read_text(encoding='utf-8'))
    if not isinstance(data,dict) or data.get('version')!=1 or data.get('algorithm')!='sha256' or not isinstance(data.get('files'),dict):
        raise ValueError('Inventário inválido.')
    before=data['files']
    if any(not isinstance(v,str) or not re.fullmatch('[0-9a-f]{64}',v) for v in before.values()): raise ValueError('Hash inválido.')
    after=scan(folder)
    return {'added':sorted(after.keys()-before.keys()),'removed':sorted(before.keys()-after.keys()),'changed':sorted(key for key in before.keys() & after.keys() if before[key]!=after[key])}

def main():
    p=argparse.ArgumentParser(description='Inventário e verificação SHA-256')
    p.add_argument('command',choices=['snapshot','verify']);p.add_argument('folder');p.add_argument('manifest')
    args=p.parse_args()
    try:
        if args.command=='snapshot': print(f'{snapshot(args.folder,args.manifest)} arquivos registrados.'); return 0
        result=verify(args.folder,args.manifest);print(json.dumps(result,indent=2,ensure_ascii=False));return int(any(result.values()))
    except (ValueError,OSError) as error: p.exit(2,f'Erro: {error}\n')

if __name__=='__main__': raise SystemExit(main())
