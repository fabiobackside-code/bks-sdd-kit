/* ===========================================================================
   OBJETO      : dbo.e  (PROCEDURE)
   DESCRICAO   : Imprime o script de um objeto para edicao, como a e do SPA: o bloco de DROP, o texto
                 como o banco o guarda, linha a linha, e os GRANT. Tabela sai como CREATE TABLE montado
                 pelas colunas. Le sys.sql_modules e corta a linha em LF, com ou sem CR.
   PARAM IN    : @objname   nome do objeto, com ou sem esquema
   RETORNO     : 0 sucesso; 1 objeto inexistente, de outra base ou sem texto
   =========================================================================== */

DROP PROCEDURE IF EXISTS dbo.e;
GO

------------------------------------------------------------------------------------------------------------------------
CREATE PROCEDURE dbo.e
------------------------------------------------------------------------------------------------------------------------
 @objname                       NVARCHAR(776)
AS
BEGIN
    SET NOCOUNT ON;
    --------------------------------------------------------------------------------------------------------------------

    DECLARE @intObjeto              INT
           ,@chrTipo                CHAR(2)
           ,@vchTipo                VARCHAR(20)
           ,@nvcNome                NVARCHAR(300)
           ,@nvcTexto               NVARCHAR(MAX)
           ,@nvcLinha               NVARCHAR(MAX)
           ,@intInicio              INT
           ,@intFim                 INT
           ,@nvcPrefixo             NVARCHAR(4);

    IF PARSENAME(@objname, 3) IS NOT NULL AND PARSENAME(@objname, 3) <> DB_NAME()
    BEGIN
        RAISERROR(15250, -1, -1);
        RETURN 1;
    END

    SELECT @intObjeto = o.object_id
          ,@chrTipo   = o.type
          ,@nvcNome   = QUOTENAME(SCHEMA_NAME(o.schema_id)) + N'.' + QUOTENAME(o.name)
      FROM sys.objects o
     WHERE o.object_id = OBJECT_ID(@objname);

    IF @intObjeto IS NULL
    BEGIN
        DECLARE @nvcBase SYSNAME = DB_NAME();
        RAISERROR(15009, -1, -1, @objname, @nvcBase);
        RETURN 1;
    END

    SET @vchTipo = CASE @chrTipo
                       WHEN 'U'  THEN 'TABLE'
                       WHEN 'V'  THEN 'VIEW'
                       WHEN 'P'  THEN 'PROCEDURE'
                       WHEN 'FN' THEN 'FUNCTION'
                       WHEN 'IF' THEN 'FUNCTION'
                       WHEN 'TF' THEN 'FUNCTION'
                       WHEN 'TR' THEN 'TRIGGER'
                       ELSE 'OBJECT'
                   END;

    PRINT N'DROP ' + @vchTipo + N' IF EXISTS ' + @nvcNome + N';';
    PRINT N'GO';
    PRINT N'';

    IF @chrTipo <> 'U'
    BEGIN
        SELECT @nvcTexto = m.definition
          FROM sys.sql_modules m
         WHERE m.object_id = @intObjeto;

        IF @nvcTexto IS NULL
        BEGIN
            IF EXISTS (SELECT 1 FROM sys.sql_modules WHERE object_id = @intObjeto)
                PRINT N'O texto do objeto esta cifrado.';
            ELSE
                RAISERROR(15197, -1, -1, @objname);
            RETURN 1;
        END

        -- Uma linha por LF; o CR que sobra no fim da linha sai.
        SET @intInicio = 1;
        WHILE @intInicio <= LEN(@nvcTexto + N'x') - 1
        BEGIN
            SET @intFim = CHARINDEX(NCHAR(10), @nvcTexto, @intInicio);
            IF @intFim = 0 SET @intFim = LEN(@nvcTexto + N'x');
            SET @nvcLinha = SUBSTRING(@nvcTexto, @intInicio, @intFim - @intInicio);
            IF RIGHT(@nvcLinha, 1) = NCHAR(13) SET @nvcLinha = LEFT(@nvcLinha, LEN(@nvcLinha + N'x') - 2);
            PRINT @nvcLinha;
            SET @intInicio = @intFim + 1;
        END
    END
    ELSE
    BEGIN
        PRINT N'CREATE TABLE ' + @nvcNome;
        PRINT N'(';
        SET @nvcPrefixo = N'    ';

        DECLARE @nvcColuna NVARCHAR(MAX);
        DECLARE curColuna CURSOR LOCAL FAST_FORWARD FOR
            SELECT LEFT(x.Coluna + REPLICATE(N' ', 32), CASE WHEN LEN(x.Coluna) > 31 THEN LEN(x.Coluna) + 1 ELSE 32 END)
                 + x.Tipo
                 + CASE
                       WHEN x.Tipo IN (N'varchar', N'char', N'varbinary', N'binary')
                           THEN N'(' + CASE WHEN c.max_length = -1 THEN N'MAX' ELSE CONVERT(NVARCHAR(10), c.max_length) END + N')'
                       WHEN x.Tipo IN (N'nvarchar', N'nchar')
                           THEN N'(' + CASE WHEN c.max_length = -1 THEN N'MAX' ELSE CONVERT(NVARCHAR(10), c.max_length / 2) END + N')'
                       WHEN x.Tipo IN (N'decimal', N'numeric')
                           THEN N'(' + CONVERT(NVARCHAR(10), c.precision) + N',' + CONVERT(NVARCHAR(10), c.scale) + N')'
                       WHEN x.Tipo IN (N'datetime2', N'time', N'datetimeoffset')
                           THEN N'(' + CONVERT(NVARCHAR(10), c.scale) + N')'
                       ELSE N''
                   END
                 + CASE WHEN c.is_identity = 1 THEN N' IDENTITY' ELSE N'' END
                 + CASE WHEN c.is_nullable = 1 THEN N' NULL' ELSE N' NOT NULL' END
              FROM sys.columns c
              JOIN sys.types   t ON t.user_type_id = c.user_type_id
             CROSS APPLY (SELECT QUOTENAME(c.name) COLLATE DATABASE_DEFAULT AS Coluna
                                ,t.name            COLLATE DATABASE_DEFAULT AS Tipo) x
             WHERE c.object_id = @intObjeto
             ORDER BY c.column_id;

        OPEN curColuna;
        FETCH NEXT FROM curColuna INTO @nvcColuna;
        WHILE @@FETCH_STATUS = 0
        BEGIN
            PRINT @nvcPrefixo + @nvcColuna;
            SET @nvcPrefixo = N'   ,';
            FETCH NEXT FROM curColuna INTO @nvcColuna;
        END
        CLOSE curColuna;
        DEALLOCATE curColuna;

        PRINT N')';
    END

    PRINT N'GO';

    -- Os GRANT do objeto, um por linha.
    DECLARE @nvcGrant NVARCHAR(MAX);
    DECLARE curGrant CURSOR LOCAL FAST_FORWARD FOR
        SELECT N'GRANT ' + p.permission_name COLLATE DATABASE_DEFAULT + N' ON ' + @nvcNome
             + N' TO ' + QUOTENAME(u.name) COLLATE DATABASE_DEFAULT
          FROM sys.database_permissions p
          JOIN sys.database_principals  u ON u.principal_id = p.grantee_principal_id
         WHERE p.major_id = @intObjeto
           AND p.class    = 1
           AND p.state    = 'G'
         ORDER BY u.name, p.permission_name;

    OPEN curGrant;
    FETCH NEXT FROM curGrant INTO @nvcGrant;
    IF @@FETCH_STATUS = 0 PRINT N'';
    WHILE @@FETCH_STATUS = 0
    BEGIN
        PRINT @nvcGrant;
        FETCH NEXT FROM curGrant INTO @nvcGrant;
    END
    CLOSE curGrant;
    DEALLOCATE curGrant;

    RETURN 0;
END
GO
