from services.estoque_service import EstoqueService
from services.venda_service import VendaService
from services.cliente_service import ClienteService

def ler_inteiro(mensagem):
    valor = input(mensagem)
    return int(valor)

def ler_float(mensagem):
    valor = input(mensagem).replace(",", ".")
    return float(valor)

def pausar():
    input("\nPressione ENTER para continuar...")

def imprimir_registros(registros, mensagem_vazia):
    if len(registros) == 0:
        print(mensagem_vazia)
        return

    for registro in registros:
        print(registro)

def mostrar_menu():
    print("\n==============================")
    print("SISTEMA DE ESTOQUE E VENDAS")
    print("==============================")
    print("1 - Cadastrar cliente")
    print("2 - Listar clientes")
    print("3 - Buscar cliente")
    print("4 - Remover cliente")
    print("5 - Cadastrar produto")
    print("6 - Listar produtos")
    print("7 - Buscar produto")
    print("8 - Atualizar estoque")
    print("9 - Remover produto")
    print("10 - Listar produtos em ordem inversa")
    print("11 - Listar produtos ordenados por ID")
    print("12 - Buscar produto por ID usando Busca Binaria")
    print("13 - Realizar venda simples de exemplo")
    print("14 - Visualizar fila de vendas")
    print("15 - Visualizar primeira venda da fila")
    print("16 - Exibir valor total do estoque")
    print("17 - Exibir valor total das vendas")
    print("18 - Exibir clientes e valores totais gastos")
    print("19 - Exibir cliente que mais gastou")
    print("20 - Exibir produto mais vendido")
    print("21 - Desfazer ultima operacao")
    print("0 - Sair")


def executar_opcao(opcao, service, cliente, venda):
    if opcao == 1:
        while True:
            try:
                nome = str(input('Nome do Cliente: '))
                cliente.cadastrar_cliente(nome)
            except:
                print('Nome inválido!')
            
    elif opcao == 2:
        pass

    elif opcao == 3:
        pass

    elif opcao == 4:
        pass
    elif opcao == 5:

        nome_produto = input("Digite o nome do produto: ")
        preco = float(input("Digite o preco do produto: "))
        quantidade = int(input("Digite a quantidade do produto: "))
        produto = service.cadastrar_produto(nome_produto, preco, quantidade)
        print(f"Produto cadastrado com sucesso: {produto}")

    elif opcao == 6:
        produtos = service.listar_produtos()
        imprimir_registros(produtos, "Nenhum produto cadastrado.")
        pass

    elif opcao == 7:

        codigo = int(input("Digite o código do produto a ser buscado: "))
        produto = service.buscar_produto(codigo)
        if produto is None:
            print("Produto não encontrado.")
        else:
            print(f"Produto encontrado: {produto}")

    elif opcao == 8:
        return service.atualizar_estoque(int(input("Digite a quantidade a ser atualizada: ")))
        #corrigir erro aqui, pois não está pegando o produto correto para atualizar o estoque.
    elif opcao == 9:
        codigo = ler_inteiro("Codigo do produto que deseja remover: ")
        produto = service.buscar_produto(codigo)

        if produto is None:
            print(f"Produto com ID {codigo} nao encontrado.")
            return

        print("\nProduto selecionado:")
        print(produto)

        confirmacao = input(
            "Tem certeza que deseja remover este produto? (s/n): "
        ).strip().lower()

        if confirmacao not in ("s", "sim"):
            print("Remocao cancelada.")
            return

        removido = service.remover_produto(codigo)

        if removido is None:
            print("Nao foi possivel remover o produto.")
        else:
            print("\nProduto removido com sucesso!")
            print(removido)

    elif opcao == 10:
        produtos = service.listar_produtos_inverso()

        print("\nProdutos em ordem inversa:")
        imprimir_registros(
         produtos,
            "Nenhum produto cadastrado."
        )

    elif opcao == 11:
        produtos = service.listar_produtos_ordenados_por_id()

        print("\nProdutos ordenados por ID:")
        imprimir_registros(
            produtos,
            "Nenhum produto cadastrado."
        )

    elif opcao == 12:
        codigo = int(input("Codigo do produto para busca binaria: "))
        produto = service.buscar_produto_binario(codigo)

        if produto is None:
            print(f"Produto com ID {codigo} nao encontrado.")
        else:
            print("\nProduto encontrado por Busca Binaria:")
            print(produto)

    elif opcao == 13:
            codigo_cliente = int(input("Código do cliente: "))
            codigo_produto = int(input("Código do produto: "))
            quantidade = int(input("Quantidade: "))

            venda.realizar_venda_exemplo(codigo_cliente, codigo_produto, quantidade)

            print("Venda realizada!")

    elif opcao == 14:

        print(venda.listar_vendas())

    elif opcao == 15:
            primeira = venda.primeira_venda()

            if primeira is None:
                print("Nenhuma venda registrada.")
            else:
                print(primeira)

    elif opcao == 16:
        total = venda.valor_total_estoque()

        print(f"Valor total do estoque: R$ {total:.2f}")

    elif opcao == 17:
        total = venda.valor_total_vendas()

        print(f"Valor total das vendas: R$ {total:.2f}")

    elif opcao == 18:
        
        print(venda.clientes_e_valores_totais_gastos())

    elif opcao == 19:
        resultado = venda.cliente_que_mais_gastou()

        if resultado is None:
            print("Nenhuma venda registrada.")
        else:
            print(resultado)

    elif opcao == 20:
        resultado = venda.produto_mais_vendido()

        if resultado is None:
            print("Nenhuma venda registrada.")
        else:
            print(resultado)

    elif opcao == 21:

        resultado = venda.desfazer_ultima_operacao()

        if resultado is None:
            print("Não há operação para desfazer.")
        else:
            print("Última operação desfeita com sucesso.")
            print(resultado)

    else:
        print("Opcao invalida. Tente novamente.")

def main():
    service = EstoqueService()
    cliente = ClienteService()
    venda = VendaService()

    while True:
        mostrar_menu()

        try:
            opcao = ler_inteiro("Escolha uma opcao: ")

            if opcao == 0:
                print("Sistema encerrado.")
                break

            executar_opcao(opcao, service, cliente, venda)

        except ValueError as erro:
            print(f"Erro: {erro}")
        except IndexError as erro:
            print(f"Erro: {erro}")
        except NotImplementedError as erro:
            print(f"Funcionalidade para completar: {erro}")

        pausar()

if __name__ == "__main__":
    main()