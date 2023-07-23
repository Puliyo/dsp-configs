# python
import re
from pathlib import Path
# vendor
import requests
# self
from .logger import get_logger

URLs = [
    'https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts',
    'https://raw.githubusercontent.com/logroid/adaway-hosts/master/hosts.txt'
]

URL_ENTRY_PATTERN = re.compile(r'^(?:127|0)\.0\.0\.(?:1|0)[ \t]+([^\s]+)')

HOSTS = [
    'localhost', # start local domains
    'localhost.localdomain',
    'local',
    'broadcasthost',
    'ip6-localhost',
    'ip6-loopback',
    'ip6-localnet',
    'ip6-mcastprefix',
    'ip6-allnodes',
    'ip6-allrouters',
    'ip6-allhosts', # end local domains
    'm.dev.youlai.cn',
    'api.youlai.cn',
    'hao.youlai.cn',
    'm.youlai.cn',
    'www.youlai.cn',
    'qxmugen.com',
    'qw.2222wf.com',
    'www.mugen.net.cn',
    'jygd.bzjjxg.cn',
    'wb1.toolssp.com',
    'lg1.toolssp.com',
    'www.leeloe.com',
    'potapo.bbcoming.cn',
    'cn.audidaili.com',
    'scandal.p2pguancha.com',
    'www.china-tomatopaste.com',
    'www.winnerlifting.com',
    'winegometa.net',
    'www.sinovest-consulting.com',
    'www.meetco-furniture.com',
    'm.31b.app',
    'pan.iospro.cn',
    'spusdt.net',
    'youji.xlhapp.cn',
    'dye.52-tk.cn',
    '3.wejffji7892.cyou',
    'www.perfumeriasana.com',
    'wfdwssfd.wiujydgjgsi.club',
]

logger = get_logger(__name__)

def generate(path: str):
    path = Path(path)
    if path.is_dir():
        path = path / 'hosts.txt'

    hosts = set()
    
    # add hosts from manually defined hosts
    logger.info(f'adding defined hosts')
    for host in HOSTS:
        hosts.add(host)
    logger.info(f'current set size {len(hosts)}')

    # add hosts from urls
    logger.info(f'adding hosts from url')
    for url in URLs:
        logger.info(f'contacting {url=}')
        r = requests.get(url, stream=True)
        if r.status_code != 200:
            logger.error(f'{r.status_code=} {url}')
            continue
        for line in r.iter_lines():
            match = URL_ENTRY_PATTERN.search(line.decode('utf-8'))
            if match:
                hosts.add(match[1].strip())
        logger.info(f'current set size {len(hosts)}')

    # write to file
    logger.info(f'writing hosts to path {path}')
    with path.open('w', encoding='utf-8') as f:
        for host in hosts:
            f.write(f'{host}\n')
