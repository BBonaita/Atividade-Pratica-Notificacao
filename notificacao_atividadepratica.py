from abc import ABC, abstractmethod
from typing import List


# Interface do Observador
class Observer(ABC):
    @abstractmethod
    def update(self, message: str):
        pass

# Interface do Sujeito (Subject)
class Subject(ABC):
    @abstractmethod
    def attach(self, observer: Observer):
        pass

    @abstractmethod
    def detach(self, observer: Observer):
        pass

    @abstractmethod
    def notify_observers(self, message: str):
        pass


# ---------------------------
# Usuário (Observer Concreto)
# ---------------------------

class User(Observer):
    def __init__(self, name: str, age: int, phone: str, email: str, notification_strategy: 'Notification'):
        self.name = name
        self.age = age
        self.phone = phone
        self.email = email
        self.notification_strategy = notification_strategy

    def update(self, message: str):
        # Notifica o usuário com base na estratégia definida
        self.notification_strategy.send(self.name, message)


# ---------------------------
# Estratégia de Notificação
# ---------------------------

class Notification(ABC):
    @abstractmethod
    def send(self, username: str, message: str):
        pass

class EmailNotification(Notification):
    def send(self, username: str, message: str):
        print(f"[EMAIL] Para: {username} - Mensagem: {message}")

class SMSNotification(Notification):
    def send(self, username: str, message: str):
        print(f"[SMS] Para: {username} - Mensagem: {message}")

class AppNotification(Notification):
    def send(self, username: str, message: str):
        print(f"[APP] Para: {username} - Mensagem: {message}")


# ---------------------------
# Factory Method
# ---------------------------

class NotificationFactory:
    @staticmethod
    def create_notification(notification_type: str) -> Notification:
        if notification_type == 'email':
            return EmailNotification()
        elif notification_type == 'sms':
            return SMSNotification()
        elif notification_type == 'app':
            return AppNotification()
        else:
            raise ValueError(f"Tipo de notificação desconhecido: {notification_type}")


# ---------------------------
# Sistema de Notificação (Subject)
# ---------------------------

class NotificationSystem(Subject):
    def __init__(self):
        self._observers: List[Observer] = []

    def attach(self, observer: Observer):
        self._observers.append(observer)

    def detach(self, observer: Observer):
        self._observers.remove(observer)

    def notify_observers(self, message: str):
        for observer in self._observers:
            observer.update(message)


# ---------------------------
# Interface de Cadastro
# ---------------------------

def cadastrar_usuario(sistema: NotificationSystem):
    print("\n=== Cadastro de Novo Usuário ===")
    nome = input("Nome: ")
    idade = int(input("Idade: "))
    telefone = input("Número de telefone: ")
    email = input("E-mail: ")
    print("Tipo de notificação (email / sms / app):")
    tipo = input("Escolha: ").strip().lower()

    try:
        notificacao = NotificationFactory.create_notification(tipo)
        novo_usuario = User(nome, idade, telefone, email, notificacao)
        sistema.attach(novo_usuario)
        print(f"Usuário {nome} cadastrado com sucesso!\n")
    except ValueError as e:
        print(e)


# ---------------------------
# Programa Principal
# ---------------------------

if __name__ == "__main__":
    sistema = NotificationSystem()

    while True:
        print("1. Cadastrar novo usuário")
        print("2. Enviar notificação")
        print("3. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cadastrar_usuario(sistema)
        elif opcao == "2":
            mensagem = input("Digite a mensagem da notificação: ")
            sistema.notify_observers(mensagem)
        elif opcao == "3":
            print("Encerrando o sistema.")
            break
        else:
            print("Opção inválida. Tente novamente.\n")
