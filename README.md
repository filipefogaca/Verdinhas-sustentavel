🌿 Verdinhas - Gamificação e Sustentabilidade
O Verdinhas é um projeto desenvolvido para gamificar o processo de reciclagem, incentivando práticas sustentáveis através de desafios, recompensas e um mapa interativo. Este repositório também inclui uma apresentação em storytelling integrada para demonstrar os impactos e KPIs da solução.

🚀 Tecnologias Utilizadas
O projeto foi construído utilizando tecnologias modernas de desenvolvimento web e análise de dados:

Backend: Python com o framework Flask.

Banco de Dados: SQLite para persistência de dados.

Análise de Dados: Pandas e Scikit-learn para processamento de informações e inteligência.

Frontend: HTML5, CSS3 e JavaScript (incluindo Chart.js para visualização de dados).

📦 Estrutura do Projeto
A organização do código separa a aplicação principal da apresentação de impacto:

Plaintext

Verdinhas/
├── .venv/                 # Ambiente virtual isolado
├── apresentacao/          # Pasta com o storytelling (app_pitch.py)
├── static/                # Arquivos CSS, JS e imagens do app principal
├── templates/             # Páginas HTML do app principal
├── app.py                 # Ponto de entrada da aplicação principal
├── requirements.txt       # Dependências limpas do projeto
└── README.md              # Documentação
⚙️ Como Executar
Este projeto utiliza um ambiente virtual (venv) para garantir a portabilidade e evitar conflitos de bibliotecas.

1. Clonar e Configurar o Ambiente
Bash

# Clone o repositório
git clone https://github.com/filipefogaca/Verdinhas.git

# Acesse a pasta
cd Verdinhas

# Ative o seu ambiente virtual
.\.venv\Scripts\activate
2. Instalar Dependências
Com o ambiente ativo, instale as bibliotecas listadas no requirements.txt:

Bash

pip install -r requirements.txt
3. Rodar a Aplicação Principal
Bash

python app.py
Acesse em: http://127.0.0.1:5000

4. Rodar a Apresentação Storytelling
Bash

python apresentacao/app_pitch.py
Acesse em: http://127.0.0.1:5001

📊 Sobre o Storytelling
A apresentação integrada utiliza dados reais sobre reciclagem e saúde pública para demonstrar como a gamificação pode reduzir custos municipais e aumentar a taxa de engajamento da população.

Desenvolvido por Filipe Fogaça
