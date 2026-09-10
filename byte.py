saldo=0.0

while True:
    print("=== ByteBank ===")
    print("[1] Consultar Saldo")
    print("[2] Depositar")
    print("[3] Sacar")
    print("[4] Sair")

    option = input("> Digite a operação desejada: ").strip()

    if option == "1":
        print(f"Seu saldo atualmente é: R$ {saldo:.2f}")

    elif option == "2":
        value_deposito = float(input("Informe o valor do depósito: R$ "))
        
        if value_deposito > 0:
            saldo += value_deposito
            print(f"Depósito de R$ {value_deposito:.2f} realizado com sucesso!")
        else:
            print("Operação negada: O valor do depósito deve ser positivo.")
    elif option == "3":
        value_saque = float(input("Informe o valor do saque: R$ "))
        
        if value_saque <= 0:
            print("Operação negada: O valor do saque deve ser positivo.")
            
        elif value_saque > saldo:
            print(f"Operação negada: Saldo insuficiente.")
            
        else:
            saldo -= value_saque
            print(f"Saque de R$ {value_saque:.2f} realizado com sucesso!")
    elif option == "4":
        print("Obrigado por utilizar o bytebank!")
        break
    else:
        print("Opção inválida. Escolha um número de 1 a 4.")