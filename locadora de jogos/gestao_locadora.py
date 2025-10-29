from datetime import date

# --- C. Testes e Tratamento de Erros (Exceções Customizadas) ---

class JogoIndisponivelException(Exception):
    """Exceção para quando se tenta alugar um jogo já alugado."""
    pass

class JogoNaoAlugadoException(Exception):
    """Exceção para quando se tenta devolver um jogo que não está alugado por aquele cliente."""
    pass

class LimiteAlugueisException(Exception):
    """Exceção para quando o cliente tenta alugar mais jogos que o limite."""
    pass


# --- A. Modelagem POO (Classes) ---

class Jogo:
    """
    Representa um Jogo (mídia física) da locadora.
    """
    def __init__(self, titulo: str, plataforma: str, codigo_barras: str):
        self.titulo = titulo
        self.plataforma = plataforma
        self.codigo_barras = codigo_barras
        self.disponivel = True

    def __str__(self):
        status = "Disponível" if self.disponivel else "Alugado"
        return f"Jogo: {self.titulo} [{self.plataforma}] - {status}"

    def alugar(self):
        """Muda o status do jogo para 'alugado' (indisponível)."""
        if not self.disponivel:
            raise JogoIndisponivelException(f"O jogo {self.titulo} [{self.plataforma}] já está alugado.")
        self.disponivel = False

    def devolver(self):
        """Muda o status do jogo para 'disponível'."""
        self.disponivel = True


class Cliente:
    """
    Representa um cliente (usuário) da locadora.
    """
    # Constantes definidas na classe
    LIMITE_ALUGUEIS = 3
    MULTA_POR_DIA = 1.00 # R$ 1,00 por dia de atraso

    def __init__(self, nome: str, id_cliente: str):
        self.nome = nome
        self.id_cliente = id_cliente
        # Armazena os aluguéis ativos em dicionários
        self.jogos_alugados = [] 

    def __str__(self):
        return f"Cliente: {self.nome} (ID: {self.id_cliente})"

    def pegar_emprestado(self, jogo: Jogo, data_devolucao_prevista: date):
        """
        Aluga um jogo para o cliente, registrando a data de devolução.
        """
        # C. Tratamento de Erro: Limite de empréstimos
        if len(self.jogos_alugados) >= self.LIMITE_ALUGUEIS:
            raise LimiteAlugueisException(f"Cliente {self.nome} atingiu o limite de {self.LIMITE_ALUGUEIS} aluguéis.")
        
        # C. Tratamento de Erro: Tentar emprestar jogo indisponível
        # A própria classe Jogo vai levantar a exceção se estiver indisponível
        jogo.alugar() 

        # Adiciona o aluguel à lista
        novo_aluguel = {
            "jogo": jogo,
            "data_devolucao_prevista": data_devolucao_prevista
        }
        self.jogos_alugados.append(novo_aluguel)
        print(f"SUCESSO: {self.nome} alugou o jogo '{jogo.titulo}'.")

    def devolver_jogo(self, jogo: Jogo, data_devolucao_real: date):
        """
        Devolve um jogo alugado e calcula a multa, se houver.
        """
        aluguel_encontrado = None
        for aluguel in self.jogos_alugados:
            if aluguel["jogo"] == jogo:
                aluguel_encontrado = aluguel
                break
        
        # C. Tratamento de Erro: Tentar devolver jogo não emprestado
        if aluguel_encontrado is None:
            raise JogoNaoAlugadoException(f"O cliente {self.nome} não possui um aluguel ativo para o jogo '{jogo.titulo}'.")

        # Remove o aluguel da lista e marca o jogo como disponível
        self.jogos_alugados.remove(aluguel_encontrado)
        jogo.devolver()

        # B. Dependências Externas (datetime): Cálculo da multa
        dias_atraso = (data_devolucao_real - aluguel_encontrado["data_devolucao_prevista"]).days
        
        multa = 0.0
        # Apenas calcula multa se dias_atraso for positivo
        if dias_atraso > 0:
            multa = dias_atraso * self.MULTA_POR_DIA
            print(f"DEVOLUÇÃO (COM ATRASO): Jogo '{jogo.titulo}' devolvido. Multa: R$ {multa:.2f}")
        else:
            print(f"DEVOLUÇÃO (NO PRAZO): Jogo '{jogo.titulo}' devolvido. Sem multa.")
            
        return multa