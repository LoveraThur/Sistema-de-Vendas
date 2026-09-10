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
            totais[cliente.codigo] = 0

        for venda in self.vendas.listar():
            if venda.codigo_cliente not in totais:
                totais[venda.codigo_cliente] = 0
            totais[venda.codigo_cliente] += venda.valor_total

        return totais


    def cliente_que_mais_gastou(self):
        totais = self.clientes_e_valores_totais_gastos()
        if not self.vendas.listar():
            return None

        codigo_cliente_mais_gastou = max(totais, key=totais.get)

        return {
            "codigo_cliente": codigo_cliente_mais_gastou,
            "total_gasto": totais[codigo_cliente_mais_gastou],
        }
    def produto_mais_vendido(self):
        quantidades = {}
        for venda in self.vendas.listar():
            for item in venda.itens:
                codigo = item["codigo_produto"]
                quantidades[codigo] = quantidades.get(codigo, 0) + item["quantidade"]

        if not quantidades:
            return None

        codigo_produto_mais_vendido = max(quantidades, key=quantidades.get)

        return {
            "codigo_produto": codigo_produto_mais_vendido,
            "quantidade_vendida": quantidades[codigo_produto_mais_vendido],
        }

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