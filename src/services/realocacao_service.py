import googlemaps
import time
from datetime import datetime
import sys
import os
import json
import unicodedata
import re
import pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from database import Database
db = Database()
import streamlit as st
api_key = st.secrets["google"]["api_key"]
gmaps = googlemaps.Client(key=api_key)

def normalizar_texto(texto):
    if not texto:
        return ""
    texto = unicodedata.normalize("NFD", texto)
    texto = texto.encode("ascii", "ignore").decode("utf-8")
    texto = re.sub(r"[^a-zA-Z0-9\s]", "", texto)

    return texto.strip().lower()

def get_address(id_endereco):
    """Retorna o endereço completo do ID do banco"""
    row = db.execute("""
        SELECT e.logradouro, e.numero, b.nome_bairro, c.nome, es.sigla, e.cep
        FROM enderecos e
        JOIN bairros b ON e.id_bairro = b.id
        JOIN cidades c ON b.cidade_id = c.id
        JOIN estados es ON c.estado_id = es.id
        WHERE e.id = ?
    """, (id_endereco,), fetchone=True)

    if not row:
        return None

    logradouro, numero, bairro, cidade, estado, cep = row
    return f"{logradouro or ''} {numero or ''}, {bairro}, {cidade}, {estado}, {cep}, Brasil"

def get_address_filiais(id_filial_func):
    
    row = db.execute("""
        SELECT e.logradouro, e.numero, b.nome_bairro, c.nome, es.sigla, e.cep
        FROM enderecos e
        JOIN bairros b ON e.id_bairro = b.id
        JOIN cidades c ON b.cidade_id = c.id
        JOIN estados es ON c.estado_id = es.id
        JOIN filiais f ON f.id_endereco = e.id
        WHERE f.id = ?
    """, (id_filial_func,), fetchone=True)

    if not row:
        return None

    logradouro, numero, bairro, cidade, estado, cep = row
    return f"{logradouro or ''} {numero or ''}, {bairro}, {cidade}, {estado}, {cep}, Brasil"

def calcular_rotas(mt_importadas=None):
    resultados = []
    if mt_importadas is not None:
        funcionarios = db.get_funcionarios_por_mt(mt_importadas)
    else:
        funcionarios = db.execute("""
            SELECT f.id, f.nome, f.id_endereco, f.id_filial
            FROM funcionarios f
            WHERE f.ativo = 1 AND f.id_endereco IS NOT NULL
        """, fetchall=True)

    filiais = db.execute("SELECT id, nome_filial, id_endereco FROM filiais", fetchall=True)

    linhas = db.execute("SELECT id, numero, nome, tarifa FROM linhas", fetchall=True)

    print(f"Encontrados {len(funcionarios)} funcionários e {len(filiais)} filiais.")
    print(type(funcionarios))
    for func in funcionarios:
        func_id = func[0]
        func_nome = func[1]
        id_endereco_func = func[2]
        id_filial_func = func[3]
        mt = func[4] if len(func) > 4 else ""
        centro_custo = func[5] if len(func) > 5 else ""

        origem = get_address(id_endereco_func)
        if not origem:
            print(f"⚠️ Funcionário {func_nome} sem endereço válido.")
            continue

        print(f"\n🔹 Calculando rotas para {func_nome} ({origem})")
        rotas_filial = {}
        distancia_antiga = None
        filial_atual = next((f for f in filiais if f[0] == id_filial_func), None)

        if filial_atual:
            _, filial_nome_atual, id_endereco_filial_atual = filial_atual
            destino_antigo = get_address(id_endereco_filial_atual)

            if destino_antigo:
                try:
                    directions_antigo = gmaps.directions(
                        origem, destino_antigo, mode="transit", departure_time=datetime.now()
                    )
                    if directions_antigo:
                        distancia_antiga = directions_antigo[0]['legs'][0]['distance']['value'] / 1000
                except Exception as e:
                    print(f"⚠️ Erro ao calcular distância antiga para {func_nome}: {e}")
            else:
                print(f"⚠️ Filial atual sem endereço válido para {func_nome}")

        for filial_id, filial_nome, id_endereco_filial in filiais:
            destino = get_address(id_endereco_filial)
            if not destino:
                continue

            custo_total = 0.0
            distancia_km = 0.0
            tempo_min = 0
            linhas_usadas = []

            try:
                directions = gmaps.directions(
                    origem, destino, mode="transit", departure_time=datetime.now()
                )

                if not directions:
                    continue

                steps = directions[0]['legs'][0]['steps']
                for step in steps:
                    if 'transit_details' in step:
                        line_info = step['transit_details']['line']
                        line_name = line_info.get('short_name', line_info.get('name', '')).strip()
                        line_name_normalizado = normalizar_texto(line_name)

                        match = next(
                            (
                                l for l in linhas
                                if normalizar_texto(l[1]) == line_name_normalizado
                                or normalizar_texto(l[2]) == line_name_normalizado
                            ),
                            None
                        )

                        if match:
                            linha_id, numero, nome, tarifa = match
                            custo_total += tarifa
                            linhas_usadas.append(f"{numero or nome}")
                        else:
                            custo_total += 7.00
                            linhas_usadas.append(f"{line_name} (estimada)")

                distancia_km = directions[0]['legs'][0]['distance']['value'] / 1000
                tempo_min = directions[0]['legs'][0]['duration']['value'] // 60

                rotas_filial[filial_id] = {
                    'filial_nome': filial_nome,
                    'distancia_km': distancia_km,
                    'tempo_min': tempo_min,
                    'custo_total': custo_total,
                    'linhas': linhas_usadas or ["Sem linha"]
                }

                time.sleep(1)

            except Exception as e:
                print(f"Erro na rota {origem} → {destino}: {e}")

        melhores = sorted(rotas_filial.values(), key=lambda x: x['custo_total'])[:3]

        linha_df = {
            "MT": mt,
            "C CUSTO": centro_custo,
            "Endereço Colaborador": origem,
            "Onde Estava Alocado": get_address_filiais(id_filial_func),
            "Antiga Distância (Destino 0)": distancia_antiga,  
            "Destino atual":filial_nome_atual
        }

        for i, rota in enumerate(melhores, start=1):
            linha_df[f"Destino{i}"] = rota["filial_nome"]
            linha_df[f"Linhas usadas {i}"] = " → ".join(rota["linhas"])
            linha_df[f"distancia{i}"] = rota["distancia_km"]

            antiga = distancia_antiga or rota["distancia_km"]
            linha_df[f"Redução {i}"] = (
                round(((antiga - rota["distancia_km"]) / antiga) * 100, 2) if antiga else 0
            )

        resultados.append(linha_df)
        print(f"✅ {func_nome}: {len(melhores)} rotas salvas com {sum(len(r['linhas']) for r in melhores)} linhas.")

    df_resultado = pd.DataFrame(resultados)
    arquivo_saida = "valida_reducoes.xlsx"

    if os.path.exists(arquivo_saida):
        os.remove(arquivo_saida)

    df_resultado.to_excel(arquivo_saida, index=False)

    print(f"✅ Arquivo '{arquivo_saida}' salvo com sucesso!")
    return df_resultado

# if __name__ == "__main__":
#     db.criar_tabelas()
#     calcular_rotas()