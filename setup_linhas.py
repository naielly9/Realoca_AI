import sqlite3
import sys
import os
DB_PATH = "realoca_ai.db"
from database import Database

def conectar():
    return sqlite3.connect(DB_PATH)


def inserir_tipos_transporte():
    conn = conectar()
    cursor = conn.cursor()

    tipos = ["Municipal", "Intermunicipal"]
    for tipo in tipos:
        cursor.execute("INSERT OR IGNORE INTO tipos_transporte (tipo) VALUES (?)", (tipo,))
    conn.commit()
    conn.close()

def inserir_linhas(db: Database):
   
    linhas_data = [
        # Jacareí municipal
        {"numero": "01A", "nome": "Vila Branca", "tarifa": 6.83, "origem": "Jacareí", "destino": "Jacareí", "tipo": "Municipal"},
        {"numero": "01B", "nome": "Vila Branca (Residencial Santa Paula)", "tarifa": 6.83, "origem": "Jacareí", "destino": "Jacareí", "tipo": "Municipal"},
        {"numero": "02", "nome": "Campo Grande (via Jardim do Vale)", "tarifa": 6.83, "origem": "Jacareí", "destino": "Jacareí", "tipo": "Municipal"},
        {"numero": "03", "nome": "Parque Meia Lua", "tarifa": 6.83, "origem": "Jacareí", "destino": "Jacareí", "tipo": "Municipal"},
        {"numero": "05", "nome": "Cidade Salvador", "tarifa": 6.83, "origem": "Jacareí", "destino": "Jacareí", "tipo": "Municipal"},
        {"numero": "06", "nome": "Parque Califórnia", "tarifa": 6.83, "origem": "Jacareí", "destino": "Jacareí", "tipo": "Municipal"},
        {"numero": "07", "nome": "Conjunto 1º de Maio - Igarapés", "tarifa": 6.83, "origem": "Jacareí", "destino": "Jacareí", "tipo": "Municipal"},
        {"numero": "08", "nome": "Parque Santo Antônio", "tarifa": 6.83, "origem": "Jacareí", "destino": "Jacareí", "tipo": "Municipal"},
        {"numero": "09", "nome": "Jardim Emília", "tarifa": 6.83, "origem": "Jacareí", "destino": "Jacareí", "tipo": "Municipal"},
        {"numero": "10", "nome": "Jardim Pedramar via Parque Imperial", "tarifa": 6.83, "origem": "Jacareí", "destino": "Jacareí", "tipo": "Municipal"},
        {"numero": "11", "nome": "Rio Comprido - Balneário Paraíba", "tarifa": 6.83, "origem": "Jacareí", "destino": "Jacareí", "tipo": "Municipal"},
        {"numero": "13", "nome": "Jardim Maria Amélia", "tarifa": 6.83, "origem": "Jacareí", "destino": "Jacareí", "tipo": "Municipal"},
        {"numero": "15", "nome": "Bandeira Branca", "tarifa": 6.83, "origem": "Jacareí", "destino": "Jacareí", "tipo": "Municipal"},
        {"numero": "16", "nome": "Veraneio Ijal - Irajá", "tarifa": 6.83, "origem": "Jacareí", "destino": "Jacareí", "tipo": "Municipal"},
        {"numero": "18", "nome": "Jardim Paraíso - Rio Abaixo", "tarifa": 6.83, "origem": "Jacareí", "destino": "Jacareí", "tipo": "Municipal"},
        {"numero": "19", "nome": "Vila Garcia - Conjunto São Benedito", "tarifa": 6.83, "origem": "Jacareí", "destino": "Jacareí", "tipo": "Municipal"},
        {"numero": "21", "nome": "Jardim Panorama - Sto Antônio Boa Vista", "tarifa": 6.83, "origem": "Jacareí", "destino": "Jacareí", "tipo": "Municipal"},
        {"numero": "21B", "nome": "Jardim Colônia", "tarifa": 6.83, "origem": "Jacareí", "destino": "Jacareí", "tipo": "Municipal"},
        {"numero": "22", "nome": "Pagador Andrade - Balneário Paraíba", "tarifa": 6.83, "origem": "Jacareí", "destino": "Jacareí", "tipo": "Municipal"},
        {"numero": "23", "nome": "Jardim Luíza - Nova Jacareí", "tarifa": 6.83, "origem": "Jacareí", "destino": "Jacareí", "tipo": "Municipal"},
        {"numero": "26", "nome": "Jardim do Portal", "tarifa": 6.83, "origem": "Jacareí", "destino": "Jacareí", "tipo": "Municipal"},
        {"numero": "27", "nome": "Conjunto 22 de Abril", "tarifa": 6.83, "origem": "Jacareí", "destino": "Jacareí", "tipo": "Municipal"},
        {"numero": "28", "nome": "Jardim Santa Marina", "tarifa": 6.83, "origem": "Jacareí", "destino": "Jacareí", "tipo": "Municipal"},
        {"numero": "29", "nome": "Jardim Novo Amanhecer", "tarifa": 6.83, "origem": "Jacareí", "destino": "Jacareí", "tipo": "Municipal"},
        {"numero": "30", "nome": "Jardim Marquês", "tarifa": 6.83, "origem": "Jacareí", "destino": "Jacareí", "tipo": "Municipal"},
        {"numero": "81", "nome": "Remédio", "tarifa": 6.83, "origem": "Jacareí", "destino": "Jacareí", "tipo": "Municipal"},
        {"numero": "82", "nome": "Parateí", "tarifa": 6.83, "origem": "Jacareí", "destino": "Jacareí", "tipo": "Municipal"},
        {"numero": "83", "nome": "Recanto dos Pássaros", "tarifa": 6.83, "origem": "Jacareí", "destino": "Jacareí", "tipo": "Municipal"},
        {"numero": "84", "nome": "Figueira", "tarifa": 6.83, "origem": "Jacareí", "destino": "Jacareí", "tipo": "Municipal"},

        # Intermunicipais Jacareí ↔ SJC
        {"numero": "5114", "nome": "Jacareí (Terminal Rodoviário) / SJC (Rodoviária Frederico Ozanam)", "tarifa": 6.00, "origem": "Jacareí", "destino": "São José dos Campos", "tipo": "Intermunicipal"},
        {"numero": "5116", "nome": "Jacareí (Terminal Rodoviário) / SJC (Rodoviária Frederico Ozanam)", "tarifa": 6.50, "origem": "Jacareí", "destino": "São José dos Campos", "tipo": "Intermunicipal"},
        {"numero": "5118", "nome": "Jacareí (Parque Meia Lua) / SJC (Rodoviária Frederico Ozanam)", "tarifa": 6.00, "origem": "Jacareí", "destino": "São José dos Campos", "tipo": "Intermunicipal"},

        # São José dos Campos municipal
        {"numero": "101", "nome": "Represa / Terminal Central", "tarifa": 6.00, "origem": "São José dos Campos", "destino": "São José dos Campos", "tipo": "Municipal"},
        {"numero": "102", "nome": "Alimentadora Jaguari / Vila Dirce", "tarifa": 6.00, "origem": "São José dos Campos", "destino": "São José dos Campos", "tipo": "Municipal"},
        {"numero": "103", "nome": "Costinha / Terminal Central", "tarifa": 6.00, "origem": "São José dos Campos", "destino": "São José dos Campos", "tipo": "Municipal"},
        {"numero": "104", "nome": "Alimentadora Vargem Grande / Alto da Ponte", "tarifa": 6.00, "origem": "São José dos Campos", "destino": "São José dos Campos", "tipo": "Municipal"},
        {"numero": "105", "nome": "Bairro dos Freitas / Av. Eng. Francisco José Longo", "tarifa": 6.00, "origem": "São José dos Campos", "destino": "São José dos Campos", "tipo": "Municipal"},
        {"numero": "107", "nome": "Altos da Vila Paiva / Av. Eng. Francisco José Longo", "tarifa": 6.00, "origem": "São José dos Campos", "destino": "São José dos Campos", "tipo": "Municipal"},
        {"numero": "108", "nome": "Canindú / Via Vila Cândida / Rodoviária", "tarifa": 6.00, "origem": "São José dos Campos", "destino": "São José dos Campos", "tipo": "Municipal"},
        {"numero": "111", "nome": "Vale dos Pinheiros / Monte Castelo", "tarifa": 6.00, "origem": "São José dos Campos", "destino": "São José dos Campos", "tipo": "Municipal"},
        {"numero": "112", "nome": "Vila Terezinha / CTA", "tarifa": 6.00, "origem": "São José dos Campos", "destino": "São José dos Campos", "tipo": "Municipal"},
        {"numero": "115", "nome": "Vila Dirce / Altos de Santana / Av. Eng. Francisco José Longo", "tarifa": 6.00, "origem": "São José dos Campos", "destino": "São José dos Campos", "tipo": "Municipal"},
        {"numero": "116", "nome": "Taquari / Rodoviária", "tarifa": 6.00, "origem": "São José dos Campos", "destino": "São José dos Campos", "tipo": "Municipal"},
        {"numero": "117", "nome": "Morumbi / Aquarius", "tarifa": 6.00, "origem": "São José dos Campos", "destino": "São José dos Campos", "tipo": "Municipal"},
        {"numero": "118", "nome": "Alimentadora Sertãozinho / Alto da Ponte", "tarifa": 6.00, "origem": "São José dos Campos", "destino": "São José dos Campos", "tipo": "Municipal"},
        {"numero": "119", "nome": "Colonial / Aquarius", "tarifa": 6.00, "origem": "São José dos Campos", "destino": "São José dos Campos", "tipo": "Municipal"},
        {"numero": "121", "nome": "Urbanova / Esplanada / Terminal Central", "tarifa": 6.00, "origem": "São José dos Campos", "destino": "São José dos Campos", "tipo": "Municipal"},
        {"numero": "122", "nome": "Altos de Santana / Parque Industrial", "tarifa": 6.00, "origem": "São José dos Campos", "destino": "São José dos Campos", "tipo": "Municipal"},
        {"numero": "124", "nome": "Buquirinha II / Av. Eng. Francisco José Longo", "tarifa": 6.00, "origem": "São José dos Campos", "destino": "São José dos Campos", "tipo": "Municipal"},
        {"numero": "128", "nome": "Urbanova-Colinas / Terminal Central", "tarifa": 6.00, "origem": "São José dos Campos", "destino": "São José dos Campos", "tipo": "Municipal"},
        {"numero": "130", "nome": "Alimentadora São Francisco Xavier / São José dos Campos", "tarifa": 6.00, "origem": "São José dos Campos", "destino": "São José dos Campos", "tipo": "Municipal"},
        {"numero": "133", "nome": "Alimentadora Nova República / Colonial", "tarifa": 6.00, "origem": "São José dos Campos", "destino": "São José dos Campos", "tipo": "Municipal"},
        {"numero": "134", "nome": "Alimentadora Cidade Nova / Terminal Central", "tarifa": 6.00, "origem": "São José dos Campos", "destino": "São José dos Campos", "tipo": "Municipal"},
        {"numero": "138", "nome": "Urbanova / Altos de Santana", "tarifa": 6.00, "origem": "São José dos Campos", "destino": "São José dos Campos", "tipo": "Municipal"},
        {"numero": "140", "nome": "Alimentadora Varzea / Rodoviária", "tarifa": 6.00, "origem": "São José dos Campos", "destino": "São José dos Campos", "tipo": "Municipal"},
        {"numero": "500", "nome": "Aeroporto / Hotéis", "tarifa": 6.00, "origem": "São José dos Campos", "destino": "São José dos Campos", "tipo": "Municipal"},
    ]

    inseridos = 0

    for linha in linhas_data:
            origem_id = db.get_or_create_cidade(linha["origem"], db.get_or_create_estado("SP", "SP")) 
            destino_id = db.get_or_create_cidade(linha["destino"], db.get_or_create_estado("SP", "SP"))
            tipo_id = db.get_or_create_tipo_transporte(linha["tipo"])

            conn = db.conectar()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id FROM linhas
                WHERE numero=? AND cidade_origem_id=? AND cidade_destino_id=? AND tipo_transporte_id=?
            """, (linha["numero"], origem_id, destino_id, tipo_id))
            if not cursor.fetchone():
                cursor.execute("""
                    INSERT INTO linhas (numero, nome, tarifa, cidade_origem_id, cidade_destino_id, tipo_transporte_id)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (linha["numero"], linha["nome"], linha["tarifa"], origem_id, destino_id, tipo_id))
                inseridos += 1
            conn.commit()
            conn.close()

    print(f"{inseridos} linhas inseridas no banco.")

if __name__ == "__main__":
    db = Database()

    inserir_tipos_transporte()
    inserir_linhas(db)
    print("✅ Linhas cadastradas com sucesso no banco realoca_ai.db")