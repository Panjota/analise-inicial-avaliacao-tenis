# Análise de Dados: Tênis de Corrida RunRepeat

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Pandas](https://img.shields.io/badge/Pandas-1.5+-green.svg)
![Matplotlib](https://img.shields.io/badge/Matplotlib-3.5+-orange.svg)
![Status](https://img.shields.io/badge/Status-Completo-success.svg)

**Universidade do Estado do Amazonas (UEA)**  
**Curso:** Engenharia da Computação  
**Disciplina:** Ciência de Dados

</div>

---

## 👥 Equipe

| Nome | Função |
|------|---------|
| **Carlos Lavor Neto** | Desenvolvedor e Analista de Dados |
| **Alexandro Pantoja** | Desenvolvedor e Analista de Dados |

---

## 📋 Sumário

- [Sobre o Projeto](#-sobre-o-projeto)
- [Objetivo](#-objetivo)
- [Dataset](#-dataset)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Notebooks de Análise](#-notebooks-de-análise)
- [Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [Como Executar](#-como-executar)
- [Principais Resultados](#-principais-resultados)
- [Estrutura de Diretórios](#-estrutura-de-diretórios)
- [Referências](#-referências)

---

## 📖 Sobre o Projeto

Este projeto consiste em uma **análise exploratória completa** de dados sobre tênis de corrida, extraídos do site RunRepeat. O trabalho foi desenvolvido como parte da disciplina de Ciência de Dados do curso de Engenharia da Computação da UEA, com foco em aplicar técnicas de análise de dados, visualização e extração de insights relevantes.

A análise abrange desde a compreensão inicial dos atributos até análises multivariadas complexas, incluindo uma análise específica de **custo-benefício** para auxiliar potenciais compradores na escolha do melhor tênis.

---

## 🎯 Objetivo

O objetivo principal deste projeto é realizar uma análise exploratória de dados (EDA) completa sobre tênis de corrida, identificando:

- ✅ Padrões e tendências no mercado de tênis de corrida
- ✅ Relação entre preço, qualidade e características técnicas
- ✅ Melhores opções de custo-benefício para diferentes perfis de corredores
- ✅ Insights sobre marcas, durabilidade e performance
- ✅ Recomendações baseadas em dados para compra de tênis

---

## 📊 Dataset

### Fonte de Dados
- **Origem:** [RunRepeat](https://runrepeat.com)
- **Total de tênis:** 530 modelos
- **Atributos:** 46 colunas
- **Período de coleta:** Novembro de 2024

### Principais Atributos
- **Identificação:** Nome, marca, URL, imagem
- **Avaliação:** Audience Score (0-100)
- **Preço:** Valores em USD
- **Características físicas:** Peso, drop, stack height
- **Durabilidade:** Toebox, heel padding, outsole
- **Performance:** Flexibilidade, respirabilidade, suporte
- **Uso recomendado:** Daily running, tempo, racing, trail

### Qualidade dos Dados
- **Completude:** Alta (>80% em atributos principais)
- **Consistência:** Dados validados e limpos
- **Confiabilidade:** Fonte especializada reconhecida

---

## 🗂️ Estrutura do Projeto

O projeto está organizado em **6 notebooks Jupyter** sequenciais, cada um focado em uma etapa específica da análise:

### 📓 Notebooks de Análise

#### 1. Compreensão dos Atributos
**Arquivo:** `01_Compreensao_Atributos.ipynb`

Análise inicial do dataset com foco em:
- Dimensões e estrutura dos dados
- Tipos de dados de cada atributo
- Identificação de variáveis numéricas e categóricas
- Estatísticas descritivas básicas

**Principais Métricas:**
- 530 tênis analisados
- 46 atributos identificados
- Classificação completa de variáveis

---

#### 2. Avaliação da Qualidade dos Dados
**Arquivo:** `02_Avaliacao_Qualidade_Dados.ipynb`

Avaliação da completude e qualidade dos dados:
- Análise de valores ausentes
- Distribuição de missingness por atributo
- Identificação de padrões de dados faltantes
- Recomendações para tratamento

**Principais Métricas:**
- Taxa de completude geral: >75%
- Atributos críticos: >90% completos
- Visualizações de missing data

---

#### 3. Visualização Univariada (1D)
**Arquivo:** `03_Visualizacao_Univariada.ipynb`

Análise individual de variáveis:
- Histogramas de distribuições
- Box plots para identificar outliers
- Gráficos de densidade
- Análise de frequências

**Visualizações:**
- Distribuição de preços
- Distribuição de scores
- Análise de peso e drop
- Frequência de marcas

---

#### 4. Visualização Bivariada (2D)
**Arquivo:** `04_Visualizacao_Bivariada.ipynb`

Análise de relações entre pares de variáveis:
- Scatter plots: Preço vs Score
- Correlações entre variáveis numéricas
- Boxplots agrupados
- Análise de peso vs drop

**Principais Insights:**
- Correlação preço x qualidade: baixa
- Relação peso x drop: moderada
- Padrões por marca

---

#### 5. Visualização Multivariada (3D+)
**Arquivo:** `05_Visualizacao_Multivariada.ipynb`

Análise de múltiplas variáveis simultaneamente:
- Heatmaps de correlação
- Pair plots
- Análises por marca e categoria
- Padrões complexos

**Principais Insights:**
- Clusters de marcas por características
- Segmentação de mercado
- Perfis de produtos

---

#### 6. Análise de Custo-Benefício ⭐
**Arquivo:** `06_Analise_Custo_Beneficio.ipynb`

Análise focada em auxiliar a compra de tênis:

**Seções Principais:**

1. **Índice de Custo-Benefício**
   - Métrica: (Score / Preço) × 100
   - Categorização por faixas de preço

2. **Análise por Faixa de Preço (DUAS PERSPECTIVAS)**
   - **Melhor Custo-Benefício:** Para economizar
   - **Melhor Qualidade:** Para máxima performance

3. **Comparação Direta**
   - Top 5 C/B vs Top 5 Qualidade
   - Explicação das diferenças

4. **Análise de Durabilidade**
   - Correlação durabilidade x preço
   - Insights sobre valor real

5. **Recomendações por Perfil**
   - Daily Running
   - Tempo
   - Racing
   - Trail Running

6. **Análise de Marcas**
   - Custo-benefício médio por marca
   - Posicionamento de mercado

7. **Guia de Compra Completo**
   - Recomendações por orçamento
   - Top 3 em cada faixa (C/B e Qualidade)

**Faixas de Preço:**
- 💰 Econômico: < $80
- 💳 Moderado: $80 - $120
- 💎 Premium: $120 - $160
- 👑 Top: > $160

---

## 🛠️ Tecnologias Utilizadas

### Linguagem de Programação
- **Python 3.8+**

### Bibliotecas Principais

#### Manipulação de Dados
- **Pandas** - Análise e manipulação de dados
- **NumPy** - Operações numéricas

#### Visualização
- **Matplotlib** - Gráficos estáticos
- **Seaborn** - Visualizações estatísticas
- **Plotly** (opcional) - Gráficos interativos

#### Ambiente de Desenvolvimento
- **Jupyter Notebook** - Ambiente interativo de análise
- **IPython** - Shell interativo

#### Web Scraping (coleta de dados)
- **BeautifulSoup4** - Parser HTML/XML
- **Requests** - Requisições HTTP
- **Selenium** - Automação web

---

## 🚀 Como Executar

### Pré-requisitos

```bash
# Python 3.8 ou superior
python --version

# pip atualizado
pip install --upgrade pip
```

### Instalação

1. **Clone o repositório**
```bash
git clone https://github.com/seu-usuario/analise-inicial-avaliacao-tenis.git
cd analise-inicial-avaliacao-tenis
```

2. **Crie um ambiente virtual (recomendado)**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

### Execução

1. **Inicie o Jupyter Notebook**
```bash
jupyter notebook
```

2. **Execute os notebooks na ordem:**
   - `01_Compreensao_Atributos.ipynb`
   - `02_Avaliacao_Qualidade_Dados.ipynb`
   - `03_Visualizacao_Univariada.ipynb`
   - `04_Visualizacao_Bivariada.ipynb`
   - `05_Visualizacao_Multivariada.ipynb`
   - `06_Analise_Custo_Beneficio.ipynb`

3. **Execute cada célula sequencialmente** (Shift + Enter)

---

## 📈 Principais Resultados

### Insights Gerais

#### 💰 Preço vs Qualidade
- **Correlação fraca:** Preço alto ≠ Qualidade alta
- **Sweet spot:** Faixa $120-$170 oferece melhor valor
- **Todas as faixas têm excelentes opções** (Score 90+)

#### 🏃 Perfil de Uso
- **Daily Running:** Maior variedade (60% do mercado)
- **Racing:** Modelos mais caros e leves
- **Trail:** Maior durabilidade, preço moderado

#### 🏭 Marcas
- **Melhor C/B médio:** Saucony, Mizuno
- **Maior variedade:** Nike, ASICS, Adidas
- **Premium:** On, Hoka, NNormal

#### 🛡️ Durabilidade
- **Baixa correlação com preço** (0.15)
- **Tênis baratos podem ser muito duráveis**
- **Faixa moderada tem boa durabilidade média**

### Top 3 Geral

#### 🏆 Melhor Custo-Benefício
1. **Asics Gel Excite 10** - $70 | Score: 85 | C/B: 121.43
2. **Mizuno Wave Rider 27** - $75 | Score: 90 | C/B: 120.00
3. **Saucony Guide 17** - $80 | Score: 92 | C/B: 115.00

#### 🌟 Melhor Qualidade Absoluta
1. **Adidas Adizero Adios Pro 4** - $250 | Score: 93
2. **NNormal Kjerag** - $195 | Score: 93
3. **PUMA Deviate Nitro Elite** - $200 | Score: 93

### Recomendações Práticas

#### Para Economizar 💰
- Foque no índice de custo-benefício
- Priorize faixa econômica (<$80) ou moderada ($80-120)
- Marcas: Saucony, Mizuno, Brooks

#### Para Máxima Performance 🏆
- Foque no score absoluto
- Invista em modelos premium ($160+)
- Marcas: Adidas, Nike, On

#### Para Iniciantes 👟
- Budget: $80-120
- Tipo: Daily Running
- Priorize conforto e durabilidade

#### Para Competição 🥇
- Budget: $160+
- Tipo: Racing
- Priorize peso e responsividade

---

## 📁 Estrutura de Diretórios

```
analise-inicial-avaliacao-tenis/
│
├── 📓 01_Compreensao_Atributos.ipynb
├── 📓 02_Avaliacao_Qualidade_Dados.ipynb
├── 📓 03_Visualizacao_Univariada.ipynb
├── 📓 04_Visualizacao_Bivariada.ipynb
├── 📓 05_Visualizacao_Multivariada.ipynb
├── 📓 06_Analise_Custo_Beneficio.ipynb
│
├── 📂 tenis_scraper_runrepeat/
│   ├── 📂 dados_brutos/          # Dados originais da coleta
│   ├── 📂 dados_finais/           # Dados processados
│   │   ├── runrepeat_shoes_complete.csv
│   │   └── runrepeat_shoes_complete.json
│   └── 📂 scripts/                # Scripts de coleta
│
├── 📂 tabelas_exportadas/         # Tabelas geradas nas análises
│   ├── dataset_info.json
│   ├── tabela_atributos_classificacao.csv
│   └── tabela_completude_atributos.csv
│
├── 📂 scrapers_antigos/           # Versões anteriores dos scrapers
│
├── 📄 requirements.txt            # Dependências do projeto
├── 📄 README.md                   # Este arquivo
└── 📄 .gitignore                  # Arquivos ignorados pelo Git
```

---

## 📊 Tabelas Exportadas

Durante a análise, diversas tabelas são geradas e salvas:

### `tabela_atributos_classificacao.csv`
Classificação completa de todos os atributos do dataset (numérico, categórico, etc.)

### `tabela_completude_atributos.csv`
Análise de completude de cada atributo com porcentagens de valores presentes/ausentes

### `dataset_info.json`
Metadados do dataset incluindo dimensões, tipos e estatísticas básicas

---

## 🔍 Metodologia

### 1. Coleta de Dados
- Web scraping automatizado do RunRepeat
- Validação e limpeza inicial
- Armazenamento em CSV e JSON

### 2. Análise Exploratória
- Compreensão dos atributos
- Avaliação da qualidade
- Visualizações univariadas, bivariadas e multivariadas

### 3. Análise Específica
- Criação de métricas personalizadas (C/B)
- Segmentação por faixas de preço
- Análise comparativa

### 4. Insights e Recomendações
- Interpretação dos resultados
- Geração de recomendações práticas
- Documentação completa

---

## 📚 Referências

### Dataset
- **RunRepeat** - https://runrepeat.com
  - Plataforma especializada em análise e avaliação de tênis de corrida
  - Dados agregados de múltiplas fontes e testes de laboratório

### Bibliotecas e Ferramentas
- **Pandas Documentation** - https://pandas.pydata.org/docs/
- **Matplotlib Documentation** - https://matplotlib.org/stable/contents.html
- **Seaborn Documentation** - https://seaborn.pydata.org/
- **Jupyter Notebook** - https://jupyter.org/

### Conceitos Aplicados
- **Análise Exploratória de Dados (EDA)**
- **Visualização de Dados**
- **Análise Estatística Descritiva**
- **Web Scraping Ético**

---

## 📝 Notas

### Limitações
- Dados limitados ao período de coleta (Nov/2024)
- Preços podem variar com o tempo
- Análise baseada em dados do RunRepeat (não incluindo todas as marcas/modelos do mercado)

### Trabalhos Futuros
- [ ] Análise temporal de preços
- [ ] Modelo preditivo de scores
- [ ] Análise de sentimento de reviews
- [ ] Comparação com dados de vendas reais
- [ ] Dashboard interativo

---

## 📧 Contato

**Universidade do Estado do Amazonas (UEA)**  
Curso de Engenharia da Computação  
Disciplina: Ciência de Dados

**Desenvolvedores:**
- Carlos Lavor Neto
- Alexandro Pantoja

---

## 📄 Licença

Este projeto foi desenvolvido para fins acadêmicos como parte da disciplina de Ciência de Dados da UEA.

---

<div align="center">

**Desenvolvido com 💙 por Carlos Lavor Neto e Alexandro Pantoja**

*Universidade do Estado do Amazonas - 2024*

</div>
