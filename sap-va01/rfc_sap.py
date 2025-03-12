import os
import sys
import time
from pyrfc import Connection
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

# Configuração da conexão com o SAP
conn_params = {
    'ashost': '********',  # Endereço do servidor SAP
    'sysnr': '********',              # Número do sistema
    'client': '********',            # Mandante
    'user': '********',            # Usuário SAP
    'passwd': '********'   # Senha
}

try:
    conn = Connection(**conn_params)
    print("Conexão com o SAP estabelecida com sucesso.")
except Exception as e:
    print(f"Erro ao conectar ao SAP: {e}")
    sys.exit(1)

# Função para chamar a função CSAP_MAT_BOM_READ
def call_csap_mat_bom_read(material):
    parameters = {
        'MATERIAL': str(material),  # Número do material
        'PLANT': '0050',            # Centro (planta)
        'BOM_USAGE': '1'            # Utilização da BOM (ex.: 1 = Produção)
    }

    try:
        result = conn.call('CSAP_MAT_BOM_READ', **parameters)
        
        # Verificar se a resposta contém os itens da BOM
        if 'T_STKO' in result and 'T_STPO' in result:
            print(f"Lista de Materiais para MATERIAL {material}:")
            for item in result['T_STPO']:
                # Verificar se o arquivo CSV já existe
                file_exists = os.path.isfile('bom_data.csv')

                # Abrir o arquivo CSV no modo append
                with open('bom_data.csv', mode='a', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)

                    # Escrever o cabeçalho se o arquivo for novo
                    if not file_exists:
                        writer.writerow(['Cod.','Material','Unidade', 'Nr BOM', 'Quantidade Base', 'Item', 'Componente', 'Quantidade','Unidade'])

                    # Escrever os dados da BOM
                    writer.writerow([
                        material,
                        result['T_STKO'][0]['ALT_TEXT'],
                        result['T_STKO'][0]['BASE_UNIT'],
                        result['T_STKO'][0]['BOM_NO'],
                        result['T_STKO'][0]['BASE_QUAN'],
                        item['ITEM_NO'],
                        item['COMPONENT'],
                        item['COMP_QTY'],
                        item['COMP_UNIT']
                    ])
        else:
            print(f"Nenhum item encontrado na BOM para MATERIAL {material}.")
    except Exception as e:
        print(f"Erro ao chamar a função para MATERIAL {material}: {e}")
 
for material in range(1000, 2300):
    call_csap_mat_bom_read(material)
    time.sleep(0.05)   

# Fechar a conexão
conn.close()