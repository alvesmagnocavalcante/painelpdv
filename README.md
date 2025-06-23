# 🖥️ Painel de Controle para PDVs - Streamlit + SSH

Este projeto é uma aplicação web feita com **Streamlit** que permite conectar-se a PDVs (Pontos de Venda) via **SSH**, 
com autenticação dinâmica e execução de comandos administrativos como reinício de sistema, reinício de aplicação, ajustes de resolução, entre outros.

---

## 🚀 Funcionalidades

- 🔐 Autenticação automática com geração de senha baseada no número do PDV, data e tipo de acesso (suporte ou root).  
- 💻 Conexão via SSH usando a biblioteca `paramiko`.  
- 🔁 Execução de comandos remotos como:  
  - Reiniciar PDV  
  - Reiniciar Aplicação  
  - Ajustar Resolução  
  - Atualizar PDV (apenas suporte)  
- 🧠 Detecção e geração de IP fixo com base no IP da máquina local.  
- 🎛 Interface simples e funcional com Streamlit.  

---

## 📦 Requisitos

- Python 3.7+
- Acesso à rede com os PDVs
- IP da máquina que executa a aplicação compatível com o padrão `172.23.X.1Y`

---

## 📚 Instalação

# Clone o repositório
git clone https://github.com/alvesmagnocavalcante/painel-pdv.git
cd painel-pdv

# Crie e ative um ambiente virtual
python -m venv venv
source venv/bin/activate  # Para Linux/macOS
venv\Scripts\activate     # Para Windows

# Instale as dependências
pip install -r requirements.txt

#Execução
streamlit run app.py

