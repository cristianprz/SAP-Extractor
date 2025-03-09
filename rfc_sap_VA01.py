import os
import sys
import time

import csv

# Verificar se a variável de ambiente SAPNWRFC_HOME está definida
if "SAPNWRFC_HOME" not in os.environ:
    raise EnvironmentError("A variável de ambiente SAPNWRFC_HOME não está definida.")

# Verificar se o diretório especificado pela variável de ambiente existe
sapnwrfc_home = os.environ["SAPNWRFC_HOME"]
if not os.path.isdir(sapnwrfc_home):
    raise EnvironmentError(f"O diretório especificado pela variável de ambiente SAPNWRFC_HOME não existe: {sapnwrfc_home}")

# Verificar se o diretório lib dentro de SAPNWRFC_HOME existe
lib_dir = os.path.join(sapnwrfc_home, "lib")
if not os.path.isdir(lib_dir):
    raise EnvironmentError(f"O diretório lib dentro de SAPNWRFC_HOME não existe: {lib_dir}")

# Verificar se as DLLs ICU estão presentes no diretório lib
required_dlls = ["icuuc57.dll", "icudt57.dll", "icuin57.dll"]
for dll in required_dlls:
    if not os.path.isfile(os.path.join(lib_dir, dll)):
        raise EnvironmentError(f"A DLL {dll} não foi encontrada no diretório lib: {lib_dir}")

print("A variável de ambiente SAPNWRFC_HOME está definida corretamente e todas as DLLs necessárias estão presentes.")

from pyrfc import Connection

# Configuração da conexão com o SAP
conn_params = {
    'ashost': '*********',  # Endereço do servidor SAP
    'sysnr': '********',              # Número do sistema
    'client': '********',            # Mandante
    'user': '********',            # Usuário SAP
    'passwd': '****************'   # Senha
}

try:
    conn = Connection(**conn_params)
    print("Conexão com o SAP estabelecida com sucesso.")
except Exception as e:
    print(f"Erro ao conectar ao SAP: {e}")
    sys.exit(1)

# Função para chamar a função CSAP_MAT_BOM_READ
def call_csap_mat_bom_read():
       # Dados do cabeçalho do pedido
    order_header = {
        "DOC_TYPE": "YBOR",          # Tipo de documento de venda
        "SALES_ORG": "0050",       # Organização de vendas
        "DISTR_CHAN": "14",        # Canal de distribuição
        "DIVISION": "02",          # Divisão
        "REQ_DATE_H": "20250228",   # Data de entrega solicitada
        "PMNTTRMS": "S252",         # Condição de pagamento
        "DLV_BLOCK": "Z2"           # Bloqueio de entrega

    }

    order_headerx = {
        "DOC_TYPE": "X",          # Tipo de documento de venda
        "SALES_ORG": "X",       # Organização de vendas
        "DISTR_CHAN": "X",        # Canal de distribuição
        "DIVISION": "X",          # Divisão
        "REQ_DATE_H": "X",   # Data de entrega solicitada
        "PMNTTRMS": "X",         # Condição de pagamento
        "DLV_BLOCK": "X"           # Bloqueio de entrega

    }

    # Lista de itens do pedido
    order_items = [{
        "ITM_NUMBER": "000010",
        "MATERIAL": "000000000000260221",
        "TARGET_QTY": "5",
        "SALES_UNIT": "UN"
    }]

    order_itemsx = [{
        "ITM_NUMBER": "000010",
        "MATERIAL": "X",
        "TARGET_QTY": "X",
        "SALES_UNIT": "X"
    }]

    # Parceiros envolvidos no pedido
    order_partners = [
        {
        "PARTN_ROLE": "AG",        # Papel do parceiro (AG = Cliente)
        "PARTN_NUMB": "0000500098"    # Número do cliente
    },
    {
        "PARTN_ROLE": "RE",        # Papel do parceiro (AG = Cliente)
        "PARTN_NUMB": "0000500098"    # Número do cliente
    },
    {
        "PARTN_ROLE": "RG",        # Papel do parceiro (AG = Cliente)
        "PARTN_NUMB": "0000500098"    # Número do cliente
    },
    {
        "PARTN_ROLE": "WE",        # Papel do parceiro (AG = Cliente)
        "PARTN_NUMB": "0000500098"    # Número do cliente
    },     
    {
        "PARTN_ROLE": "ZS",        # Papel do parceiro (AG = Cliente)
        "PARTN_NUMB": "0000500044"    # Número do cliente
    } ]

    order_schedules = [{
        "ITM_NUMBER": "000010",
        "REQ_QTY": "5",

    }]

    order_schedulesx = [{
        "ITM_NUMBER": "000010",
        "REQ_QTY": "X",

    }]


    conditions = [{
        "ITM_NUMBER": "000010", 
        "COND_TYPE": "PR00",
        "COND_VALUE": "3671.00",
        "CURRENCY": "BRL"

    }]

 
            # Chamar a BAPI no SAP
    result = conn.call(
            "BAPI_SALESORDER_CREATEFROMDAT2",
            ORDER_HEADER_IN=order_header,
            ORDER_HEADER_INX=order_headerx,
            ORDER_ITEMS_IN=order_items,
            ORDER_ITEMS_INX=order_itemsx,
            ORDER_PARTNERS=order_partners,
            ORDER_SCHEDULES_IN=order_schedules,
            ORDER_SCHEDULES_INX=order_schedulesx,
            ORDER_CONDITIONS_IN = conditions

        )
        # Exibir mensagens de retorno
    has_error = False
    return_messages = result.get("RETURN", [])

    for msg in return_messages:
            if msg['TYPE'] in ('E', 'A'):  # Erro ou Abend
                has_error = True                
                print(f"{msg['TYPE']}: {msg['MESSAGE']}")
 

    if has_error: 
            conn.call('BAPI_TRANSACTION_ROLLBACK')
            print("Transação cancelada devido a erros.")
    else:
             
            conn.call('BAPI_TRANSACTION_COMMIT', WAIT='X')
            sales_document = result['SALESDOCUMENT']
            print(f"Ordem de venda criada com sucesso: {sales_document}")
    return result.get("SALESDOCUMENT", "Pedido não criado")
 

call_csap_mat_bom_read()
     
conn.close()