### **Passo 3.2: Estratégia de Geração de Testes**

Para CADA classe no projeto principal, seguir este processo:

#### **Template para Testes Unitários**

**Localização:** `tests/[SolutionName].Tests/Unit/[Namespace]/[ClassName]Tests.cs`

```csharp
using Moq;
using Xunit;
using [SolutionName].Tests.Shared.Builders;
using [SolutionName].Tests.Shared.Fixtures;

namespace [SolutionName].Tests.Unit.[SubNamespace];

/// <summary>
/// Testes unitários para [ClassName].
/// Cobertura de cenários: sucesso, falha, edge cases.
/// Meta de cobertura: 90%+
/// </summary>
public class [ClassName]Tests
{
    // Fixtures e Mocks
    private readonly Mock<IDependency1> _mockDependency1;
    private readonly Mock<IDependency2> _mockDependency2;
    private readonly [ClassName] _sut; // System Under Test

    public [ClassName]Tests()
    {
        // Arrange - Setup compartilhado
        _mockDependency1 = new Mock<IDependency1>();
        _mockDependency2 = new Mock<IDependency2>();
        
        _sut = new [ClassName](
            _mockDependency1.Object,
            _mockDependency2.Object
        );
    }

    [Fact]
    public async Task [MethodName1]_WithValidParameters_ReturnsSuccess()
    {
        // Arrange
        var input = [ClassName]Builder.CreateValid(); // Usando builder do Shared/
        _mockDependency1
            .Setup(x => x.Metodo(It.IsAny<TipoParam>()))
            .ReturnsAsync(valorEsperado);

        // Act
        var result = await _sut.[MethodName1](input);

        // Assert
        Assert.NotNull(result);
        Assert.True(result.IsSuccess);
        Assert.Equal(valorEsperado, result.Value);
        
        _mockDependency1.Verify(
            x => x.Metodo(It.IsAny<TipoParam>()), 
            Times.Once
        );
    }

    [Fact]
    public async Task [MethodName1]_WithNullParameter_ThrowsArgumentNullException()
    {
        // Arrange
        object? nullInput = null;

        // Act
        Func<Task> act = async () => await _sut.[MethodName1](nullInput!);

        // Assert
        var ex = await Assert.ThrowsAsync<ArgumentNullException>(act);
        Assert.Contains("parameter", ex.Message);
    }

    [Theory]
    [InlineData("")]
    [InlineData("   ")]
    [InlineData(null)]
    public async Task [MethodName1]_WithInvalidString_ReturnsFailure(string invalidString)
    {
        // Arrange & Act
        var result = await _sut.[MethodName1](invalidString);

        // Assert
        Assert.NotNull(result);
        Assert.True(result.IsFailure);
        Assert.Contains("inválid", result.Error);
    }

    [Fact]
    public async Task [MethodName1]_WhenDependencyFails_Propagates()
    {
        // Arrange
        var exception = new Exception("Erro na dependência");
        _mockDependency1
            .Setup(x => x.Metodo(It.IsAny<TipoParam>()))
            .ThrowsAsync(exception);
        var input = [ClassName]Builder.CreateValid();

        // Act
        Func<Task> act = async () => await _sut.[MethodName1](input);

        // Assert
        var ex = await Assert.ThrowsAsync<Exception>(act);
        Assert.Equal("Erro na dependência", ex.Message);
    }

}
```

#### **Template para Testes de Integração**

**Localização:** `tests/[SolutionName].Tests/Integration/API/[Feature]IntegrationTests.cs`

```csharp
using Microsoft.AspNetCore.Mvc.Testing;
using Microsoft.Extensions.DependencyInjection;
using Xunit;
using System.Net;
using System.Net.Http.Json;
using [SolutionName].Tests.Shared.Fixtures;

namespace [SolutionName].Tests.Integration.API;

/// <summary>
/// Testes de integração para [Endpoint/Feature].
/// Testa fluxo completo incluindo banco de dados, autenticação, etc.
/// Meta de cobertura: 90%+
/// </summary>
[Collection("IntegrationTests")]
public class [Feature]IntegrationTests : IClassFixture<CustomWebApplicationFactory>
{
    private readonly CustomWebApplicationFactory _factory;
    private readonly HttpClient _client;

    public [Feature]IntegrationTests(CustomWebApplicationFactory factory)
    {
        _factory = factory;
        _client = _factory.CreateClient();
    }

    [Fact]
    public async Task Post_[Endpoint]_WithValidData_Returns201Created()
    {
        // Arrange
        var requestData = new RequestDto
        {
            Campo1 = "valor válido",
            Campo2 = 123
        };

        // Act
        var response = await _client.PostAsJsonAsync("/api/[endpoint]", requestData);

        // Assert
        Assert.Equal(HttpStatusCode.Created, response.StatusCode);
        
        var result = await response.Content.ReadFromJsonAsync<ResponseDto>();
        Assert.NotNull(result);
        Assert.True(result!.Id > 0);
    }

    [Fact]
    public async Task Get_[Endpoint]_WithExistingItems_Returns200WithList()
    {
        // Arrange - Seed data
        await _factory.SeedDatabaseAsync();

        // Act
        var response = await _client.GetAsync("/api/[endpoint]");

        // Assert
        Assert.Equal(HttpStatusCode.OK, response.StatusCode);
        
        var result = await response.Content.ReadFromJsonAsync<List<ItemDto>>();
        Assert.NotEmpty(result);
        Assert.NotEmpty(result);
    }

    [Fact]
    public async Task Put_[Endpoint]_WithUnknownId_Returns404()
    {
        // Arrange
        var idInexistente = 99999;
        var updateData = new UpdateDto { /* ... */ };

        // Act
        var response = await _client.PutAsJsonAsync(
            $"/api/[endpoint]/{idInexistente}", 
            updateData
        );

        // Assert
        Assert.Equal(HttpStatusCode.NotFound, response.StatusCode);
    }
}
```

#### **Template para Shared Builder**

**Localização:** `tests/[SolutionName].Tests/Shared/Builders/[ClassName]Builder.cs`

```csharp
using Bogus;

namespace [SolutionName].Tests.Shared.Builders;

/// <summary>
/// Builder para criar instâncias de [ClassName] para testes.
/// Usado tanto em testes unitários quanto de integração.
/// </summary>
public static class [ClassName]Builder
{
    private static readonly Faker<[ClassName]> _faker = new Faker<[ClassName]>()
        .RuleFor(x => x.Propriedade1, f => f.Lorem.Word())
        .RuleFor(x => x.Propriedade2, f => f.Random.Int(1, 100))
        .RuleFor(x => x.Email, f => f.Internet.Email());

    public static [ClassName] CreateValid()
    {
        return _faker.Generate();
    }

    public static [ClassName] CreateInvalid()
    {
        var invalid = _faker.Generate();
        invalid.Propriedade1 = null; // Forçar invalidez
        return invalid;
    }

    public static [ClassName] CreateWith(Action<[ClassName]> customization)
    {
        var entity = CreateValid();
        customization(entity);
        return entity;
    }

    public static List<[ClassName]> CreateMany(int count = 3)
    {
        return _faker.Generate(count);
    }
}
```

#### **Template para Shared Fixture**

**Localização:** `tests/[SolutionName].Tests/Shared/Fixtures/CustomWebApplicationFactory.cs`

```csharp
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Mvc.Testing;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;

namespace [SolutionName].Tests.Shared.Fixtures;

/// <summary>
/// Factory customizada para testes de integração.
/// Compartilhada entre todos os testes de integração.
/// </summary>
public class CustomWebApplicationFactory : WebApplicationFactory<Program>
{
    protected override void ConfigureWebHost(IWebHostBuilder builder)
    {
        builder.ConfigureServices(services =>
        {
            // Remover DbContext real
            var descriptor = services.SingleOrDefault(
                d => d.ServiceType == typeof(DbContextOptions<AppDbContext>));
            
            if (descriptor != null)
                services.Remove(descriptor);

            // Adicionar DbContext InMemory
            services.AddDbContext<AppDbContext>(options =>
            {
                options.UseInMemoryDatabase("InMemoryDbForTesting");
            });

            // Build service provider
            var sp = services.BuildServiceProvider();

            // Garantir que banco está criado
            using var scope = sp.CreateScope();
            var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();
            db.Database.EnsureCreated();
        });
    }

    public async Task SeedDatabaseAsync()
    {
        using var scope = Services.CreateScope();
        var context = scope.ServiceProvider.GetRequiredService<AppDbContext>();
        
        // Limpar dados existentes
        context.Database.EnsureDeleted();
        context.Database.EnsureCreated();
        
        // Adicionar dados de teste usando Builders
        context.[Entity].AddRange(
            [ClassName]Builder.CreateMany(5)
        );
        
        await context.SaveChangesAsync();
    }
}

[CollectionDefinition("IntegrationTests")]
public class IntegrationTestsCollection : ICollectionFixture<CustomWebApplicationFactory>
{
    // Esta classe não tem código, apenas define a coleção xUnit
}
```

