from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse, StreamingResponse
import plotly.express as px
import entities
from sqlalchemy.orm import Session
import services.analytics_service as analytics_service
from db import get_db

router = APIRouter(prefix="/analytics", tags=["Análise Estatística e Gráficos"])

@router.get("/stars-distribution-chart")
def obter_grafico_distribuicao_estelar(db: Session = Depends(get_db)):
    """
    Gera dinamicamente um gráfico científico relacionando a Massa e a Temperatura 
    de todas as estrelas catalogadas no banco de dados.
    """
    imagem_buffer = analytics_service.gerar_grafico_massa_vs_temperatura(db)
    return StreamingResponse(imagem_buffer, media_type="image/png")

@router.get("/raw-data")
def obter_dados_brutos(db: Session = Depends(get_db)):
    """Retorna todos os dados científicos consolidados para alimentar o painel interativo."""
    return analytics_service.obter_dados_completos_universo(db)

@router.get("/dashboard", response_class=HTMLResponse)
def exibir_dashboard_interativo(db: Session = Depends(get_db)):
    """
    Gera um dashboard científico interativo no back-end (Python) e o entrega 
    pronto para o navegador, funcionando 100% offline (sem depender de CDNs).
    """
    # 1. Busca os dados reais do banco SQLite
    estrelas = db.query(entities.Estrela).all()
    
    # 2. Estrutura os dados em listas para o Plotly
    dados_grafico = {
        "Nome da Estrela": [e.nome for e in estrelas],
        "Massa Estelar (M☉)": [e.massa for e in estrelas],
        "Temperatura Superficial (K)": [e.temperatura for e in estrelas],
        "Idade (Bilhões de anos)": [e.idade_bilhoes_anos for e in estrelas]
    }

    # 3. Cria o gráfico de dispersão interativo usando o Plotly do Python
    fig = px.scatter(
        dados_grafico,
        x="Massa Estelar (M☉)",
        y="Temperatura Superficial (K)",
        hover_name="Nome da Estrela",
        size="Idade (Bilhões de anos)", # O tamanho do ponto varia conforme a idade!
        color="Temperatura Superficial (K)", # A cor muda conforme a temperatura (Física pura)
        color_continuous_scale=px.colors.sequential.Plasma,
        title="Painel Interativo AstroVision: Massa vs. Temperatura (Dados Reais NASA)"
    )

    # 4. Customiza o visual para o "Dark Mode" elegante que você escolheu
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0f172a", # bg-slate-900 do Tailwind
        plot_bgcolor="#1e293b",  # bg-slate-800
        title_font_color="#818cf8", # Indigo-400
        font_family="sans-serif",
        height=600
    )

    # 5. Transforma o gráfico em HTML Puro com o script embutido (Inlined Script)
    # O parâmetro include_plotlyjs='cdn' seria o padrão, mas usando 'directory' ou embutindo o script básico
    # o Plotly injeta todo o motor gráfico dentro da própria string HTML enviada pela API!
    html_puro = fig.to_html(full_html=True, include_plotlyjs='inline')

    return HTMLResponse(content=html_puro)

