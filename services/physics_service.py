from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import models
import numpy as np
import plotly.graph_objects as go

def calcular_distancia_kepleriana(db: Session, planeta_id: int) -> dict:
    # 1. Busca o planeta no banco
    planeta = db.query(models.Planeta).filter(models.Planeta.id == planeta_id).first()
    if not planeta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Planeta não encontrado no universo catalogado."
        )
    
    if not planeta.periodo_orbital_dias:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Este planeta não possui dados de período orbital para cálculo."
        )

    # 2. Aplicação da Terceira Lei de Kepler (Física Computacional)
    # Converte o período orbital de dias terrestres para anos terrestres (P)
    p_anos = planeta.periodo_orbital_dias / 365.25
    
    # P² = a³  ==>  a = ³√(P²)  ==>  a = (P²)^(1/3)
    distancia_ua = (p_anos ** 2) ** (1 / 3)
    
    # Converte Unidades Astronômicas para Quilômetros (1 UA ≈ 149.597.870 KM)
    distancia_km = distancia_ua * 149597870.7

    return {
        "planeta_id": planeta.id,
        "nome_planeta": planeta.nome,
        "estrela_hospedeira": planeta.estrela.nome if planeta.estrela else "Órbita Interestelar",
        "dados_calculados": {
            "periodo_orbital_dias": planeta.periodo_orbital_dias,
            "periodo_orbital_anos_luz": round(p_anos, 4),
            "semieixo_maior_ua": round(distancia_ua, 4),
            "distancia_media_estrela_km": round(distancia_km, 2)
        },
        "metodologia": "Terceira Lei de Kepler (Harmônica) aplicada a sistemas de exoplanetas"
    }

def gerar_visualizacao_orbita_kepler(db: Session, planeta_id: int) -> str:
    # 1. Busca os dados físicos e faz o cálculo que criamos no passo anterior
    dados = calcular_distancia_kepleriana(db, planeta_id)
    raio_ua = dados["dados_calculados"]["semieixo_maior_ua"]
    nome_planeta = dados["nome_planeta"]
    nome_estrela = dados["estrela_hospedeira"]

    # 2. Gera os pontos geométricos da órbita (360 graus)
    t = np.linspace(0, 2 * np.pi, 200)
    # Simulando uma leve excentricidade orbital (característica física real)
    excentricidade = 0.1 
    x_orbita = raio_ua * (np.cos(t) - excentricidade)
    y_orbita = raio_ua * np.sin(t) * np.sqrt(1 - excentricidade**2)

    # 3. Cria a figura do Plotly
    fig = go.Figure()

    # Desenha a Órbita (Linha tracejada espacial)
    fig.add_trace(go.Scatter(
        x=x_orbita, y=y_orbita,
        mode='lines',
        name='Trajetória Orbital',
        line=dict(color='#475569', width=2, dash='dash'),
        hoverinfo='skip'
    ))

    # Desenha a Estrela Hospedeira no Centro (Foco da elipse)
    fig.add_trace(go.Scatter(
        x=[0], y=[0],
        mode='markers+text',
        name='Estrela',
        text=[nome_estrela],
        textposition="top center",
        marker=dict(size=25, color='#fbbf24', symbol='star', line=dict(color='#b45309', width=2)),
        hovertemplate=f"<b>{nome_estrela}</b><br>Massa do Sistema<extra></extra>"
    ))

    # Desenha o Planeta em uma posição fixa da órbita (ex: 45 graus)
    pos_x = raio_ua * (np.cos(np.pi/4) - excentricidade)
    pos_y = raio_ua * np.sin(np.pi/4) * np.sqrt(1 - excentricidade**2)
    
    fig.add_trace(go.Scatter(
        x=[pos_x], y=[pos_y],
        mode='markers+text',
        name='Planeta',
        text=[nome_planeta],
        textposition="bottom center",
        marker=dict(size=14, color='#38bdf8', line=dict(color='#0369a1', width=2)),
        hovertemplate=f"<b>{nome_planeta}</b><br>Distância Média: {raio_ua:.4f} UA<br>Período: {dados['dados_calculados']['periodo_orbital_dias']} dias<extra></extra>"
    ))

    # 4. Estilização do Espaço Sideral (Dark Mode)
    fig.update_layout(
        title=dict(
            text=f"Simulador Orbital Kepleriano: Sistema {nome_planeta}",
            font=dict(size=18, color='#818cf8', family="sans-serif")
        ),
        template="plotly_dark",
        paper_bgcolor="#0f172a",
        plot_bgcolor="#0f172a",
        showlegend=True,
        height=650,
        xaxis=dict(title="Distância em Unidades Astronômicas (UA)", gridcolor="#1e293b", zeroline=False, range=[-raio_ua*1.5, raio_ua*1.5]),
        yaxis=dict(title="Distância em Unidades Astronômicas (UA)", gridcolor="#1e293b", zeroline=False, scaleanchor="x", scaleratio=1, range=[-raio_ua*1.5, raio_ua*1.5])
    )

    # 5. Exporta como HTML Puro com scripts embutidos (Totalmente offline)
    return fig.to_html(full_html=True, include_plotlyjs='inline')
