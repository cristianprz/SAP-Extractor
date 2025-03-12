# SAP Extractor Projects

Este repositório contém dois projetos principais para integração com o SAP: `sap-extractor` e `sap-va01`.

## Projetos

### 1. SAP Extractor

O projeto `sap-extractor` é uma aplicação Python para extrair dados de BOM (Bill of Materials) do SAP e armazená-los em um banco de dados SQL Server.

#### Funcionalidades

- Conexão com SAP usando RFC
- Conexão com SQL Server
- Processamento em lote de materiais
- Criação e verificação automática de tabelas no banco de dados
- Tratamento de erros e logging

#### Estrutura do Projeto

```
sap-extractor/
├── src/
│   ├── connections/
│   │   ├── __init__.py
│   │   ├── sap_connection.py
│   │   └── sql_connection.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── bom.py
│   │   └── material_query.py
│   ├── config/
│   │   ├── __init__.py
│   │   ├── sap_config.py
│   │   └── sql_config.py
│   └── utils/
│       ├── __init__.py
│       └── validators.py
├── tests/
│   ├── __init__.py
│   └── test_connections.py
├── README.md
└── requirements.txt
```

### 2. SAP VA01 Order Creation

O projeto `sap-va01` é um script Python para criar ordens de venda no SAP usando a BAPI `BAPI_SALESORDER_CREATEFROMDAT2`.

#### Funcionalidades

- Conexão com SAP usando a biblioteca `pyrfc`
- Criação de ordens de venda com cabeçalho, itens, parceiros, agendamentos e condições
- Tratamento de erros e rollback de transações em caso de falhas

#### Estrutura do Projeto

```
sap-va01/
├── rfc_sap_VA01.py
├── requirements.txt
└── README.md
```

## Pré-requisitos Comuns

- Python 3.7+
- SAP RFC SDK
- ODBC Driver 17 for SQL Server (para `sap-extractor`)
- Acesso ao sistema SAP
- Acesso ao banco de dados SQL Server (para `sap-extractor`)

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/yourusername/SAP-Extractor.git
cd SAP-Extractor
```

2. Instale os pacotes necessários:
```bash
pip install -r requirements.txt
```

## Configuração

### SAP Configuration (`config/sap_config.py`):
```python
SAP_CONFIG = {
    'ashost': 'your_sap_host',
    'sysnr': '00',
    'client': '100',
    'user': 'your_user',
    'passwd': 'your_password',
    'timeout': '300',
    'auto_commit': True
}
```

### SQL Configuration (`config/sql_config.py`):
```python
SQL_CONFIG = {
    'driver': 'ODBC Driver 17 for SQL Server',
    'server': 'your_server',
    'database': 'your_database',
    'uid': 'your_username',
    'pwd': 'your_password',
    'timeout': 300,
    'autocommit': True
}
```

## Uso

### SAP Extractor

Execute o script principal para extrair dados de BOM:
```bash
python -m src.main
```

### SAP VA01 Order Creation

Execute o script principal para criar uma ordem de venda:
```bash
python sap-va01/rfc_sap_VA01.py
```

## Contribuição

1. Faça um fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Faça push para a branch (`git push origin feature/nova-feature`)
5. Crie um novo Pull Request

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para mais detalhes.