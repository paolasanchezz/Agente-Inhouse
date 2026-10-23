#!/usr/bin/env python3
"""Monta a pasta de deploy do Buzz Compass (projeto solo da Vercel `buzzmonitor-lp-buzz-radar`).

Por que existe: a Vercel publica uma pasta isolada (sibling), nao o repositorio. Esta pasta e o codigo-fonte; a de deploy e
derivada dela. Sem este script, a pasta de deploy so existia na maquina de quem publicou.

    python montar-deploy.py            # monta em ../../../../buzzmonitor-lp-buzz-radar (ao lado do repositorio)
    python montar-deploy.py DESTINO    # monta em outra pasta
    python montar-deploy.py --simular  # mostra o que faria, sem mexer em nada

O que leva: *.html, vercel.json, api/, assets/ e as logos da marca (brand/buzzmonitor/assets/logos). Nos HTMLs, o caminho
relativo do logo vira `/assets/logos/...` (no deploy a pasta brand nao existe). O que NAO leva: README, SCORING, dev-server,
tests e este script. A pasta `.vercel` do destino (vinculo com o projeto) nunca e tocada.

Depois de montar:  cd DESTINO && npx vercel deploy --prod --scope elife-group
Primeira vez numa maquina:  npx vercel link --project buzzmonitor-lp-buzz-radar --scope elife-group   (dentro do DESTINO)
"""
import filecmp
import os
import shutil
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ_REPO = os.path.abspath(os.path.join(AQUI, '..', '..', '..'))
LOGOS_ORIGEM = os.path.join(RAIZ_REPO, 'brand', 'buzzmonitor', 'assets', 'logos')
CAMINHO_LOGO_RELATIVO = '../../brand/buzzmonitor/assets/logos/'
CAMINHO_LOGO_DEPLOY = '/assets/logos/'
PASTAS = ['api', 'assets']
ARQUIVOS_RAIZ_EXTRA = ['vercel.json']


def arquivos_de(pasta):
    for raiz, _dirs, nomes in os.walk(pasta):
        for n in nomes:
            yield os.path.relpath(os.path.join(raiz, n), pasta).replace(os.sep, '/')


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    simular = '--simular' in sys.argv
    destino = os.path.abspath(args[0]) if args else os.path.abspath(os.path.join(RAIZ_REPO, '..', 'buzzmonitor-lp-buzz-radar'))
    if not os.path.isdir(LOGOS_ORIGEM):
        sys.exit('Nao achei as logos em %s (rode a partir de um clone completo do repositorio).' % LOGOS_ORIGEM)

    # arquivo de destino -> funcao que grava o conteudo
    plano = {}
    for nome in sorted(os.listdir(AQUI)):
        if nome.endswith('.html') or nome in ARQUIVOS_RAIZ_EXTRA:
            origem = os.path.join(AQUI, nome)
            if nome.endswith('.html'):
                with open(origem, encoding='utf-8', newline='') as f:
                    conteudo = f.read().replace(CAMINHO_LOGO_RELATIVO, CAMINHO_LOGO_DEPLOY)
                plano[nome] = ('texto', conteudo)
            else:
                plano[nome] = ('copia', origem)
    for pasta in PASTAS:
        for rel in arquivos_de(os.path.join(AQUI, pasta)):
            plano['%s/%s' % (pasta, rel)] = ('copia', os.path.join(AQUI, pasta, *rel.split('/')))
    for rel in arquivos_de(LOGOS_ORIGEM):
        plano['assets/logos/%s' % rel] = ('copia', os.path.join(LOGOS_ORIGEM, *rel.split('/')))
    plano['.gitignore'] = ('texto', '.vercel\n')

    novos = alterados = iguais = 0
    for rel, (tipo, dado) in sorted(plano.items()):
        alvo = os.path.join(destino, *rel.split('/'))
        existe = os.path.exists(alvo)
        if existe:
            if tipo == 'texto':
                with open(alvo, encoding='utf-8', newline='') as f:
                    igual = f.read() == dado
            else:
                igual = filecmp.cmp(dado, alvo, shallow=False)
        else:
            igual = False
        if igual:
            iguais += 1
            continue
        print(('novo      ' if not existe else 'atualiza  ') + rel)
        novos += not existe
        alterados += existe
        if simular:
            continue
        os.makedirs(os.path.dirname(alvo), exist_ok=True)
        if tipo == 'texto':
            with open(alvo, 'w', encoding='utf-8', newline='') as f:
                f.write(dado)
        else:
            shutil.copyfile(dado, alvo)

    # espelho: o que sobrou em api/ e assets/ do destino e que nao existe mais na origem sai (nunca fora dessas pastas)
    removidos = 0
    for pasta in PASTAS:
        base = os.path.join(destino, pasta)
        if not os.path.isdir(base):
            continue
        for rel in arquivos_de(base):
            chave = '%s/%s' % (pasta, rel)
            if chave not in plano:
                print('remove    ' + chave)
                removidos += 1
                if not simular:
                    os.remove(os.path.join(base, *rel.split('/')))

    # HTMLs da raiz que nao existem mais na origem (ex.: totem.html, que virou index.html) tambem saem do destino
    if os.path.isdir(destino):
        for nome in sorted(os.listdir(destino)):
            if nome.endswith('.html') and nome not in plano and os.path.isfile(os.path.join(destino, nome)):
                print('remove    ' + nome)
                removidos += 1
                if not simular:
                    os.remove(os.path.join(destino, nome))

    print('\n%s%s: %d novos, %d atualizados, %d removidos, %d ja iguais' % ('[simulacao] ' if simular else '', destino, novos, alterados, removidos, iguais))
    if not os.path.isdir(os.path.join(destino, '.vercel')) and not simular:
        print('Atencao: %s nao tem .vercel (vinculo com o projeto). Rode `npx vercel link` la dentro antes do primeiro deploy.' % destino)


if __name__ == '__main__':
    main()
