# Projeto-de-IA---1-Parte
Análise de Desempenho e Valuation das Empresas do S&P 500 com IA Generativa
Este repositório contém o projeto de análise exploratória dos dados financeiros das empresas listadas no índice S&P 500. O objetivo é compreender e extrair insights a partir de informações fundamentais, tais como Price/Earnings, Market Cap, EBITDA, entre outras, utilizando técnicas de análise de dados em Python.

Descrição do Projeto
O projeto consiste em:

Carregar e explorar o dataset: Utilizando o arquivo constituents-financials_csv.csv que contém dados públicos (obtidos de fontes como EDGAR, SEC, etc.) com as seguintes colunas: Symbol, Name, Sector, Price, Price/Earnings, Dividend Yield, Earnings/Share, 52 Week Low, 52 Week High, Market Cap, EBITDA, Price/Sales, Price/Book e SEC Filings.

Realizar análises exploratórias: Obtenção de estatísticas descritivas, verificação de dados faltantes, criação de visualizações (boxplots, scatter plots) e aplicação de normalização em métricas para facilitar a comparação.

Preparar os dados para análises futuras: Os insights obtidos nesta etapa servirão como base para integrações futuras com ferramentas de IA (ex.: para geração automatizada de resumos e relatórios).


------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
S&P 500 Insights – Parte 2
💡 Visão Geral
O S&P 500 Insights é um dashboard interativo e inteligente para análise financeira, comparação de empresas e geração automatizada de recomendações, usando inteligência artificial (ChatGPT) sobre os dados das empresas do índice S&P 500.
Esta segunda entrega (N2) apresenta o sistema final, pronto para uso, com todas as funcionalidades implementadas, código documentado e relatório acadêmico completo.

🚀 Funcionalidades Principais
Visualização por setor: análise interativa de todos os setores do S&P 500, com KPIs, rankings e gráficos customizados.

Análise completa da empresa: exibição de todos os indicadores financeiros (cards, tabela, gráficos) e geração de análise SWOT/recomendações automáticas via ChatGPT.

Comparação de empresas: escolha de duas empresas do mesmo setor, comparação visual em duas escalas (indicadores grandes/proporcionais), cards detalhados e análise comparativa automática gerada por IA.

Interface moderna e responsiva: layout escuro, cards, gráficos em Plotly, uso fácil em desktop e mobile.

Segurança: a API Key da OpenAI fica protegida no .env, seguindo as melhores práticas.

🛠️ Instalação e Execução
Pré-requisitos:

Python 3.9+

Dependências listadas em requirements.txt

Conta e API Key da OpenAI (colocar em arquivo .env)

Instale as dependências:

bash
Copiar
Editar
pip install -r requirements.txt
Crie o arquivo .env:

ini
Copiar
Editar
OPENAI_API_KEY=sk-...
Execute o dashboard:

bash
Copiar
Editar
streamlit run app.py
📊 Dataset
Fonte: Kaggle – “S&P 500 Companies with Financial Information”

Arquivo: constituents-financials_csv.csv

Descrição: Informações financeiras atualizadas das empresas do S&P 500 (ticker, nome, setor, preço, P/L, dividend yield, market cap, EBITDA, etc.)

🧑‍💻 Principais Tecnologias
Python

Pandas

Streamlit

Plotly

OpenAI API (ChatGPT)

dotenv

🔎 Arquitetura e Organização
app.py — dashboard completo e interativo (código comentado, pronto para apresentação)

constituents-financials_csv.csv — dataset utilizado

.env — arquivo para a API Key (não enviar para o repositório)

requirements.txt — dependências do projeto

Relatorio_SNP500_IA_Mackenzie.docx — relatório acadêmico final

📚 Como Utilizar
Escolha o setor na barra lateral para visualizar os KPIs e os principais rankings do setor.

Selecione uma empresa para ver seus indicadores completos, análise SWOT e recomendações automáticas geradas pela IA.

Compare duas empresas do mesmo setor, visualize gráficos separados por escala e gere análises comparativas da IA.

Clique nos botões “Gerar análise IA” para receber recomendações inteligentes, sempre com explicação expandida.


