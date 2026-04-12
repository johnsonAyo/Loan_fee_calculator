FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src
COPY ["LoanFeeCalculator.Api/LoanFeeCalculator.Api.csproj", "LoanFeeCalculator.Api/"]
RUN dotnet restore "LoanFeeCalculator.Api/LoanFeeCalculator.Api.csproj"
COPY . .
WORKDIR "/src/LoanFeeCalculator.Api"
RUN dotnet build "LoanFeeCalculator.Api.csproj" -c Release -o /app/build

FROM build AS publish
RUN dotnet publish "LoanFeeCalculator.Api.csproj" -c Release -o /app/publish

FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS final
WORKDIR /app
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "LoanFeeCalculator.Api.dll"]
