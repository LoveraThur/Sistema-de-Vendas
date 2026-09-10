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
        if produto.estoque < quantidade:
            raise ValueError(f"Estoque insuficiente para o produto {produto.nome}. Estoque atual: {produto.estoque}")

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
        pass
    
    def valor_total_vendas(self):
        pass
    
    def clientes_e_valores_totais_gastos(self):
        pass
    
    def cliente_que_mais_gastou(self):
        pass
    
    def produto_mais_vendido(self):
        pass
    
    def desfazer_ultima_operacao(self):
        pass