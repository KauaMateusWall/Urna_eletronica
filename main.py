from tkinter import *
import mysql.connector
from mysql.connector import errorcode

# Conexão com o banco de dados
conn = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="0000",
    database="urna"
)

cursor = conn.cursor()

# Função para verificar se o usuário já votou
def identificar_usuario(idUsuario):
    cursor.execute("SELECT id_usuario FROM votos WHERE id_usuario = %s", (idUsuario,))
    for _ in cursor:
        return False
    return True

# Função para inserir o voto no banco de dados
def votar(idUsuario, idCandidato):
    cursor.execute("INSERT INTO votos(id_candidato, id_usuario) VALUES(%s, %s)", (idCandidato, idUsuario))
    conn.commit()
    return True

class LoginApp:
    def __init__(self, master=None):
        self.master = master
        self.master.title("Tela de Login")

        # Container e título
        self.fontePadrao = ("Arial", "10")
        self.titulo = Label(master, text="Dados do usuário", font=("Arial", "10", "bold"))
        self.titulo.pack(pady=10)

        # Campo para o Nome do Usuário
        self.nomeLabel = Label(master, text="Usuário", font=self.fontePadrao)
        self.nomeLabel.pack()

        self.nome = Entry(master, font=self.fontePadrao)
        self.nome.pack()

        # Campo para a Senha
        self.senhaLabel = Label(master, text="Senha", font=self.fontePadrao)
        self.senhaLabel.pack()

        self.senha = Entry(master, show="*", font=self.fontePadrao)
        self.senha.pack()

        # Botão de Entrar
        self.entrar = Button(master, text="Entrar", font=("Calibri", "8"), width=12, command=self.verificaSenha)
        self.entrar.pack(pady=10)

        # Mensagem de retorno
        self.mensagem = Label(master, text="", font=self.fontePadrao)
        self.mensagem.pack()

    # Método para verificar a senha e abrir a tela de votação
    def verificaSenha(self):
        usuario = self.nome.get()
        
        idUsuario = int(usuario)
        if identificar_usuario(idUsuario):
            self.master.destroy()
            self.abrir_votacao(idUsuario)
        else:
            self.mensagem.config(text="Usuário já votou.", fg="red")
        return

    # Método para abrir a tela de votação
    def abrir_votacao(self, idUsuario):
        root_votacao = Tk()
        VotingApp(root_votacao, idUsuario)
        root_votacao.mainloop()

class VotingApp:
    def __init__(self, master=None, idUsuario=None):
        self.master = master
        self.master.title("Sistema de Votação")
        self.idUsuario = idUsuario

        # Definindo candidatos
        self.candidatos = {
            1: "Lula",
            2: "Bolsonaro",
            3: "Enéas Carneiro"
        }

        # Título da votação
        self.titulo = Label(master, text="Digite o número do candidato:", font=("Arial", 12, "bold"))
        self.titulo.pack(pady=10)

        # Caixa de entrada para o número do candidato
        self.numero_candidato = Entry(master, font=("Arial", 10))
        self.numero_candidato.pack(pady=5)

        # Botão para confirmar o voto
        self.botao_votar = Button(master, text="Votar", font=("Calibri", 10), command=self.registrar_voto)
        self.botao_votar.pack(pady=10)

        # Mensagem de confirmação
        self.mensagem = Label(master, text="", font=("Arial", 10))
        self.mensagem.pack(pady=20)

    def registrar_voto(self):
        try:
            id_candidato = int(self.numero_candidato.get())
            if id_candidato in self.candidatos:
                votar(self.idUsuario, id_candidato)
                self.mensagem.config(text=f"Voto computado para {self.candidatos[id_candidato]}")
            elif id_candidato == 0:
                votar(self.idUsuario, 0)  # Voto em branco
                self.mensagem.config(text="Voto em Branco computado")
            else:
                votar(self.idUsuario, -1)  # Voto nulo
                self.mensagem.config(text="Voto Nulo computado")
            
            self.master.after(2000, self.master.destroy)  # Fecha a tela após 2 segundos
        except ValueError:
            self.mensagem.config(text="Digite um número válido.", fg="red")

# Inicializa a aplicação com a tela de login
root_login = Tk()
LoginApp(root_login)
root_login.mainloop()

# Fecha a conexão com o banco de dados
conn.close()
