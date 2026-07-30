import io
import matplotlib
# Configura o matplotlib para rodar em modo "headless" (essencial para servidores de API)
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy.orm import Session
import models

def gerar_grafico_massa_vs_temperatura(db: Session) -> io.BytesIO:
    # 1. Extrai os dados do banco de dados real
    estrelas = db.query(models.Estrela).all()
    
    # 2. Converte os dados do SQLAlchemy para listas limpas (Estruturação de dados)
    massas = [e.massa for e in estrelas if e.massa is not None]
    temperaturas = [e.temperatura for e in estrelas if e.temperatura is not None]

    # Estilização do gráfico com o Seaborn (Visualização Científica)
    sns.set_theme(style="darkgrid")
    plt.figure(figsize=(10, 6))
    
    # Cria o Gráfico de Dispersão (Scatter Plot) com linha de tendência física
    sns.scatterplot(x=massas, y=temperaturas, s=100, color="purple", edgecolor="black", alpha=0.7)
    
    # Configurações de Física/Astronomia nos eixos
    plt.title("Relação Física: Massa da Estrela vs. Temperatura Efetiva", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("Massa Estelar (Unidades de Massa Solar - M☉)", fontsize=12)
    plt.ylabel("Temperatura Superficial (Kelvin - K)", fontsize=12)
    
    # Ajusta o layout para não cortar os rótulos
    plt.tight_layout()

    # 3. Salva o gráfico em um buffer de memória (Padrão de alta performance para APIs)
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png", dpi=150)
    plt.close() # Libera a memória do servidor tirando o gráfico do cache
    buffer.seek(0)
    
    return buffer

def obter_dados_completos_universo(db: Session) -> dict:
    estrelas = db.query(models.Estrela).all()
    planetas = db.query(models.Planeta).all()
    meteoros = db.query(models.Meteoro).all()

    return {
        "estrelas": [
            {"nome": e.nome, "massa": e.massa, "temperatura": e.temperatura, "idade": e.idade_bilhoes_anos}
            for e in estrelas
        ],
        "planetas": [
            {"nome": p.nome, "tipo": p.tipo, "raio_km": p.raio_km, "periodo_orbital": p.periodo_orbital_dias}
            for p in planetas
        ],
        "meteoros": [
            {"nome": m.nome, "composicao": m.composicao, "velocidade_km_s": m.velocidade_km_s, "tamanho_metros": m.tamanho_metros}
            for m in meteoros
        ]
    }
