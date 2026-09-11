import os

from estruturas.fila import Fila
from estruturas.lde import LDE
from estruturas.lse import LSE
from services.persistencia_service import PersistenciaService
from models.venda import Venda

class VendaService:
    def __init__(self):
        pasta_raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        pasta_data = os.path.join(pasta_raiz, "data")
    
        self.clientes = LSE()
        self.produtos = LDE()
        self.vendas = Fila()
        self.persistencia = PersistenciaService(pasta_data)
    
        self.carregar_dados()
    
    def carregar_dados(self):
        for produto in self.persistencia.carregar_produtos():
            if self.produtos.buscar(produto.codigo) is None:
                self.produtos.inserir_fim(produto)
    
        for venda in self.persistencia.carregar_vendas():
            self.vendas.enqueue(venda)


    def realizar_venda_exemplo(self, codigo_cliente, codigo_produto, quantidade):

        cliente = self.clientes.buscar(codigo_cliente)
        produto = self.produtos.buscar(codigo_produto)

        if cliente is None:
            raise ValueError(f"Cliente com ID {codigo_cliente} não encontrado.")
        if produto is None:
            raise ValueError(f"Produto com ID {codigo_produto} não encontrado.")    
        if quantidade <= 0:
            raise ValueError("A quantidade deve ser maior que zero.")
        if produto.quantidade < quantidade:
            raise ValueError(f"Estoque insuficiente para o produto {produto.nome}. Estoque atual: {produto.quantidade}")

        vendas = self.vendas.listar()
        codigo_venda = len(vendas) + 1

        codigo_venda = max((venda.codigo for venda in vendas), default=0) + 1

        item = {
            "codigo_produto": produto.codigo,
            "quantidade": quantidade,
            "preco_unitario": produto.preco
        }

        venda = Venda(codigo_venda, codigo_cliente, [item])

        produto.atualizar_estoque(-quantidade)
        self.vendas.enqueue(venda)

        self.persistencia.salvar_vendas(self.vendas.listar())
        self.persistencia.salvar_produtos(self.produtos.listar())

        return venda
        
    
    def listar_vendas(self):
        return self.vendas.listar()
    
    def primeira_venda(self):

        if self.vendas.is_empty():
            return None

        return self.vendas.front()
    
    def valor_total_estoque(self):
        total = 0
        
        for produto in self.produtos.listar():
            total += produto.preco * produto.quantidade
            
        return total 
    
    def valor_total_vendas(self):
        total = 0

        for venda in self.vendas.listar():
            for item in venda.itens:
                total += item["quantidade"] * item["preco_unitario"]
        return total
    
    def clientes_e_valores_totais_gastos(self):
        totais = {}

        for cliente in self.clientes.listar():
            totais[cliente.nome] = 0

        for venda in self.vendas.listar():
            cliente = self.clientes.buscar(venda.codigo_cliente)

            if cliente is not None:
                totais[cliente.nome] += venda.valor_total

        return totais


    def cliente_que_mais_gastou(self):
        if not self.vendas.listar():
            return None

        totais = self.clientes_e_valores_totais_gastos()

        maior_nome = None
        maior_total = 0

        for nome, total in totais.items():
            if maior_nome is None or total > maior_total:
                maior_nome = nome
                maior_total = total

        return maior_nome, maior_total

    def produto_mais_vendido(self):
        quantidades = {}

        for venda in self.vendas.listar():
            for item in venda.itens:
                codigo = item["codigo_produto"]

                if codigo not in quantidades:
                    quantidades[codigo] = 0

                quantidades[codigo] += item["quantidade"]

        if not quantidades:
            return None

        codigo_mais_vendido = None
        maior_quantidade = 0

        for codigo, quantidade in quantidades.items():
            if quantidade > maior_quantidade:
                codigo_mais_vendido = codigo
                maior_quantidade = quantidade

        produto = self.produtos.buscar(codigo_mais_vendido)

        if produto is None:
            return None
        return produto.nome, maior_quantidade

    
    def desfazer_ultima_operacao(self):
        vendas = self.vendas.listar()
        if not vendas:
            return None

        ultima_venda = vendas.pop()
        for item in ultima_venda.itens:
            produto = self.produtos.buscar(item["codigo_produto"])
            if produto is not None:
                produto.atualizar_estoque(item["quantidade"])

        self.vendas = Fila()

        for venda in vendas:
            self.vendas.enqueue(venda)

        self.persistencia.salvar_vendas(self.vendas.listar())
        self.persistencia.salvar_produtos(self.produtos.listar())

        return ultima_venda