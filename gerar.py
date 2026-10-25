import gzip
import os
import tempfile
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path

import requests

BASE = Path(__file__).resolve().parent
DESTINO = BASE / 'guides' / 'brasil.xml'
FONTES = [
    ('FreeEPG', 'https://www.free-epg.de/api/epg/br.xml.gz'),
    ('EPGShare01 (BR1)', 'https://epgshare01.online/epgshare01/epg_ripper_BR1.xml.gz'),
    ('EPGShare01 (BR2)', 'https://epgshare01.online/epgshare01/epg_ripper_BR2.xml.gz'),
]


def baixar(nome, url):
    print(f'\nBaixando {nome}: {url}', flush=True)
    resposta = requests.get(url, timeout=(20, 180), headers={'User-Agent': 'GamaTV-EPG/1.0'})
    resposta.raise_for_status()
    dados = resposta.content
    if dados.startswith(b'\x1f\x8b'):
        dados = gzip.decompress(dados)
    raiz = ET.fromstring(dados)
    if raiz.tag != 'tv':
        raise ValueError('A resposta não é XMLTV (raiz <tv> ausente).')
    canais = raiz.findall('channel')
    programas = raiz.findall('programme')
    if not canais or not programas:
        raise ValueError('XMLTV sem canais ou sem programas.')
    print(f'  OK: {len(canais)} canais e {len(programas)} programas')
    return raiz


def executar():
    DESTINO.parent.mkdir(parents=True, exist_ok=True)
    canais = {}
    programas = {}
    por_canal = defaultdict(int)
    sucesso = 0

    for nome, url in FONTES:
        try:
            raiz = baixar(nome, url)
            sucesso += 1
            for canal in raiz.findall('channel'):
                cid = canal.get('id')
                if cid and cid not in canais:
                    canais[cid] = canal
            for programa in raiz.findall('programme'):
                cid = programa.get('channel')
                if not cid:
                    continue
                # Deduplicação por conteúdo, mantém programas distintos
                # que tenham mesmo horário, mas informações diferentes
                chave = (cid, programa.get('start'), programa.get('stop'),
                         ET.tostring(programa, encoding='unicode'))
                if chave not in programas:
                    programas[chave] = programa
                    por_canal[cid] += 1
        except (requests.RequestException, OSError, ValueError, ET.ParseError, EOFError) as erro:
            print(f'  Falhou {nome}: {erro}')

    if sucesso == 0 or not programas:
        print('\nNenhuma fonte válida. Arquivo anterior preservado.')
        return

    # XMLTV exige declaração de canais para os IDs referenciados
    for cid in por_canal:
        if cid not in canais:
            canais[cid] = ET.Element('channel', {'id': cid})
            ET.SubElement(canais[cid], 'display-name').text = cid

    tv = ET.Element('tv', {'generator-info-name': 'GamaTV EPG Merge'})
    for cid in sorted(canais):
        tv.append(canais[cid])
    for chave in sorted(programas, key=lambda k: (k[0], k[1] or '', k[2] or '')):
        tv.append(programas[chave])

    fd, temporario = tempfile.mkstemp(prefix='brasil_', suffix='.xml', dir=DESTINO.parent)
    os.close(fd)
    try:
        ET.ElementTree(tv).write(temporario, encoding='utf-8', xml_declaration=True)
        ET.parse(temporario)  # valida antes de substituir
        os.replace(temporario, DESTINO)
    finally:
        if os.path.exists(temporario):
            os.unlink(temporario)

    print(f'\nArquivo gerado: {DESTINO}')
    print(f'Fontes utilizadas: {sucesso}/{len(FONTES)}')
    print(f'Canais: {len(canais)} | Programas: {len(programas)}')
    print(f'Tamanho: {DESTINO.stat().st_size / 1024 / 1024:.2f} MB')
    print('Observação: IDs diferentes para um mesmo canal foram preservados.')


if __name__ == '__main__':
    executar()
