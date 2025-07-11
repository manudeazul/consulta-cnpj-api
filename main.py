from fastapi import FastAPI
import httpx

app = FastAPI()

# Exemplo: usando a API pública do gov.br para consultar CNPJ
# Você pode trocar essa URL por qualquer outra
API_EXTERNA_URL = "https://open.cnpja.com/office/"
@app.get("/buscar/{cnpj}")
async def buscar_cnpj(cnpj: str):
    try:
        async with httpx.AsyncClient() as client:
            # Faz a requisição para a API externa usando o CNPJ no final da URL
            response = await client.get(f"{API_EXTERNA_URL}{cnpj}")
            response.raise_for_status()

            json = response.json()
            nome_empresa = json.get("company", {}).get("name")
            if nome_empresa:
                return {"razao_social": nome_empresa}
            else:
                return {"erro": "Campo 'company.name' não encontrado na resposta."}
    except httpx.HTTPError as e:
        return {"erro": str(e)}
