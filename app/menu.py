# app/menu.py
from app.controller import MenuController
from rich.console import Console
# ... resto igual


console = Console()

def exibir_menu():
    console.print("\n[bold cyan]Menu:[/bold cyan]")
    print("1 - Adicionar dinheiro")
    print("2 - Adicionar moedas")
    print("3 - Alterar nome")
    print("4 - Alterar ID")
    print("5 - Definir rank")
    print("6 - Liberar todos os carros")
    print("7 - Liberar equipamentos masculinos")
    print("8 - Liberar equipamentos femininos")
    print("9 - Combustível infinito")
    print("10 - Clonar conta")
    print("0 - Sair")

def main():
    console.print("[bold green]Sistema de Gerenciamento[/bold green]")
    chave = input("Digite a chave de acesso: ")
    controller = MenuController(chave)

    while True:
        opcao_inicial = input("Deseja fazer login ou registrar? (login/registrar): ").strip().lower()
        email = input("Email: ")
        senha = input("Senha: ")

        if opcao_inicial == "login":
            erro = controller.login(email, senha)
            if erro == 0:
                console.print("[green]Login realizado com sucesso![/green]")
                break
            else:
                console.print(f"[red]Erro no login (código {erro})[/red]")
        elif opcao_inicial == "registrar":
            erro = controller.register(email, senha)
            if erro == 0:
                console.print("[green]Conta registrada com sucesso![/green]")
            else:
                console.print(f"[red]Erro ao registrar (código {erro})[/red]")

    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ")

        match opcao:
            case "1":
                valor = int(input("Quantidade de dinheiro: "))
                controller.adicionar_dinheiro(valor)
            case "2":
                valor = int(input("Quantidade de moedas: "))
                controller.adicionar_moedas(valor)
            case "3":
                nome = input("Novo nome: ")
                controller.alterar_nome(nome)
            case "4":
                id = input("Novo ID: ")
                controller.alterar_id(id)
            case "5":
                controller.definir_rank()
            case "6":
                controller.liberar_todos_os_carros()
            case "7":
                controller.liberar_equipamentos_masculinos()
            case "8":
                controller.liberar_equipamentos_femininos()
            case "9":
                controller.combustível_infinito()
            case "10":
                novo_email = input("Email da nova conta: ")
                nova_senha = input("Senha da nova conta: ")
                controller.clonar_conta(novo_email, nova_senha)
            case "0":
                console.print("[bold red]Saindo...[/bold red]")
                break
            case _:
                console.print("[yellow]Opção inválida.[/yellow]")

if __name__ == "__main__":
    main()
