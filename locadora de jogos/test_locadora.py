import pytest
from datetime import date, timedelta
from gestao_locadora import Jogo, Cliente, JogoIndisponivelException, JogoNaoAlugadoException, LimiteAlugueisException

# --- Fixtures (preparações para os testes) ---

@pytest.fixture
def cliente_maria():
    """Cria um cliente padrão para os testes."""
    return Cliente(nome="Maria Oliveira", id_cliente="C101")

@pytest.fixture
def jogo_zelda():
    """Cria um jogo padrão para os testes."""
    return Jogo(titulo="Zelda: Breath of the Wild", plataforma="Switch", codigo_barras="123456")

@pytest.fixture
def tres_jogos():
    """Cria uma lista de 3 jogos para teste de limite."""
    return [
        Jogo(titulo="FIFA 25", plataforma="PS5", codigo_barras="A001"),
        Jogo(titulo="Elden Ring", plataforma="PS5", codigo_barras="A002"),
        Jogo(titulo="Mario Kart 8", plataforma="Switch", codigo_barras="B001")
    ]

# --- Testes ---

def test_alugar_jogo_sucesso(cliente_maria, jogo_zelda):
    """Testa um aluguel bem-sucedido."""
    data_devolucao = date.today() + timedelta(days=7)
    cliente_maria.pegar_emprestado(jogo_zelda, data_devolucao)
    
    assert len(cliente_maria.jogos_alugados) == 1
    assert cliente_maria.jogos_alugados[0]["jogo"] == jogo_zelda
    assert not jogo_zelda.disponivel

def test_erro_alugar_jogo_indisponivel(cliente_maria, jogo_zelda):
    """Testa a exceção ao tentar alugar um jogo já alugado."""
    data_devolucao = date.today() + timedelta(days=7)
    cliente_maria.pegar_emprestado(jogo_zelda, data_devolucao) # Aluga 1a vez
    
    # Cria outro cliente para tentar alugar o mesmo jogo
    cliente_joao = Cliente("Joao", "C102")
    with pytest.raises(JogoIndisponivelException):
        cliente_joao.pegar_emprestado(jogo_zelda, data_devolucao)

def test_erro_limite_alugueis(cliente_maria, tres_jogos):
    """Testa a exceção ao tentar alugar mais que o limite de 3 jogos."""
    data_devolucao = date.today() + timedelta(days=7)
    
    # Aluga os 3 jogos
    cliente_maria.pegar_emprestado(tres_jogos[0], data_devolucao)
    cliente_maria.pegar_emprestado(tres_jogos[1], data_devolucao)
    cliente_maria.pegar_emprestado(tres_jogos[2], data_devolucao)
    
    assert len(cliente_maria.jogos_alugados) == 3
    
    # Tenta alugar o quarto jogo
    jogo_extra = Jogo(titulo="Hogwarts Legacy", plataforma="PC", codigo_barras="D001")
    with pytest.raises(LimiteAlugueisException):
        cliente_maria.pegar_emprestado(jogo_extra, data_devolucao)

def test_devolver_jogo_sem_multa(cliente_maria, jogo_zelda):
    """Testa a devolução de um jogo no prazo."""
    data_hoje = date.today()
    data_devolucao_prevista = data_hoje + timedelta(days=7)
    
    cliente_maria.pegar_emprestado(jogo_zelda, data_devolucao_prevista)
    
    # Devolve no prazo (no último dia)
    multa = cliente_maria.devolver_jogo(jogo_zelda, data_devolucao_prevista)
    
    assert multa == 0.0
    assert len(cliente_maria.jogos_alugados) == 0
    assert jogo_zelda.disponivel

def test_devolver_jogo_com_multa(cliente_maria, jogo_zelda):
    """Testa a devolução com atraso e cálculo da multa."""
    data_hoje = date.today()
    data_devolucao_prevista = data_hoje + timedelta(days=7)
    
    cliente_maria.pegar_emprestado(jogo_zelda, data_devolucao_prevista)
    
    # Devolve 2 dias atrasado
    data_devolucao_real = data_devolucao_prevista + timedelta(days=2)
    multa = cliente_maria.devolver_jogo(jogo_zelda, data_devolucao_real)
    
    # Multa esperada: 2 dias * R$ 1.00/dia = R$ 2.00
    assert multa == 2.00
    assert len(cliente_maria.jogos_alugados) == 0

def test_erro_devolver_jogo_nao_alugado(cliente_maria, jogo_zelda):
    """Testa a exceção ao tentar devolver um jogo que o cliente não alugou."""
    data_hoje = date.today()
    
    # Garante que o jogo não está alugado pela Maria
    assert len(cliente_maria.jogos_alugados) == 0
    
    with pytest.raises(JogoNaoAlugadoException):
        cliente_maria.devolver_jogo(jogo_zelda, data_hoje)