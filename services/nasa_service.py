import requests
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import models

def popular_banco_com_dados_nasa(db: Session) -> dict:
    url_nasa = (
        "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"
        "?query=select+top+150+pl_name,hostname,st_spectype,st_mass,st_teff,st_age,pl_rade,pl_orbper+from+ps"
        "&format=json"
    )
    
    try:
        headers = {
            "User-Agent": "AstroVisionApp/1.0 (Contact: josuecpn93@gmail.com)"
        }
        response = requests.get(url_nasa, headers=headers, timeout=15)
        response.raise_for_status()
        dados_nasa = response.json()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Erro ao conectar com a API da NASA: {str(e)}"
        )

    estrelas_criadas = 0
    planetas_criados = 0
    estrelas_em_memoria = {}
    planetas_em_memoria = set()

    for registro in dados_nasa:
        nome_estrela = registro.get("hostname")
        nome_planeta = registro.get("pl_name")
        
        if not nome_estrela or not nome_planeta:
            continue

        # 1. Validação do Planeta
        if nome_planeta in planetas_em_memoria:
            continue

        planeta_existe = db.query(models.Planeta).filter(models.Planeta.nome == nome_planeta).first()
        if planeta_existe:
            continue

        # 2. Busca a estrela primeiro no cache local
        estrela = estrelas_em_memoria.get(nome_estrela)
        
        # Se não estiver no cache local, busca no banco real
        if not estrela:
            estrela = db.query(models.Estrela).filter(models.Estrela.nome == nome_estrela).first()
        
        # Se ela não existir em lugar nenhum, cria uma nova
        if not estrela:
            estrela = models.Estrela(
                codigo_estelar=f"NASA-{nome_estrela.replace(' ', '-')}",
                nome=nome_estrela,
                tipo_espectral=registro.get("st_spectype") or "Não Catalogado",
                massa=float(registro["st_mass"]) if registro.get("st_mass") is not None else 1.0,
                temperatura=int(registro["st_teff"]) if registro.get("st_teff") is not None else 5000,
                idade_bilhoes_anos=float(registro["st_age"]) if registro.get("st_age") is not None else 4.5
            )
            db.add(estrela)
            db.flush() 
            
            # Guarda no cache
            estrelas_em_memoria[nome_estrela] = estrela
            estrelas_criadas += 1

        # 3. Tratamento e Inserção do Planeta
        raio_terra = registro.get("pl_rade")
        raio_km = (float(raio_terra) * 6371.0) if raio_terra is not None else 6000.0

        novo_planeta = models.Planeta(
            nome=nome_planeta,
            tipo="Exoplaneta Confirmado",
            raio_km=raio_km,
            habitavel=0,
            periodo_orbital_dias=float(registro["pl_orbper"]) if registro.get("pl_orbper") is not None else 365.0,
            estrela_id=estrela.id
        )
        db.add(novo_planeta)

        planetas_em_memoria.add(nome_planeta)
        planetas_criados += 1

    # --- PIPELINE DE ENGENHARIA DE DADOS: GERAÇÃO DE METEOROS/ASTEROIDES ---
    # Vincula estrelas e planetas recentemente cadastrados no banco para criar os vínculos
    todas_estrelas = db.query(models.Estrela).all()
    todos_planetas = db.query(models.Planeta).all()
    meteoros_criados = 0

    # Massa típica e nomes baseados em meteoritos famosos e asteroides capturados
    composicoes = ["Ferro-Níquel", "Silicato (Rochoso)", "Carbonáceo (Rico em Carbono)", "Metálico-Rochoso"]
    nomes_base = ["Apophis", "Bennu", "Churyumov", "Halley", "Encke", "Ceres-Fragment", "Vesta-Minor"]

    # Cria cerca de 30 meteoros no universo para análise de dados
    for i in range(30):
        nome_meteoro = f"{nomes_base[i % len(nomes_base)]}-{100 + i}"
        
        # Validação preventiva para não duplicar meteoros se rodar o script de novo
        if db.query(models.Meteoro).filter(models.Meteoro.nome == nome_meteoro).first():
            continue

        # Simulação Física de Captura Gravitacional:
        # Usa uma lógica probabilística: corpos maiores têm mais chance de capturar meteoros
        sorteio = i % 3 
        estrela_id_vinculo = None
        planeta_id_vinculo = None

        if sorteio == 1 and todos_planetas:
            # Capturado por um Planeta aleatório (Ex: Meteoritos que caem na Terra)
            planeta_alvo = todos_planetas[i % len(todos_planetas)]
            # Planetas maiores (maior raio_km) têm gravidade mais forte e capturam mais facilmente
            if planeta_alvo.raio_km > 5000: 
                planeta_id_vinculo = planeta_alvo.id
                # Se está preso ao planeta, também está no sistema da estrela daquele planeta
                estrela_id_vinculo = planeta_alvo.estrela_id 

        elif sorteio == 2 and todas_estrelas:
            # Capturado diretamente pela Estrela (Ex: Cometas de longo período)
            estrela_alva = todas_estrelas[i % len(todas_estrelas)]
            if estrela_alva.massa > 0.3: # Estrelas com massa considerável
                estrela_id_vinculo = estrela_alva.id

        # Se sorteio == 0, ele continua como um "Viajante Errante" (Chaves estrangeiras como null)

        # Dados físicos simulados do meteoro
        novo_meteoro = models.Meteoro(
            nome=nome_meteoro,
            composicao=composicoes[i % len(composicoes)],
            velocidade_km_s=round(11.2 + (i * 1.5) % 60, 2), # Velocidades típicas de escape espacial (km/s)
            massa_kg=float(5000 + (i * 12500)),
            tamanho_metros=round(1.5 + (i * 0.8) % 45, 2),
            estrela_id=estrela_id_vinculo,
            planeta_id=planeta_id_vinculo
        )
        db.add(novo_meteoro)
        meteoros_criados += 1

    db.commit()
    
    return {
        "mensagem": "Carga de dados espaciais finalizada com sucesso!",
        "estrelas_importadas": estrelas_criadas,
        "planetas_importados": planetas_criados,
        "meteoros_gerados_gravitacionalmente": meteoros_criados,
        "fonte": "NASA Exoplanet Archive + Simulação de Captura Cinética"
    }

