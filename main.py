#!/usr/bin/python

import random
import requests
from time import sleep
import os, signal, sys
from rich.console import Console
from rich.prompt import Prompt, IntPrompt
from rich.text import Text
from rich.style import Style
import pystyle
from pystyle import Colors, Colorate

from noelcpm import CPMnoelcpm

__CHANNEL_USERNAME__ = "@noel_vendas"
__GROUP_USERNAME__   = "11978458163"

def signal_handler(sig, frame):
    print("\n Bye Bye...")
    sys.exit(0)

def gradient_text(text, colors):
    lines = text.splitlines()
    height = len(lines)
    width = max(len(line) for line in lines)
    colorful_text = Text()
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char != ' ':
                color_index = int(((x / (width - 1 if width > 1 else 1)) + (y / (height - 1 if height > 1 else 1))) * 0.5 * (len(colors) - 1))
                color_index = min(max(color_index, 0), len(colors) - 1)  # Ensure the index is within bounds
                style = Style(color=colors[color_index])
                colorful_text.append(char, style=style)
            else:
                colorful_text.append(char)
        colorful_text.append("\n")
    return colorful_text

#BANNER PRINCIPAL

def banner(console):
    os.system('cls' if os.name == 'nt' else 'clear')

    # Cores atualizadas
    cor_borda = Style(color="#00ced1")          # Ciano claro para bordas
    cor_logo = Style(color="#000080", bgcolor="white")  # Azul naval com borda branca
    cor_texto = Style(color="white")            # Texto principal
    cor_destaque = Style(color="#00ced1")       # Ciano para bullets
    cor_aviso = Style(color="#0000ff")          # Azul para avisos

    # Banner com contornos simplificados
    banner_lines = [
        "┌───────────────────────────────────────────────────────────┐",
        "│                                                           │",
        "│                     ██████╗ ██╗  ██╗                      │",
        "│                     ██╔══██╗██║  ██║                      │",
        "│                     ██████╔╝███████║                      │",
        "│                     ██╔══██╗██╔══██║                      │",
        "│                     ██████╔╝██║  ██║                      │",
        "│                     ╚═════╝ ╚═╝  ╚═╝                      │",
        "│    ██╗   ██╗███████╗███╗   ██╗██████╗  █████╗ ███████╗    │",
        "│    ██║   ██║██╔════╝████╗  ██║██╔══██╗██╔══██╗██╔════╝    │",
        "│    ██║   ██║█████╗  ██╔██╗ ██║██║  ██║███████║███████╗    │",
        "│    ╚██╗ ██╔╝██╔══╝  ██║╚██╗██║██║  ██║██╔══██║╚════██║    │",
        "│     ╚████╔╝ ███████╗██║ ╚████║██████╔╝██║  ██║███████║    │",
        "│      ╚═══╝  ╚══════╝╚═╝  ╚═══╝╚═════╝ ╚═╝  ╚═╝╚══════╝    │", 
        "│                                                           │",
        "│           FERRAMENTA PREMIUM - BH VENDAS                  │",
        "│                                                           │",
        "│  • Desconecte-se da conta CPM antes de usar               │",
        "│  • Adquira sua key: (67) 99187-0782                       │",
        "│                                                           │",
        "│  ⚠ Não revenda sua licença ou compartilhe o tool          │",
        "│  ⚠ @bh_vendas - Suporte exclusivo                         │",
        "│                                                           │",
        "└───────────────────────────────────────────────────────────┘",
        "┌───────────────────────────────────────────────────────────┐",
        "│  © 2024 BH VENDAS - TODOS OS DIREITOS RESERVADOS          │",
        "└───────────────────────────────────────────────────────────┘"
    ]

    # Elementos especiais para estilização
    elementos = {
        'borda': "┌┐└┘─│",
        'detalhe': "•⚠",
        'logo': "█",
        'copy': "©"
    }

    # Renderização
    for line in banner_lines:
        styled_line = Text()
        for char in line:
            if char in elementos['borda']:
                styled_line.append(char, style=cor_borda)
            elif char in elementos['detalhe']:
                styled_line.append(char, style=cor_destaque)
            elif char in elementos['logo']:
                styled_line.append(char, style=cor_logo)
            elif char in elementos['copy']:
                styled_line.append(char, style=cor_destaque)
            else:
                styled_line.append(char, style=cor_texto)
        console.print(styled_line)




def load_player_data(cpm):
    response = cpm.get_player_data()

    # Cores atualizadas conforme solicitado
    ciano = Style(color="#00ced1")               # Ciano para rótulos (substitui o amarelo)
    azul_escuro = Style(color="#000080")         # Azul escuro para símbolos de separação
    ciano_escuro = Style(color="#008b8b")        # Ciano escuro para o título
    white = Style(color="white")                 # Branco para valores

    # Símbolos que devem ficar em AZUL ESCURO
    border_symbols = ['=', '[', ']', '-']

    if response.get('ok'):
        data = response.get('data')
        if 'floats' in data and 'localID' in data and 'money' in data and 'coin' in data:
            # Linha do título (em ciano escuro com símbolos em azul escuro)
            title_line = Text()
            title_text = "==========[ INFORMACOES DO JOGADOR ]=========="
            for char in title_text:
                if char in border_symbols:
                    title_line.append(char, azul_escuro)
                else:
                    title_line.append(char, ciano_escuro)

            console = Console()
            console.print(title_line)

            # Linhas de informações (rótulo em ciano, valor em branco)
            infos = [
                ("NOME", data.get('Name', 'UNDEFINED')),
                ("SEU ID NO JOGO", data.get('localID')),
                ("DINHEIRO", data.get('money')),
                ("GOLDS", data.get('coin'))
            ]

            for label, value in infos:
                line = Text()
                # Adiciona o rótulo em ciano
                line.append(f"{label}: ", ciano)
                # Adiciona o valor em branco
                line.append(str(value), white)
                console.print(line)

        else:
            error_line = Text()
            error_msg = "! ERRO: Contas novas devem ser movimentadas ao menos uma vez !"
            for char in error_msg:
                if char in border_symbols:
                    error_line.append(char, azul_escuro)
                else:
                    error_line.append(char, ciano)
            console.print(error_line)
            exit(1)
    else:
        error_line = Text()
        error_msg = "! ERRO: Seu login não está configurado corretamente !"
        for char in error_msg:
            if char in border_symbols:
                error_line.append(char, azul_escuro)
            else:
                error_line.append(char, ciano)
        console.print(error_line)
        exit(1)



def load_key_data(cpm):
    data = cpm.get_key_data()

    # Cores atualizadas conforme solicitado
    ciano = Style(color="#00ced1")               # Ciano para rótulos (substitui o amarelo)
    azul_escuro = Style(color="#000080")         # Azul escuro para símbolos de separação
    ciano_escuro = Style(color="#008b8b")        # Ciano escuro para o título
    white = Style(color="white")                 # Branco para valores

    # Símbolos que devem ficar em AZUL ESCURO
    border_symbols = ['=', '[', ']', '-']

    # Linha do título (em ciano escuro com símbolos em azul escuro)
    title_line = Text()
    title_text = "========[ DETALHES DA CHAVE DE ACESSO ]========"
    for char in title_text:
        if char in border_symbols:
            title_line.append(char, azul_escuro)
        else:
            title_line.append(char, ciano_escuro)

    console = Console()
    console.print(title_line)

    # Linhas de informações (rótulo em ciano, valor em branco)
    infos = [
        ("CHAVE DE ACESSO", str(data.get("access_key", "None"))),
        ("ID DO TELEGRAM", str(data.get("telegram_id", "None"))),
        ("SEU SALDO $", str(data.get("coins", "None")) if not data.get("is_unlimited", False) else "ilimitado")
    ]

    for label, value in infos:
        line = Text()
        # Adiciona o rótulo em ciano
        line.append(f"{label}: ", ciano)
        # Adiciona o valor em branco (garantindo que é string)
        line.append(str(value), white)
        console.print(line)



console = Console()

def prompt_valid_value(content, tag, password=False):
    while True:
        value = Prompt.ask(content, password=password)
        if not value or value.isspace():
            console.print(
                f"{tag} não pode estar vazio ou conter apenas espaços. Por favor, tente novamente.",
                style="bold red"
            )
        else:
            return value


def load_client_details():
    response = requests.get("http://ip-api.com/json")
    data = response.json()

    # Cores atualizadas conforme padrão solicitado
    ciano = Style(color="#00ced1")               # Ciano para rótulos
    azul_escuro = Style(color="#000080")        # Azul escuro para símbolos
    ciano_escuro = Style(color="#008b8b")       # Ciano escuro para títulos
    white = Style(color="white")                # Branco para valores

    # Símbolos que devem ficar em AZUL ESCURO
    border_symbols = ['=', '[', ']', '-']

    console = Console()

    # Título Localização (símbolos azul escuro, texto ciano escuro)
    title_line = Text()
    title_text = "=============[ LOCALIZACAO ]============="
    for char in title_text:
        if char in border_symbols:
            title_line.append(char, azul_escuro)
        else:
            title_line.append(char, ciano_escuro)
    console.print(title_line)

    # Dados de localização (rótulos em ciano, valores em branco)
    infos = [
        ("ENDERECO IP", data.get("query", "N/A")),
        ("CIDADE", f"{data.get('city', 'N/A')} {data.get('regionName', 'N/A')} {data.get('countryCode', 'N/A')}"),
        ("PAIS", f"{data.get('country', 'N/A')} {data.get('zip', '')}")
    ]

    for label, value in infos:
        line = Text()
        line.append(f"{label}: ", ciano)        # Rótulo em ciano
        line.append(str(value), white)          # Valor em branco
        console.print(line)

    # Título Menu (símbolos azul escuro, texto ciano escuro)
    menu_title = Text()
    menu_text = "===============[ MENU ]==============="
    for char in menu_text:
        if char in border_symbols:
            menu_title.append(char, azul_escuro)
        else:
            menu_title.append(char, ciano_escuro)
    console.print(menu_title)


def interpolate_color(start_color, end_color, fraction):
    start_rgb = tuple(int(start_color[i:i+2], 16) for i in (1, 3, 5))
    end_rgb = tuple(int(end_color[i:i+2], 16) for i in (1, 3, 5))
    interpolated_rgb = tuple(int(start + fraction * (end - start)) for start, end in zip(start_rgb, end_rgb))
    return "{:02x}{:02x}{:02x}".format(*interpolated_rgb)

def rainbow_gradient_string(customer_name):
    modified_string = ""
    num_chars = len(customer_name)
    start_color = "{:06x}".format(random.randint(0, 0xFFFFFF))
    end_color = "{:06x}".format(random.randint(0, 0xFFFFFF))
    for i, char in enumerate(customer_name):
        fraction = i / max(num_chars - 1, 1)
        interpolated_color = interpolate_color(start_color, end_color, fraction)
        modified_string += f'[{interpolated_color}]{char}'
    return modified_string



from rich.console import Console
from rich.text import Text
from rich.style import Style

def print_menu_line(line):
    """
    Imprime linhas formatadas do menu com padrão consistente
    """
    # Cores padronizadas conforme load_key_data
    ciano = Style(color="#00ced1")               # Ciano para rótulos
    azul_escuro = Style(color="#000080")         # Azul escuro para símbolos
    ciano_escuro = Style(color="#008b8b")        # Ciano escuro para títulos
    white = Style(color="white")                 # Branco para valores

    console = Console()
    try:
        if line.startswith('{') and ':' in line:
            # Para itens de menu (rótulo ciano, valor branco)
            num_part, rest = line.split(':', 1)

            if any(c.isdigit() for c in rest.split()[-1]):
                parts = rest.rsplit(maxsplit=1)
                if len(parts) == 2:
                    text_part, price_part = parts
                    styled_line = Text()
                    styled_line.append(f"{num_part}:", style=ciano)
                    styled_line.append(text_part, style=white)
                    styled_line.append(f" {price_part}", style="bright_black")
                    console.print(styled_line)
                else:
                    styled_line = Text()
                    styled_line.append(f"{num_part}:", style=ciano)
                    styled_line.append(rest, style="bright_black")
                    console.print(styled_line)
            else:
                styled_line = Text()
                styled_line.append(f"{num_part}:", style=ciano)
                styled_line.append(rest, style=white)
                console.print(styled_line)

        elif line.startswith('=') or line.startswith('[') or line.startswith('─'):
            # Linhas de separação padronizadas (como em load_key_data)
            title_line = Text()
            for char in line:
                if char in ['=', '[', ']', '─']:
                    title_line.append(char, style=azul_escuro)
                else:
                    title_line.append(char, style=ciano_escuro)
            console.print(title_line)

        else:
            console.print(line, style=white)

    except Exception:
        console.print(line, style=white)

if __name__ == "__main__":
    console = Console()
    signal.signal(signal.SIGINT, signal_handler)
    while True:
        banner(console)
        acc_email = prompt_valid_value("[bold][?] INSIRA SEU EMAIL[/bold]", "Email", password=False)
        acc_password = prompt_valid_value("[bold][?] INSIRA SUA SENHA[/bold]", "Password", password=False)
        acc_access_key = prompt_valid_value("[bold][?] INSIRA SUA CHAVE DE ACESSO[/bold]", "Access Key", password=False)
        console.print("[bold cyan][%] Trying to Login[/bold cyan]: ", end=None)
        cpm = CPMnoelcpm(acc_access_key)
        login_response = cpm.login(acc_email, acc_password)
        if login_response != 0:
            if login_response == 100:
                console.print("[bold red]ESSA CONTA NAO EXISTE.[/bold red]")
                sleep(2)
                continue
            elif login_response == 101:
                console.print("[bold red]SENHA INVALIDA.[/bold red]")
                sleep(2)
                continue
            elif login_response == 103:
                console.print("[bold red]CHAVE DE ACESSO INVALIDA.[/bold red]")
                sleep(2)
                continue
            else:
                console.print("[bold red]TENTE NOVAMENTE.[/bold red]")
                console.print("[bold red]! ATENCAO: BANCO DE DADOS LOTADO, FALE COM O SUPORTE ![/bold red]")
                sleep(2)
                continue
        else:
            console.print("[bold green]SUCESSO.[/bold green]")
            sleep(2)
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            load_player_data(cpm)
            load_key_data(cpm)
            load_client_details()
            choices = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26"]

            # Menu com separações padronizadas
            print_menu_line('{01}: ADICIONAR DINHEIRO           1.000K')
            print_menu_line('{02}: ADICIONAR GOLDS              3.500K')
            print_menu_line('{03}: INSERIR RANK KING            4.000K')
            print_menu_line('{04}: MUDAR ID                     3.500K')
            print_menu_line('{05}: MUDAR NOME                   100')
            print_menu_line('{06}: MUDAR NOME (RGB)             100')
            print_menu_line('{07}: NUMEROS PLACAS               2.000K')
            print_menu_line('{08}: DELETAR CONTA')
            print_menu_line('{09}: REGISTRAR CONTA')
            print_menu_line('{10}: DELETAR AMIGOS               500')
            print_menu_line('{11}: DESBLOQUEAR CARROS PAGOS     4.000K')
            print_menu_line('{12}: DESBLOQUEAR TODOS CARROS     3.000K')
            print_menu_line('{13}: SIRENE EM TODOS CARROS       2.000K')
            print_menu_line('{14}: DESBLOQUEAR W16              3.000K')
            print_menu_line('{15}: DESBLOQUEAR BUZINAS          3.000K')
            print_menu_line('{16}: MOTOR NAO QUEBRA             2.000K')
            print_menu_line('{17}: GASOLINA INFINITA            2.000K')
            print_menu_line('{18}: DESBLOQUEAR CASA 3           3.500K')
            print_menu_line('{19}: DESBLOQUEAR FUMACA           2.000K')
            print_menu_line('{20}: DESBLOQUEAR ANIMAÇÕES        2.000K')
            print_menu_line('{21}: DESBLOQUEAR RODAS            4.000K')
            print_menu_line('{22}: DESBLOQUEAR ROUPAS MASCULINAS 3.000K')
            print_menu_line('{23}: DESBLOQUEAR ROUPAS FEMININAS  3.000K')
            print_menu_line('{24}: ALTERAR CORRIDAS GANHAS      1.000K')
            print_menu_line('{25}: ALTERAR CORRIDAS PERDIDAS    1.000K')
            print_menu_line('{26}: CLONAR CONTA                 5.000K')
            print_menu_line('{0} : SAIR')
            print_menu_line("========[ 𝐂𝐏𝐌☆ ]========")

            service = IntPrompt.ask(f"[bold][?] SELECIONE UM SERVICO [red][1-{choices[-1]} or 0][/red][/bold]", 
                                  choices=choices, 
                                  show_choices=False)

            print_menu_line("========[ 𝐂𝐏𝐌☆ ]========")
            if service == 0:  # Exit
                console.print(f"[gold1]VOLTE SEMPRE....: @{__CHANNEL_USERNAME__}.[/gold1]")

            elif service == 1: # Increase Money
                console.print("[white][?] INSIRA A QUANTIDADE DE DINHEIRO QUE DESEJA ADICIONAR .[/white]")
                amount = IntPrompt.ask("[white][?] QUANTIDADE[/white]")
                console.print("[cyan][%] SALVANDO DADOS: [/cyan]", end="")

                if amount > 0 and amount <= 999999999:
                    if cpm.set_player_money(amount):
                        console.print("[bold green]SUCESSO[/bold green]")
                        console.print("[gold1]======================================[/gold1]")
                        answ = Prompt.ask("[blue][?] DESEJA SAIR ? USE Y PARA SIM E N PARA NAO [/blue]", 
                                        choices=["y", "n"], default="n")
                        if answ == "y": 
                            console.print(f"[gold1] VOLTE SEMPRE : @{__CHANNEL_USERNAME__}.[/gold1]")
                        else: 
                            continue
                    else:
                        console.print("[bold red]FALHA.[/bold red]")
                        console.print("[red]TENTE NOVAMENTE.[/red]")
                        sleep(2)
                        continue
                else:
                    console.print("[bold red]FALHA[/bold red]")
                    console.print("[red]UTILIZE VALORES VÁLIDOS.[/red]")
                    sleep(2)
                    continue


            elif service == 2:  # Increase Coins
                console.print("[white][?] INSIRA A QUANTIDADE DE GOLDS QUE DESEJA ADICIONAR.[/white]")
                amount = IntPrompt.ask("[white][?] QUANTIDADE[/white]")
                console.print("[cyan][%] SALVANDO DADOS: [/cyan]", end="")
                if amount > 0 and amount <= 999999999:
                    if cpm.set_player_coins(amount):
                        console.print("[bold green]SUCESSO[/bold green]")
                        console.print("[white]======================================[/white]")
                        answ = Prompt.ask("[white][?] DESEJA SAIR ? USE Y PARA SIM E N PARA NAO [/white]", 
                                        choices=["y", "n"], default="n")
                        if answ == "y": 
                            console.print(f"[white] VOLTE SEMPRE : @{__CHANNEL_USERNAME__}.[/white]")
                        else: 
                            continue
                    else:
                        console.print("[bold red]FALHA.[/bold red]")
                        console.print("[red]TENTE NOVAMENTE.[/red]")
                        sleep(2)
                        continue
                else:
                    console.print("[bold red]FALHA.[/bold red]")
                    console.print("[red]USE VALORES VALIDOS.[/red]")
                    sleep(2)
                    continue


            elif service == 3:  # King Rank
                console.print("[bold red][!] ATENCAO:[/bold red] SE O KING NAO APARECER, SAIA E ABRA O JOGO ALGUMAS VEZES.")
                console.print("[bold red][!] ATENCAO:[/bold red] POR FAVOR NAO DESBLOQUEIE O KING NA MESMA CONTA DUAS VEZES.")
                sleep(2)
                console.print("[cyan][%] ADICIONANDO O KING NA SUA CONTA: [/cyan]", end="")

                if cpm.set_player_rank():
                    console.print("[bold green]SUCESSO[/bold green]")
                    console.print("[white]======================================[/white]")
                    console.print("[white]======================================[/white]")

                    answ = Prompt.ask("[white][?] DESEJA SAIR ? USE Y PARA SIM E N PARA NAO ?[/white]", 
                                   choices=["y", "n"], default="n")
                    if answ == "y": 
                       console.print(f"[white]VOLTE SEMPRE....: @{__CHANNEL_USERNAME__}.[/white]")
                    else: 
                       continue
                else:
                    console.print("[bold red]FALHA.[/bold red]")
                    console.print("[red]TENTE NOVAMENTE.[/red]")
                    sleep(2)
                    continue


            elif service == 4:  # Change ID
                console.print("[white][?] INSIRA SEU NOVO ID.[/white]")
                new_id = Prompt.ask("[white][?] ID[/white]")
                console.print("[cyan][%] SALVANDO DADOS: [/cyan]", end="")

                if len(new_id) >= 0 and len(new_id) <= 999999999 and (' ' in new_id) == False:
                    if cpm.set_player_localid(new_id.upper()):
                        console.print("[bold green]SUCESSO[/bold green]")
                        console.print("[white]======================================[/white]")
                        answ = Prompt.ask("[white][?] DESEJA SAIR ? USE Y PARA SIM E N PARA NAO [/white]", 
                                        choices=["y", "n"], default="n")
                        if answ == "y": 
                            console.print(f"[white] VOLTE SEMPRE : @{__CHANNEL_USERNAME__}.[/white]")
                        else: 
                            continue
                    else:
                        console.print("[bold red]FALHA.[/bold red]")
                        console.print("[red]TENTE NOVAMENTE.[/red]")
                        sleep(2)
                        continue
                else:
                    console.print("[bold red]FALHA.[/bold red]")
                    console.print("[red]ESSE ID JA ESTA EM USO TENTE OUTRO.[/red]")
                    sleep(2)
                    continue


            elif service == 5:  # Change Name
                console.print("[white][?] INSIRA SEU NOVO NOME.[/white]")
                new_name = Prompt.ask("[white][?] NOME[/white]")
                console.print("[cyan][%] SALVANDO DADOS: [/cyan]", end="")

                if len(new_name) >= 0 and len(new_name) <= 999999999:
                    if cpm.set_player_name(new_name):
                        console.print("[bold green]SUCESSO[/bold green]")
                        console.print("[white]======================================[/white]")
                        answ = Prompt.ask("[white][?] DESEJA SAIR ? USE Y PARA SIM E N PARA NAO [/white]", 
                                        choices=["y", "n"], default="n")
                        if answ == "y": 
                            console.print(f"[white] VOLTE SEMPRE : @{__CHANNEL_USERNAME__}.[/white]")
                        else: 
                            continue
                    else:
                        console.print("[bold red]FALHA.[/bold red]")
                        console.print("[red]TENTE NOVAMENTE.[/red]")
                        sleep(2)
                        continue
                else:
                    console.print("[bold red]FALHA.[/bold red]")
                    console.print("[red]USE VALORES VALIDOS.[/red]")
                    sleep(2)
                    continue

            elif service == 6:  # Change Name Rainbow
                 console.print("[white][?] INSIRA SEU NOVO NOME (RGB).[/white]")
                 new_name = Prompt.ask("[white][?] NOME[/white]")
                 console.print("[cyan][%] SALVANDO DADOS: [/cyan]", end="")

                 if len(new_name) >= 0 and len(new_name) <= 999999999:
                     if cpm.set_player_name(rainbow_gradient_string(new_name)):  # Mantido o efeito RGB apenas aqui
                        console.print("[bold green]SUCESSO[/bold green]")
                        console.print("[white]======================================[/white]")
                        answ = Prompt.ask("[white][?] DESEJA SAIR ? USE Y PARA SIM E N PARA NAO [/white]", 
                                        choices=["y", "n"], default="n")
                        if answ == "y": 
                            console.print(f"[white] VOLTE SEMPRE : @{__CHANNEL_USERNAME__}.[/white]")
                        else: 
                             continue
                     else:
                         console.print("[bold red]FALHA.[/bold red]")
                         console.print("[red]TENTE NOVAMENTE.[/red]")
                         sleep(2)
                         continue
                 else:
                     console.print("[bold red]FALHA.[/bold red]")
                     console.print("[red]USE VALORES VALIDOS.[/red]")
                     sleep(2)
                     continue

            elif service == 7:  # Number Plates
                console.print("[cyan][%] ADICIONANDO NÚMERO ÀS PLACAS: [/cyan]", end="")
                if cpm.set_player_plates():
                    console.print("[bold green]SUCESSO[/bold green]")
                    console.print("[white]======================================[/white]")
                    answ = Prompt.ask("[white][?] DESEJA SAIR ? USE Y PARA SIM E N PARA NAO ?[/white]", 
                                    choices=["y", "n"], default="n")
                    if answ == "y": 
                       console.print(f"[white]VOLTE SEMPRE....: @{__CHANNEL_USERNAME__}.[/white]")
                    else: 
                        continue
                else:
                    console.print("[bold red]FALHA.[/bold red]")
                    console.print("[red]TENTE NOVAMENTE.[/red]")
                    sleep(2)
                    continue

            elif service == 8:  # Account Delete
                console.print("[bold red][!] APÓS DELETAR A CONTA NÃO TERÁ COMO VOLTAR ATRÁS!![/bold red]")
                answ = Prompt.ask("[white][?] DESEJA REALMENTE DELETAR A CONTA? (use 'y' para sim e 'n' para não)[/white]", 
                                choices=["y", "n"], default="n")
                if answ == "y":
                    cpm.delete()
                    console.print("[bold green]SUCESSO[/bold green]")
                    console.print("[white]======================================[/white]")
                    console.print(f"[white]VOLTE SEMPRE....: @{__CHANNEL_USERNAME__}.[/white]")
                else: 
                    continue

            elif service == 9:  # Account Register
                console.print("[yellow][!] VAMOS REGISTRAR SUA NOVA CONTA.[/yellow]")
                acc2_email = prompt_valid_value("[white][?] INSIRA UM EMAIL[/white]", "Email", password=False)
                acc2_password = prompt_valid_value("[white][?] INSIRA UMA SENHA[/white]", "Password", password=True)
                console.print("[cyan][%] CRIANDO SUA NOVA CONTA: [/cyan]", end="")

                status = cpm.register(acc2_email, acc2_password)
                if status == 0:
                    console.print("[bold green]SUCESSO[/bold green]")
                    console.print("[white]======================================[/white]")
                    console.print("[yellow]INFO: AGORA VOCÊ JÁ PODE MODIFICAR ESTA CONTA.[/yellow]")
                    console.print("[yellow]ENTRE PELO MENOS UMA VEZ NO JOGO USANDO ESSA CONTA ANTES DE ADICIONAR QUALQUER SERVIÇO.[/yellow]")
                    sleep(7)
                    continue
                elif status == 105:
                    console.print("[bold red]FALHA.[/bold red]")
                    console.print("[red]ESSE EMAIL JÁ EXISTE, TENTE UM NOVO EMAIL QUE NÃO ESTEJA SENDO USADO![/red]")
                    sleep(3)
                    continue
                else:
                    console.print("[bold red]FALHA.[/bold red]")
                    console.print("[red]TENTE NOVAMENTE.[/red]")
                    sleep(2)
                    continue

            elif service == 10:  # Delete Friends
                console.print("[cyan][%] DELETANDO SUA LISTA DE AMIGOS: [/cyan]", end="")
                if cpm.delete_player_friends():
                    console.print("[bold green]SUCESSO[/bold green]")
                    console.print("[white]======================================[/white]")
                    answ = Prompt.ask("[white][?] DESEJA SAIR? USE Y PARA SIM E N PARA NÃO[/white]", 
                                    choices=["y", "n"], default="n")
                    if answ == "y":
                        console.print(f"[white]VOLTE SEMPRE....: @{__CHANNEL_USERNAME__}.[/white]")
                    else:
                        continue
                else:
                    console.print("[bold red]FALHA.[/bold red]")
                    console.print("[red]TENTE NOVAMENTE.[/red]")
                    sleep(2)
                    continue

            elif service == 11:  # Unlock All Paid Cars
                console.print("[bold red][!] ATENÇÃO: ESSA FUNÇÃO DEMORA UM POUCO PARA SER CONCLUÍDA. NÃO CANCELE.[/bold red]")
                console.print("[cyan][%] DESBLOQUEANDO TODOS CARROS PAGOS: [/cyan]", end="")

                if cpm.unlock_paid_cars():
                    console.print("[bold green]SUCESSO[/bold green]")
                    console.print("[white]======================================[/white]")
                    answ = Prompt.ask("[white][?] DESEJA SAIR? USE Y PARA SIM E N PARA NÃO[/white]", 
                                    choices=["y", "n"], default="n")
                    if answ == "y":
                        console.print(f"[white]VOLTE SEMPRE....: @{__CHANNEL_USERNAME__}.[/white]")
                    else:
                        continue
                else:
                    console.print("[bold red]FALHA.[/bold red]")
                    console.print("[red]TENTE NOVAMENTE.[/red]")
                    sleep(2)
                    continue

            elif service == 12:  # Unlock All Cars
                 console.print("[cyan][%] DESBLOQUEANDO TODOS CARROS: [/cyan]", end="")

                 if cpm.unlock_all_cars():
                     console.print("[bold green]SUCESSO[/bold green]")
                     console.print("[white]======================================[/white]")
                     answ = Prompt.ask("[white][?] DESEJA SAIR? USE Y PARA SIM E N PARA NÃO[/white]", 
                                     choices=["y", "n"], default="n")
                     if answ == "y":
                         console.print(f"[white]VOLTE SEMPRE....: @{__CHANNEL_USERNAME__}.[/white]")
                     else:
                         continue
                 else:
                     console.print("[bold red]FALHA.[/bold red]")
                     console.print("[red]TENTE NOVAMENTE.[/red]")
                     sleep(2)
                     continue

            elif service == 13:  # Unlock All Cars Siren
                console.print("[cyan][%] ADICIONANDO SIRENE EM TODOS OS CARROS DA CONTA: [/cyan]", end="")

                if cpm.unlock_all_cars_siren():
                    console.print("[bold green]SUCESSO[/bold green]")
                    console.print("[white]======================================[/white]")
                    answ = Prompt.ask("[white][?] DESEJA SAIR? USE Y PARA SIM E N PARA NÃO[/white]", 
                                   choices=["y", "n"], default="n")
                    if answ == "y":
                       console.print(f"[white]VOLTE SEMPRE....: @{__CHANNEL_USERNAME__}.[/white]")
                    else:
                        continue
                else:
                    console.print("[bold red]FALHA.[/bold red]")
                    console.print("[red]TENTE NOVAMENTE.[/red]")
                    sleep(2)
                    continue


            elif service == 14:  # Unlock w16 Engine
                console.print("[cyan][%] DESBLOQUEANDO W16: [/cyan]", end="")

                if cpm.unlock_w16():
                    console.print("[bold green]SUCESSO[/bold green]")
                    console.print("[white]======================================[/white]")
                    answ = Prompt.ask("[white][?] DESEJA SAIR? USE Y PARA SIM E N PARA NÃO[/white]", 
                                    choices=["y", "n"], default="n")
                    if answ == "y":
                        console.print(f"[white]VOLTE SEMPRE....: @{__CHANNEL_USERNAME__}.[/white]")
                    else:
                        continue
                else:
                    console.print("[bold red]FALHA.[/bold red]")
                    console.print("[red]TENTE NOVAMENTE.[/red]")
                    sleep(2)
                    continue

            elif service == 15:  # Unlock All Horns
                console.print("[cyan][%] DESBLOQUEANDO TODAS AS BUZINAS: [/cyan]", end="")

                if cpm.unlock_horns():
                    console.print("[bold green]SUCESSO[/bold green]")
                    console.print("[white]======================================[/white]")
                    answ = Prompt.ask("[white][?] DESEJA SAIR? USE Y PARA SIM E N PARA NÃO[/white]", 
                                    choices=["y", "n"], default="n")
                    if answ == "y":
                        console.print(f"[white]VOLTE SEMPRE....: @{__CHANNEL_USERNAME__}.[/white]")
                    else: 
                        continue
                else:
                    console.print("[bold red]FALHA.[/bold red]")
                    console.print("[red]TENTE NOVAMENTE.[/red]")
                    sleep(2)
                    continue

            elif service == 16:  # Disable Engine Damage
                console.print("[cyan][%] DESATIVANDO DANO AO MOTOR: [/cyan]", end="")

                if cpm.disable_engine_damage():
                    console.print("[bold green]SUCESSO[/bold green]")
                    console.print("[white]======================================[/white]")
                    answ = Prompt.ask("[white][?] DESEJA SAIR? USE Y PARA SIM E N PARA NÃO[/white]", 
                                    choices=["y", "n"], default="n")
                    if answ == "y":
                        console.print(f"[white]VOLTE SEMPRE....: @{__CHANNEL_USERNAME__}.[/white]")
                    else:
                        continue
                else:
                    console.print("[bold red]FALHA.[/bold red]")
                    console.print("[red]TENTE NOVAMENTE.[/red]")
                    sleep(2)
                    continue

            elif service == 17:  # Unlimited Fuel
                console.print("[cyan][%] ATIVANDO GASOLINA INFINITA: [/cyan]", end="")

                if cpm.unlimited_fuel():
                    console.print("[bold green]SUCESSO[/bold green]")
                    console.print("[white]======================================[/white]")
                    answ = Prompt.ask("[white][?] DESEJA SAIR? USE Y PARA SIM E N PARA NÃO[/white]", 
                                    choices=["y", "n"], default="n")
                    if answ == "y":
                        console.print(f"[white]VOLTE SEMPRE....: @{__CHANNEL_USERNAME__}.[/white]")
                    else:
                        continue
                else:
                    console.print("[bold red]FALHA[/bold red]")
                    console.print("[red]TENTE NOVAMENTE.[/red]")
                    sleep(2)
                    continue


            elif service == 18:  # Unlock House 3
                console.print("[cyan][%] DESBLOQUEANDO CASA 3: [/cyan]", end="")

                if cpm.unlock_houses():
                    console.print("[bold green]SUCESSO[/bold green]")
                    console.print("[white]======================================[/white]")
                    answ = Prompt.ask("[white][?] DESEJA SAIR? USE Y PARA SIM E N PARA NÃO[/white]", 
                                    choices=["y", "n"], default="n")
                    if answ == "y":
                        console.print(f"[white]VOLTE SEMPRE....: @{__CHANNEL_USERNAME__}.[/white]")
                    else:
                        continue
                else:
                    console.print("[bold red]FALHA.[/bold red]")
                    console.print("[red]TENTE NOVAMENTE.[/red]")
                    sleep(2)
                    continue

            elif service == 19:  # Unlock Smoke
                console.print("[cyan][%] DESBLOQUEANDO FUMAÇA: [/cyan]", end="")

                if cpm.unlock_smoke():
                    console.print("[bold green]SUCESSO[/bold green]")
                    console.print("[white]======================================[/white]")
                    answ = Prompt.ask("[white][?] DESEJA SAIR? USE Y PARA SIM E N PARA NÃO[/white]", 
                                    choices=["y", "n"], default="n")
                    if answ == "y":
                        console.print(f"[white]VOLTE SEMPRE....: @{__CHANNEL_USERNAME__}.[/white]")
                    else: 
                        continue
                else:
                    console.print("[bold red]FALHA.[/bold red]")
                    console.print("[red]TENTE NOVAMENTE.[/red]")
                    sleep(2)
                    continue


            elif service == 20:  # Unlock Animations
                console.print("[cyan][%] DESBLOQUEANDO ANIMAÇÕES: [/cyan]", end="")

                if cpm.unlock_animations():
                    console.print("[bold green]SUCESSO[/bold green]")
                    console.print("[white]======================================[/white]")
                    answ = Prompt.ask("[white][?] DESEJA SAIR? USE Y PARA SIM E N PARA NÃO[/white]", 
                                    choices=["y", "n"], default="n")
                    if answ == "y":
                        console.print(f"[white]VOLTE SEMPRE....: @{__CHANNEL_USERNAME__}.[/white]")
                    else:
                        continue
                else:
                    console.print("[bold red]FALHA.[/bold red]")
                    console.print("[red]TENTE NOVAMENTE.[/red]")
                    sleep(2)
                    continue


            elif service == 21:  # Unlock Wheels
                console.print("[cyan][%] DESBLOQUEANDO RODAS: [/cyan]", end="")

                if cpm.unlock_wheels():
                    console.print("[bold green]SUCESSO[/bold green]")
                    console.print("[white]======================================[/white]")
                    answ = Prompt.ask("[white][?] DESEJA SAIR? USE Y PARA SIM E N PARA NÃO[/white]", 
                                    choices=["y", "n"], default="n")
                    if answ == "y":
                        console.print(f"[white]VOLTE SEMPRE....: @{__CHANNEL_USERNAME__}.[/white]")
                    else:
                        continue
                else:
                    console.print("[bold red]FALHA.[/bold red]")
                    console.print("[red]TENTE NOVAMENTE.[/red]")
                    sleep(2)
                    continue

            elif service == 22:  # Unlock Male Clothing
                console.print("[cyan][%] DESBLOQUEANDO ROUPAS MASCULINAS: [/cyan]", end="")

                if cpm.unlock_equipments_male():
                    console.print("[bold green]SUCESSO[/bold green]")
                    console.print("[white]======================================[/white]")
                    answ = Prompt.ask("[white][?] DESEJA SAIR? USE Y PARA SIM E N PARA NÃO[/white]", 
                                    choices=["y", "n"], default="n")
                    if answ == "y":
                        console.print(f"[white]VOLTE SEMPRE....: @{__CHANNEL_USERNAME__}.[/white]")
                    else:
                        continue
                else:
                    console.print("[bold red]FALHA.[/bold red]")
                    console.print("[red]TENTE NOVAMENTE.[/red]")
                    sleep(2)
                    continue


            elif service == 23:  # Unlock Female Clothing
                console.print("[cyan][%] DESBLOQUEANDO ROUPAS FEMININAS: [/cyan]", end="")

                if cpm.unlock_equipments_female():
                    console.print("[bold green]SUCESSO[/bold green]")
                    console.print("[white]======================================[/white]")
                    answ = Prompt.ask("[white][?] DESEJA SAIR? USE Y PARA SIM E N PARA NÃO[/white]", 
                                    choices=["y", "n"], default="n")
                    if answ == "y":
                        console.print(f"[white]VOLTE SEMPRE....: @{__CHANNEL_USERNAME__}.[/white]")
                    else:
                        continue
                else:
                    console.print("[bold red]FALHA.[/bold red]")
                    console.print("[red]TENTE NOVAMENTE.[/red]")
                    sleep(2)
                    continue

            elif service == 24:  # Change Races Wins
                console.print("[yellow][!] INSIRA A QUANTIDADE DE CORRIDAS GANHAS[/yellow]")
                amount = IntPrompt.ask("[white][?] INSIRA AQUI[/white]")
                console.print("[cyan][%] SALVANDO DADOS: [/cyan]", end="")

                if amount > 0 and amount <= 999999999999999999999999999:
                    if cpm.set_player_wins(amount):
                        console.print("[bold green]SUCESSO[/bold green]")
                        console.print("[white]======================================[/white]")
                        answ = Prompt.ask("[white][?] DESEJA SAIR? USE Y PARA SIM E N PARA NÃO[/white]", 
                                        choices=["y", "n"], default="n")
                        if answ == "y":
                            console.print(f"[white]VOLTEM SEMPRE: @{__CHANNEL_USERNAME__}.[/white]")
                        else:
                            continue
                    else:
                        console.print("[bold red]FALHA.[/bold red]")
                        console.print("[red]TENTE NOVAMENTE.[/red]")
                        sleep(2)
                        continue
                else:
                    console.print("[bold red]FALHA.[/bold red]")
                    console.print("[red][!] USE VALORES VÁLIDOS.[/red]")
                    sleep(2)
                    continue

            elif service == 25:  # Change Races Loses
                console.print("[yellow][!] INSIRA A QUANTIDADE DE CORRIDAS PERDIDAS[/yellow]")
                amount = IntPrompt.ask("[white][?] INSIRA AQUI[/white]")
                console.print("[cyan][%] SALVANDO DADOS: [/cyan]", end="")

                if amount > 0 and amount <= 999999999999999999999:
                    if cpm.set_player_loses(amount):
                        console.print("[bold green]BOA PARÇA, CONCLUÍDO[/bold green]")
                        console.print("[white]======================================[/white]")
                        answ = Prompt.ask("[white][?] DESEJA SAIR? USE Y PARA SIM E N PARA NÃO[/white]", 
                                        choices=["y", "n"], default="n")
                        if answ == "y":
                            console.print(f"[white]VOLTE SEMPRE....: @{__CHANNEL_USERNAME__}.[/white]")
                        else:
                            continue
                    else:
                        console.print("[bold red]VACILOU HEIN[/bold red]")
                        console.print("[red][!] COLOCA OS VALORES CERTOS PARÇA[/red]")
                        sleep(2)
                        continue
                else:
                    console.print("[bold red]VACILOU HEIN[/bold red]")
                    console.print("[red][!] COLOCA OS VALORES CERTOS PARÇA[/red]")
                    sleep(2)
                    continue

            elif service == 26:  # Clone Account
                console.print("[yellow][!] ADICIONE O EMAIL PARA CLONAR A CONTA NELE (OBRIGATÓRIO: SAIR DAS CONTAS ANTES!)[/yellow]")
                to_email = prompt_valid_value("[white][?] EMAIL DA CONTA[/white]", "Email", password=False)
                to_password = prompt_valid_value("[white][?] SENHA DA CONTA[/white]", "Password", password=True)
                console.print("[cyan][%] CLONANDO SUA CONTA: [/cyan]", end="")

                if cpm.account_clone(to_email, to_password):
                    console.print("[bold green]SUCESSO[/bold green]")
                    console.print("[white]======================================[/white]")
                    answ = Prompt.ask("[white][?] DESEJA SAIR? USE Y PARA SIM E N PARA NÃO[/white]", 
                                    choices=["y", "n"], default="n")
                    if answ == "y":
                        console.print(f"[white]VOLTE SEMPRE....: @{__CHANNEL_USERNAME__}.[/white]")
                    else:
                        continue
                else:
                    console.print("[bold red]VACILOU HEIN[/bold red]")
                    console.print("[red][!] USE OS DADOS CORRETOS PARÇA[/red]")
                    sleep(2)
                    continue
            else: continue
            break
        break
