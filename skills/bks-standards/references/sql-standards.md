# Padrões SQL — formato de procedure e function (SQL Server)

O banco guarda o texto de cada procedure e function como foi escrito. É esse texto que quem mantém lê
no `sp_helptext` ou na `e`, a procedure que imprime um objeto para edição. Por isso o texto segue um
formato fixo, que se lê coluna a coluna e não depende de editor.

O formato vem das procedures do SPA (Sistema Padrão de Agência), o legado bancário em que ele nasceu.
Vale para procedure e function nova e para toda alteração. Um projeto pode sobrescrever qualquer
regra em `brain/engineering/`.

## 1. As regras

1. **Quebra de linha do Windows (CRLF) no arquivo inteiro.** Linha só com avanço de linha (LF) sai
   emendada na `e`. O `.gitattributes` do repositório fixa `*.sql text eol=crlf`.
2. **Uma linha por item, com a vírgula à esquerda.** Vale para parâmetro, variável de `DECLARE`,
   atribuição de `SELECT`, coluna de `OPENJSON` e de `FOR JSON`, coluna e valor de
   `INSERT ... VALUES` e coluna do `SET` de `UPDATE`. A tabela de valores (`FROM (VALUES ...)`) fica
   com uma linha por tupla.
3. **Colunas alinhadas.** Nome, tipo, padrão e `OUTPUT` de cada parâmetro começam na mesma coluna.
   Referência: nome até a coluna 32, tipo até a 47.
4. **Chamada nomeada.** `EXEC proc @parametro = valor`, um argumento por linha e o `=` alinhado. A
   chamada não depende da ordem dos parâmetros da procedure chamada.
5. **Variáveis no início.** As variáveis usadas em mais de um bloco são declaradas juntas, logo depois
   das constantes, agrupadas pelo bloco que as preenche. A de uso pontual (uma mensagem de recusa, um
   envelope, o número do erro no `CATCH`) fica no bloco que a usa.
6. **Valor inicial calculado fica no lugar.** Ao subir um `DECLARE @x T = expr`, a declaração sobe e
   o valor vira `SET @x = expr` no ponto original. Em T-SQL a variável vale para o lote inteiro: subir
   a declaração não muda o comportamento; mover o cálculo pode mudar.
7. **Régua de traços** antes e depois do `CREATE` e em volta de cada bloco numerado.
8. **Uma linha em branco antes de cada `IF`**, salvo logo depois de `BEGIN` ou do comentário que o
   introduz, e nunca em `ELSE IF`.
9. **Documentação dentro do lote.** O cabeçalho que explica o objeto fica depois do `GO` do `DROP`,
   colado ao `CREATE`. Assim ele é gravado no banco e aparece na `e`. Comentário antes do `DROP` fica
   só no arquivo.

## 2. Exemplo

Antes, tudo amontoado:

```sql
DECLARE @ContaExiste BIT = 0, @TR SMALLINT, @Situacao TINYINT;
SELECT @ContaExiste = 1, @TR = c.TR, @Situacao = c.Situacao
  FROM dbo.Conta c WHERE c.Agencia = @Agencia AND c.NumeroConta = @Conta;
EXEC dbo.spxConsultaCartao @Produto, @Agencia, @Conta, @Consultado OUTPUT, @Encontrado OUTPUT;
```

Depois:

```sql
    DECLARE @ContaExiste                BIT
           ,@TR                         SMALLINT
           ,@Situacao                   TINYINT;
    ...
        SET @ContaExiste = 0;

        SELECT @ContaExiste = 1
              ,@TR          = c.TR
              ,@Situacao    = c.Situacao
          FROM dbo.Conta c
         WHERE c.Agencia     = @Agencia
           AND c.NumeroConta = @Conta;

        EXEC dbo.spxConsultaCartao @pProdutoId     = @Produto
                                  ,@pAgenciaConta  = @Agencia
                                  ,@pNumeroConta   = @Conta
                                  ,@pConsultado    = @Consultado  OUTPUT
                                  ,@pEncontrado    = @Encontrado  OUTPUT;
```

Esqueleto de procedure:

```sql
DROP PROCEDURE IF EXISTS dbo.spxExemplo;
GO

/* cabecalho: o que e, entrada, saida, erros, quem le e quem escreve */

------------------------------------------------------------------------------------------------------------------------
CREATE PROCEDURE dbo.spxExemplo
------------------------------------------------------------------------------------------------------------------------
 @pInstituicaoId                SMALLINT
,@pAgencia                      SMALLINT       = NULL  OUTPUT
,@pMsgErro                      VARCHAR(8000)          OUTPUT
AS
BEGIN
    SET NOCOUNT ON;
    --------------------------------------------------------------------------------------------------------------------

    DECLARE @Variavel                   INT;
    ...
END
GO
```

## 3. As ferramentas

Ficam em `tools/sql/`, ao lado desta referência. Copie para o repositório do projeto, por exemplo em
`scripts/banco/`.

| Ferramenta | O que faz |
|---|---|
| `e.sql` | cria a `dbo.e`: `EXEC e 'objeto'` imprime o `DROP IF EXISTS`, o texto linha a linha e os `GRANT`; tabela sai como `CREATE TABLE` montado pelas colunas. Lê `sys.sql_modules` e corta em LF, com ou sem CR |
| `Conferir-Formato.ps1` | acusa item amontoado na linha (`DECLARE`, `SELECT`, argumento, `INSERT`, `VALUES`, `SET`) e `EXEC` posicional. Zero achado é a condição para levar o arquivo ao banco |
| `Comparar-Layout.ps1` | prova que uma reformatação não mudou a lógica. Compara os tokens de cada arquivo com a versão do git, sem espaço nem comentário. Leva o `EXEC` à forma nomeada pela assinatura da procedure chamada e conta o `DECLARE` como conjunto de variáveis. Recusa linha sem CR |

Uso, na raiz do repositório, em Windows PowerShell 5.1 ou superior:

```powershell
scripts/banco/Conferir-Formato.ps1 -Pasta app/sql/minhabase
scripts/banco/Comparar-Layout.ps1 -Raizes app/sql
```

O `Comparar-Layout` lê as assinaturas das procedures nos próprios scripts. Passe em `-Raizes` todas
as pastas cujas procedures são chamadas, inclusive as de outra base. Rode pela janela do PowerShell:
chamado de outro shell, o console pode trocar a codificação dos acentos e acusar divergência falsa.

## 4. Reformatar um conjunto existente

1. Fixe o `*.sql text eol=crlf` no `.gitattributes`.
2. Reescreva um piloto à mão e aprove o formato pela `e`.
3. Reformate o resto. Cada arquivo só passa com `igual` no `Comparar-Layout` e zero achado no
   `Conferir-Formato`. Os dois portões tornam seguro dividir o trabalho entre agentes.
4. Aplique numa transação, com backup das definições. Function `WITH SCHEMABINDING` não se derruba
   enquanto outra a referencia: derrube em rodadas as que ninguém referencia
   (`sys.sql_expression_dependencies` com `is_schema_bound_reference = 1`) e recrie na ordem inversa.
5. Ao dividir o script nos `GO`, consuma a quebra de linha que segue cada um. Senão o texto gravado
   começa com um LF solto.
6. Confira o texto gravado: `OBJECT_DEFINITION` igual ao arquivo, sem linha sem CR.
