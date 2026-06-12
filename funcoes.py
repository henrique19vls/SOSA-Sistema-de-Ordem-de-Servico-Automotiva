from database import *


# cadastra novos clientes no sistema
def cadastrar_cliente():

    print("\n=== CADASTRAR CLIENTE ===")

    # continua perguntando até receber um nome válido
    while True:
        nome = input("\nNome do cliente: ").strip()
        if nome and all(letra.isalpha() or letra.isspace() for letra in nome):
            break
        print("Nome inválido! Use apenas letras.")

    # continua perguntando até receber um telefone válido
    while True:
        telefone = input("Telefone (apenas números): ").strip()
        if telefone.isdigit() and len(telefone) >= 8:
            break
        print("Telefone inválido! Digite apenas números (mínimo 8 dígitos).")

    # abre conexão com o banco
    conn = conectar()
    cursor = conn.cursor()

    # verifica se já existe cliente com o mesmo nome e telefone
    cursor.execute("""
        SELECT id FROM clientes
        WHERE nome = %s AND telefone = %s
    """, (nome, telefone))

    if cursor.fetchone():
        print("\nCliente já cadastrado com esse nome e telefone!")
        cursor.close()
        conn.close()
        return

    # insere o cliente no banco
    cursor.execute("""
        INSERT INTO clientes (nome, telefone)
        VALUES (%s, %s)
    """, (nome, telefone))

    conn.commit()
    print("\nCliente cadastrado com sucesso!")

    cursor.close()
    conn.close()


# registra nova ordem de serviço
def registrar_ordem():

    print("\n=== ABRIR ORDEM DE SERVIÇO ===")

    conn = conectar()
    cursor = conn.cursor()

    # busca clientes cadastrados
    cursor.execute("SELECT id, nome, telefone FROM clientes ORDER BY nome")
    clientes = cursor.fetchall()

    # verifica se há clientes cadastrados
    if not clientes:
        print("\nNenhum cliente cadastrado. Cadastre um cliente primeiro.")
        cursor.close()
        conn.close()
        return

    print("\n=== CLIENTES CADASTRADOS ===")
    for c in clientes:
        print(f"ID: {c[0]} - {c[1]} | Tel: {c[2]}")

    ids_validos_clientes = [c[0] for c in clientes]

    # continua perguntando até receber ID válido
    while True:
        try:
            id_cliente = int(input("\nID do cliente: "))
            if id_cliente in ids_validos_clientes:
                break
            print("ID inválido! Escolha um ID da lista.")
        except ValueError:
            print("Digite apenas números válidos!")

    # busca tipos de serviço disponíveis
    cursor.execute("SELECT id, descricao FROM tipos_servico ORDER BY id")
    tipos = cursor.fetchall()

    print("\n=== TIPO DE SERVIÇO ===")
    for t in tipos:
        print(f"ID: {t[0]} - {t[1]}")

    ids_validos_tipos = [t[0] for t in tipos]

    # continua perguntando até receber ID válido
    while True:
        try:
            id_tipo = int(input("\nID do tipo de serviço: "))
            if id_tipo in ids_validos_tipos:
                break
            print("ID inválido! Escolha um ID da lista.")
        except ValueError:
            print("Digite apenas números válidos!")

    # continua perguntando até receber uma descrição válida
    while True:
        descricao = input("\nDescreva o problema do veículo: ").strip()
        if descricao:
            break
        print("A descrição não pode ficar vazia!")

    # continua perguntando até receber modelo válido
    while True:
        modelo_veiculo = input("Modelo do veículo (ex: Gol 2015): ").strip()
        if modelo_veiculo:
            break
        print("O modelo do veículo não pode ficar vazio!")

    # insere a ordem de serviço no banco
    cursor.execute("""
        INSERT INTO ordens_servico
        (cliente_id, tipo_servico_id, descricao, modelo_veiculo, status)
        VALUES (%s, %s, %s, %s, 'aberta')
    """, (id_cliente, id_tipo, descricao, modelo_veiculo))

    conn.commit()
    print("\nOrdem de serviço registrada com sucesso!")

    cursor.close()
    conn.close()


# encaminha ordem de serviço para mecânico
def encaminhar_ordem():

    conn = conectar()
    cursor = conn.cursor()

    print("\n=== ORDENS DE SERVIÇO ABERTAS ===")

    # busca ordens abertas com nome do cliente e tipo de serviço
    cursor.execute("""
        SELECT o.id, c.nome, ts.descricao, o.modelo_veiculo, o.descricao
        FROM ordens_servico o
        JOIN clientes c ON o.cliente_id = c.id
        JOIN tipos_servico ts ON o.tipo_servico_id = ts.id
        WHERE o.status = 'aberta'
    """)

    ordens = cursor.fetchall()

    # verifica se existem ordens abertas
    if not ordens:
        print("\nNenhuma ordem de serviço aberta.")
        cursor.close()
        conn.close()
        return

    for o in ordens:
        print(f"\nID: {o[0]}")
        print(f"Cliente: {o[1]}")
        print(f"Serviço: {o[2]}")
        print(f"Veículo: {o[3]}")
        print(f"Problema: {o[4]}")

    ids_validos_ordens = [o[0] for o in ordens]

    # continua perguntando até receber ID válido
    while True:
        try:
            id_ordem = int(input("\nID da ordem de serviço: "))
            if id_ordem in ids_validos_ordens:
                break
            print("ID inválido! Escolha um ID da lista.")
        except ValueError:
            print("Digite apenas números válidos!")

    print("\n=== URGÊNCIA E GRAVIDADE ===")

    # continua perguntando até receber valor válido
    while True:
        try:
            urgencia = int(input("Urgência: (1) Baixa  (2) Média  (3) Alta: \n"))
            if urgencia in [1, 2, 3]:
                break
            print("Valor inválido! Digite 1, 2 ou 3.")
        except ValueError:
            print("Valor inválido! Digite apenas 1, 2 ou 3.")

    # continua perguntando até receber valor válido
    while True:
        try:
            gravidade = int(input("Gravidade do problema: (1) Leve  (2) Moderada  (3) Grave: \n"))
            if gravidade in [1, 2, 3]:
                break
            print("Valor inválido! Digite 1, 2 ou 3.")
        except ValueError:
            print("Valor inválido! Digite apenas 1, 2 ou 3.")

    # define prioridade com base na matriz urgência × gravidade
    # urgência tem peso maior que gravidade
    matriz = {
        (1, 1): "Baixa",
        (1, 2): "Baixa",
        (1, 3): "Média",
        (2, 1): "Média",
        (2, 2): "Média",
        (2, 3): "Alta",
        (3, 1): "Alta",
        (3, 2): "Alta",
        (3, 3): "Alta",
    }

    prioridade = matriz[(urgencia, gravidade)]
    print(f"\nPrioridade definida: {prioridade}")

    print("\n=== MECÂNICOS DISPONÍVEIS ===")

    # busca mecânicos compatíveis com a prioridade
    if prioridade == "Baixa":
        cursor.execute("""
            SELECT id, nome, nivel FROM mecanicos
            WHERE nivel = 'auxiliar de mecanico' OR nivel = 'estagiario'
        """)
    elif prioridade == "Média":
        cursor.execute("""
            SELECT id, nome, nivel FROM mecanicos
            WHERE nivel = 'mecanico' OR nivel = 'auxiliar de mecanico'
        """)
    else:
        cursor.execute("""
            SELECT id, nome, nivel FROM mecanicos
            WHERE nivel = 'mecanico chefe' OR nivel = 'mecanico'
        """)

    mecanicos = cursor.fetchall()

    # verifica se existem mecânicos
    if not mecanicos:
        print("\nNenhum mecânico disponível para essa prioridade.")
        cursor.close()
        conn.close()
        return

    for m in mecanicos:
        print(f"\nID: {m[0]}")
        print(f"Mecânico: {m[1]}")
        print(f"Nível: {m[2]}")

    ids_validos_mecanicos = [m[0] for m in mecanicos]

    # continua perguntando até receber ID válido
    while True:
        try:
            id_mec = int(input("\nID do mecânico responsável: "))
            if id_mec in ids_validos_mecanicos:
                break
            print("ID inválido! Escolha um mecânico da lista.")
        except ValueError:
            print("Digite apenas números válidos!")

    # busca o próximo número de ordem
    cursor.execute("SELECT COALESCE(MAX(num_ordem), 0) + 1 FROM ordens_servico")
    num_ordem = cursor.fetchone()[0]

    # atualiza a ordem com mecânico, prioridade e número de ordem
    cursor.execute("""
        UPDATE ordens_servico
        SET mecanico_id = %s, prioridade = %s, status = 'em manutencao', num_ordem = %s
        WHERE id = %s
    """, (id_mec, prioridade, num_ordem, id_ordem))

    conn.commit()
    print("\nOrdem de serviço encaminhada com sucesso!")

    cursor.close()
    conn.close()


# finaliza ordem de serviço em manutenção
def concluir_ordem():

    conn = conectar()
    cursor = conn.cursor()

    print("\n=== ORDENS EM MANUTENÇÃO ===")

    # busca ordens em manutenção com nome do mecânico e do cliente
    cursor.execute("""
        SELECT o.id, o.num_ordem, m.nome, c.nome, ts.descricao,
               o.modelo_veiculo, o.descricao, o.status, o.mecanico_id
        FROM ordens_servico o
        JOIN mecanicos m ON o.mecanico_id = m.id
        JOIN clientes c ON o.cliente_id = c.id
        JOIN tipos_servico ts ON o.tipo_servico_id = ts.id
        WHERE o.status = 'em manutencao'
    """)

    ordens = cursor.fetchall()

    # verifica se existem ordens em manutenção
    if not ordens:
        print("\nNenhuma ordem em manutenção.")
        cursor.close()
        conn.close()
        return

    for o in ordens:
        print(f"\nNº Ordem: {o[1]}")
        print(f"OS ID: {o[0]}")
        print(f"Mecânico: {o[2]}")
        print(f"Cliente: {o[3]}")
        print(f"Serviço: {o[4]}")
        print(f"Veículo: {o[5]}")
        print(f"Problema: {o[6]}")
        print(f"Status: {o[7]}")

    ids_validos = [o[0] for o in ordens]

    # continua perguntando até receber ID válido
    while True:
        try:
            id_ordem = int(input("\nID da ordem de serviço: "))
            if id_ordem in ids_validos:
                break
            print("ID inválido!")
        except ValueError:
            print("Digite apenas números válidos!")

    # continua perguntando até receber descrição válida
    while True:
        solucao_aplicada = input("\nDescreva a solução aplicada: ").strip()
        if solucao_aplicada:
            break
        print("A descrição da solução não pode ficar vazia!")

    # busca o mecanico_id da ordem selecionada
    ordem = next(o for o in ordens if o[0] == id_ordem)
    id_mecanico = ordem[8]

    # insere no histórico
    cursor.execute("""
        INSERT INTO historico (ordem_id, mecanico_id, solucao_aplicada)
        VALUES (%s, %s, %s)
    """, (id_ordem, id_mecanico, solucao_aplicada))

    # atualiza status para finalizada
    cursor.execute("""
        UPDATE ordens_servico
        SET status = 'finalizada'
        WHERE id = %s
    """, (id_ordem,))

    conn.commit()
    print("\nOrdem de serviço finalizada com sucesso!")

    cursor.close()
    conn.close()


# exibe histórico das ordens finalizadas
def historico_ordens():

    conn = conectar()
    cursor = conn.cursor()

    print("\n=== HISTÓRICO DE ORDENS DE SERVIÇO ===")

    cursor.execute("""
        SELECT
            h.id,
            o.id,
            o.num_ordem,
            c.nome,
            c.telefone,
            m.nome,
            ts.descricao,
            o.modelo_veiculo,
            o.descricao,
            h.solucao_aplicada,
            h.data_finalizacao
        FROM historico h
        JOIN ordens_servico o ON h.ordem_id = o.id
        JOIN mecanicos m ON h.mecanico_id = m.id
        JOIN clientes c ON o.cliente_id = c.id
        JOIN tipos_servico ts ON o.tipo_servico_id = ts.id
        ORDER BY h.data_finalizacao DESC
    """)

    historico = cursor.fetchall()

    # verifica se existem registros
    if not historico:
        print("\nNenhuma ordem finalizada ainda.")
        cursor.close()
        conn.close()
        return

    for h in historico:
        print(f"\nHistórico ID: {h[0]}")
        print(f"OS ID: {h[1]}")
        print(f"Nº Ordem: {h[2]}")
        print(f"Cliente: {h[3]} | Tel: {h[4]}")
        print(f"Mecânico responsável: {h[5]}")
        print(f"Tipo de serviço: {h[6]}")
        print(f"Veículo: {h[7]}")
        print(f"Problema relatado: {h[8]}")
        print(f"Solução aplicada: {h[9]}")
        print(f"Finalizado em: {h[10]}")

    cursor.close()
    conn.close()


# função auxiliar: exibe ordens filtradas por status
def exibir_por_status(cursor, status, titulo):

    cursor.execute("""
        SELECT o.id, o.num_ordem, c.nome, ts.descricao,
               o.modelo_veiculo, o.descricao, o.status, o.prioridade
        FROM ordens_servico o
        JOIN clientes c ON o.cliente_id = c.id
        JOIN tipos_servico ts ON o.tipo_servico_id = ts.id
        LEFT JOIN mecanicos m ON o.mecanico_id = m.id
        WHERE o.status = %s
    """, (status,))

    registros = cursor.fetchall()

    print(f"\n=== {titulo} ===")

    if not registros:
        print("Nenhuma ordem encontrada.")
        return

    for o in registros:
        print(f"\nID: {o[0]}")
        if o[1]:
            print(f"Nº Ordem: {o[1]}")
        print(f"Cliente: {o[2]}")
        print(f"Serviço: {o[3]}")
        print(f"Veículo: {o[4]}")
        print(f"Problema: {o[5]}")
        print(f"Status: {o[6]}")
        if o[7]:
            print(f"Prioridade: {o[7]}")


# exibe estatísticas por status, prioridade e filtros
def relatorio():

    print("\n=== ESTATÍSTICAS ===")
    print("1 - Resumo geral (totais por status e prioridade)")
    print("2 - Ordens em aberto")
    print("3 - Ordens em manutenção")
    print("4 - Ordens finalizadas")
    print("5 - Consultar por prioridade")
    print("6 - Consultar por cliente")
    print("7 - Voltar ao menu principal")

    conn = conectar()
    cursor = conn.cursor()

    # impede erro ao digitar letra no input
    try:
        escolha = int(input("\nDigite o número da opção desejada: "))
    except ValueError:
        print("Opção inválida!")
        cursor.close()
        conn.close()
        return

    # totais por status e por prioridade via COUNT + GROUP BY
    if escolha == 1:

        print("\n--- Totais por status ---")
        cursor.execute("""
            SELECT status, COUNT(*) AS total
            FROM ordens_servico
            GROUP BY status
        """)
        for row in cursor.fetchall():
            print(f"  {row[0].capitalize()}: {row[1]}")

        print("\n--- Totais por prioridade ---")
        cursor.execute("""
            SELECT prioridade, COUNT(*) AS total
            FROM ordens_servico
            WHERE prioridade IS NOT NULL
            GROUP BY prioridade
        """)
        resultado = cursor.fetchall()
        if resultado:
            for row in resultado:
                print(f"  Prioridade {row[0]}: {row[1]}")
        else:
            print("  Nenhuma ordem com prioridade definida ainda.")

    elif escolha == 2:
        exibir_por_status(cursor, 'aberta', 'ORDENS EM ABERTO')

    elif escolha == 3:
        exibir_por_status(cursor, 'em manutencao', 'ORDENS EM MANUTENÇÃO')

    elif escolha == 4:
        exibir_por_status(cursor, 'finalizada', 'ORDENS FINALIZADAS')

    # consulta por prioridade
    elif escolha == 5:

        print("\nPrioridade: (1) Baixa  (2) Média  (3) Alta")
        opcoes = {"1": "Baixa", "2": "Média", "3": "Alta"}
        op = input("Escolha: ").strip()

        if op not in opcoes:
            print("Opção inválida!")
            cursor.close()
            conn.close()
            return

        cursor.execute("""
            SELECT o.id, c.nome, ts.descricao, o.modelo_veiculo, o.status, o.prioridade
            FROM ordens_servico o
            JOIN clientes c ON o.cliente_id = c.id
            JOIN tipos_servico ts ON o.tipo_servico_id = ts.id
            WHERE o.prioridade = %s
            ORDER BY o.data_criacao DESC
        """, (opcoes[op],))

        ordens = cursor.fetchall()
        print(f"\n=== ORDENS COM PRIORIDADE {opcoes[op].upper()} ===")

        if not ordens:
            print("Nenhuma ordem encontrada.")
        else:
            for o in ordens:
                print(f"\nID: {o[0]} | Cliente: {o[1]} | Serviço: {o[2]}")
                print(f"Veículo: {o[3]} | Status: {o[4]} | Prioridade: {o[5]}")

    # consulta por cliente
    elif escolha == 6:

        nome_busca = input("\nDigite o nome do cliente: ").strip()

        if not nome_busca:
            print("Nome não pode ficar vazio!")
            cursor.close()
            conn.close()
            return

        cursor.execute("""
            SELECT o.id, c.nome, ts.descricao, o.modelo_veiculo,
                   o.status, o.prioridade, o.data_criacao
            FROM ordens_servico o
            JOIN clientes c ON o.cliente_id = c.id
            JOIN tipos_servico ts ON o.tipo_servico_id = ts.id
            WHERE c.nome LIKE %s
            ORDER BY o.data_criacao DESC
        """, (f"%{nome_busca}%",))

        ordens = cursor.fetchall()
        print(f"\n=== ORDENS DO CLIENTE: {nome_busca.upper()} ===")

        if not ordens:
            print("Nenhuma ordem encontrada para esse cliente.")
        else:
            for o in ordens:
                print(f"\nID: {o[0]} | Serviço: {o[2]} | Veículo: {o[3]}")
                print(f"Status: {o[4]} | Prioridade: {o[5] if o[5] else 'Não definida'} | Aberto em: {o[6]}")

    elif escolha == 7:
        print("Voltando ao menu principal...\n")

    else:
        print("Opção inválida!")

    cursor.close()
    conn.close()
