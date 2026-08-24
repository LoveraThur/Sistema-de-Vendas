import os

from estruturas.fila import Fila
from services.persistencia_service import PersistenciaService

class VendaService:
    def __init__(self):
        pasta_raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        pasta_data = os.path.join(pasta_raiz, "data")
    
        self.vendas = Fila()
        self.persistencia = PersistenciaService(pasta_data)
    
        self.carregar_dados()
    
    def carregar_dados(self):
        for cliente in self.persistencia.carregar_clientes():
            if self.clientes.buscar(cliente.codigo) is None:
                self.clientes.inserir_fim(cliente)
    
        for produto in self.persistencia.carregar_produtos():
            if self.produtos.buscar(produto.codigo) is None:
                self.produtos.inserir_fim(produto)
    
        for venda in self.persistencia.carregar_vendas():
            self.vendas.enqueue(venda)


    def realizar_venda_exemplo(self, codigo_cliente, codigo_produto, quantidade):
        pass
    
    def listar_vendas(self):
        pass
    
    def primeira_venda(self):
        pass
    
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