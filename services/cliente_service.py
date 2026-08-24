import os

from estruturas.lse import LSE
from services.persistencia_service import PersistenciaService


class ClienteService:

    def __init__(self):
        pasta_raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        pasta_data = os.path.join(pasta_raiz, "data")
    
        self.clientes = LSE()

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
            
    def cadastrar_cliente(self, nome):
        print('aqui')
    
    def listar_clientes(self):
        pass
    
    def buscar_cliente(self, codigo):
        pass
    
    def remover_cliente(self, codigo):
        pass