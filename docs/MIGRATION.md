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

# comandos duplicados no vault
<vault>/.claude/commands/{brain,canonize,new-project,prd,review}.md
```

Skills que nao fazem parte do kit — as especificas de um cliente ou motor proprietario —
permanecem locais em `~/.claude/skills/`.

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
