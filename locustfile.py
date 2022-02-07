from locust import between, task, HttpUser
from json import load, loads
from random import choice


class CargaAtendimentoStatusCliente(HttpUser):

    wait_time = between(1.0, 3.0)

    ENDPOINT_PRIFIX_ATENDIMENTO = "/api/StatusCliente"
    COD_VENDEDOR = [
        "00511899",
        "00005095",
        "00015614"
    ]
    COD_CLIENTE = [
        "0001005443"
    ]

    @task  # (2) definir o peso = priorizacao de execucao.
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
                print(f"01 - Consulta cliente bloqueado e desbloqueado \n {resposta['meta']['count']}")
                if resposta["meta"]["count"] == 0:
                    response.failure(
                        "Count retornou = 0"
                    )
            except KeyError:
                print(f"01 - FALHA Consulta cliente bloq/desbloq. \n {response.text} \n Status Code: {response.status_code}")
                response.failure(
                    "Nao foi possivel acessar o valor meta.count"
                )
            #            if not response.status_code == 404:
            #                response.failure(f"O status da resposta foi {response.status_code}, que e o diferente do esperado 404")

    @task
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
                print(f"02 - Consulta status cliente \n {resposta['success']} \n {len(resposta['data'])} \n Status Code: {response.status_code}")
                if resposta["success"] != True and len(resposta["data"]) != 21:
                    response.failure(f"Corpo de resposta diferente do esperado: {response.text}")
            except KeyError:
                print(f"02 - FALHA busca cliente \n {response.text} \n Status code: {response.status_code}")
                response.failure(
                    "Nao foi possivel acessar os valores success/data"
                )
    
    @task
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
                    f"03 - Obter clientes montantes \n {resposta['success']} \n {len(resposta['data'])} \n Status Code: {response.status_code}")
                if resposta["success"] != True and len(resposta["data"]) != 24:
                    response.failure(
                        f"Corpo de resposta diferente do esperado: {response.text}")
            except KeyError:
                print(
                    f"03 - FALHA obter clientes montantes \n {response.text} \n Status code: {response.status_code}")
                response.failure(
                    "Nao foi possivel acessar os valores de data"
                )

        




# codigos = {COD_VENDEDOR:[COD_CLIENTE]}
# codigos[COD_VENDEDOR][0]