import os

from models.cliente import Cliente
from estruturas.fila import Fila
from estruturas.lse import LSE
from services.persistencia_service import PersistenciaService


class ClienteService:

    def __init__(self):
        pasta_raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        pasta_data = os.path.join(pasta_raiz, "data")
    
        self.clientes = LSE()
        self.cliente = Cliente
        self.persistencia = PersistenciaService(pasta_data)
    
        self.carregar_dados()
    
    def carregar_dados(self):
        for cliente in self.persistencia.carregar_clientes():
            if self.clientes.buscar(cliente.codigo) is None:
                self.clientes.inserir_fim(cliente)

    def salvar_clientes(self):
            self.persistencia.salvar_clientes(self.clientes.listar())
            
    def cadastrar_cliente(self, nome):
        self.clientes.inserir_fim(nome)
        self.cliente
        #aperfeiçoar: importar classe cliente, criar intancia de cliente, adicionar no inserir fim
        # salvar arquivo do cliente e retornar.
    
    def listar_clientes(self):
        return self.clientes.listar()
    
    def buscar_cliente(self, codigo): 
        return self.clientes.buscar(codigo)
     
    def remover_cliente(self, codigo):
        return self.clientes.remover(codigo) 
    #salvar quando o valor for removido.
        