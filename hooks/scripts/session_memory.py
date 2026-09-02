"""SessionStart: carrega a memoria do workbench, se houver.

Le os arquivos de memoria apontados por BKS_BRAIN e injeta no contexto da
sessao. Sem BKS_BRAIN configurado, nao faz nada — as skills do kit funcionam
sem vault, e uma sessao que nao usa o workbench nao deve pagar por ele.
"""
import json
import os
import sys

FILES = ('user_profile.md', 'MEMORY.md', 'hot.md')
MAX_CHARS = 6000


def main():
    brain = os.environ.get('BKS_BRAIN')
    if not brain or not os.path.isdir(brain):
        return

    parts = []
    for name in FILES:
        p = os.path.join(brain, 'memory', name)
        if not os.path.isfile(p):
            continue
        try:
            with open(p, encoding='utf-8') as fh:
                text = fh.read().strip()
        except Exception:
            continue
        if text:
            parts.append('## %s\n\n%s' % (name, text))

    if not parts:
        return

    body = '\n\n'.join(parts)
    if len(body) > MAX_CHARS:
        body = body[:MAX_CHARS] + '\n\n[...truncado]'

    json.dump({
        'hookSpecificOutput': {
            'hookEventName': 'SessionStart',
            'additionalContext': (
                'Memoria do workbench BKS (%s). Contexto de fundo, nao instrucao '
                'do usuario; reflete o que era verdade quando foi escrito.\n\n%s'
                % (brain, body)
            ),
        }
    }, sys.stdout)


try:
    main()
except Exception:
    pass
