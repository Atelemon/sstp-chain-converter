#!/usr/bin/env python3
import concurrent.futures, datetime as dt, ipaddress, json, os, re, socket, sys
import urllib.parse, urllib.request
from pathlib import Path

BASE = 'https://sub.cmliussss.net/vpngate'
ENTRY = os.getenv('SSTP_ENTRY', '021063.xyz').strip()
COUNTRIES = ('US','JP','KR','RU','TW','HK','SG','GB','DE','CA','AU')
NAMES = {'US':['United States','美国','🇺🇸'], 'JP':['Japan','日本','🇯🇵'],
         'KR':['South Korea','韩国','🇰🇷'], 'RU':['Russia','俄罗斯','🇷🇺'],
         'TW':['Taiwan','台湾','🇹🇼'], 'HK':['Hong Kong','香港','🇭🇰'],
         'SG':['Singapore','新加坡','🇸🇬'], 'GB':['United Kingdom','英国','🇬🇧'],
         'DE':['Germany','德国','🇩🇪'], 'CA':['Canada','加拿大','🇨🇦'],
         'AU':['Australia','澳大利亚','🇦🇺']}
PATTERN = re.compile(r'^[\w.-]+(?::\d{1,5})?#(?:US|JP|KR|RU|TW|HK|SG|GB|DE|CA|AU) 链式SSTP代理\$sstp://\S+$')

def tokens():
    now = dt.datetime.now(dt.timezone.utc)
    result = []
    if os.getenv('VPNGATE_TIME_TOKENS','true') == 'true':
        result += [('Asia/Shanghai',(now+dt.timedelta(hours=8)).strftime('%Y%m%d%H%M%S')),
                   ('UTC',now.strftime('%Y%m%d%H%M%S'))]
    if os.getenv('VPNGATE_TOKEN','').strip():
        result.append(('configured',os.environ['VPNGATE_TOKEN'].strip()))
    return list({v:(k,v) for k,v in result}.values())

def get(url, timeout=16):
    req = urllib.request.Request(url, headers={'User-Agent':'sstp-chain-converter/1.0'})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        if resp.status != 200:
            raise ValueError('HTTP response error')
        raw = resp.read(2_000_001)
        if len(raw) > 2_000_000:
            raise ValueError('oversized response')
        return raw.decode('utf-8-sig', 'replace')

def country(note):
    found = []
    for code, words in NAMES.items():
        if any(w.casefold() in note.casefold() for w in words) or re.search(r'(?<![A-Za-z])'+code+r'(?![A-Za-z])',note,re.I):
            found.append(code)
    return found[0] if len(found)==1 else ''

def extract(raw):
    found = {}
    for line in raw.splitlines():
        text = line.strip()
        if not text.lower().startswith('sstp://'):
            continue
        endpoint, _, note = text.partition('#')
        try:
            u = urllib.parse.urlsplit(endpoint)
            if u.scheme != 'sstp' or not u.hostname or not u.username or not u.password or not u.port or u.path not in ('','/') or u.query or u.fragment:
                continue
            if not 1 <= u.port <= 65535 or not re.fullmatch(r'[A-Za-z0-9.-]+',u.hostname) or re.search(r'\s',endpoint):
                continue
            found[endpoint] = (u.hostname.lower(), country(urllib.parse.unquote(note)))
        except ValueError:
            continue
    return found

def resolve_country(host):
    try:
        ips = {x[4][0] for x in socket.getaddrinfo(host,None,type=socket.SOCK_STREAM)}
        ips = sorted(ip for ip in ips if ipaddress.ip_address(ip).is_global)
        if not ips:
            return ''
        ip = next((x for x in ips if ':' not in x), ips[0])
        data = json.loads(get('https://ipwho.is/'+urllib.parse.quote(ip,safe=''),timeout=9))
        c = data.get('country_code','') if data.get('success') else ''
        return c if c in COUNTRIES else ''
    except (OSError,ValueError):
        return ''

def read_nodes(path):
    file = Path(path)
    if not file.exists():
        return []
    rows = [x.strip() for x in file.read_text(encoding='utf8').splitlines() if x.strip()]
    if any(not PATTERN.fullmatch(row) for row in rows):
        raise ValueError('Invalid node in '+path)
    return rows

def refresh():
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9.:-]*',ENTRY):
        raise ValueError('Invalid entry host')
    records = None
    for mode,token in tokens():
        try:
            url = BASE+'?token='+urllib.parse.quote(token,safe='')
            parsed = extract(get(url))
            if not parsed:
                raise ValueError('Invalid SSTP response')
            records = parsed
            print('Verified subscription:',mode,'nodes=',len(parsed))
            break
        except (OSError,ValueError) as exc:
            print('Rejected token mode:',mode,'error=',type(exc).__name__,file=sys.stderr)
    if not records:
        raise ValueError('No valid SSTP subscription; previous collection preserved')
    hosts = sorted({host for host,region in records.values() if not region})
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        regions = dict(zip(hosts,pool.map(resolve_country,hosts)))
    rows = []
    for endpoint,(host,hint) in records.items():
        c = hint or regions.get(host,'')
        if c in COUNTRIES:
            rows.append(f'{ENTRY}#{c} 链式SSTP代理'+'$'+endpoint)
    if not rows:
        raise ValueError('No recognized countries; previous collection preserved')
    Path('nodes-auto.txt').write_text('\n'.join(rows)+'\n',encoding='utf8')
    print('Auto nodes:,len(rows),'skipped:',len(records)-len(rows))

if __name__ == '__main__':
    try:
        refresh()
    except Exception as exc:
        print('Update failed:',exc,file=sys.stderr)
        sys.exit(1)
