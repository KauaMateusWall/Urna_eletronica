from tkinter import *

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
        senha = self.senha.get()
        if usuario == "teste" and senha == "teste":
            self.master.destroy()  # Fecha a tela de login
            self.abrir_votacao()   # Abre a tela de votação
        else:
            self.mensagem.config(text="Erro na autenticação", fg="red")

    # Método para abrir a tela de votação
    def abrir_votacao(self):
        root_votacao = Tk()
        VotingApp(root_votacao)
        root_votacao.mainloop()

class VotingApp:
    def __init__(self, master=None):
        self.master = master
        self.master.title("Sistema de Votação")

        self.candidatos = {
            1: {"nome": "Lula", "votos": 0},
            2: {"nome": "Bolsonaro", "votos": 0},
            3: {"nome": "Enéas Carneiro", "votos": 0}
        }

        self.votos_branco = 0
        self.votos_nulo = 0

        # Título da votação
        self.titulo = Label(master, text="Vote em um dos candidatos abaixo:", font=("Arial", 12, "bold"))
        self.titulo.pack(pady=10)

        # Botões de votação para cada candidato
        for id_candidato, dados in self.candidatos.items():
            botao = Button(master, text=f"Votar em {dados['nome']}", font=("Calibri", 10), command=lambda id=id_candidato: self.votar(id))
            botao.pack(pady=5)

        # Botão de voto em branco
        self.botao_branco = Button(master, text="Votar em Branco", font=("Calibri", 10), command=self.votar_branco)
        self.botao_branco.pack(pady=5)

        # Botão de voto nulo
        self.botao_nulo = Button(master, text="Votar Nulo", font=("Calibri", 10), command=self.votar_nulo)
        self.botao_nulo.pack(pady=5)

        # Label para exibir os resultados
        self.resultado_label = Label(master, text="", font=("Arial", 10))
        self.resultado_label.pack(pady=20)

        # Botão para mostrar resultados
        self.mostrar_resultados = Button(master, text="Mostrar Resultados", font=("Calibri", 10, "bold"), command=self.exibir_resultados)
        self.mostrar_resultados.pack(pady=10)

    def votar(self, id_candidato):
        self.candidatos[id_candidato]["votos"] += 1
        self.resultado_label.config(text=f"Voto computado para {self.candidatos[id_candidato]['nome']}")

    def votar_branco(self):
        self.votos_branco += 1
        self.resultado_label.config(text="Voto em Branco computado")

    def votar_nulo(self):
        self.votos_nulo += 1
        self.resultado_label.config(text="Voto Nulo computado")

    def exibir_resultados(self):
        resultados = "\n".join([f"{dados['nome']}: {dados['votos']} votos" for dados in self.candidatos.values()])
        resultados += f"\nBranco: {self.votos_branco} votos"
        resultados += f"\nNulo: {self.votos_nulo} votos"
        self.resultado_label.config(text=resultados)

# Inicializa a aplicação com a tela de login
root_login = Tk()
LoginApp(root_login)
root_login.mainloop()
