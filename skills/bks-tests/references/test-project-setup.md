## 📋 FASE 2: CRIAR OU MELHORAR PROJETO ÚNICO DE TESTES

### **Passo 2.1: Decisão - Criar Novo ou Melhorar Existente**

**IMPORTANTE:** O projeto de testes fica em `tests/[SolutionName].Tests/`, ao lado de `src/`, e
entra na mesma solution. A suíte de arquitetura fica dentro dele, em `Architecture/`.

**SE não existe projeto de testes COM xUnit:**

```bash
# CRIAR projeto de testes em tests/
dotnet new xunit -n [SolutionName].Tests -o tests/[SolutionName].Tests

# Adicionar projeto à solution
dotnet sln add tests/[SolutionName].Tests/[SolutionName].Tests.csproj

# Adicionar referências a TODOS os projetos principais que estão em src/
cd tests/[SolutionName].Tests
dotnet add reference ../../src/[ProjectName1]/[ProjectName1].csproj
dotnet add reference ../../src/[ProjectName2]/[ProjectName2].csproj
# ... adicionar todos os projetos em src/ que serão testados
cd ../..

# Verificar estrutura criada
ls -la src/ tests/
# Deve mostrar: src/[ProjectName1]/, src/[ProjectName2]/, tests/[SolutionName].Tests/
```

**SE existem MÚLTIPLOS projetos de teste:**

```markdown
**ATENÇÃO:** Existem múltiplos projetos de teste separados.

Ação recomendada:
1. Criar NOVO projeto consolidado em tests/[SolutionName].Tests/
2. Migrar testes existentes para estrutura unificada
3. Organizar em pastas Unit/, Integration/, Shared/ e Architecture/
4. Remover projetos antigos após migração

Deseja prosseguir com a consolidação? [aguardar confirmação]
```

**SE o projeto de testes existe dentro de src/:**

```bash
# VERIFICAR se o projeto de testes está em src/
if [ -d "src/[SolutionName].Tests" ]; then
    echo "ATENÇÃO: projeto de testes em src/; o lugar dele é tests/[SolutionName].Tests/."
    echo "Confirme com o usuário antes de mover."

    # MOVER projeto existente
    mkdir -p tests
    git mv src/[SolutionName].Tests tests/[SolutionName].Tests

    # ATUALIZAR a solution
    dotnet sln remove src/[SolutionName].Tests/[SolutionName].Tests.csproj
    dotnet sln add tests/[SolutionName].Tests/[SolutionName].Tests.csproj

    # ATUALIZAR referências entre projetos (de ../ para ../../src/)
    cd tests/[SolutionName].Tests
    dotnet remove reference ../[ProjectName1]/[ProjectName1].csproj
    dotnet add reference ../../src/[ProjectName1]/[ProjectName1].csproj
    cd ../..

    echo "✅ Projeto movido de src/ para tests/"
fi
```

**SE existe mas NÃO é xUnit:**

```markdown
**ATENÇÃO:** Projeto de testes usa [NUnit/MSTest].

Opções:
1. Migrar para xUnit (recomendado)
2. Continuar com framework existente

Decisão: [aguardar input do usuário]
```

### **Passo 2.2: Criar Estrutura Interna Organizada**

Criar estrutura de pastas DENTRO do projeto único em src/:

```bash
cd tests/[SolutionName].Tests

# Criar estrutura organizada internamente
mkdir -p Unit
mkdir -p Integration
mkdir -p Shared

# Estrutura Unit - espelha o projeto principal
mkdir -p Unit/Domain/Core/Entities
mkdir -p Unit/Domain/Core/ValueObjects
mkdir -p Unit/Domain/Core/Aggregates
mkdir -p Unit/Application/UseCases
mkdir -p Unit/Application/Services
mkdir -p Unit/Adapters/Outbound

# Estrutura Integration
mkdir -p Integration/API
mkdir -p Integration/Database
mkdir -p Integration/ExternalServices

# Shared - recursos compartilhados
mkdir -p Shared/Builders
mkdir -p Shared/Fixtures
mkdir -p Shared/Helpers
mkdir -p Shared/Mocks

cd ../..
```

**Estrutura final do projeto:**

```
src/
├── [ProjectName1]/
└── [ProjectName2]/
tests/
└── [SolutionName].Tests/          ← PROJETO DE TESTES AQUI
    ├── Unit/                       # TESTES UNITÁRIOS
    │   ├── Domain/
    │   │   ├── Core/
    │   │   │   ├── Entities/
    │   │   │   ├── ValueObjects/
    │   │   │   └── Aggregates/
    │   │   └── Exceptions/
    │   ├── Application/
    │   │   ├── UseCases/
    │   │   ├── Services/
    │   │   └── Validators/
    │   └── Adapters/
    │       ├── Inbound/
    │       └── Outbound/
    │
    ├── Integration/                # TESTES DE INTEGRAÇÃO
    │   ├── API/
    │   │   ├── Controllers/
    │   │   └── Endpoints/
    │   ├── Database/
    │   │   ├── Repositories/
    │   │   └── Migrations/
    │   └── ExternalServices/
    │       ├── Cache/
    │       └── MessageBus/
    │
    ├── Architecture/               # REGRAS DE ARQUITETURA COMO TESTE
    └── Shared/                     # RECURSOS COMPARTILHADOS
        ├── Builders/               # Test Data Builders
        ├── Fixtures/               # xUnit Fixtures
        ├── Helpers/                # Test Helpers
        └── Mocks/                  # Mock Factories
```

### **Passo 2.3: Instalar Pacotes Essenciais**

Para o projeto de teste ÚNICO em src/, garantir que tenha:

```bash
cd tests/[SolutionName].Tests

# Pacotes base xUnit
dotnet add package xunit --version 2.6.6
dotnet add package xunit.runner.visualstudio --version 2.5.6
dotnet add package Microsoft.NET.Test.Sdk --version 17.8.0

# Cobertura de código
dotnet add package coverlet.collector --version 6.0.0
dotnet add package coverlet.msbuild --version 6.0.0

# Mocking (assertions: Assert nativo do xUnit - NUNCA FluentAssertions)
dotnet add package Moq --version 4.20.70

# Geração de dados fake
dotnet add package Bogus --version 35.4.0

# Para testes de integração
dotnet add package Microsoft.AspNetCore.Mvc.Testing --version 8.0.0
dotnet add package Microsoft.EntityFrameworkCore.InMemory --version 8.0.0

# Voltar ao root
cd ../..
```

### **Passo 2.4: Configurar Coverage no .csproj**

Adicionar ao arquivo `tests/[SolutionName].Tests/[SolutionName].Tests.csproj`:

```xml
<Project Sdk="Microsoft.NET.Sdk">
  
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <ImplicitUsings>enable</ImplicitUsings>
    <Nullable>enable</Nullable>
    <IsPackable>false</IsPackable>
    <IsTestProject>true</IsTestProject>
    
    <!-- Configurações de Cobertura -->
    <CollectCoverage>true</CollectCoverage>
    <CoverletOutputFormat>cobertura,json,lcov,opencover</CoverletOutputFormat>
    <CoverletOutput>./TestResults/</CoverletOutput>
    <!-- Excluir o próprio projeto de testes e, se houver, os projetos de infraestrutura (<PADRAO>) -->
    <Exclude>[*.Tests]*,[*<PADRAO>*]*</Exclude>
    <ExcludeByAttribute>Obsolete,GeneratedCode,CompilerGenerated,ExcludeFromCodeCoverage</ExcludeByAttribute>
    <ExcludeByFile>**/*.Designer.cs,**/*.g.cs,**/*.g.i.cs,**/<PADRAO>*/**</ExcludeByFile>

    <!-- Thresholds de Cobertura - 90% -->
    <Threshold>90</Threshold>
    <ThresholdType>line,branch,method</ThresholdType>
    <ThresholdStat>total</ThresholdStat>
  </PropertyGroup>

  <!-- Resto do arquivo... -->
</Project>
```

### **Passo 2.5: Criar Arquivo de Configuração de Testes**

**Criar arquivo:** `tests/[SolutionName].Tests/xunit.runner.json`

```json
{
  "$schema": "https://xunit.net/schema/current/xunit.runner.schema.json",
  "methodDisplay": "method",
  "methodDisplayOptions": "all",
  "parallelizeAssembly": true,
  "parallelizeTestCollections": true,
  "maxParallelThreads": 4,
  "diagnosticMessages": false,
  "internalDiagnosticMessages": false
}
```

---

