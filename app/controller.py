# controller.py
from noelcpm import CPMnoelcpm

class MenuController:
    def __init__(self, access_key):
        self.api = CPMnoelcpm(access_key)
        self.logged = False

    def login(self, email, password):
        erro = self.api.login(email, password)
        self.logged = erro == 0
        return erro

    def register(self, email, password):
        return self.api.register(email, password)

    def deletar_conta(self):
        self.api.delete()

    def definir_rank(self):
        return self.api.set_player_rank()

    def adicionar_dinheiro(self, amount):
        return self.api.set_player_money(amount)

    def adicionar_moedas(self, amount):
        return self.api.set_player_coins(amount)

    def alterar_nome(self, nome):
        return self.api.set_player_name(nome)

    def alterar_id(self, id):
        return self.api.set_player_localid(id)

    def adicionar_placas(self):
        return self.api.set_player_plates()

    def deletar_amigos(self):
        return self.api.delete_player_friends()

    def liberar_w16(self):
        return self.api.unlock_w16()

    def liberar_buzinas(self):
        return self.api.unlock_horns()

    def desativar_dano_motor(self):
        return self.api.disable_engine_damage()

    def combustível_infinito(self):
        return self.api.unlimited_fuel()

    def setar_vitorias(self, qtd):
        return self.api.set_player_wins(qtd)

    def setar_derrotas(self, qtd):
        return self.api.set_player_loses(qtd)

    def liberar_casas(self):
        return self.api.unlock_houses()

    def liberar_animacoes(self):
        return self.api.unlock_animations()

    def liberar_rodas(self):
        return self.api.unlock_wheels()

    def liberar_equipamentos_masculinos(self):
        return self.api.unlock_equipments_male()

    def liberar_equipamentos_femininos(self):
        return self.api.unlock_equipments_female()

    def liberar_fumaca(self):
        return self.api.unlock_smoke()

    def liberar_carros_pagos(self):
        return self.api.unlock_paid_cars()

    def liberar_todos_os_carros(self):
        return self.api.unlock_all_cars()

    def liberar_sirene_carros(self):
        return self.api.unlock_all_cars_siren()

    def clonar_conta(self, email, senha):
        return self.api.account_clone(email, senha)

    def get_dados_jogador(self):
        return self.api.get_player_data()
