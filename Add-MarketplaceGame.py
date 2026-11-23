"""Stage an additional compatible game/demo/app and update the downloadable catalogue."""
import argparse, hashlib, json, re, shutil, zipfile
from pathlib import Path
from urllib.parse import urlparse, quote

p=argparse.ArgumentParser(description=__doc__)
p.add_argument('package',type=Path)
p.add_argument('--metadata',required=True,type=Path,help='JSON with id, title, category, runtimeId, executable, contentPath, contentKind')
p.add_argument('--catalogue',required=True,type=Path)
p.add_argument('--release-url',required=True,help='GitHub releases/download/<tag>/ URL')
p.add_argument('--output',required=True,type=Path)
a=p.parse_args()
g=json.loads(a.metadata.read_text(encoding='utf-8-sig'))
required=('id','title','category','runtimeId','executable','contentPath','contentKind')
if any(not g.get(k) for k in required):p.error('Missing metadata: '+', '.join(k for k in required if not g.get(k)))
if not re.fullmatch('[a-z0-9-]{1,100}',g['id']):p.error('Use a lowercase ID containing letters, numbers and hyphens.')
categories=['Xbox 360 Full Games','Xbox Indie Games','Xbox 360 Arcade','Original Xbox Games','Xbox 360 Demos','Xbox 360 Apps']
if g['category'] not in categories or g['contentKind'] not in ('game','demo','application'):p.error('Choose a supported category and content kind.')
base=urlparse(a.release_url)
if base.scheme!='https' or base.netloc!='github.com' or '/releases/download/' not in base.path or base.query or base.fragment:p.error('Use an HTTPS GitHub release download directory.')
if not a.package.is_file() or not zipfile.is_zipfile(a.package):p.error('Choose a ZIP-format game package.')
with zipfile.ZipFile(a.package) as z:
    names=set();total=0
    for e in z.infolist():
        name=e.filename.replace('\\','/')
        if name.startswith('/') or ':' in name or any(c in ('','..','.') for c in name.rstrip('/').split('/')):p.error('Unsafe package path: '+name)
        if name.lower() in names:p.error('Duplicate package path: '+name)
        names.add(name.lower());total+=e.file_size
        if any(c.lower() in ('gamesaves','savedata','eeprom.bin','.env','credentials.json','token.json') for c in name.split('/')):p.error('Remove personal data from the package: '+name)
    if g['executable'].lower() not in names:p.error('Executable is missing from the package.')
    if not any(n==g['contentPath'].lower() or n.startswith(g['contentPath'].lower().rstrip('/')+'/') for n in names):p.error('Content path is missing from the package.')
g['downloadBytes']=a.package.stat().st_size;g['installedBytes']=total
with a.package.open('rb') as f:g['sha256']=hashlib.file_digest(f,'sha256').hexdigest()
g['package']='';g.pop('downloadPageUrl',None);g.pop('downloadUrl',None);g.pop('downloadParts',None)
a.output.mkdir(parents=True,exist_ok=True)
base=a.release_url.rstrip('/')+'/'
name=g['id']+'.xbliggame'
limit=1500000000
if g['downloadBytes']<limit:
    dest=a.output/name
    if dest.resolve()!=a.package.resolve():shutil.copyfile(a.package,dest)
    g['downloadUrl']=base+quote(name)
else:
    g['downloadParts']=[]
    with a.package.open('rb') as src:
        left=g['downloadBytes'];index=1
        while left:
            size=min(left,limit);dest=a.output/(name+f'.part{index:02d}')
            digest=hashlib.sha256()
            with dest.open('wb') as dst:
                remaining=size
                while remaining:
                    chunk=src.read(min(1024*1024,remaining))
                    if not chunk:raise IOError('Package changed during staging')
                    dst.write(chunk);digest.update(chunk);remaining-=len(chunk)
            g['downloadParts'].append({'url':base+quote(dest.name),'bytes':size,'sha256':digest.hexdigest()})
            left-=size;index+=1
catalogue=json.loads(a.catalogue.read_text()) if a.catalogue.exists() else {'games':[]}
catalogue['games']=[old for old in catalogue['games'] if old['id']!=g['id']]+[g]
temp=a.catalogue.with_suffix('.json.new');temp.write_text(json.dumps(catalogue,indent=2)+'\n');temp.replace(a.catalogue)
print('Prepared '+g['title']+'. Upload the assets, then publish the updated catalogue.json. The matching runtime must already be supported by the Unity client.')
