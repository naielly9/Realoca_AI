import re

def carregar_custom_css_do_tema(caminho_arquivo_css: str, tema: str) -> dict:
    
    with open(caminho_arquivo_css, "r") as f:
        css = f.read()

    padrao_bloco = re.compile(rf"\.{tema}\s+(\.ag-[\w\-]+)\s*\{{([^}}]+)\}}", re.MULTILINE)
    custom_css = {}

    for match in padrao_bloco.finditer(css):
        seletor = match.group(1).strip()
        propriedades_brutas = match.group(2).strip()

        propriedades = {}
        for linha in propriedades_brutas.split(";"):
            if ":" in linha:
                chave, valor = linha.split(":", 1)
                propriedades[chave.strip()] = valor.strip()

        custom_css[seletor] = propriedades

    return custom_css
