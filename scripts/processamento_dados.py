import pandas as pd


class Dados:
    def __init__(self, path, tipo_dados):
        self.path = path
        self.tipo_dados = tipo_dados
        self.dados = self.leitura_dados()
        self.nome_colunas = self.get_columns()
        self.qtd_linhas = self.size_data()

    def leitura_dados(self):
        if self.tipo_dados == "csv":
            return pd.read_csv(self.path)

        elif self.tipo_dados == "json":
            return pd.read_json(self.path)

        elif self.tipo_dados == "dataframe":
            return self.path

        else:
            raise ValueError("Tipo de dados inválido. Use: 'csv', 'json' ou 'dataframe'.")

    def get_columns(self):
        return list(self.dados.columns)

    def size_data(self):
        return len(self.dados)

    def rename_columns(self, key_mapping):
        self.dados = self.dados.rename(columns=key_mapping)
        self.nome_colunas = self.get_columns()

    def join(dadosA, dadosB):
        dados_combinados = pd.concat(
            [dadosA.dados, dadosB.dados],
            ignore_index=True
        )

        return Dados(dados_combinados, "dataframe")

    def salvando_dados(self, path):
        self.dados.to_csv(path, index=False)