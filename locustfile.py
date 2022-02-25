from asyncio import Task
import gevent
from locust import between, task, HttpUser, tag
from locust.env import Environment
from json import loads
from random import choice

mensagemFalha = "Nao foi possivel acessar o valor de data"

class CargaApiAtendimento(HttpUser):

    host = "https://brf-api-pim-attendance.azurewebsites.net"
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

    host = "https://brf-api-pim-customer.azurewebsites.net"
    wait_time = between(1.0, 3.0)

    ENDPOINT_PRIFIX_CUSTOMER_DEVOLUCOES = "/api/Devolucoes"
    ENDPOINT_PRIFIX_CUSTOMER_VOLUMECAPTADO = "/api/VolumeCaptado"
    ENDPOINT_PRIFIX_CUSTOMER_MIXUSUAL = "/api/MixUsual"
    ENDPOINT_PRIFIX_CUSTOMER_STATUS_PEDIDO = "/api/StatusPedidos"
    ENDPOINT_PRIFIX_CUSTOMER_PEDIDOS_RECUSADOS = "/api/PedidosRecusados"
    ENDPOINT_PRIFIX_CUSTOMER_PEDIDOS_ANTECIPADOS = "/api/PedidosAntecipados"
    ENDPOINT_PRIFIX_CUSTOMER_RISCO_DEVOLUCAO = "/api/AlertaRiscoDevolucao"
    ENDPOINT_PRIFIX_CUSTOMER_CLIENTES = "/api/Clientes"
    ENDPOINT_PRIFIX_CUSTOMER_ESTOQUEDISPONIVEL = "/api/EstoqueDisponivel"
    ENDPOINT_PRIFIX_CUSTOMER_HISTMOTIVODEVOLUCAO = "/api/HistoricoMotivoDevolucao"
    ENDPOINT_PRIFIX_CUSTOMER_MIX_INTELIGENTE = "/api/MixInteligente"
    ENDPOINT_PRIFIX_CUSTOMER_PEDIDO_MINIMO = "/api/PedidoMinimo"
    COD_PEDIDOS = [
        "1202750987",
        "1202429886"
    ]
    COD_VENDEDOR_CUSTOMER = [
        "00580849",
        "00307501",
        "00553615"
    ]
    COD_CLIENTE_CUSTOMER = [
        "0000091263",
        "0000143001",
        "0000244644",
        "0007437648",
        "0007798681",
        "0007552224"
    ]
    CNPJ_CLIENTES = [
        "00813880000115",
        "03927907000270",
        "11697339000105",
        "73807471000422",
        "28194564000121",
        "73807471000341",
    ]
    RISCO_DEVOLUCAO_REDES = [
        "REDE TOSTA",
        "OUTRAS",
        "SUPERM BOA SORT SPC",
        "MERCADAO ECONOMICO"
    ]
    QTD_PAGINAS = [
        1,
        2,
        3
    ]
    CENTRO_DISTRIBUICAO = [
        "1642",
        "1641",
        "1644"
    ]
    CODIGO_ITEMS = [
        "000000000000239698",
        "000000000000340278",
        "000000000000239701",
        "000000000000500426"
    ]
    PERIODO_BUSCA = [
        "A",
        "M",
        "T"
    ]

# Alerta Risco Devolucoes

    @task
    def risco_devolucao_obter_cliente(self):

        consult_client_endpoint = f"{self.ENDPOINT_PRIFIX_CUSTOMER_RISCO_DEVOLUCAO}/ObterCliente"
        body = {
           "codVendedor": "00357064",
           "codCliente": "0007425106" 
        }
        with self.client.post(url=consult_client_endpoint,
                              name="CargaApiCustomer 01 - Risco devolucao, obter cliente",
                              catch_response=True, json=body) as response:
            resposta = loads(response.text or "null")

            try:
               print( 
               f"============= \n 01 - Risco devolucao, obter cliente \n {resposta['success']} \n {len(resposta['data'])} \n Status Code: {response.status_code}")
               if resposta["success"] != True and len(resposta["data"]) != 6:
                    response.failure(
                        f"Corpo de resposta diferente do esperado: {response.text}")
            except KeyError:
                print(
                    f"============= \n 01 - FALHA ao obter cliente, risco devolucao \n {response.text} \n Status code: {response.status_code}")
                response.failure(
                    mensagemFalha
                )

    @task
    def risco_devolucao_obter_lista_redes(self):

        consult_client_endpoint = f"{self.ENDPOINT_PRIFIX_CUSTOMER_RISCO_DEVOLUCAO}/ObterListaRedes"
        body = {
           "codVendedor": "00357064",
           "itensPorPagina": 10,
           "pagina": 1,
           "search": choice(self.RISCO_DEVOLUCAO_REDES)
        }
        with self.client.post(url=consult_client_endpoint,
                              name="CargaApiCustomer 02 - Risco devolucao, obter lista redes",
                              catch_response=True, json=body) as response:
            resposta = loads(response.text or "null")

            try:
               print( 
               f"============= \n 02 - Risco devolucao, obter lista redes \n {resposta['success']} \n {len(resposta['data'])} \n Status Code: {response.status_code}")
               if resposta["success"] != True and len(resposta["data"]) != 5:
                    response.failure(
                        f"Corpo de resposta diferente do esperado: {response.text}")
            except KeyError:
                print(
                    f"============= \n 02 - FALHA ao obter lista de redes, risco devolucao \n {response.text} \n Status code: {response.status_code}")
                response.failure(
                    mensagemFalha
                )

    @task
    def risco_devolucao_obter_clientes(self):

        consult_client_endpoint = f"{self.ENDPOINT_PRIFIX_CUSTOMER_RISCO_DEVOLUCAO}/ObterClientes"
        body = {
           "codVendedor": "00357064",
           "itensPorPagina": 10,
           "pagina": choice(self.QTD_PAGINAS),
           "search": ""
        }
        with self.client.post(url=consult_client_endpoint,
                              name="CargaApiCustomer 03 - Risco devolucao, obter clientes",
                              catch_response=True, json=body) as response:
            resposta = loads(response.text or "null")

            try:
               print( 
               f"============= \n 03 - Risco devolucao, obter clientes \n {resposta['success']} \n {len(resposta['data'])} \n Status Code: {response.status_code}")
               if resposta["success"] != True and len(resposta["data"]) != 6:
                    response.failure(
                        f"Corpo de resposta diferente do esperado: {response.text}")
            except KeyError:
                print(
                    f"============= \n 03 - FALHA ao obter clientes, risco devolucao \n {response.text} \n Status code: {response.status_code}")
                response.failure(
                    mensagemFalha
                )

#   @task endpoint com problema
    def risco_devolucao_obter_rede_clientes(self):

        consult_client_endpoint = f"{self.ENDPOINT_PRIFIX_CUSTOMER_RISCO_DEVOLUCAO}/ObterRedeClientes"
        body = {
           "codVendedor": "00357064",
           "itensPorPagina": 10,
           "pagina": choice(self.QTD_PAGINAS),
           "search": ""
        }
        with self.client.post(url=consult_client_endpoint,
                              name="CargaApiCustomer 04 - Risco devolucao, obter rede clientes",
                              catch_response=True, json=body) as response:
            resposta = loads(response.text or "null")

            try:
               print( 
               f"============= \n 04 - Risco devolucao, obter rede clientes \n {resposta['success']} \n {len(resposta['data'])} \n Status Code: {response.status_code}")
               if resposta["success"] != True and len(resposta["data"]) != 6:
                    response.failure(
                        f"Corpo de resposta diferente do esperado: {response.text}")
            except KeyError:
                print(
                    f"============= \n 04 - FALHA ao obter rede clientes, risco devolucao \n {response.text} \n Status code: {response.status_code}")
                response.failure(
                    mensagemFalha
                )                

#Clientes

    @task
    def quantidade_total_clientes(self):

        consult_client_endpoint = f"{self.ENDPOINT_PRIFIX_CUSTOMER_CLIENTES}/QuantidadeTotalClientes"
        body = {
           "codVendedor": choice(self.COD_VENDEDOR_CUSTOMER)
        }
        with self.client.post(url=consult_client_endpoint,
                              name="CargaApiCustomer 05 - Quantidade total clientes",
                              catch_response=True, json=body) as response:
            resposta = loads(response.text or "null")

            try:
                print(
                    f"============= \n 05 - Quantidade total clientes \n {resposta['success']} \n {len(resposta['data'])} \n Status Code: {response.status_code}")
                if resposta["success"] != True and len(resposta["data"]) != 1:
                    response.failure(
                        f"Corpo de resposta diferente do esperado: {response.text}")
            except KeyError:
                print(
                    f"============= \n 05 - FALHA ao obter quantidade total de clientes \n {response.text} \n Status code: {response.status_code}")
                response.failure(
                    mensagemFalha
                )

    @task
    def lista_clientes(self):

        consult_client_endpoint = f"{self.ENDPOINT_PRIFIX_CUSTOMER_CLIENTES}/ListaClientes"
        body = {
           "codVendedor": choice(self.COD_VENDEDOR_CUSTOMER),
           "search": "",
           "pagina": choice(self.QTD_PAGINAS),
           "itensPorPagina": 10
        }
        with self.client.post(url=consult_client_endpoint,
                              name="CargaApiCustomer 06 - Lista clientes",
                              catch_response=True, json=body) as response:
            resposta = loads(response.text or "null")

            try:
                print(
                    f"============= \n 06 - Lista clientes \n {resposta['success']} \n {len(resposta['data'])} \n Status Code: {response.status_code}")
                if resposta["success"] != True and len(resposta["data"]) != 4:
                    response.failure(
                        f"Corpo de resposta diferente do esperado: {response.text}")
            except KeyError:
                print(
                    f"============= \n 06 - FALHA ao obter lista de clientes \n {response.text} \n Status code: {response.status_code}")
                response.failure(
                    mensagemFalha
                )

    @task
    def get_clientes(self):

        consult_client_endpoint = f"{self.ENDPOINT_PRIFIX_CUSTOMER_CLIENTES}/GetCliente"
        body = {
           "codCliente": choice(self.COD_CLIENTE_CUSTOMER),
           "cnpj": ""
        }
        with self.client.post(url=consult_client_endpoint,
                              name="CargaApiCustomer 07 - Get clientes",
                              catch_response=True, json=body) as response:
            resposta = loads(response.text or "null")

            try:
                print(
                    f"============= \n 07 - Get clientes \n {resposta['success']} \n {len(resposta['data'])} \n Status Code: {response.status_code}")
                if resposta["success"] != True and len(resposta["data"]) != 4:
                    response.failure(
                        f"Corpo de resposta diferente do esperado: {response.text}")
            except KeyError:
                print(
                    f"============= \n 07 - FALHA ao obter get clientes \n {response.text} \n Status code: {response.status_code}")
                response.failure(
                    mensagemFalha
                )

#   @task endpoint com problema
    def get_clientes_cnpj(self):

        consult_client_endpoint = f"{self.ENDPOINT_PRIFIX_CUSTOMER_CLIENTES}/GetClienteCNPJ"
        body = {
           "cnpj": choice(self.CNPJ_CLIENTES)
        }
        with self.client.post(url=consult_client_endpoint,
                              name="CargaApiCustomer 08 - Get clientes CNPJ",
                              catch_response=True, json=body) as response:
            resposta = loads(response.text or "null")

            try:
                print(
                    f"============= \n 08 - Get clientes CNPJ \n {resposta['success']} \n {len(resposta['data'])} \n Status Code: {response.status_code}")
                if resposta["success"] != True and len(resposta["data"]) != 6:
                    response.failure(
                        f"Corpo de resposta diferente do esperado: {response.text}")
            except KeyError:
                print(
                    f"============= \n 08 - FALHA ao obter clientes pelo CNPJ \n {response.text} \n Status code: {response.status_code}")
                response.failure(
                    mensagemFalha
                )

    @task #endpoint com retorno diferente do esperado
    def salva_cliente_tipologia(self):

        consult_client_endpoint = f"{self.ENDPOINT_PRIFIX_CUSTOMER_CLIENTES}/SalvaClienteTipologia"
        body = {
           "cnpj": "00658059000171",
           "descricaoTipologia": "1",
           "codVendedor": "00580849"
        }
        with self.client.post(url=consult_client_endpoint,
                              name="CargaApiCustomer 09 - Salva cliente Tipologia",
                              catch_response=True, json=body) as response:
            resposta = loads(response.text or "null")

            try:
                print(
                    f"============= \n 09 - Salva cliente Tipologia \n {resposta['success']} \n {len(resposta['data'])} \n Status Code: {response.status_code}")
                if resposta["success"] != True and len(resposta["data"]) != 0:
                    response.failure(
                        f"Corpo de resposta diferente do esperado: {response.text}")
            except KeyError:
                print(
                    f"============= \n 09 - FALHA ao salvar cliente Tipologia \n {response.text} \n Status code: {response.status_code}")
                response.failure(
                    mensagemFalha
                )

    @task #endpoint com retorno diferente do esperado
    def cliente_tipologia_foi_concluida(self):

        consult_client_endpoint = f"{self.ENDPOINT_PRIFIX_CUSTOMER_CLIENTES}/ClienteTipologiaFoiConcluida"
        body = {
           "cnpj": "00658059000171"
        }
        with self.client.post(url=consult_client_endpoint,
                              name="CargaApiCustomer 10 - Cliente tipologia concluida",
                              catch_response=True, json=body) as response:
            resposta = loads(response.text or "null")

            try:
                print(
                    f"============= \n 10 - Cliente tipologia concluida \n {resposta['success']} \n Status Code: {response.status_code}")
                if resposta["success"] != True:
                    response.failure(
                        f"Corpo de resposta diferente do esperado: {response.text}")
            except KeyError:
                print(
                    f"============= \n 10 - FALHA ao concluir cliente Tipologia \n {response.text} \n Status code: {response.status_code}")
                response.failure(
                    mensagemFalha
                )

# Estoque Disponivel

    @task
    def obter_lista_centros(self):

        consult_client_endpoint = f"{self.ENDPOINT_PRIFIX_CUSTOMER_ESTOQUEDISPONIVEL}/ObterListaCentros"
        body = {
           "codVendedor": choice(self.COD_VENDEDOR_CUSTOMER),
           "itensPorPagina": 10,
           "pagina": 1,
           "search": "" 
        }
        with self.client.post(url=consult_client_endpoint,
                              name="CargaApiCustomer 11 - Obter lista de centros",
                              catch_response=True, json=body) as response:
            resposta = loads(response.text or "null")

            try:
                print(
                    f"============= \n 11 - Obter lista de centros \n {resposta['success']} \n {len(resposta['data'])} \n Status Code: {response.status_code}")
                if resposta["success"] != True and len(resposta["data"]) != 2:
                    response.failure(
                        f"Corpo de resposta diferente do esperado: {response.text}")
            except KeyError:
                print(
                    f"============= \n 11 - FALHA ao obter lista de centros \n {response.text} \n Status code: {response.status_code}")
                response.failure(
                    mensagemFalha
                )

    @task
    def obter_itens_centros(self):

        consult_client_endpoint = f"{self.ENDPOINT_PRIFIX_CUSTOMER_ESTOQUEDISPONIVEL}/ObterItensCentro"
        body = {
           "centro": choice(self.CENTRO_DISTRIBUICAO),
           "itensPorPagina": 10,
           "pagina": 1,
           "search": ""
        }
        with self.client.post(url=consult_client_endpoint,
                              name="CargaApiCustomer 12 - Obter itens de centros",
                              catch_response=True, json=body) as response:
            resposta = loads(response.text or "null")

            try:
                print(
                    f"============= \n 12 - Obter itens de centros \n {resposta['success']} \n {len(resposta['data'])} \n Status Code: {response.status_code}")
                if resposta["success"] != True and len(resposta["data"]) != 9:
                    response.failure(
                        f"Corpo de resposta diferente do esperado: {response.text}")
            except KeyError:
                print(
                    f"============= \n 12 - FALHA ao obter itens de centros \n {response.text} \n Status code: {response.status_code}")
                response.failure(
                    mensagemFalha
                )

    @task
    def obter_item_centro(self):

        consult_client_endpoint = f"{self.ENDPOINT_PRIFIX_CUSTOMER_ESTOQUEDISPONIVEL}/ObterItemCentro"
        body = {
           "centro": "1642",
           "item": choice(self.CODIGO_ITEMS)
        }
        with self.client.post(url=consult_client_endpoint,
                              name="CargaApiCustomer 13 - Obter item de centro",
                              catch_response=True, json=body) as response:
            resposta = loads(response.text or "null")

            try:
                print(
                    f"============= \n 13 - Obter item centro \n {resposta['success']} \n {len(resposta['data'])} \n Status Code: {response.status_code}")
                if resposta["success"] != True and len(resposta["data"]) != 9:
                    response.failure(
                        f"Corpo de resposta diferente do esperado: {response.text}")
            except KeyError:
                print(
                    f"============= \n 13 - FALHA ao obter itens de centros \n {response.text} \n Status code: {response.status_code}")
                response.failure(
                    mensagemFalha
                )

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
                              name="CargaApiCustomer 14 - Busca devoluções por categorias",
                              catch_response=True, json=body) as response:
            resposta = loads(response.text or "null")

            try:
                print(
                    f"============= \n 14 - Busca devolucoes por categoria \n {resposta['success']} \n {len(resposta['data'])} \n Status Code: {response.status_code}")
                if resposta["success"] != True and len(resposta["data"]) != 5:
                    response.failure(
                        f"Corpo de resposta diferente do esperado: {response.text}")
            except KeyError:
                print(
                    f"============= \n 14 - FALHA ao obter resultado de devolucoes por categoria \n {response.text} \n Status code: {response.status_code}")
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
                              name="CargaApiCustomer 15 - Busca devoluções por cliente",
                              catch_response=True, json=body) as response:
            resposta = loads(response.text or "null")

            try:
                print(
                    f"============= \n 15 - Busca devolucoes por cliente \n {resposta['success']} \n {len(resposta['data'])} \n Status Code: {response.status_code}")
                if resposta["success"] != True and len(resposta["data"]) != 7:
                    response.failure(
                        f"Corpo de resposta diferente do esperado: {response.text}")
            except KeyError:
                print(
                    f"============= \n 15 - FALHA ao obter resultado de devolucoes por cliente \n {response.text} \n Status code: {response.status_code}")
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
                              name="CargaApiCustomer 16 - Busca devolucoes por SKU",
                              catch_response=True, json=body) as response:
            resposta = loads(response.text or "null")

            try:
                print(
                    f"============= \n 16 - Busca devolucoes por SKU \n {resposta['success']} \n {len(resposta['data'])} \n Status Code: {response.status_code}")
                if resposta["success"] != True and len(resposta["data"]) != 9:
                    response.failure(
                        f"Corpo de resposta diferente do esperado: {response.text}")
            except KeyError:
                print(
                    f"============= \n 16 - FALHA ao obter resultado de devolucoes por SKU \n {response.text} \n Status code: {response.status_code}")
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
                              name="CargaApiCustomer 17 - Busca soma devoluções",
                              catch_response=True, json=body) as response:
            resposta = loads(response.text or "null")

            try:
                print(
                    f"============= \n 17 - Busca soma de devolucoes \n {resposta['success']} \n {len(resposta['data'])} \n Status Code: {response.status_code}")
                if resposta["success"] != True and len(resposta["data"]) != 5 and len(resposta["grafico"]) > 10:
                    response.failure(
                        f"Corpo de resposta diferente do esperado: {response.text}")
            except KeyError:
                print(
                    f"============= \n 17 - FALHA ao obter resultado da soma de devolucoes \n {response.text} \n Status code: {response.status_code}")
                response.failure(
                    mensagemFalha
                )
# Historio Motivo Devolucao

    @task
    def busca_historico_motivo_devolucao(self):

        consult_client_endpoint = f"{self.ENDPOINT_PRIFIX_CUSTOMER_HISTMOTIVODEVOLUCAO}/BuscaHistoricoMotivoDevolucao"
        body = {
           "periodo": choice(self.PERIODO_BUSCA),
           "codCliente": "0000065122",
           "codVendedor": "00307501"
        }
        with self.client.post(url=consult_client_endpoint,
                              name="CargaApiCustomer 18 - Busca historico motivo devolucao",
                              catch_response=True, json=body) as response:
            resposta = loads(response.text or "null")

            try:
                print(
                    f"============= \n 18 - Busca historico motivo devolucao \n {resposta['success']} \n {len(resposta['data'])} \n Status Code: {response.status_code}")
                if resposta["success"] != True and len(resposta["data"]) != 8:
                    response.failure(
                        f"Corpo de resposta diferente do esperado: {response.text}")
            except KeyError:
                print(
                    f"============= \n 18 - FALHA ao buscar historico motivo devolucao \n {response.text} \n Status code: {response.status_code}")
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
                              name="CargaApiCustomer 19 - Soma volume captado",
                              catch_response=True, json=body) as response:
            resposta = loads(response.text or "null")

            try:
                print(
                    f"============= \n 19 - Soma volume captado \n {resposta['success']} \n {len(resposta['data'])} \n Status Code: {response.status_code}")
                if resposta["success"] != True and len(resposta["data"]) != 4:
                    response.failure(
                        f"Corpo de resposta diferente do esperado: {response.text}")
            except KeyError:
                print(
                    f"============= \n 19 - FALHA ao obter resultado da soma de volume captado \n {response.text} \n Status code: {response.status_code}")
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
                              name="CargaApiCustomer 20 - Soma categoria volume captado",
                              catch_response=True, json=body) as response:
            resposta = loads(response.text or "null")

            try:
                print(
                    f"============= \n 20 - Soma categoria volume captado \n {resposta['success']} \n {len(resposta['data'])} \n Status Code: {response.status_code}")
                if resposta["success"] != True and len(resposta["data"]) != 5:
                    response.failure(
                        f"Corpo de resposta diferente do esperado: {response.text}")
            except KeyError:
                print(
                    f"============= \n 20 - FALHA ao obter resultado da soma categoria de volume captado \n {response.text} \n Status code: {response.status_code}")
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
                              name="CargaApiCustomer 21 - Busca volume captado por SKU",
                              catch_response=True, json=body) as response:
            resposta = loads(response.text or "null")

            try:
                print(
                    f"============= \n 21 - Busca volume captado por SKU \n {resposta['success']} \n {len(resposta['data'])} \n Status Code: {response.status_code}")
                if resposta["success"] != True and len(resposta["data"]) != 9:
                    response.failure(
                        f"Corpo de resposta diferente do esperado: {response.text}")
            except KeyError:
                print(
                    f"============= \n 21 - FALHA ao obter resultado da soma categoria de volume captado \n {response.text} \n Status code: {response.status_code}")
                response.failure(
                    mensagemFalha
                )

# Mix Inteligente

    @task
    def mix_inteligente_lista_clientes(self):

        consult_client_endpoint = f"{self.ENDPOINT_PRIFIX_CUSTOMER_MIX_INTELIGENTE}/ListaClientes"
        body = {
           "codVendedor": "00553615",
           "itensPorPagina": 10,
           "pagina": choice(self.QTD_PAGINAS),
           "search": ""
        }
        with self.client.post(url=consult_client_endpoint,
                              name="CargaApiCustomer 22 - Lista Mix Inteligente Clientes",
                              catch_response=True, json=body) as response:
            resposta = loads(response.text or "null")

            try:
                print(
                    f"============= \n 22 - Lista Mix Inteligente Clientes \n {resposta['success']} \n {len(resposta['data'])} \n Status Code: {response.status_code}")
                if resposta["success"] != True and len(resposta["data"]) != 6:
                    response.failure(
                        f"Corpo de resposta diferente do esperado: {response.text}")
            except KeyError:
                print(
                    f"============= \n 22 - FALHA ao obter lista mix inteligente clientes \n {response.text} \n Status code: {response.status_code}")
                response.failure(
                    mensagemFalha
                )

    @tag('teste')
    @task
    def mix_inteligente_lista_itens_sugeridos(self):

        consult_client_endpoint = f"{self.ENDPOINT_PRIFIX_CUSTOMER_MIX_INTELIGENTE}/ListaItensSugeridos"
        body = {
           "codCliente": choice(self.COD_CLIENTE_CUSTOMER),
           "itensPorPagina": 10,
           "pagina": 1,
           "search": ""
        }
        with self.client.post(url=consult_client_endpoint,
                              name="CargaApiCustomer 23 - Lista Itens Sugeridos",
                              catch_response=True, json=body) as response:
            resposta = loads(response.text or "null")

            try:
                print(
                    f"============= \n 23 - Lista Itens Sugeridos \n {resposta['success']} \n {len(resposta['data'])} \n Status Code: {response.status_code}")
                if resposta["success"] != True and len(resposta["data"]) != 5:
                    response.failure(
                        f"Corpo de resposta diferente do esperado: {response.text}")
            except KeyError:
                print(
                    f"============= \n 23 - FALHA ao obter lista itens sugeridos \n {response.text} \n Status code: {response.status_code}")
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
                              name="CargaApiCustomer 24 - Lista Mix Usual",
                              catch_response=True, json=body) as response:
            resposta = loads(response.text or "null")

            try:
                print(
                    f"============= \n 24 - Lista Mix usual \n {resposta['success']} \n {len(resposta['data'])} \n Status Code: {response.status_code}")
                if resposta["success"] != True and len(resposta["data"]) != 11:
                    response.failure(
                        f"Corpo de resposta diferente do esperado: {response.text}")
            except KeyError:
                print(
                    f"============= \n 24 - FALHA ao obter lista mix usual de clientes \n {response.text} \n Status code: {response.status_code}")
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
                              name="CargaApiCustomer 25 - Lista pedidos Status S10",
                              catch_response=True, json=body) as response:
            resposta = loads(response.text or "null")

            try:
                print(
                    f"============= \n 25 - Lista pedidos status S10 \n {resposta['success']} \n {len(resposta['data'])} \n Status Code: {response.status_code}")
                if resposta["success"] != True and len(resposta["data"]) != 8:
                    response.failure(
                        f"Corpo de resposta diferente do esperado: {response.text}")
            except KeyError:
                print(
                    f"============= \n 25 - FALHA ao obter lista de pedidos status S10 \n {response.text} \n Status code: {response.status_code}")
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
                              name="CargaApiCustomer 26 - Obter pedidos S10",
                              catch_response=True, json=body) as response:
            resposta = loads(response.text or "null")

            try:
                print(
                    f"============= \n 26 - Obter pedidos S10 \n {resposta['success']} \n {len(resposta['data'])} \n Status Code: {response.status_code}")
                if resposta["success"] != True and len(resposta["data"]) != 17:
                    response.failure(
                        f"Corpo de resposta diferente do esperado: {response.text}")
            except KeyError:
                print(
                    f"============= \n 26 - FALHA ao obter pedidos S10 \n {response.text} \n Status code: {response.status_code}")
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
                              name="CargaApiCustomer 27 - Envia push Vendedor",
                              catch_response=True, json=body) as response:
            resposta = loads(response.text or "null")

            try:
                print(
                    f"============= \n 27 - Envia push vendedor \n {resposta['success']} \n {len(resposta['data'])} \n Status Code: {response.status_code}")
                if resposta["success"] != True and len(resposta["data"]) != 3:
                    response.failure(
                        f"Corpo de resposta diferente do esperado: {response.text}")
            except KeyError:
                print(
                    f"============= \n 27 - FALHA ao enviar push ao vendedor \n {response.text} \n Status code: {response.status_code}")
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
                              name="CargaApiCustomer 28 - Lista pedidos recusados",
                              catch_response=True, json=body) as response:
            resposta = loads(response.text or "null")

        try:
            print(
                f"============= \n 28 - Lista pedidos recusados \n {resposta['success']} \n {len(resposta['data'])} \n Status Code: {response.status_code}")
            if resposta["success"] != True and len(resposta["data"]) != 9:
                response.failure(
                    f"Corpo de resposta diferente do esperado: {response.text}")
        except KeyError:
            print(
                f"============= \n 28 - FALHA ao listar pedidos recusados \n {response.text} \n Status code: {response.status_code}")
            response.failure(
                mensagemFalha
            )

#   @task endpoint com problema
    def obter_pedido(self):

        consult_client_endpoint = f"{self.ENDPOINT_PRIFIX_CUSTOMER_PEDIDOS_RECUSADOS}/ObterPedido"
        body = {
           "codigo": "1202106635" 
        }
        with self.client.post(url=consult_client_endpoint,
                              name="CargaApiCustomer 29 - Obter pedido",
                              catch_response=True, json=body) as response:
            resposta = loads(response.text or "null")
        
        try:
            print(
                f"============= \n 29 - Obter pedido \n {resposta['success']} \n {len(resposta['data'])} \n Status Code: {response.status_code}")
            if resposta["success"] != True and len(resposta["data"]) != 10:
                response.failure(
                    f"Corpo de resposta diferente do esperado: {response.text}")
        except KeyError:
            print(
                f"============= \n 29 - FALHA ao obter pedidos \n {response.text} \n Status code: {response.status_code}")
            response.failure(
                mensagemFalha
            )

# Pedido Minimo

    @task
    def pedido_minimo_total_pedidos(self):

        consult_client_endpoint = f"{self.ENDPOINT_PRIFIX_CUSTOMER_PEDIDO_MINIMO}/TotalPedidos"
        body = {
           "codVendedor": choice(self.COD_VENDEDOR_CUSTOMER)
        }

        with self.client.post(url=consult_client_endpoint,
                              name="CargaApiCustomar 30 - Total Pedidos",
                              catch_response=True, json=body) as response:
            resposta = loads(response.text or "null")

        try:
            print(
                f"============= \n 30 - Total pedidos \n {resposta['success']} \n {len(resposta['data'])} \n Status Code: {response.status_code}")
            if resposta["success"] != True and len(resposta["data"]) != 1:
                response.failure(
                    f"Corpo de resposta diferente do esperado: {response.text}")
        except KeyError:
            print(
                f"============= \n 30 - FALHA ao buscar total pedidos \n {response.text} \n Status code: {response.status_code}")
            response.failure(
                mensagemFalha
            )

    @task
    def lista_pedido_minimo(self):

        consult_client_endpoint = f"{self.ENDPOINT_PRIFIX_CUSTOMER_PEDIDO_MINIMO}/ListaPedidoMinimo"
        body = {
           "codVendedor": choice(self.COD_VENDEDOR_CUSTOMER)
        }

        with self.client.post(url=consult_client_endpoint,
                              name="CargaApiCustomar 31 - Lista Pedido Pedido Minimo",
                              catch_response=True, json=body) as response:
            resposta = loads(response.text or "null")

        try:
            print(
                f"============= \n 31 - Lista pedido minimo \n {resposta['success']} \n {len(resposta['data'])} \n Status Code: {response.status_code}")
            if resposta["success"] != True and len(resposta["data"]) != 1:
                response.failure(
                    f"Corpo de resposta diferente do esperado: {response.text}")
        except KeyError:
            print(
                f"============= \n 31 - FALHA listar pedidos minimos \n {response.text} \n Status code: {response.status_code}")
            response.failure(
                mensagemFalha
            )

# Pedidos Antecipados

    @task
    def buscar_pedidos_antecipados(self):

        consult_client_endpoint = f"{self.ENDPOINT_PRIFIX_CUSTOMER_PEDIDOS_ANTECIPADOS}/BuscarPedidosAntecipados"
        body = {
           "codCliente": "0007425106",
           "codVendedor": "00357064" 
        }

        with self.client.post(url=consult_client_endpoint,
                              name="CargaApiCustomar 32 - Buscar pedido antecipado",
                              catch_response=True, json=body) as response:
            resposta = loads(response.text or "null")

        try:
            print(
                f"============= \n 32 - Buscar pedido antecipado \n {resposta['success']} \n {len(resposta['data'])} \n Status Code: {response.status_code}")
            if resposta["success"] != True and len(resposta["data"]) != 16:
                response.failure(
                    f"Corpo de resposta diferente do esperado: {response.text}")
        except KeyError:
            print(
                f"============= \n 32 - FALHA ao buscar pedidos antecipados \n {response.text} \n Status code: {response.status_code}")
            response.failure(
                mensagemFalha
            )

    @task
    def obter_pedido_antecipado(self):

        consult_client_endpoint = f"{self.ENDPOINT_PRIFIX_CUSTOMER_PEDIDOS_ANTECIPADOS}/ObterPedidoAntecipado"
        body = {
            "codVendedor": "00357064",
            "codCliente": "0007425106",
            "numPedidoSAP": "1201074534",
            "dataSaida": "2022-01-10"
        }

        with self.client.post(url=consult_client_endpoint,
                              name="CargaApiCustomar 33 - Obter pedido antecipado",
                              catch_response=True, json=body) as response:
            resposta = loads(response.text or "null")

        try:
            print(
                f"============= \n 33 - Obter pedido antecipado \n {resposta['success']} \n {len(resposta['data'])} \n Status Code: {response.status_code}")
            if resposta["success"] != True and len(resposta["data"]) != 16:
                response.failure(
                    f"Corpo de resposta diferente do esperado: {response.text}")
        except KeyError:
            print(
                f"============= \n 33 - FALHA ao obter pedidos antecipados \n {response.text} \n Status code: {response.status_code}")
            response.failure(
                mensagemFalha
            )

class CargaApiProducts(HttpUser):

    host = "https://brf-api-pim-product.azurewebsites.net"
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

class CargaApiProductivity(HttpUser):
    
    host = "https://brf-api-pim-productivity.azurewebsites.net/"
    wait_time = between(1.0, 3.0)

    ENDPOINT_PRIFIX_PRODUCTIVITY = "/api/PainelIndicador"
    COD_VENDEDOR_PRODUCTIVITY = [
        "00580849",
        "00307501",
        "00553615"
    ]

    @task
    def painel_indicador_monta_filtro(self):

        consult_client_endpoint = f"{self.ENDPOINT_PRIFIX_PRODUCTIVITY}/MontaFiltro"
        body = {
           "codVendedor": choice(self.COD_VENDEDOR_PRODUCTIVITY)
        }

        with self.client.post(url=consult_client_endpoint,
                              name="CargaApiProductivity 01 - Painel indicador monta filtro",
                              catch_response=True, json=body) as response:
            resposta = loads(response.text or "null")

        try:
            print(
                f"============= \n 01 - Painel indicador monta filtro \n {resposta['success']} \n {len(resposta['data'])} \n Status Code: {response.status_code}")
            if resposta["success"] != True and len(resposta["data"]) != 8:
                response.failure(
                    f"Corpo de resposta diferente do esperado: {response.text}")
        except KeyError:
            print(
                f"============= \n 01 - FALHA montar filtro \n {response.text} \n Status code: {response.status_code}")
            response.failure(
                mensagemFalha
            )

    @task
    def painel_indicador_busca_indicador(self):

        consult_client_endpoint = f"{self.ENDPOINT_PRIFIX_PRODUCTIVITY}/BuscaIndicador"
        body = {
           "codVendedor": choice(self.COD_VENDEDOR_PRODUCTIVITY),
           "codCliente": "",
           "mesPesquisa": "ATUAL" 
        }

        with self.client.post(url=consult_client_endpoint,
                              name="CargaApiProductivity 02 - Painel indicador busca indicador",
                              catch_response=True, json=body) as response:
            resposta = loads(response.text or "null")

        try:
            print(
                f"============= \n 02 - Painel bsuca indicador \n {resposta['success']} \n {len(resposta['data'])} \n Status Code: {response.status_code}")
            if resposta["success"] != True and len(resposta["data"]) != 8:
                response.failure(
                    f"Corpo de resposta diferente do esperado: {response.text}")
        except KeyError:
            print(
                f"============= \n 02 - FALHA ao buscar indicador \n {response.text} \n Status code: {response.status_code}")
            response.failure(
                mensagemFalha
            )

class CargaApiLeadership(HttpUser):

    host = "https://brf-api-pim-leadership.azurewebsites.net"
    wait_time = between(1.0, 3.0)

    ENDPOINT_PRIFIX_LEADERSHIP = "/api/v1/phasing"

    @task
    def phasing_leadership(self):

        consult_client_endpoint = f"{self.ENDPOINT_PRIFIX_LEADERSHIP}/Volume/00511899/CurrentMonth"
        
        with self.client.get(url=consult_client_endpoint,
                             name="CargaApiLeadership 01 - Painel Faseamento",
                             catch_response=True) as response:
            resposta = loads(response.text or "null")

        try:
            print(
                f"============= \n 01 - Painel Faseamento \n {resposta['success']} \n {len(resposta['data'])} \n Status Code: {response.status_code}")
            if resposta["success"] != True and len(resposta["data"]) != 7:
                response.failure(
                    f"Corpo de resposta diferente do esperado: {response.text}")
        except KeyError:
            print(
                f"============= \n 01 - FALHA ao buscar resposta do faseamento \n {response.text} \n Status code: {response.status_code}")
            response.failure(
                mensagemFalha
            )        

if __name__ == "__main__":
    env = Environment(user_classes=[CargaApiCustomer])
    env.create_local_runner()
    env.create_web_ui("127.0.0.1", 8089)
    env.runner.start(500, spawn_rate=10)
    gevent.spawn_later(3600, lambda: env.runner.quit())
    env.runner.greenlet.join()
    env.web_ui.stop()
#  tags = ['teste'])