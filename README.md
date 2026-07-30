# 🪐 AstroVision

O **AstroVision** é uma API REST desenvolvida em Python com FastAPI voltada para o catálogo, simulação física e análise estatística de corpos celestes. O projeto combina dados reais de exoplanetas obtidos via API da NASA com geração de dados sintéticos baseados em mecânica celeste clássica.

A aplicação foi desenhada seguindo rigorosos padrões de arquitetura corporativa para garantir alta legibilidade, responsabilidade única (SRP) e facilidade de manutenção.

---

## 🛠️ Tecnologias Utilizadas

- **Core:** Python 3.12+ & FastAPI
- **Banco de Dados & ORM:** SQLite, SQLAlchemy & Alembic (Migrations)
- **Engenharia & Análise de Dados:** Requests, Matplotlib, Seaborn & Plotly Python
- **Validação de Camada:** Pydantic V2

---

## 📐 Arquitetura do Projeto

O projeto adota o padrão **Router-Service-Repository**, desacoplando totalmente as responsabilidades HTTP, regras de negócios/física e persistência de dados.

```text
├── db/               # Configurações de infraestrutura do banco (SQLAlchemy)
├── models/         # Modelos/Tabelas do banco de dados (Entidades)
├── schemas/          # Modelos de validação de dados de entrada/saída (Pydantic)
├── services/         # Camada de Negócio e Física Computacional (Services)
├── routers/          # Controladores HTTP e Rotas (Controllers/Routers)
├── alembic/          # Histórico de versionamento estrutural do banco
├── main.py           # Ponto de entrada e inicialização da API
└── README.md         # Documentação do ecossistema
```

---

## 🌌 Recursos e Funcionalidades Principais

### 1. Modelagem com Integridade Referencial
O universo mapeia 3 entidades principais com chaves estrangeiras (`nullable=True`) altamente flexíveis:
- **Estrelas:** O coração dos sistemas lineares.
- **Planetas:** Podem orbitar uma estrela hospedeira ou vagar livremente.
- **Meteoros:** Podem pertencer a uma estrela, a um planeta (captura gravitacional) ou cruzar o espaço como viajantes errantes.

### 2. Pipeline de Ingestão de Dados (NASA API)
O sistema consome o arquivo oficial **NASA Exoplanet Archive**. O pipeline foi blindado com conceitos avançados de Engenharia de Dados:
- **Idempotência:** Validação preventiva na memória interna que impede colisões de chaves únicas (`UNIQUE constraint`) ao reexecutar a carga.
- **Data Cleaning:** Tratamento de dados nulos do governo americano e conversão de grandezas físicas (raios terrestres convertidos para quilômetros).

### 3. Painel de Data Visualization (Dashboard Offline)
Através do módulo de Analytics, a API compila dados de múltiplas tabelas relacionais e renderiza um dashboard interativo em HTML/Plotly embutido. O motor gráfico roda direto no back-end, garantindo que o painel funcione **100% offline**, sem dependência de internet ou CDNs de terceiros.

### 4. Física Computacional (Terceira Lei de Kepler)
Um módulo dedicado aplica a **Lei Harmônica de Kepler ($P^2 = a^3$)** para deduzir o semieixo maior da órbita de exoplanetas a partir do seu período orbital em dias. Além do retorno estruturado em JSON, a API plota uma **visualização elíptica espacial** do planeta orbitando sua estrela.

---

## 🚀 Como Rodar o Projeto Localmente

1. **Clone o repositório:**
   ```bash
   git clone https://github.com
   cd astrovision
   ```

2. **Ative o seu ambiente virtual (`venv`):**
   ```bash
   # Windows:
   .venv\Scripts\activate
   # Linux/Mac:
   source .venv/bin/activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install fastapi uvicorn sqlalchemy alembic requests matplotlib seaborn plotly numpy
   ```

4. **Execute as Migrações do Banco:**
   ```bash
   alembic upgrade head
   ```

5. **Inicie o servidor local:**
   ```bash
   uvicorn main:app --reload
   ```

6. **Explore a documentação:**
   - Documentação Swagger Interativa: /docs
   - Painel Estatístico Interativo: /analytics/dashboard
   - Simulador Orbital Kepleriano: /physics/kepler-law/{id_cadastrado_do_planeta}/view
