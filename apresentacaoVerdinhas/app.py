from flask import Flask, render_template, jsonify

app = Flask(__name__)

# --- DADOS PARA OS GRÁFICOS ---

# Dados para a Página 2 (Contexto)
dados_lixo_brasil = {
    "labels": ["2010", "2015", "2017", "2018", "2019", "2020", "2021", "2022", "2023"],
    "data": [66.7, 72.5, 78.4, 79.0, 79.1, 82.48, 82.66, 81.81, 81.0]
}
dados_lixo_global = {
    "labels": ["2010", "2015", "2018", "2020", "2021", "2022", "2023", "2024"],
    "data": [1.84, 2.02, 2.10, 2.10, 2.15, 2.20, 2.30, 2.33]
}

# Dados para a Página 3 (Impactos)
dados_impacto_ambiental = {
    "labels": ["Resíduos", "Agricultura", "Energia", "Outros"],
    "data": [20, 40, 35, 5]
}
dados_impacto_social = {
    "labels": ["Não Expostos (Longe)", "Expostos (Perto de Lixões)"],
    "data": [7.5, 13.4]
}
# EM app.py

# CÓDIGO NOVO E CORRIGIDO
dados_impacto_economico = {
    "labels": [["Perda por", "Falta de Reciclagem"], ["Custo de Gestão", "RSU (2023)"]],
    "data": [14, 37]
}


# Dados para a Página de Alerta
dados_decomposicao = {
    "labels": ["Jornal", "Papelão", "Chicletes", "Filtro de Cigarro", "Madeira Pintada", "Náilon", "Couro", "Garrafa PET", "Lata de Alumínio", "Pilhas", "Plástico", "Fralda"],
    "data": [0.08, 0.38, 5, 5, 13, 30, 50, 100, 200, 300, 400, 450]
}
dados_taxa_reciclagem = {
    "labels": ["Alemanha", "Coréia do Sul", "Áustria", "Eslovênia", "Bélgica", "Brasil"],
    "data": [66, 59, 58, 58, 55, 4]
}


# --- ROTAS DA APLICAÇÃO ---

@app.route('/')
def index():
    # Página 1: Vídeo
    return render_template('index.html')

@app.route('/contexto')
def pagina2():
    # Página 2: Gráficos de Linha (Brasil e Global)
    return render_template('pagina2.html', kpi_brasil="75M")

@app.route('/impactos')
def pagina3():
    # Página 3: Impactos (Ambiental, Social, Econômico)
    return render_template('pagina3.html')

@app.route('/alerta')
def pagina_alerta():
    # Nova Página: Alerta e Comparação
    return render_template('pagina_alerta.html')

@app.route('/solucao')
def pagina4():
    # Página Final: Solução
    return render_template('pagina4.html')


# --- API PARA OS DADOS ---

@app.route('/api/dados')
def get_dados():
    return jsonify({
        "lixoBrasil": dados_lixo_brasil,
        "lixoGlobal": dados_lixo_global,
        "impactoAmbiental": dados_impacto_ambiental,
        "impactoSocial": dados_impacto_social,
        "impactoEconomico": dados_impacto_economico,
        "decomposicao": dados_decomposicao,
        "taxaReciclagem": dados_taxa_reciclagem
    })

if __name__ == '__main__':
    app.run(debug=True)
