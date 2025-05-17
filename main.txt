#!/usr/bin/python

# ========================================
# Importações de Bibliotecas
# ========================================
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

# Importação do módulo personalizado para interação com o CPM
from noelcpm import CPMnoelcpm

# ========================================
# Configurações e Constantes
# ========================================
__CHANNEL_USERNAME__ = "bh_vendas"  # Nome do canal no Instagram
__GROUP_USERNAME__   = "67 99187-0782"  # Número do WhatsApp para contato

# ========================================
# Manipulador de Sinais para saída limpa
# ========================================
def signal_handler(sig, frame):
    """Função chamada quando o usuário pressiona Ctrl+C para sair"""
    print("\nSaindo... Até mais!")
    sys.exit(0)

# ========================================
# Utilitários de Texto e Cores
# ========================================
def gradient_text(text, colors):
    """
    Cria um efeito de gradiente no texto usando múltiplas cores
    Args:
        text: Texto a ser colorido
        colors: Lista de cores no formato RGB
    Returns:
        Texto formatado com o gradiente
    """
    lines = text.splitlines()
    height = len(lines)
    width = max(len(line) for line in lines)
    colorful_text = Text()
    
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char != ' ':
                # Calcula o índice da cor baseado na posição do caractere
                color_index = int(((x / (width - 1 if width > 1 else 1)) + 
                                 (y / (height - 1 if height > 1 else 1))) * 0.5 * (len(colors) - 1))
                color_index = min(max(color_index, 0), len(colors) - 1)
                style = Style(color=colors[color_index])
                colorful_text.append(char, style=style)
            else:
                colorful_text.append(char)
        colorful_text.append("\n")
    return colorful_text

def interpolate_color(start_color, end_color, fraction):
    """
    Interpola entre duas cores hexadecimais
    Args:
        start_color: Cor inicial (hex)
        end_color: Cor final (hex)
        fraction: Fração da interpolação (0 a 1)
    Returns:
        Cor interpolada (string hex)
    """
    start_rgb = tuple(int(start_color[i:i+2], 16) for i in (1, 3, 5))
    end_rgb = tuple(int(end_color[i:i+2], 16) for i in (1, 3, 5))
    interpolated_rgb = tuple(int(start + fraction * (end - start)) for start, end in zip(start_rgb, end_rgb))
    return "#{:02x}{:02x}{:02x}".format(*interpolated_rgb)

def rainbow_gradient_string(customer_name):
    """
    Cria um efeito arco-íris no texto
    Args:
        customer_name: Texto a ser formatado
    Returns:
        String com códigos de cores para efeito arco-íris
    """
    modified_string = ""
    num_chars = len(customer_name)
    # Gera cores aleatórias para início e fim do gradiente
    start_color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
    end_color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
    
    for i, char in enumerate(customer_name):
        fraction = i / max(num_chars - 1, 1)
        interpolated_color = interpolate_color(start_color, end_color, fraction)
        modified_string += f'[{interpolated_color}]{char}'
    return modified_string

# ========================================
# Funções de Interface do Usuário
# ========================================
def banner(console):
    """Exibe o banner colorido da ferramenta"""
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Texto principal do banner
    brand_name = "░▄▄░░▄░░▄░░░░░▄░░░▄░▄▄▄░▄▄░░░▄░▄▄░░░░▄▄▄ ░░▄▄▄▄░
░█░█░█░░█░░░░░█░░░█░█░░░█░█░░█░█░▀▄░█░░░█░█░░░░░
░█▄▀░█▄▄█░▄▄░░█░░░█░█▄░░█░░█░█░█░░█░█▄▄▄█░░▀█▄░░
░█░█░█░░█░░░░░░█░█░░█░░░█░░█░█░█░░█░█░░░█░░░░░█░
░█▄▀░█░░█░░░░░░░▀░░░█▄▄░█░░░▀█░█▄▄▀░█░░░█░▀▀▀▀░░"
    
    # Lista de cores para o efeito gradiente
    colors = [
        "rgb(255,0,0)", "rgb(255,69,0)", "rgb(255,140,0)", "rgb(255,215,0)", 
        "rgb(173,255,47)", "rgb(0,255,0)", "rgb(0,255,255)", "rgb(0,191,255)", 
        "rgb(0,0,255)", "rgb(139,0,255)", "rgb(255,0,255)"
    ]
    
    # Aplica o efeito gradiente
    colorful_text = gradient_text(brand_name, colors)
    console.print(colorful_text)
    
    # Linhas decorativas e informações de contato
    print(Colorate.Horizontal(Colors.rainbow, '='*70))
    print(Colorate.Horizontal(Colors.rainbow, '\tFAÇA LOGOUT DO CPM ANTES DE USAR ESTA FERRAMENTA'))
    print(Colorate.Horizontal(Colors.rainbow, 'COMPARTILHAR A CHAVE DE ACESSO NÃO É PERMITIDO - SERÁ BLOQUEADO'))
    print(Colorate.Horizontal(Colors.rainbow, f'INSTAGRAM: @{__CHANNEL_USERNAME__} WHATSAPP: {__GROUP_USERNAME__}'))
    print(Colorate.Horizontal(Colors.rainbow, '='*70))

def prompt_valid_value(content, tag, password=False):
    """
    Solicita entrada do usuário com validação
    Args:
        content: Texto a ser exibido no prompt
        tag: Identificador do campo para mensagens de erro
        password: Se True, oculta a entrada (para senhas)
    Returns:
        Valor válido inserido pelo usuário
    """
    while True:
        value = Prompt.ask(content, password=password)
        if not value or value.isspace():
            print(Colorate.Horizontal(Colors.rainbow, f'{tag} não pode estar vazio. Por favor, tente novamente.'))
        else:
            return value

# ========================================
# Funções de Carregamento de Dados
# ========================================
def load_player_data(cpm):
    """Carrega e exibe os dados do jogador"""
    response = cpm.get_player_data()
    
    if response.get('ok'):
        data = response.get('data')
        if all(key in data for key in ['floats', 'localID', 'money', 'coin']):
            print(Colorate.Horizontal(Colors.rainbow, '='*15 + '[ INFORMAÇÕES DO JOGADOR ]' + '='*15))
            print(Colorate.Horizontal(Colors.rainbow, f'NOME: {(data.get("Name") or "UNDEFINED")}'))
            print(Colorate.Horizontal(Colors.rainbow, f'ID NO JOGO: {data.get("localID")}'))
            print(Colorate.Horizontal(Colors.rainbow, f'DINHEIRO: {data.get("money")}'))
            print(Colorate.Horizontal(Colors.rainbow, f'GOLDS: {data.get("coin")}'))
        else:
            print(Colorate.Horizontal(Colors.rainbow, 'ERRO: Contas novas precisam entrar no jogo pelo menos uma vez!'))
            exit(1)
    else:
        print(Colorate.Horizontal(Colors.rainbow, 'ERRO: Seu login não está configurado corretamente!'))
        exit(1)

def load_key_data(cpm):
    """Carrega e exibe os dados da chave de acesso"""
    data = cpm.get_key_data()
    
    print(Colorate.Horizontal(Colors.rainbow, '='*15 + '[ DETALHES DA CHAVE DE ACESSO ]' + '='*15))
    print(Colorate.Horizontal(Colors.rainbow, f'CHAVE DE ACESSO: {data.get("access_key")}'))
    print(Colorate.Horizontal(Colors.rainbow, f'ID DO TELEGRAM: {data.get("telegram_id")}'))
    print(Colorate.Horizontal(Colors.rainbow, f'SALDO: {data.get("coins") if not data.get("is_unlimited") else "ILIMITADO"}'))

def load_client_details():
    """Obtém e exibe informações de localização do cliente"""
    response = requests.get("http://ip-api.com/json")
    data = response.json()
    
    print(Colorate.Horizontal(Colors.rainbow, '='*15 + '[ LOCALIZAÇÃO ]' + '='*15))
    print(Colorate.Horizontal(Colors.rainbow, f'IP: {data.get("query")}'))
    print(Colorate.Horizontal(Colors.rainbow, f'CIDADE: {data.get("city")}, {data.get("regionName")} ({data.get("countryCode")})'))
    print(Colorate.Horizontal(Colors.rainbow, f'PAÍS: {data.get("country")} - CEP: {data.get("zip")}'))
    print(Colorate.Horizontal(Colors.rainbow, '='*15 + '[ MENU ]' + '='*15))

# ========================================
# Programa Principal
# ========================================
if __name__ == "__main__":
    # Configurações iniciais
    console = Console()
    signal.signal(signal.SIGINT, signal_handler)  # Configura o handler para Ctrl+C
    
    # Loop principal de autenticação
    while True:
        # Exibe o banner e solicita credenciais
        banner(console)
        acc_email = prompt_valid_value("[bold][?] INSIRA SEU EMAIL[/bold]", "Email")
        acc_password = prompt_valid_value("[bold][?] INSIRA SUA SENHA[/bold]", "Senha", password=True)
        acc_access_key = prompt_valid_value("[bold][?] INSIRA SUA CHAVE DE ACESSO[/bold]", "Chave de Acesso")
        
        # Tenta fazer login
        console.print("[bold cyan][%] Tentando login...[/bold cyan]", end="")
        cpm = CPMnoelcpm(acc_access_key)
        login_response = cpm.login(acc_email, acc_password)
        
        # Processa a resposta do login
        if login_response != 0:
            if login_response == 100:
                print(Colorate.Horizontal(Colors.rainbow, 'ERRO: Conta não existe!'))
            elif login_response == 101:
                print(Colorate.Horizontal(Colors.rainbow, 'ERRO: Senha inválida!'))
            elif login_response == 103:
                print(Colorate.Horizontal(Colors.rainbow, 'ERRO: Chave de acesso inválida!'))
            else:
                print(Colorate.Horizontal(Colors.rainbow, 'ERRO: Tente novamente mais tarde!'))
                print(Colorate.Horizontal(Colors.rainbow, 'O banco de dados pode estar sobrecarregado!'))
            sleep(2)
            continue
        else:
            print(Colorate.Horizontal(Colors.rainbow, 'SUCESSO: Login realizado!'))
            sleep(2)
        
        # Menu principal de serviços
        while True:
            banner(console)
            load_player_data(cpm)
            load_key_data(cpm)
            load_client_details()
            
            # Exibe o menu de opções
            choices = [str(i) for i in range(27)]  # 0-26
            print(Colorate.Horizontal(Colors.rainbow, '{01}: ADICIONAR DINHEIRO (1.000K)'))
            print(Colorate.Horizontal(Colors.rainbow, '{02}: ADICIONAR GOLDS (3.500K)'))
            print(Colorate.Horizontal(Colors.rainbow, '{03}: INSERIR RANK KING (4.000K)'))
            print(Colorate.Horizontal(Colors.rainbow, '{04}: MUDAR ID (3.500K'))
            print(Colorate.Horizontal(Colors.rainbow, '{05}: MUDAR NOME (100 '))
            print(Colorate.Horizontal(Colors.rainbow, '{06}: MUDAR NOME ( RGB ) (100'))
            print(Colorate.Horizontal(Colors.rainbow, '{07}: NUMEROS PLACAS (2.000K'))
            print(Colorate.Horizontal(Colors.rainbow, '{08}: DELETAR CONTA (GRATIS '))
            print(Colorate.Horizontal(Colors.rainbow, '{09}: REGISTRAR CONTA (GRATIS'))
            print(Colorate.Horizontal(Colors.rainbow, '{10}: DELETAR AMIGOS (500'))
            print(Colorate.Horizontal(Colors.rainbow, '{11}: DESBLOQUEAR CARROS PAGOS (4.000K'))
            print(Colorate.Horizontal(Colors.rainbow, '{12}: DESBLOQUEAR TODOS CARROS (3.000K'))
            print(Colorate.Horizontal(Colors.rainbow, '{13}: SIRENE EM TODOS CARROS (2.000K'))
            print(Colorate.Horizontal(Colors.rainbow, '{14}: DESBLOQUEAR W16 (3.000K'))
            print(Colorate.Horizontal(Colors.rainbow, '{15}: DESBLOQUEAR BUZINAS (3.000K'))
            print(Colorate.Horizontal(Colors.rainbow, '{16}: MOTOR NAO QUEBRA (2.000K'))
            print(Colorate.Horizontal(Colors.rainbow, '{17}: GASOLINA INFINITA (2.000K'))
            print(Colorate.Horizontal(Colors.rainbow, '{18}: DESBLOQUEAR CASA 3 (3.500K'))
            print(Colorate.Horizontal(Colors.rainbow, '{19}: DESBLOQUEAR FUMACA (2.000K'))
            print(Colorate.Horizontal(Colors.rainbow, '{20}: DESBLOQUEAR ANIMAÇÕES (2.000K'))
            print(Colorate.Horizontal(Colors.rainbow, '{21}: DESBLOQUEAR RODAS (4.000K'))
            print(Colorate.Horizontal(Colors.rainbow, '{22}: DESBLOQUEAR ROUPAS MASCULINAS (3.000K'))
            print(Colorate.Horizontal(Colors.rainbow, '{23}: DESBLOQUEAR ROUPAS FEMININAS (3.000K'))
            print(Colorate.Horizontal(Colors.rainbow, '{24}: ALTERAR CORRIDAS GANHAS (1.000K'))
            print(Colorate.Horizontal(Colors.rainbow, '{25}: ALTERAR CORRIDAS PERDIDAS (1.000K'))
            print(Colorate.Horizontal(Colors.rainbow, '{26}: CLONAR CONTA (5.000K)'))
            print(Colorate.Horizontal(Colors.rainbow, '{00}: SAIR'))
            print(Colorate.Horizontal(Colors.rainbow, '='*15 + '[ CPM☆ ]' + '='*15))
            
            # Obtém a seleção do usuário
            service = IntPrompt.ask(
                "[bold][?] SELECIONE UM SERVIÇO [red][1-26 ou 0][/red][/bold]", 
                choices=choices, 
                show_choices=False
            )
            print(Colorate.Horizontal(Colors.rainbow, '='*15 + '[ CPM☆ ]' + '='*15))
            
            # Processa a seleção do serviço
            if service == 0:  # Sair
                print(Colorate.Horizontal(Colors.rainbow, f'Volte sempre! @{__CHANNEL_USERNAME__}'))
                break
                
            elif service == 1:  # Adicionar dinheiro
                print(Colorate.Horizontal(Colors.rainbow, '[?] QUANTIDADE DE DINHEIRO PARA ADICIONAR:'))
                amount = IntPrompt.ask("[?] QUANTIDADE", min=1, max=999999999)
                
                console.print("[%] PROCESSANDO...", end="")
                if cpm.set_player_money(amount):
                    print(Colorate.Horizontal(Colors.rainbow, 'SUCESSO: Dinheiro adicionado!'))
                    if Prompt.ask("[?] SAIR? (Y/N)", choices=["y", "n"], default="n") == "y":
                        break
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'ERRO: Falha ao adicionar dinheiro!'))
                    sleep(2)
            elif service == 2:  # Adicionar Golds
                print(Colorate.Horizontal(Colors.rainbow, '[?] QUANTIDADE DE GOLDS PARA ADICIONAR:'))
                amount = IntPrompt.ask("[?] QUANTIDADE", min=1, max=999999999)
                
                console.print("[%] PROCESSANDO...", end="")
                if cpm.set_player_coins(amount):
                    print(Colorate.Horizontal(Colors.rainbow, 'SUCESSO: Golds adicionados!'))
                    if Prompt.ask("[?] SAIR? (Y/N)", choices=["y", "n"], default="n") == "y":
                        break
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'ERRO: Falha ao adicionar golds!'))
                    sleep(2)

            elif service == 3:  # Inserir Rank King
                console.print("[!] ATENÇÃO: Se o King não aparecer, saia e abra o jogo algumas vezes.", end="")
                console.print("[!] NÃO DESBLOQUEIE O KING NA MESMA CONTA DUAS VEZES.", end="")
                sleep(2)
                
                console.print("[%] ADICIONANDO RANK KING...", end="")
                if cpm.set_player_rank():
                    print(Colorate.Horizontal(Colors.rainbow, 'SUCESSO: Rank King adicionado!'))
                    if Prompt.ask("[?] SAIR? (Y/N)", choices=["y", "n"], default="n") == "y":
                        break
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'ERRO: Falha ao adicionar rank!'))
                    sleep(2)

            elif service == 4:  # Mudar ID
                print(Colorate.Horizontal(Colors.rainbow, '[?] INSIRA O NOVO ID:'))
                new_id = Prompt.ask("[?] NOVO ID").upper()
                
                console.print("[%] PROCESSANDO...", end="")
                if len(new_id) > 0 and ' ' not in new_id:
                    if cpm.set_player_localid(new_id):
                        print(Colorate.Horizontal(Colors.rainbow, 'SUCESSO: ID alterado!'))
                        if Prompt.ask("[?] SAIR? (Y/N)", choices=["y", "n"], default="n") == "y":
                            break
                    else:
                        print(Colorate.Horizontal(Colors.rainbow, 'ERRO: ID já em uso!'))
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'ERRO: ID inválido!'))
                sleep(2)

            elif service == 5:  # Mudar Nome
                print(Colorate.Horizontal(Colors.rainbow, '[?] INSIRA O NOVO NOME:'))
                new_name = Prompt.ask("[?] NOME")
                
                console.print("[%] PROCESSANDO...", end="")
                if cpm.set_player_name(new_name):
                    print(Colorate.Horizontal(Colors.rainbow, 'SUCESSO: Nome alterado!'))
                    if Prompt.ask("[?] SAIR? (Y/N)", choices=["y", "n"], default="n") == "y":
                        break
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'ERRO: Falha ao alterar nome!'))
                    sleep(2)

            elif service == 6:  # Mudar Nome (RGB)
                print(Colorate.Horizontal(Colors.rainbow, '[?] INSIRA O NOVO NOME (EFEITO RGB):'))
                new_name = Prompt.ask("[?] NOME")
                
                console.print("[%] PROCESSANDO...", end="")
                if cpm.set_player_name(rainbow_gradient_string(new_name)):
                    print(Colorate.Horizontal(Colors.rainbow, 'SUCESSO: Nome RGB aplicado!'))
                    if Prompt.ask("[?] SAIR? (Y/N)", choices=["y", "n"], default="n") == "y":
                        break
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'ERRO: Falha ao aplicar efeito!'))
                    sleep(2)

            elif service == 7:  # Números em Placas
                console.print("[%] ADICIONANDO NÚMEROS NAS PLACAS...", end="")
                if cpm.set_player_plates():
                    print(Colorate.Horizontal(Colors.rainbow, 'SUCESSO: Placas modificadas!'))
                    if Prompt.ask("[?] SAIR? (Y/N)", choices=["y", "n"], default="n") == "y":
                        break
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'ERRO: Falha ao modificar placas!'))
                    sleep(2)

            elif service == 8:  # Deletar Conta
                print(Colorate.Horizontal(Colors.rainbow, '[!] ATENÇÃO: ESTA AÇÃO É IRREVERSÍVEL!'))
                confirm = Prompt.ask("[?] CONFIRMAR DELETAR CONTA? (Y/N)", choices=["y", "n"], default="n")
                
                if confirm == "y":
                    console.print("[%] DELETANDO CONTA...", end="")
                    if cpm.delete():
                        print(Colorate.Horizontal(Colors.rainbow, 'SUCESSO: Conta deletada!'))
                        break
                    else:
                        print(Colorate.Horizontal(Colors.rainbow, 'ERRO: Falha ao deletar conta!'))
                        sleep(2)

            elif service == 9:  # Registrar Conta
                print(Colorate.Horizontal(Colors.rainbow, '[!] REGISTRO DE NOVA CONTA'))
                new_email = prompt_valid_value("[?] INSIRA UM EMAIL", "Email")
                new_pass = prompt_valid_value("[?] INSIRA UMA SENHA", "Senha", password=True)
                
                console.print("[%] REGISTRANDO...", end="")
                status = cpm.register(new_email, new_pass)
                
                if status == 0:
                    print(Colorate.Horizontal(Colors.rainbow, 'SUCESSO: Conta criada!'))
                    print(Colorate.Horizontal(Colors.rainbow, 'ENTRE NO JOGO COM ESTA CONTA ANTES DE MODIFICÁ-LA'))
                    sleep(5)
                elif status == 105:
                    print(Colorate.Horizontal(Colors.rainbow, 'ERRO: Email já em uso!'))
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'ERRO: Falha no registro!'))
                sleep(2)

            elif service == 10:  # Deletar Amigos
                console.print("[%] DELETANDO LISTA DE AMIGOS...", end="")
                if cpm.delete_player_friends():
                    print(Colorate.Horizontal(Colors.rainbow, 'SUCESSO: Amigos removidos!'))
                    if Prompt.ask("[?] SAIR? (Y/N)", choices=["y", "n"], default="n") == "y":
                        break
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'ERRO: Falha ao remover amigos!'))
                    sleep(2)

            elif service == 11:  # Desbloquear Carros Pagos
                console.print("[!] ESTE PROCESSO PODE DEMORAR ALGUNS MINUTOS...", end="")
                console.print("[%] DESBLOQUEANDO CARROS PAGOS...", end="")
                if cpm.unlock_paid_cars():
                    print(Colorate.Horizontal(Colors.rainbow, 'SUCESSO: Carros desbloqueados!'))
                    if Prompt.ask("[?] SAIR? (Y/N)", choices=["y", "n"], default="n") == "y":
                        break
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'ERRO: Falha ao desbloquear carros!'))
                    sleep(2)

            elif service == 12:  # Desbloquear Todos Carros
                console.print("[%] DESBLOQUEANDO TODOS OS CARROS...", end="")
                if cpm.unlock_all_cars():
                    print(Colorate.Horizontal(Colors.rainbow, 'SUCESSO: Todos carros desbloqueados!'))
                    if Prompt.ask("[?] SAIR? (Y/N)", choices=["y", "n"], default="n") == "y":
                        break
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'ERRO: Falha ao desbloquear carros!'))
                    sleep(2)

            elif service == 13:  # Sirene em Todos Carros
                console.print("[%] ADICIONANDO SIRENE AOS CARROS...", end="")
                if cpm.unlock_all_cars_siren():
                    print(Colorate.Horizontal(Colors.rainbow, 'SUCESSO: Sirenes adicionadas!'))
                    if Prompt.ask("[?] SAIR? (Y/N)", choices=["y", "n"], default="n") == "y":
                        break
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'ERRO: Falha ao adicionar sirenes!'))
                    sleep(2)

            elif service == 14:  # Desbloquear W16
                console.print("[%] DESBLOQUEANDO MOTOR W16...", end="")
                if cpm.unlock_w16():
                    print(Colorate.Horizontal(Colors.rainbow, 'SUCESSO: W16 desbloqueado!'))
                    if Prompt.ask("[?] SAIR? (Y/N)", choices=["y", "n"], default="n") == "y":
                        break
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'ERRO: Falha ao desbloquear W16!'))
                    sleep(2)

            elif service == 15:  # Desbloquear Buzinas
                console.print("[%] DESBLOQUEANDO TODAS AS BUZINAS...", end="")
                if cpm.unlock_horns():
                    print(Colorate.Horizontal(Colors.rainbow, 'SUCESSO: Buzinas desbloqueadas!'))
                    if Prompt.ask("[?] SAIR? (Y/N)", choices=["y", "n"], default="n") == "y":
                        break
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'ERRO: Falha ao desbloquear buzinas!'))
                    sleep(2)

            elif service == 16:  # Motor Indestrutível
                console.print("[%] CONFIGURANDO MOTOR INDESTRUTÍVEL...", end="")
                if cpm.disable_engine_damage():
                    print(Colorate.Horizontal(Colors.rainbow, 'SUCESSO: Motor configurado!'))
                    if Prompt.ask("[?] SAIR? (Y/N)", choices=["y", "n"], default="n") == "y":
                        break
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'ERRO: Falha na configuração!'))
                    sleep(2)

            elif service == 17:  # Gasolina Infinita
                console.print("[%] CONFIGURANDO GASOLINA INFINITA...", end="")
                if cpm.unlimited_fuel():
                    print(Colorate.Horizontal(Colors.rainbow, 'SUCESSO: Gasolina infinita ativada!'))
                    if Prompt.ask("[?] SAIR? (Y/N)", choices=["y", "n"], default="n") == "y":
                        break
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'ERRO: Falha na configuração!'))
                    sleep(2)

            elif service == 18:  # Desbloquear Casa 3
                console.print("[%] DESBLOQUEANDO CASA 3...", end="")
                if cpm.unlock_houses():
                    print(Colorate.Horizontal(Colors.rainbow, 'SUCESSO: Casa 3 desbloqueada!'))
                    if Prompt.ask("[?] SAIR? (Y/N)", choices=["y", "n"], default="n") == "y":
                        break
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'ERRO: Falha ao desbloquear casa!'))
                    sleep(2)

            elif service == 19:  # Desbloquear Fumaça
                console.print("[%] DESBLOQUEANDO EFEITOS DE FUMO...", end="")
                if cpm.unlock_smoke():
                    print(Colorate.Horizontal(Colors.rainbow, 'SUCESSO: Fumaças desbloqueadas!'))
                    if Prompt.ask("[?] SAIR? (Y/N)", choices=["y", "n"], default="n") == "y":
                        break
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'ERRO: Falha ao desbloquear fumaças!'))
                    sleep(2)

            elif service == 20:  # Desbloquear Animações
                console.print("[%] DESBLOQUEANDO ANIMAÇÕES...", end="")
                if cpm.unlock_animations():
                    print(Colorate.Horizontal(Colors.rainbow, 'SUCESSO: Animações desbloqueadas!'))
                    if Prompt.ask("[?] SAIR? (Y/N)", choices=["y", "n"], default="n") == "y":
                        break
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'ERRO: Falha ao desbloquear animações!'))
                    sleep(2)

            elif service == 21:  # Desbloquear Rodas
                console.print("[%] DESBLOQUEANDO RODAS ESPECIAIS...", end="")
                if cpm.unlock_wheels():
                    print(Colorate.Horizontal(Colors.rainbow, 'SUCESSO: Rodas desbloqueadas!'))
                    if Prompt.ask("[?] SAIR? (Y/N)", choices=["y", "n"], default="n") == "y":
                        break
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'ERRO: Falha ao desbloquear rodas!'))
                    sleep(2)

            elif service == 22:  # Desbloquear Roupas Masculinas
                console.print("[%] DESBLOQUEANDO ROUPAS MASCULINAS...", end="")
                if cpm.unlock_equipments_male():
                    print(Colorate.Horizontal(Colors.rainbow, 'SUCESSO: Roupas desbloqueadas!'))
                    if Prompt.ask("[?] SAIR? (Y/N)", choices=["y", "n"], default="n") == "y":
                        break
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'ERRO: Falha ao desbloquear roupas!'))
                    sleep(2)

            elif service == 23:  # Desbloquear Roupas Femininas
                console.print("[%] DESBLOQUEANDO ROUPAS FEMININAS...", end="")
                if cpm.unlock_equipments_female():
                    print(Colorate.Horizontal(Colors.rainbow, 'SUCESSO: Roupas desbloqueadas!'))
                    if Prompt.ask("[?] SAIR? (Y/N)", choices=["y", "n"], default="n") == "y":
                        break
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'ERRO: Falha ao desbloquear roupas!'))
                    sleep(2)

            elif service == 24:  # Alterar Corridas Ganhas
                print(Colorate.Horizontal(Colors.rainbow, '[?] QUANTIDADE DE CORRIDAS GANHAS:'))
                amount = IntPrompt.ask("[?] QUANTIDADE", min=0, max=999999999)
                
                console.print("[%] PROCESSANDO...", end="")
                if cpm.set_player_wins(amount):
                    print(Colorate.Horizontal(Colors.rainbow, 'SUCESSO: Corridas ganhas atualizadas!'))
                    if Prompt.ask("[?] SAIR? (Y/N)", choices=["y", "n"], default="n") == "y":
                        break
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'ERRO: Falha ao atualizar!'))
                    sleep(2)

            elif service == 25:  # Alterar Corridas Perdidas
                print(Colorate.Horizontal(Colors.rainbow, '[?] QUANTIDADE DE CORRIDAS PERDIDAS:'))
                amount = IntPrompt.ask("[?] QUANTIDADE", min=0, max=999999999)
                
                console.print("[%] PROCESSANDO...", end="")
                if cpm.set_player_loses(amount):
                    print(Colorate.Horizontal(Colors.rainbow, 'SUCESSO: Corridas perdidas atualizadas!'))
                    if Prompt.ask("[?] SAIR? (Y/N)", choices=["y", "n"], default="n") == "y":
                        break
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'ERRO: Falha ao atualizar!'))
                    sleep(2)
            elif service == 26:  # Clonar conta
                print(Colorate.Horizontal(Colors.rainbow, '[!] O EMAIL DE DESTINO DEVE SER UMA CONTA EXISTENTE (CRIADA NA OPÇÃO 9)'))
                to_email = prompt_valid_value("[?] EMAIL DA CONTA DESTINO", "Email")
                to_password = prompt_valid_value("[?] SENHA DA CONTA DESTINO", "Senha", password=True)
                
                console.print("[%] CLONANDO CONTA...", end="")
                if cpm.account_clone(to_email, to_password):
                    print(Colorate.Horizontal(Colors.rainbow, 'SUCESSO: Conta clonada!'))
                    if Prompt.ask("[?] SAIR? (Y/N)", choices=["y", "n"], default="n") == "y":
                        break
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'ERRO: Falha ao clonar conta!'))
                    sleep(2)
        
        # Sai do loop principal após sair do menu
        break
