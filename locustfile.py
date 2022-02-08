from locust import between, task, HttpUser
from json import load, loads
from random import choice


class CargaTestsApisTina(HttpUser):

    wait_time = between(1.0, 3.0)

    ENDPOINT_PRIFIX_ATENDIMENTO = "/api/StatusCliente"
    ENDPOINT_PRIFIX_CUSTOMER_DEVOLUCOES = "/api/Devolucoes"
    ENDPOINT_PRIFIX_CUSTOMER_VOLUMECAPTADO = "/api/VolumeCaptado"
    COD_VENDEDOR = [
        "00511899",
        "00005095",
        "00015614"
    ]
    COD_VENDEDOR_CUSTOMER = [
        "00580849"
    ]
    COD_CLIENTE = [
        "0001005443"
    ]

# APIs Atendimento
# Status Cliente

#    @task  # (2) definir o peso = priorizacao de execucao.
    def busca_cli_des_bloq(self):

        consult_cliente_endpoint = f"{self.ENDPOINT_PRIFIX_ATENDIMENTO}/BuscaClientesBloqueadosDesbloqueados"
        body = {
            "codVendedor": choice(self.COD_VENDEDOR),
            "itensPorPagina": 30,
            "pagina": 1,
            "tipoCliente": "b",
            "search": ""
        }
        with self.client.post(url=consult_cliente_endpoint,
                              name="01 - Consulta cliente bloqueado e desbloqueado",
                              catch_response=True, json=body) as response:
            resposta = loads(response.text or "null")

            try:
                print(f"============= \n 01 - Consulta cliente bloqueado e desbloqueado \n {resposta['meta']['count']}")
                if resposta["meta"]["count"] == 0:
                    response.failure(
                        "Count retornou = 0"
                    )
            except KeyError:
                print(f"============= \n 01 - FALHA Consulta cliente bloq/desbloq. \n {response.text} \n Status Code: {response.status_code}")
                response.failure(
                    "Nao foi possivel acessar o valor meta.count"
                )

#    @task
    def busca_status_cliente(self):

        consult_client_endpoint = f"{self.ENDPOINT_PRIFIX_ATENDIMENTO}/BuscaStatusCliente"
        body = {
            "codCliente": self.COD_CLIENTE[0],
            "codVendedor": "00511899"
        }
        with self.client.post(url=consult_client_endpoint,
                              name="02 - Consulta status cliente",
                              catch_response=True, json=body) as response:
            resposta = loads(response.text or "null")

            try:
                print(f"============= \n 02 - Consulta status cliente \n {resposta['success']} \n {len(resposta['data'])} \n Status Code: {response.status_code}")
                if resposta["success"] != True and len(resposta["data"]) != 21:
                    response.failure(f"Corpo de resposta diferente do esperado: {response.text}")
            except KeyError:
                print(f"============= \n 02 - FALHA busca cliente \n {response.text} \n Status code: {response.status_code}")
                response.failure(
                    "Nao foi possivel acessar os valores success/data"
                )
    
#    @task
    def obter_cliente_montante(self):

        consult_client_endpoint = f"{self.ENDPOINT_PRIFIX_ATENDIMENTO}/ObterClientesMontantes"
        body = {
            "codVendedor": choice(self.COD_VENDEDOR),
            "itensPorPagina": 5,
            "pagina": 1,
            "search": ""
        }
        with self.client.post(url=consult_client_endpoint,
                              name="03 - Obter clientes montantes",
                              catch_response=True, json=body) as response:
            resposta = loads(response.text or "null")

            try:
                print(
                    f"============= \n 03 - Obter clientes montantes \n {resposta['success']} \n {len(resposta['data'])} \n Status Code: {response.status_code}")
                if resposta["success"] != True and len(resposta["data"]) != 24:
                    response.failure(
                        f"Corpo de resposta diferente do esperado: {response.text}")
            except KeyError:
                print(
                    f"============= \n 03 - FALHA obter clientes montantes \n {response.text} \n Status code: {response.status_code}")
                response.failure(
                    "Nao foi possivel acessar os valores de data"
                )

# APIs Customer
# Devoluções

#    @task
    def busca_devolucoes_categoria(self):

        consult_client_endpoint = f"{self.ENDPOINT_PRIFIX_CUSTOMER_DEVOLUCOES}/BuscarDevolucoesPorCategoria"
        body = {
           "codVendedor": self.COD_VENDEDOR_CUSTOMER[0],
           "codCliente": "",
           "periodo": "m",
           "categoriaGM": "LINGUICA FRESCA (DOMESTICA)"
        }
        with self.client.post(url=consult_client_endpoint,
                              name="01 - Busca devoluções por categorias",
                              catch_response=True, json=body) as response:
            resposta = loads(response.text or "null")

            try:
                print(
                    f"============= \n 01 - Busca devolucoes por categoria \n {resposta['success']} \n {len(resposta['data'])} \n Status Code: {response.status_code}")
                if resposta["success"] != True and len(resposta["data"]) != 5:
                    response.failure(
                        f"Corpo de resposta diferente do esperado: {response.text}")
            except KeyError:
                print(
                    f"============= \n 01 - FALHA ao obter resultado de devolucoes por categoria \n {response.text} \n Status code: {response.status_code}")
                response.failure(
                    "Nao foi possivel acessar os valores de data"
                )

#    @task
    def busca_devolucao_cliente(self):

        consult_client_endpoint = f"{self.ENDPOINT_PRIFIX_CUSTOMER_DEVOLUCOES}/BuscarDevolucoesPorCliente"
        body = {
           "codVendedor": self.COD_VENDEDOR_CUSTOMER[0],
           "codCliente": "0000091263",
           "periodo": "m"
        }
        with self.client.post(url=consult_client_endpoint,
                              name="02 - Busca devoluções por cliente",
                              catch_response=True, json=body) as response:
            resposta = loads(response.text or "null")

            try:
                print(
                    f"============= \n 02 - Busca devolucoes por cliente \n {resposta['success']} \n {len(resposta['data'])} \n Status Code: {response.status_code}")
                if resposta["success"] != True and len(resposta["data"]) != 7:
                    response.failure(
                        f"Corpo de resposta diferente do esperado: {response.text}")
            except KeyError:
                print(
                    f"============= \n 02 - FALHA ao obter resultado de devolucoes por cliente \n {response.text} \n Status code: {response.status_code}")
                response.failure(
                    "Nao foi possivel acessar os valores de data"
                )

#    @task
    def busca_devolucao_sku(self):

        consult_client_endpoint = f"{self.ENDPOINT_PRIFIX_CUSTOMER_DEVOLUCOES}/BuscarDevolucoesPorSKU"
        body = {
           "codVendedor": self.COD_VENDEDOR_CUSTOMER[0],
           "codCliente": "0000091263",
           "periodo": "m",
           "nome": "",
           "categoriaGM": "LINGUICA FRESCA (DOMESTICA)" 
        }
        with self.client.post(url=consult_client_endpoint,
                              name="03 - Busca devolucoes por SKU",
                              catch_response=True, json=body) as response:
            resposta = loads(response.text or "null")

            try:
                print(
                    f"============= \n 03 - Busca devolucoes por SKU \n {resposta['success']} \n {len(resposta['data'])} \n Status Code: {response.status_code}")
                if resposta["success"] != True and len(resposta["data"]) != 9:
                    response.failure(
                        f"Corpo de resposta diferente do esperado: {response.text}")
            except KeyError:
                print(
                    f"============= \n 03 - FALHA ao obter resultado de devolucoes por SKU \n {response.text} \n Status code: {response.status_code}")
                response.failure(
                    "Nao foi possivel acessar os valores de data"
                )

#    @task
    def soma_devolucoes(self):

        consult_client_endpoint = f"{self.ENDPOINT_PRIFIX_CUSTOMER_DEVOLUCOES}/GetSomaDevolucoes"
        body = {
           "codVendedor": self.COD_VENDEDOR_CUSTOMER[0],
           "codCliente": "0000091263" 
        }
        with self.client.post(url=consult_client_endpoint,
                              name="04 - Busca soma devoluções",
                              catch_response=True, json=body) as response:
            resposta = loads(response.text or "null")

            try:
                print(
                    f"============= \n 04 - Busca soma de devolucoes \n {resposta['success']} \n {len(resposta['data'])} \n Status Code: {response.status_code}")
                if resposta["success"] != True and len(resposta["data"]) != 5 and len(resposta["grafico"]) > 10:
                    response.failure(
                        f"Corpo de resposta diferente do esperado: {response.text}")
            except KeyError:
                print(
                    f"============= \n 04 - FALHA ao obter resultado da soma de devolucoes \n {response.text} \n Status code: {response.status_code}")
                response.failure(
                    "Nao foi possivel acessar os valores de data ou grafico"
                )

# Volume Captado

#    @task
    def soma_volume_captado(self):

        consult_client_endpoint = f"{self.ENDPOINT_PRIFIX_CUSTOMER_VOLUMECAPTADO}/GetSomaVolumeCaptado"
        body = {
           "codVendedor": "00307501",
           "dataDe": "2022-02-01T14:13:16.660Z",
           "dataAte": "2022-02-08T14:13:16.660Z" 
        }
        with self.client.post(url=consult_client_endpoint,
                              name="05 - Soma volume captado",
                              catch_response=True, json=body) as response:
            resposta = loads(response.text or "null")

            try:
                print(
                    f"============= \n 05 - Soma volume captado \n {resposta['success']} \n {len(resposta['data'])} \n Status Code: {response.status_code}")
                if resposta["success"] != True and len(resposta["data"]) != 4:
                    response.failure(
                        f"Corpo de resposta diferente do esperado: {response.text}")
            except KeyError:
                print(
                    f"============= \n 05 - FALHA ao obter resultado da soma de volume captado \n {response.text} \n Status code: {response.status_code}")
                response.failure(
                    "Nao foi possivel acessar os valores de data"
                )

#    @task
    def soma_categoria_volume_captado(self):

        consult_client_endpoint = f"{self.ENDPOINT_PRIFIX_CUSTOMER_VOLUMECAPTADO}/GetSomaCategoriaVolumeCaptado"
        body = {
           "codVendedor": "00333982",
           "dataDe": "2022-02-01T14:57:53.211Z",
           "dataAte": "2022-02-08T14:57:53.211Z",
           "categoriaGM": "EMPANADO (DOMESTICO)"   
        }
        with self.client.post(url=consult_client_endpoint,
                              name="06 - Soma categoria volume captado",
                              catch_response=True, json=body) as response:
            resposta = loads(response.text or "null")

            try:
                print(
                    f"============= \n 06 - Soma categoria volume captado \n {resposta['success']} \n {len(resposta['data'])} \n Status Code: {response.status_code}")
                if resposta["success"] != True and len(resposta["data"]) != 5:
                    response.failure(
                        f"Corpo de resposta diferente do esperado: {response.text}")
            except KeyError:
                print(
                    f"============= \n 06 - FALHA ao obter resultado da soma categoria de volume captado \n {response.text} \n Status code: {response.status_code}")
                response.failure(
                    "Nao foi possivel acessar os valores de data"
                )

    @task
    def busca_sku_volume_captado(self):

        consult_client_endpoint = f"{self.ENDPOINT_PRIFIX_CUSTOMER_VOLUMECAPTADO}/GetSKUVolumeCaptado"
        body = {
           "codVendedor": "00318256",
           "dataDe": "2022-02-01T17:43:12.923Z",
           "dataAte": "2022-02-08T17:43:12.923Z",
           "categoriaGM": "MARGARINA QUALY",
           "materialDescricao": "MARGARINA VEG.CREM.C/SAL QUALY 500G" 
        }
        with self.client.post(url=consult_client_endpoint,
                              name="07 - Busca volume captado por SKU",
                              catch_response=True, json=body) as response:
            resposta = loads(response.text or "null")

            try:
                print(
                    f"============= \n 07 - Busca volume captado por SKU \n {resposta['success']} \n {len(resposta['data'])} \n Status Code: {response.status_code}")
                if resposta["success"] != True and len(resposta["data"]) != 9:
                    response.failure(
                        f"Corpo de resposta diferente do esperado: {response.text}")
            except KeyError:
                print(
                    f"============= \n 07 - FALHA ao obter resultado da soma categoria de volume captado \n {response.text} \n Status code: {response.status_code}")
                response.failure(
                    "Nao foi possivel acessar os valores de data"
                )