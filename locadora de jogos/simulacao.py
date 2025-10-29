from datetime import date, timedelta
from gestao_locadora import Jogo, Cliente
from gestao_locadora import JogoIndisponivelException, JogoNaoAlugadoException, LimiteAlugueisException

print("--- Iniciando Sistema da Locadora de Jogos ---")

# Criando Jogos no catálogo
jogo1 = Jogo(titulo="The Last of Us Part II", plataforma="PS4", codigo_barras="PS4-001")
jogo2 = Jogo(titulo="Cyberpunk 2077", plataforma="PS5", codigo_barras="PS5-001")
jogo3 = Jogo(titulo="Animal Crossing", plataforma="Switch", codigo_barras="SW-001")

# Criando Clientes
cliente_carlos = Cliente(nome="Carlos Pereira", id_cliente="C200")
cliente_beatriz = Cliente(nome="Beatriz Lima", id_cliente="C201")

print(jogo1)
print(jogo2)
print(cliente_carlos)
print("-" * 30)

# --- Simulação de Aluguéis ---

# Datas de referência (baseadas na data da atividade: 23/10/2025)
hoje = date(2025, 10, 23)
devolucao_padrao = hoje + timedelta(days=7) # Aluguel de 7 dias

try:
    # 1. Carlos aluga um jogo
    cliente_carlos.pegar_emprestado(jogo1, devolucao_padrao)
    print(jogo1) # Deve mostrar 'Alugado'

    # 2. Beatriz tenta alugar o mesmo jogo (deve falhar)
    print(f"\nTentativa de Beatriz alugar '{jogo1.titulo}':")
    cliente_beatriz.pegar_emprestado(jogo1, devolucao_padrao)

except JogoIndisponivelException as e:
    print(f"ERRO: {e}")
except LimiteAlugueisException as e:
    print(f"ERRO: {e}")
except Exception as e:
    print(f"ERRO INESPERADO: {e}")

print("-" * 30)

try:
    # 3. Carlos tenta devolver um jogo que não alugou (deve falhar)
    print(f"\nTentativa de Carlos devolver '{jogo2.titulo}':")
    cliente_carlos.devolver_jogo(jogo2, hoje)

except JogoNaoAlugadoException as e:
    print(f"ERRO: {e}")
except Exception as e:
    print(f"ERRO INESPERADO: {e}")

print("-" * 30)

# --- Simulação de Devolução com Multa ---

# 4. Beatriz aluga o Cyberpunk
data_aluguel_beatriz = hoje
data_prevista_beatriz = data_aluguel_beatriz + timedelta(days=3) # Aluguel curto
cliente_beatriz.pegar_emprestado(jogo2, data_prevista_beatriz)
print(jogo2) # Deve mostrar 'Alugado'

# 5. Beatriz devolve com 5 dias de atraso
data_devolucao_real_beatriz = data_prevista_beatriz + timedelta(days=5) # 8 dias depois
print(f"\nBeatriz devolvendo o '{jogo2.titulo}'...")
multa_beatriz = cliente_beatriz.devolver_jogo(jogo2, data_devolucao_real_beatriz)

print(f"Multa total de Beatriz: R$ {multa_beatriz:.2f}")
print(jogo2) # Deve mostrar 'Disponível'

print("\n--- Fim da Simulação ---")