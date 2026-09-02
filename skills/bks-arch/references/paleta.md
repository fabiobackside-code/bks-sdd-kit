# Paleta BKS

Derivada da marca Backside. As duas primeiras vieram do logotipo; as demais foram construidas no
mesmo nivel de saturacao para conviverem sem competir.

## Base — a marca

| Token | Hex | Origem |
|---|---|---|
| `bks-azul-claro` | `#98CBFF` | marca, 84,7% do logotipo |
| `bks-azul-escuro` | `#336698` | marca, contorno |

## Semantica — o que cada cor significa

Cor carrega significado. Um no verde e armazenamento, sempre; nao e "o verde ficou melhor ali".

| Papel | Preenchimento | Contorno | Texto | Para |
|---|---|---|---|---|
| **backend** | `#336698` | `#1F4266` | `#FFFFFF` | servico, API, worker, use case |
| **storage** | `#4A7C63` | `#2E5140` | `#FFFFFF` | banco, blob, filesystem, cache |
| **broker** | `#B5713C` | `#8A5228` | `#FFFFFF` | Kafka, RabbitMQ, fila, topico |
| **acesso** | `#9E4B4B` | `#733535` | `#FFFFFF` | gateway, ingress, canal externo, usuario |
| **componente** | `#B39038` | `#8A6E26` | `#1A1A1A` | biblioteca, SDK, DLL, pacote |
| **externo** | `#6B7280` | `#4B5563` | `#FFFFFF` | sistema de terceiro, fora da fronteira |
| **destaque** | `#98CBFF` | `#336698` | `#1A1A1A` | o no em foco do diagrama |

## Estrutura — fundo e texto

| Token | Claro | Escuro |
|---|---|---|
| fundo | `#FFFFFF` | `#14181D` |
| fundo de agrupamento | `#F4F6F8` | `#1C2229` |
| contorno de agrupamento | `#D5DBE1` | `#2E3742` |
| texto | `#1A1A1A` | `#E8EBEE` |
| texto secundario | `#5A6472` | `#9AA4B0` |
| linha | `#5A6472` | `#8A94A0` |

## Linhas

| Traco | Significa |
|---|---|
| continua | conexao direta, sincrona — quem chama espera resposta |
| pontilhada | fluxo assincrono — mensagem, evento, fila |
| espessa | caminho critico do diagrama |
| dupla | fronteira de confianca atravessada |

A distincao entre continua e pontilhada e a mais importante do diagrama. Um leitor que so olha as
linhas ja sabe onde estao os pontos de acoplamento temporal.

## Regras

**Sem cor viva.** Toda cor aqui esta dessaturada de proposito. Um diagrama de trinta nos em cor
saturada cansa antes de ser lido.

**Contraste minimo 4.5:1** entre texto e preenchimento. Os pares acima ja atendem.

**Cor nunca e a unica informacao.** Todo no tem rotulo. Quem imprime em preto e branco, ou nao
distingue cor, continua lendo o diagrama.

**Sete papeis, nao mais.** Se um elemento nao cabe em nenhum, ele provavelmente e um `externo` ou
nao deveria estar no diagrama.

## Verificacao

Antes de entregar um diagrama:

- [ ] cada cor corresponde ao papel semantico, nao a estetica
- [ ] linha pontilhada so onde o fluxo e realmente assincrono
- [ ] texto legivel sobre o preenchimento, em tema claro e escuro
- [ ] diagrama continua compreensivel em escala de cinza
