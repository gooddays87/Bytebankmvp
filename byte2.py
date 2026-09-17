
saldo_principal = 1000.0

# 1. Cofrinhos
cofrinhos = {
    "Reserva": 500.0,
    "Viagem": 200.0
}


historico_gastos = []
CATEGORIAS_DISPONIVEIS = ("Alimentação", "Transporte", "Lazer", "Contas")


limite_credito = 2000.0
saldo_fatura = 0.0
compras_credito = []

taxas_cambio = {
    "USD": 5.50,
    "EUR": 6.00,
    "BTC": 350000.0
}
saldos_moedas = {
    "USD": 0.0,
    "EUR": 0.0,
    "BTC": 0.0
}


bytepoints = 0


parcelas_emprestimo = []


def criar_cofrinho(nome):
    nome = nome.strip().capitalize()
    if not nome:
        print("Erro: O nome do cofrinho não pode ser vazio.")
        return
    if nome in cofrinhos:
        print(f"Erro: O cofrinho '{nome}' já existe.")
        return
    cofrinhos[nome] = 0.0
    print(f"Cofrinho '{nome}' criado com sucesso!")


def guardar_no_cofrinho(nome, valor):
    global saldo_principal
    nome = nome.strip().capitalize()
    if nome not in cofrinhos:
        print(f"Erro: Cofrinho '{nome}' não encontrado.")
        return
    if valor <= 0:
        print("Erro: O valor deve ser maior que zero.")
        return
    if valor > saldo_principal:
        print(f"Erro: Saldo insuficiente. Disponível: R$ {saldo_principal:.2f}")
        return
    saldo_principal -= valor
    cofrinhos[nome] += valor
    print(f"Guardado R$ {valor:.2f} no cofrinho '{nome}'.")
    print(f"Saldo na conta: R$ {saldo_principal:.2f} | Saldo no cofrinho: R$ {cofrinhos[nome]:.2f}")


def resgatar_do_cofrinho(nome, valor):
    global saldo_principal
    nome = nome.strip().capitalize()
    if nome not in cofrinhos:
        print(f"Erro: Cofrinho '{nome}' não encontrado.")
        return
    if valor <= 0:
        print("Erro: O valor a resgatar deve ser maior que zero.")
        return
    if valor > cofrinhos[nome]:
        print(f"Erro: Saldo insuficiente no cofrinho. Disponível: R$ {cofrinhos[nome]:.2f}")
        return
    cofrinhos[nome] -= valor
    saldo_principal += valor
    print(f"Resgatado R$ {valor:.2f} do cofrinho '{nome}'.")
    print(f"Saldo na conta: R$ {saldo_principal:.2f} | Saldo restante no cofrinho: R$ {cofrinhos[nome]:.2f}")


def listar_cofrinhos():
    print("\n--- Meus Cofrinhos ---")
    if not cofrinhos:
        print("Nenhum cofrinho cadastrado.")
        return
    for nome, valor in cofrinhos.items():
        print(f"- {nome}: R$ {valor:.2f}")


def simular_rendimento(taxa_mensal=0.005):
    if not cofrinhos:
        print("Nenhum cofrinho cadastrado para render.")
        return
    print(f"\n--- Rendimento de {taxa_mensal * 100:.1f}% aplicado ---")
    for nome in cofrinhos:
        rendimento = cofrinhos[nome] * taxa_mensal
        cofrinhos[nome] += rendimento
        print(f"Cofrinho '{nome}': +R$ {rendimento:.2f} (Total: R$ {cofrinhos[nome]:.2f})")


def menu_cofrinhos():
    while True:
        print("\n--- Menu Cofrinhos ---")
        print("[1] Listar cofrinhos")
        print("[2] Criar novo cofrinho")
        print("[3] Guardar dinheiro")
        print("[4] Resgatar dinheiro")
        print("[5] Simular rendimento (+0,5%)")
        print("[6] Voltar ao menu principal")
        sub_opcao = input("> Escolha uma ação: ").strip()

        if sub_opcao == "1":
            listar_cofrinhos()
        elif sub_opcao == "2":
            nome = input("Nome do novo cofrinho: ")
            criar_cofrinho(nome)
        elif sub_opcao == "3":
            nome = input("Nome do cofrinho: ")
            valor = float(input("Valor para guardar: R$ "))
            guardar_no_cofrinho(nome, valor)
        elif sub_opcao == "4":
            nome = input("Nome do cofrinho: ")
            valor = float(input("Valor para resgatar: R$ "))
            resgatar_do_cofrinho(nome, valor)
        elif sub_opcao == "5":
            simular_rendimento()
        elif sub_opcao == "6":
            break
        else:
            print("Opção inválida.")



def selecionar_categoria():
    while True:
        print("\nCategorias de despesa:")
        for idx, cat in enumerate(CATEGORIAS_DISPONIVEIS, start=1):
            print(f"[{idx}] {cat}")
        escolha = input("> Selecione a categoria da despesa: ").strip()
        if escolha.isdigit() and 1 <= int(escolha) <= len(CATEGORIAS_DISPONIVEIS):
            return CATEGORIAS_DISPONIVEIS[int(escolha) - 1]
        print("Categoria inválida. Tente novamente.")


def registrar_despesa(categoria, valor):
    historico_gastos.append({"categoria": categoria, "valor": valor})


def relatorio_categoria():
    print("\n=== Relatório de Gastos por Categoria ===")
    if not historico_gastos:
        print("Nenhuma transação registrada no histórico.")
        return

    total_geral = sum(item["valor"] for item in historico_gastos)
    agrupado = {}
    for item in historico_gastos:
        cat = item["categoria"]
        val = item["valor"]
        agrupado[cat] = agrupado.get(cat, 0.0) + val

    for cat, total_cat in agrupado.items():
        percentual = (total_cat / total_geral) * 100
        print(f"- {cat}: R$ {total_cat:.2f} ({percentual:.1f}%)")
    print(f"Total gasto: R$ {total_geral:.2f}")



def comprar_no_credito(valor, estabelecimento):
    global saldo_fatura
    if valor <= 0:
        print("Erro: O valor da compra deve ser positivo.")
        return
    limite_disponivel = limite_credito - saldo_fatura
    if valor > limite_disponivel:
        print(f"Erro: Limite insuficiente. Disponível: R$ {limite_disponivel:.2f}")
        return

    saldo_fatura += valor
    compras_credito.append({"estabelecimento": estabelecimento, "valor": valor})
    print(f"Compra de R$ {valor:.2f} em '{estabelecimento}' aprovada!")
    print(f"Fatura atual: R$ {saldo_fatura:.2f} | Limite disponível: R$ {(limite_credito - saldo_fatura):.2f}")


def pagar_fatura():
    global saldo_principal, saldo_fatura
    if saldo_fatura == 0:
        print("Fatura zerada. Nenhum pagamento necessário.")
        return

    print(f"Valor atual da fatura: R$ {saldo_fatura:.2f}")
    valor = float(input("Quanto deseja pagar da fatura? R$ "))

    if valor <= 0:
        print("Erro: O valor do pagamento deve ser positivo.")
        return
    if valor > saldo_principal:
        print(f"Erro: Saldo em conta insuficiente. Saldo atual: R$ {saldo_principal:.2f}")
        return
    if valor > saldo_fatura:
        print("Erro: O valor de pagamento excede o saldo da fatura.")
        return

    saldo_principal -= valor
    saldo_fatura -= valor
    print(f"Pagamento de R$ {valor:.2f} realizado!")
    print(f"Fatura restante: R$ {saldo_fatura:.2f} | Saldo em conta: R$ {saldo_principal:.2f}")


def menu_cartao():
    while True:
        limite_disp = limite_credito - saldo_fatura
        print("\n--- Menu Cartão de Crédito ---")
        print(f"Limite Total: R$ {limite_credito:.2f} | Disponível: R$ {limite_disp:.2f} | Fatura: R$ {saldo_fatura:.2f}")
        print("[1] Comprar no Crédito")
        print("[2] Pagar Fatura")
        print("[3] Voltar")
        sub_opcao = input("> Escolha uma ação: ").strip()

        if sub_opcao == "1":
            estab = input("Estabelecimento: ").strip()
            val = float(input("Valor da compra: R$ "))
            comprar_no_credito(val, estab)
        elif sub_opcao == "2":
            pagar_fatura()
        elif sub_opcao == "3":
            break
        else:
            print("Opção inválida.")


def comprar_moeda_estrangeira(moeda, valor_brl):
    global saldo_principal
    moeda = moeda.strip().upper()
    if moeda not in taxas_cambio:
        print("Erro: Moeda não suportada.")
        return
    if valor_brl <= 0:
        print("Erro: Valor deve ser positivo.")
        return
    if valor_brl > saldo_principal:
        print(f"Erro: Saldo em conta insuficiente. Disponível: R$ {saldo_principal:.2f}")
        return

    taxa = taxas_cambio[moeda]
    qtd_comprada = valor_brl / taxa
    saldo_principal -= valor_brl
    saldos_moedas[moeda] += qtd_comprada

    print(f"Compra realizada: {qtd_comprada:.4f} {moeda} adicionados à carteira.")
    print(f"Saldo restante em BRL: R$ {saldo_principal:.2f}")


def vender_moeda_estrangeira(moeda, quantidade):
    global saldo_principal
    moeda = moeda.strip().upper()
    if moeda not in taxas_cambio:
        print("Erro: Moeda não suportada.")
        return
    if quantidade <= 0:
        print("Erro: A quantidade deve ser positiva.")
        return
    if quantidade > saldos_moedas[moeda]:
        print(f"Erro: Saldo insuficiente de {moeda}. Você tem: {saldos_moedas[moeda]:.4f}")
        return

    taxa = taxas_cambio[moeda]
    valor_brl = quantidade * taxa
    saldos_moedas[moeda] -= quantidade
    saldo_principal += valor_brl

    print(f"Venda efetuada: creditado R$ {valor_brl:.2f} na conta corrente.")
    print(f"Saldo restante em {moeda}: {saldos_moedas[moeda]:.4f}")


def menu_cambio():
    while True:
        print("\n--- Carteira Multimoedas ---")
        for m, taxa in taxas_cambio.items():
            print(f"- {m}: Cotação R$ {taxa:.2f} | Saldo: {saldos_moedas[m]:.4f}")
        print("[1] Comprar Moeda")
        print("[2] Vender Moeda")
        print("[3] Voltar")
        sub_opcao = input("> Escolha uma ação: ").strip()

        if sub_opcao == "1":
            m = input("Moeda desejada (USD/EUR/BTC): ")
            v = float(input("Quanto deseja gastar em BRL? R$ "))
            comprar_moeda_estrangeira(m, v)
        elif sub_opcao == "2":
            m = input("Moeda para venda (USD/EUR/BTC): ")
            q = float(input(f"Quantidade de {m} a vender: "))
            vender_moeda_estrangeira(m, q)
        elif sub_opcao == "3":
            break
        else:
            print("Opção inválida.")


def acumular_pontos(valor_transacao):
    global bytepoints
    pontos_ganhos = int(valor_transacao // 10)
    if pontos_ganhos > 0:
        bytepoints += pontos_ganhos
        print(f"+{pontos_ganhos} BytePoints acumulados! (Total: {bytepoints})")


def consultar_pontos():
    cashback_equivalente = (bytepoints / 100) * 5.0
    print(f"\nSaldo de BytePoints: {bytepoints} pts")
    print(f"Equivalente em Cashback: R$ {cashback_equivalente:.2f}")


def resgatar_cashback(pontos_a_resgatar):
    global bytepoints, saldo_principal
    if pontos_a_resgatar <= 0:
        print("Erro: Quantidade de pontos deve ser positiva.")
        return
    if pontos_a_resgatar > bytepoints:
        print(f"Erro: Pontos insuficientes. Você tem {bytepoints} pontos.")
        return
    if pontos_a_resgatar % 100 != 0:
        print("Erro: Os pontos devem ser resgatados em blocos de 100.")
        return

    blocos = pontos_a_resgatar // 100
    valor_resgatado = blocos * 5.0
    bytepoints -= pontos_a_resgatar
    saldo_principal += valor_resgatado

    print(f"Resgate efetuado: R$ {valor_resgatado:.2f} creditados na conta.")
    print(f"Pontos restantes: {bytepoints} | Novo saldo: R$ {saldo_principal:.2f}")


def menu_fidelidade():
    while True:
        print("\n--- Programa BytePoints ---")
        print("[1] Consultar Pontos e Cashback")
        print("[2] Resgatar Cashback (100 pts = R$ 5,00)")
        print("[3] Voltar")
        sub_opcao = input("> Escolha uma ação: ").strip()

        if sub_opcao == "1":
            consultar_pontos()
        elif sub_opcao == "2":
            pts = int(input("Quantidade de pontos para resgate: "))
            resgatar_cashback(pts)
        elif sub_opcao == "3":
            break
        else:
            print("Opção inválida.")


def simular_emprestimo(valor, parcelas):
    limite = saldo_principal * 3
    if valor <= 0 or parcelas <= 0:
        print("Erro: Valores e parcelas devem ser maiores que zero.")
        return None
    if valor > limite:
        print(f"Erro: Valor excede o limite pré-aprovado de R$ {limite:.2f} (3x o saldo).")
        return None

    montante = valor * 1.10  # 10% de juros
    valor_parcela = montante / parcelas
    print(f"\n--- Simulação de Empréstimo ---")
    print(f"Valor solicitado: R$ {valor:.2f}")
    print(f"Montante com juros (10%): R$ {montante:.2f}")
    print(f"Plano: {parcelas}x de R$ {valor_parcela:.2f}")
    return valor_parcela


def contratar_emprestimo(valor, parcelas):
    global saldo_principal
    valor_parcela = simular_emprestimo(valor, parcelas)
    if valor_parcela is None:
        return

    confirmar = input("Confirma contratação? (s/n): ").strip().lower()
    if confirmar == 's':
        saldo_principal += valor
        parcelas_emprestimo.extend([valor_parcela] * parcelas)
        print(f"Empréstimo contratado! R$ {valor:.2f} creditados na sua conta.")
    else:
        print("Contratação cancelada.")


def pagar_parcela_emprestimo():
    global saldo_principal
    if not parcelas_emprestimo:
        print("Nenhuma parcela pendente de pagamento.")
        return

    proxima_parcela = parcelas_emprestimo[0]
    print(f"Valor da próxima parcela: R$ {proxima_parcela:.2f}")
    if saldo_principal < proxima_parcela:
        print(f"Erro: Saldo insuficiente. Você tem R$ {saldo_principal:.2f}")
        return

    saldo_principal -= proxima_parcela
    parcelas_emprestimo.pop(0)
    print(f"Parcela quitada com sucesso! Restam {len(parcelas_emprestimo)} parcelas.")


def menu_emprestimos():
    while True:
        limite = saldo_principal * 3
        print(f"\n--- Empréstimos Pré-Aprovados (Limite disponível: R$ {limite:.2f}) ---")
        print(f"Parcelas ativas: {len(parcelas_emprestimo)}")
        print("[1] Simular Empréstimo")
        print("[2] Contratar Empréstimo")
        print("[3] Pagar Parcela")
        print("[4] Voltar")
        sub_opcao = input("> Escolha uma ação: ").strip()

        if sub_opcao == "1":
            v = float(input("Valor do empréstimo: R$ "))
            p = int(input("Número de parcelas: "))
            simular_emprestimo(v, p)
        elif sub_opcao == "2":
            v = float(input("Valor do empréstimo: R$ "))
            p = int(input("Número de parcelas: "))
            contratar_emprestimo(v, p)
        elif sub_opcao == "3":
            pagar_parcela_emprestimo()
        elif sub_opcao == "4":
            break
        else:
            print("Opção inválida.")


while True:
    print("\n=== ByteBank MVP ===")
    print("[1] Consultar Saldo")
    print("[2] Depositar")
    print("[3] Sacar (com Categoria & BytePoints)")
    print("[4] Cofrinhos")
    print("[5] Relatório Analytics (Gastos)")
    print("[6] Cartão de Crédito")
    print("[7] Câmbio Multimoedas")
    print("[8] BytePoints / Fidelidade")
    print("[9] Empréstimos")
    print("[0] Sair")

    option = input("> Digite a operação desejada: ").strip()

    if option == "1":
        print(f"Seu saldo atualmente é: R$ {saldo_principal:.2f}")

    elif option == "2":
        value_deposito = float(input("Informe o valor do depósito: R$ "))
        if value_deposito > 0:
            saldo_principal += value_deposito
            print(f"Depósito de R$ {value_deposito:.2f} realizado com sucesso!")
        else:
            print("Operação negada: O valor do depósito deve ser positivo.")

    elif option == "3":
        value_saque = float(input("Informe o valor do saque: R$ "))
        if value_saque <= 0:
            print("Operação negada: O valor do saque deve ser positivo.")
        elif value_saque > saldo_principal:
            print("Operação negada: Saldo insuficiente.")
        else:
            cat = selecionar_categoria()
            saldo_principal -= value_saque
            registrar_despesa(cat, value_saque)
            acumular_pontos(value_saque)
            print(f"Saque de R$ {value_saque:.2f} na categoria '{cat}' realizado!")

    elif option == "4":
        menu_cofrinhos()

    elif option == "5":
        relatorio_categoria()

    elif option == "6":
        menu_cartao()

    elif option == "7":
        menu_cambio()

    elif option == "8":
        menu_fidelidade()

    elif option == "9":
        menu_emprestimos()

    elif option == "0":
        print("Obrigado por utilizar o ByteBank!")
        break

    else:
        print("Opção inválida. Escolha uma das opções listadas.")