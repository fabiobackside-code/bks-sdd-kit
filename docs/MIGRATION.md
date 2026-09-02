# Migracao — de instalacao solta para o plugin

## Situacao anterior

As pecas do kit viviam em tres lugares:

- skills em `~/.claude/skills/bks-*`
- comandos em `~/.claude/commands/`, com cinco deles duplicados byte-a-byte no `.claude/commands/`
  do vault
- agentes em `brain/_bks-ai/agents/`, invocados por caminho — invisiveis ao seletor de subagentes

Nenhum dos tres era versionado. Editar um comando deixava a copia gemea desatualizada em silencio.

## Depois

Tudo vem do plugin. As copias locais saem.

## Passos

### 1. Instalar o plugin

```
/plugin marketplace add fabiobackside-code/bks-sdd-kit
/plugin install bks-sdd-kit@bks-sdd-kit
```

### 2. Configurar o vault

Em `~/.claude/settings.json`, no bloco `env`:

```json
{
  "env": {
    "BKS_VAULT": "D:/caminho/do/vault",
    "BKS_BRAIN": "D:/caminho/do/vault/brain/_bks-ai",
    "BKS_REPOS": "D:/caminho/do/vault/repos"
  }
}
```

### 3. Remover as copias antigas

Faca backup antes — estas pastas nao estavam versionadas.

```
# skills globais
~/.claude/skills/bks-sdd
~/.claude/skills/bks-dotnet-solutions
~/.claude/skills/bks-typescript-solutions
~/.claude/skills/bks-create-plan-tasks

# comandos globais
~/.claude/commands/{arch,brain,canonize,loop,new-project,note,prd,review,save,spec}.md

# virou a skill bks-tests
~/.claude/commands/CLAUDE-TESTS.md

# comandos duplicados no vault
<vault>/.claude/commands/{brain,canonize,new-project,prd,review}.md
```

Skills que nao fazem parte do kit — as especificas de um cliente ou motor proprietario —
permanecem locais em `~/.claude/skills/`.

### 3b. Saber o que muda no dia a dia

O plugin traz guardas que **recusam escrita** em `.cs`, coisa que a instalacao anterior nao tinha:

- codigo com `MediatR` ou dispatcher equivalente e recusado
- bloco de comentario acima de cinco linhas, ou com marca de severidade, e recusado
- arquivo que declara tipo publico e recusado enquanto `README.md` e `ARCHITECTURE.md` nao
  estiverem entre as mudancas pendentes do repositorio

Em repositorio legado isso aparece na primeira edicao. Se a intencao for migrar aos poucos, o
caminho e desabilitar o hook em `settings.json` do projeto ate a base estar em conformidade — nao
contornar a regra arquivo a arquivo.

Os guardas exigem `python` no PATH.

### 4. Verificar

```
/plugin
```

As quatro skills, dez comandos e quatro agentes devem aparecer sob `bks-sdd-kit`. Rode `/brain`
para confirmar que as variaveis do vault resolvem.

## Se algo quebrar

O plugin e aditivo: desinstalar devolve o estado anterior, desde que o backup do passo 3 exista.

```
/plugin uninstall bks-sdd-kit@bks-sdd-kit
```
