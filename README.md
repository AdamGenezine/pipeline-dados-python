# Pipeline de Dados em Python

Projeto de pipeline de dados para integrar duas bases de produtos de empresas diferentes. O fluxo lê arquivos brutos em JSON e CSV, padroniza os nomes das colunas, combina os registros em uma única tabela e salva o resultado em CSV.

## Visão geral

O projeto implementa um pequeno processo de ETL:

1. **Extract**: leitura dos dados brutos da Empresa A (`.json`) e da Empresa B (`.csv`).
2. **Transform**: renomeação das colunas da Empresa B para o mesmo padrão usado pela Empresa A.
3. **Load**: união das duas bases e gravação do arquivo consolidado em `data/processed/dados_combinados.csv`.

## Estrutura do projeto

```text
.
+-- data/
|   +-- raw/
|   |   +-- dados_empresaA.json
|   |   `-- dados_empresaB.csv
|   `-- processed/
|       `-- dados_combinados.csv
+-- notebooks/
|   `-- exploração.ipynb
+-- scripts/
|   +-- fusao_mercado.py
|   `-- processamento_dados.py
+-- .gitignore
`-- README.md
```

## Arquivos principais

| Arquivo | Descrição |
| --- | --- |
| `scripts/processamento_dados.py` | Define a classe `Dados`, responsável por ler arquivos, consultar colunas, contar linhas, renomear colunas, unir bases e salvar o resultado. |
| `scripts/fusao_mercado.py` | Script principal do pipeline. Executa a leitura das fontes, transforma a base da Empresa B, une os dados e salva o CSV final. |
| `notebooks/exploração.ipynb` | Notebook usado para exploração inicial das bases com Pandas. |
| `data/raw/dados_empresaA.json` | Base bruta da Empresa A em JSON. |
| `data/raw/dados_empresaB.csv` | Base bruta da Empresa B em CSV. |
| `data/processed/dados_combinados.csv` | Base final consolidada gerada pelo pipeline. |

## Dados de entrada

### Empresa A

Arquivo: `data/raw/dados_empresaA.json`

Quantidade de registros: **3.123**

Colunas:

- `Nome do Produto`
- `Categoria do Produto`
- `Preço do Produto (R$)`
- `Quantidade em Estoque`
- `Filial`

### Empresa B

Arquivo: `data/raw/dados_empresaB.csv`

Quantidade de registros: **1.323**

Colunas originais:

- `Nome do Item`
- `Classificação do Produto`
- `Valor em Reais (R$)`
- `Quantidade em Estoque`
- `Nome da Loja`
- `Data da Venda`

## Padronização das colunas

Antes da união das bases, o script `scripts/fusao_mercado.py` aplica o seguinte mapeamento na base da Empresa B:

| Coluna original | Coluna padronizada |
| --- | --- |
| `Nome do Item` | `Nome do Produto` |
| `Classificação do Produto` | `Categoria do Produto` |
| `Valor em Reais (R$)` | `Preço do Produto (R$)` |
| `Quantidade em Estoque` | `Quantidade em Estoque` |
| `Nome da Loja` | `Filial` |
| `Data da Venda` | `Data da Venda` |

Como a base da Empresa A não possui a coluna `Data da Venda`, esses registros ficam sem valor nessa coluna após a concatenação.

## Dados de saída

Arquivo gerado: `data/processed/dados_combinados.csv`

Quantidade de registros: **4.446**

Colunas finais:

- `Nome do Produto`
- `Categoria do Produto`
- `Preço do Produto (R$)`
- `Quantidade em Estoque`
- `Filial`
- `Data da Venda`

## Pré-requisitos

- Python 3.10 ou superior
- Pandas
- Jupyter Notebook ou VS Code com suporte a notebooks, caso queira abrir `notebooks/exploração.ipynb`

## Como configurar o ambiente

Crie e ative um ambiente virtual:

```bash
python -m venv venv
```

No Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

No Linux ou macOS:

```bash
source venv/bin/activate
```

Instale a dependência principal:

```bash
pip install pandas
```

Para usar o notebook, instale também:

```bash
pip install notebook
```

## Como executar o pipeline

Execute o script principal a partir da raiz do projeto:

```bash
python scripts/fusao_mercado.py
```

Ao final da execução, o arquivo consolidado será salvo em:

```text
data/processed/dados_combinados.csv
```

Durante a execução, o script também imprime no terminal:

- colunas da Empresa A;
- quantidade de linhas da Empresa A;
- colunas da Empresa B;
- quantidade de linhas da Empresa B;
- colunas da Empresa B após a padronização;
- colunas e quantidade de linhas da base final;
- caminho do arquivo salvo.

## Como o código funciona

A classe `Dados`, definida em `scripts/processamento_dados.py`, centraliza as operações do pipeline.

### Leitura dos dados

O método `leitura_dados()` aceita três tipos de entrada:

- `csv`: lê arquivos com `pd.read_csv`;
- `json`: lê arquivos com `pd.read_json`;
- `dataframe`: recebe um `DataFrame` já carregado.

### Metadados da base

Ao criar uma instância de `Dados`, o objeto armazena:

- `dados`: o `DataFrame` carregado;
- `nome_colunas`: lista com os nomes das colunas;
- `qtd_linhas`: quantidade de linhas da base.

### Transformação

O método `rename_columns()` recebe um dicionário de mapeamento e renomeia as colunas do `DataFrame`.

### União

O método `join()` usa `pd.concat` para empilhar as duas bases e retorna um novo objeto `Dados`.

### Gravação

O método `salvando_dados()` exporta o `DataFrame` para CSV sem salvar o índice.

## Observações

- O diretório `venv/` está listado no `.gitignore`, então o ambiente virtual não deve ser versionado.
- O projeto ainda não possui um arquivo `requirements.txt`. Se quiser registrar as dependências, gere um com:

```bash
pip freeze > requirements.txt
```

- O pipeline usa caminhos relativos. Por isso, execute os comandos a partir da raiz do projeto.
