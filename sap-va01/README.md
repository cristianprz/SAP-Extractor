# SAP VA01 Order Creation

Este projeto é um script Python para criar ordens de venda no SAP usando a BAPI `BAPI_SALESORDER_CREATEFROMDAT2`.

## Funcionalidades

- Conexão com o SAP usando a biblioteca `pyrfc`
- Verificação de variáveis de ambiente e dependências
- Criação de ordens de venda com cabeçalho, itens, parceiros, agendamentos e condições
- Tratamento de erros e rollback de transações em caso de falhas

## Pré-requisitos

- Python 3.7+
- SAP RFC SDK
- Variável de ambiente `SAPNWRFC_HOME` configurada corretamente
- Acesso ao sistema SAP

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/yourusername/SAP-Extractor.git
cd SAP-Extractor/sap-va01
```

2. Instale os pacotes necessários:
```bash
pip install -r requirements.txt
```

## Configuração

### Configuração da Conexão SAP

Certifique-se de que o arquivo `sap_config.py` contenha as configurações corretas para a conexão com o SAP:

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

### Variável de Ambiente

Certifique-se de que a variável de ambiente `SAPNWRFC_HOME` esteja configurada corretamente e que o diretório especificado contenha as DLLs necessárias (`icuuc57.dll`, `icudt57.dll`, `icuin57.dll`).

## Uso

Execute o script principal para criar uma ordem de venda:

```bash
python rfc_sap_VA01.py
```

O script irá:

1. Verificar a configuração da variável de ambiente `SAPNWRFC_HOME`
2. Conectar ao SAP
3. Criar uma ordem de venda com os dados fornecidos
4. Exibir mensagens de retorno e tratar erros

## Estrutura do Projeto

```
sap-va01/
├── rfc_sap_VA01.py
├── requirements.txt
└── README.md
```

## Tratamento de Erros

O script inclui tratamento de erros para:

- Conexão com o SAP
- Criação de ordens de venda
- Rollback de transações em caso de falhas

## Contribuição

1. Faça um fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Faça push para a branch (`git push origin feature/nova-feature`)
5. Crie um novo Pull Request

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para mais detalhes.