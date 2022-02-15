from asyncio import Task
import gevent
from locust import between, task, HttpUser, tag
from locust.env import Environment
from json import loads
from random import choice


mensagemFalha = "Nao foi possivel acessar o valor de data"

class CargaApiAtendimento(HttpUser):

    host = "https://brf-api-pim-attendance-dev.azurewebsites.net"
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
                              name="CargaApiAtendimento 01 - Consulta cliente bloqueado e desbloqueado",
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
                    mensagemFalha
                )

    @task
    def busca_status_cliente(self):

        consult_client_endpoint = f"{self.ENDPOINT_PRIFIX_ATENDIMENTO}/BuscaStatusCliente"
        body = {
            "codCliente": self.COD_CLIENTE[0],
            "codVendedor": "00511899"
        }
        with self.client.post(url=consult_client_endpoint,
                              name="CargaApiAtendimento 02 - Consulta status cliente",
                              catch_response=True, json=body) as response:
            resposta = loads(response.text or "null")

            try:
                print(f"============= \n 02 - Consulta status cliente \n {resposta['success']} \n {len(resposta['data'])} \n Status Code: {response.status_code}")
                if resposta["success"] != True and len(resposta["data"]) != 21:
                    response.failure(f"Corpo de resposta diferente do esperado: {response.text}")
            except KeyError:
                print(f"============= \n 02 - FALHA busca cliente \n {response.text} \n Status code: {response.status_code}")
                response.failure(
                    mensagemFalha
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
                              name="CargaApiAtendimento 03 - Obter clientes montantes",
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
                    mensagemFalha
                )

class CargaApiCustomer(HttpUser):

    host = "https://brf-api-pim-customer-dev.azurewebsites.net"
    wait_time = between(1.0, 3.0)

    ENDPOINT_PRIFIX_CUSTOMER_DEVOLUCOES = "/api/Devolucoes"
    ENDPOINT_PRIFIX_CUSTOMER_VOLUMECAPTADO = "/api/VolumeCaptado"
    ENDPOINT_PRIFIX_CUSTOMER_MIXUSUAL = "/api/MixUsual"
    ENDPOINT_PRIFIX_CUSTOMER_STATUS_PEDIDO = "/api/StatusPedidos"
    ENDPOINT_PRIFIX_CUSTOMER_PEDIDOS_RECUSADOS = "/api/PedidosRecusados"
    COD_PEDIDOS = [
        "1202086713",
        "1202429886"
    ]
    COD_VENDEDOR_CUSTOMER = [
        "00580849",
        "00307501",
        "00553615"
    ]

# Devolucoes

    @task
    def busca_devolucoes_categoria(self):

        consult_client_endpoint = f"{self.ENDPOINT_PRIFIX_CUSTOMER_DEVOLUCOES}/BuscarDevolucoesPorCategoria"
        body = {
           "codVendedor": self.COD_VENDEDOR_CUSTOMER[0],
           "codCliente": "",
           "periodo": "m",
           "categoriaGM": "LINGUICA FRESCA (DOMESTICA)"
        }
        with self.client.post(url=consult_client_endpoint,
                              name="CargaApiCustomer 01 - Busca devoluções por categorias",
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
                    mensagemFalha
                )

    @task
    def busca_devolucao_cliente(self):

        consult_client_endpoint = f"{self.ENDPOINT_PRIFIX_CUSTOMER_DEVOLUCOES}/BuscarDevolucoesPorCliente"
        body = {
           "codVendedor": self.COD_VENDEDOR_CUSTOMER[0],
           "codCliente": "0000091263",
           "periodo": "m"
        }
        with self.client.post(url=consult_client_endpoint,
                              name="CargaApiCustomer 02 - Busca devoluções por cliente",
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
                    mensagemFalha
                )

    @task
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
                              name="CargaApiCustomer 03 - Busca devolucoes por SKU",
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
                    mensagemFalha
                )

    @task
    def soma_devolucoes(self):

        consult_client_endpoint = f"{self.ENDPOINT_PRIFIX_CUSTOMER_DEVOLUCOES}/GetSomaDevolucoes"
        body = {
           "codVendedor": self.COD_VENDEDOR_CUSTOMER[0],
           "codCliente": "0000091263" 
        }
        with self.client.post(url=consult_client_endpoint,
                              name="CargaApiCustomer 04 - Busca soma devoluções",
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
                    mensagemFalha
                )

# Volume Captado

    @task
    def soma_volume_captado(self):

        consult_client_endpoint = f"{self.ENDPOINT_PRIFIX_CUSTOMER_VOLUMECAPTADO}/GetSomaVolumeCaptado"
        body = {
           "codVendedor": choice(self.COD_VENDEDOR_CUSTOMER),
           "dataDe": "2022-02-01T14:13:16.660Z",
           "dataAte": "2022-02-08T14:13:16.660Z" 
        }
        with self.client.post(url=consult_client_endpoint,
                              name="CargaApiCustomer 05 - Soma volume captado",
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
                    mensagemFalha
                )

    @task
    def soma_categoria_volume_captado(self):

        consult_client_endpoint = f"{self.ENDPOINT_PRIFIX_CUSTOMER_VOLUMECAPTADO}/GetSomaCategoriaVolumeCaptado"
        body = {
           "codVendedor": "00333982",
           "dataDe": "2022-02-01T14:57:53.211Z",
           "dataAte": "2022-02-08T14:57:53.211Z",
           "categoriaGM": "EMPANADO (DOMESTICO)"   
        }
        with self.client.post(url=consult_client_endpoint,
                              name="CargaApiCustomer 06 - Soma categoria volume captado",
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
                    mensagemFalha
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
                              name="CargaApiCustomer 07 - Busca volume captado por SKU",
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
                    mensagemFalha
                )

# Mix Usual

    @task
    def mix_usual_cliente(self):

        consult_client_endpoint = f"{self.ENDPOINT_PRIFIX_CUSTOMER_MIXUSUAL}/ListaMixUsual"
        body = {
           "codCliente": "0000578835",
           "cnpj": "58767252000716" 
        }
        with self.client.post(url=consult_client_endpoint,
                              name="CargaApiCustomer 08 - Lista Mix Usual",
                              catch_response=True, json=body) as response:
            resposta = loads(response.text or "null")

            try:
                print(
                    f"============= \n 08 - Lista Mix usual \n {resposta['success']} \n {len(resposta['data'])} \n Status Code: {response.status_code}")
                if resposta["success"] != True and len(resposta["data"]) != 11:
                    response.failure(
                        f"Corpo de resposta diferente do esperado: {response.text}")
            except KeyError:
                print(
                    f"============= \n 08 - FALHA ao obter lista mix usual de clientes \n {response.text} \n Status code: {response.status_code}")
                response.failure(
                    mensagemFalha
                )

# Status Pedido

    @task
    def lista_pedidos_status_s10(self):

        consult_client_endpoint = f"{self.ENDPOINT_PRIFIX_CUSTOMER_STATUS_PEDIDO}/ListaPedidosStatusS10"
        body = {
           "codVendedor": "00146263",
           "codCliente": "0007905542",
           "dataDe": "2022-02-01",
           "dataAte": "2022-02-28"
        }
        with self.client.post(url=consult_client_endpoint,
                              name="CargaApiCustomer 09 - Lista pedidos Status S10",
                              catch_response=True, json=body) as response:
            resposta = loads(response.text or "null")

            try:
                print(
                    f"============= \n 09 - Lista pedidos status S10 \n {resposta['success']} \n {len(resposta['data'])} \n Status Code: {response.status_code}")
                if resposta["success"] != True and len(resposta["data"]) != 8:
                    response.failure(
                        f"Corpo de resposta diferente do esperado: {response.text}")
            except KeyError:
                print(
                    f"============= \n 09 - FALHA ao obter lista de pedidos status S10 \n {response.text} \n Status code: {response.status_code}")
                response.failure(
                    mensagemFalha
                )

    @task
    def obter_pedidos_s10(self):

        consult_client_endpoint = f"{self.ENDPOINT_PRIFIX_CUSTOMER_STATUS_PEDIDO}/ObterPedidoS10"
        body = {
           "codigo": choice(self.COD_PEDIDOS),
           "dataDe": "2022-02-01",
           "dataAte": "2022-02-28" 
        }
        with self.client.post(url=consult_client_endpoint,
                              name="CargaApiCustomer 10 - Obter pedidos S10",
                              catch_response=True, json=body) as response:
            resposta = loads(response.text or "null")

            try:
                print(
                    f"============= \n 10 - Obter pedidos S10 \n {resposta['success']} \n {len(resposta['data'])} \n Status Code: {response.status_code}")
                if resposta["success"] != True and len(resposta["data"]) != 17:
                    response.failure(
                        f"Corpo de resposta diferente do esperado: {response.text}")
            except KeyError:
                print(
                    f"============= \n 10 - FALHA ao obter pedidos S10 \n {response.text} \n Status code: {response.status_code}")
                response.failure(
                    mensagemFalha
                )

# Pedidos Recusados

    @task
    def envia_push_vendedor(self):

        consult_client_endpoint = f"{self.ENDPOINT_PRIFIX_CUSTOMER_PEDIDOS_RECUSADOS}/EnviaPushVendedor"
        body = {
           "codigo": choice(self.COD_VENDEDOR_CUSTOMER) 
        }
        with self.client.post(url=consult_client_endpoint,
                              name="CargaApiCustomer 11 - Envia push Vendedor",
                              catch_response=True, json=body) as response:
            resposta = loads(response.text or "null")

            try:
                print(
                    f"============= \n 11 - Envia push vendedor \n {resposta['success']} \n {len(resposta['data'])} \n Status Code: {response.status_code}")
                if resposta["success"] != True and len(resposta["data"]) != 3:
                    response.failure(
                        f"Corpo de resposta diferente do esperado: {response.text}")
            except KeyError:
                print(
                    f"============= \n 11 - FALHA ao enviar push ao vendedor \n {response.text} \n Status code: {response.status_code}")
                response.failure(
                    mensagemFalha
                )

    @task
    def lista_pedidos_recusados(self):

        consult_client_endpoint = f"{self.ENDPOINT_PRIFIX_CUSTOMER_PEDIDOS_RECUSADOS}/ListaPedidosRecusados"
        body = {
           "codVendedor": choice(self.COD_VENDEDOR_CUSTOMER),
           "dataInicio": "2022-02-01T14:36:19.605Z",
           "dataFim": "2022-02-14T14:36:19.605Z" 
        }
        with self.client.post(url=consult_client_endpoint,
                              name="CargaApiCustomer 12 - Lista pedidos recusados",
                              catch_response=True, json=body) as response:
            resposta = loads(response.text or "null")

        try:
            print(
                f"============= \n 12 - Lista pedidos recusados \n {resposta['success']} \n {len(resposta['data'])} \n Status Code: {response.status_code}")
            if resposta["success"] != True and len(resposta["data"]) != 9:
                response.failure(
                    f"Corpo de resposta diferente do esperado: {response.text}")
        except KeyError:
            print(
                f"============= \n 12 - FALHA ao listar pedidos recusados \n {response.text} \n Status code: {response.status_code}")
            response.failure(
                mensagemFalha
            )

#    @task endpoint com problema
    def obter_pedido(self):

        consult_client_endpoint = f"{self.ENDPOINT_PRIFIX_CUSTOMER_PEDIDOS_RECUSADOS}/ObterPedido"
        body = {
           "codigo": "1202106635" 
        }
        with self.client.post(url=consult_client_endpoint,
                              name="CargaApiCustomer 13 - Obter pedido",
                              catch_response=True, json=body) as response:
            resposta = loads(response.text or "null")
        
        try:
            print(
                f"============= \n 13 - Obter pedido \n {resposta['success']} \n {len(resposta['data'])} \n Status Code: {response.status_code}")
            if resposta["success"] != True and len(resposta["data"]) != 10:
                response.failure(
                    f"Corpo de resposta diferente do esperado: {response.text}")
        except KeyError:
            print(
                f"============= \n 13 - FALHA ao obter pedidos \n {response.text} \n Status code: {response.status_code}")
            response.failure(
                mensagemFalha
            )

class CargaApiProducts(HttpUser):

    host = "https://brf-api-pim-product-dev.azurewebsites.net"
    wait_time = between(1.0, 3.0)

    ENDPOINT_PRIFIX_PRODUTOS = "/api/Produtos"

    @task
    def busca_categoria_produto(self):

        consult_client_endpoint = f"{self.ENDPOINT_PRIFIX_PRODUTOS}/BuscaCategorias"

        with self.client.post(url=consult_client_endpoint,
                              name="CargaApiProducts 01 - Busca categorias produto",
                              catch_response=True) as response:
            resposta = loads(response.text or "null")

        try:
            print(
                f"============= \n 01 - Busca categorias produto \n {resposta['success']} \n {len(resposta['data'])} \n Status Code: {response.status_code}")
            if resposta["success"] != True and len(resposta["data"]) != 1:
                response.failure(
                    f"Corpo de resposta diferente do esperado: {response.text}")
        except KeyError:
            print(
                f"============= \n 01 - FALHA ao buscar categorias \n {response.text} \n Status code: {response.status_code}")
            response.failure(
                mensagemFalha
            )

    @task
    def busca_produtos(self):

        consult_client_endpoint = f"{self.ENDPOINT_PRIFIX_PRODUTOS}/BuscaProdutos"
        body = {
           "categoria": "Batata frita"
        }

        with self.client.post(url=consult_client_endpoint,
                              name="CargaApiProducts 02 - Busca produtos",
                              catch_response=True, json=body) as response:
            resposta = loads(response.text or "null")

        try:
            print(
                f"============= \n 02 - Busca produtos \n {resposta['success']} \n {len(resposta['data'])} \n Status Code: {response.status_code}")
            if resposta["success"] != True and len(resposta["data"]) != 5:
                response.failure(
                    f"Corpo de resposta diferente do esperado: {response.text}")
        except KeyError:
            print(
                f"============= \n 02 - FALHA ao buscar produtos \n {response.text} \n Status code: {response.status_code}")
            response.failure(
                mensagemFalha
            )

#    @task endpoint com problema
    def busca_ficha_produto(self):

        consult_client_endpoint = f"{self.ENDPOINT_PRIFIX_PRODUTOS}/BuscaFichaProduto"
        body = {
           "codMaterial": "000000000000677510"
        }

        with self.client.post(url=consult_client_endpoint,
                              name="CargaApiProducts 03 - Busca ficha produto",
                              catch_response=True, json=body) as response:
            resposta = loads(response.text or "null")

        try:
            print(
                f"============= \n 03 - Busca ficha produto \n {resposta['success']} \n {len(resposta['data'])} \n Status Code: {response.status_code}")
            if resposta["success"] != True and len(resposta["data"]) != 19:
                response.failure(
                    f"Corpo de resposta diferente do esperado: {response.text}")
        except KeyError:
            print(
                f"============= \n 03 - FALHA ao buscar ficha de produtos \n {response.text} \n Status code: {response.status_code}")
            response.failure(
                mensagemFalha
            )

    @task
    def busca_detalhe_produto(self):

        consult_client_endpoint = f"{self.ENDPOINT_PRIFIX_PRODUTOS}/BuscaDetalheProduto"
        body = {
           "codMaterial": "000000000000677510"
        }

        with self.client.post(url=consult_client_endpoint,
                              name="CargaApiProducts 04 - Busca detalhe produto",
                              catch_response=True, json=body) as response:
            resposta = loads(response.text or "null")

        try:
            print(
                f"============= \n 04 - Busca detalhe produto \n {resposta['success']} \n {len(resposta['data'])} \n Status Code: {response.status_code}")
            if resposta["success"] != True and len(resposta["data"]) != 19:
                response.failure(
                    f"Corpo de resposta diferente do esperado: {response.text}")
        except KeyError:
            print(
                f"============= \n 04 - FALHA ao buscar detalhe dos produtos \n {response.text} \n Status code: {response.status_code}")
            response.failure(
                mensagemFalha
            )

#    @task endpoint com problema
    def oportunidade_inovacao(self):

        consult_client_endpoint = f"{self.ENDPOINT_PRIFIX_PRODUTOS}/OportunidadeInovacao"

        with self.client.get(url=consult_client_endpoint,
                              name="CargaApiProducts 05 - Oportunidade inovacao",
                              catch_response=True) as response:
            resposta = loads(response.text or "null")

        try:
            print(
                f"============= \n 05 - Oportunidade inovacao \n {resposta['success']} \n {len(resposta['data'])} \n Status Code: {response.status_code}")
            if resposta["success"] != True and len(resposta["data"]) != 12:
                response.failure(
                    f"Corpo de resposta diferente do esperado: {response.text}")
        except KeyError:
            print(
                f"============= \n 05 - FALHA ao trazer oportundiade e inovacao \n {response.text} \n Status code: {response.status_code}")
            response.failure(
                mensagemFalha
            )

if __name__ == "__main__":
    env = Environment(user_classes=[CargaApiAtendimento, CargaApiCustomer, CargaApiProducts])
    env.create_local_runner()
    env.create_web_ui("127.0.0.1", 8089)
    env.runner.start(200, spawn_rate=10)
    gevent.spawn_later(3600, lambda: env.runner.quit())
    env.runner.greenlet.join()
    env.web_ui.stop()
#  tags = ['teste'])