"""Refaz o README.md a partir da lista pública de links do KCUuLab.

Fonte: https://services.gguerreiro232.com/go/links.json (gerada pelo funil do site).
Corre sozinho na GitHub Action `atualizar-readme.yml` (todos os dias e a pedido).
Só mexe no que está entre os marcadores <!-- LINKS:INICIO --> e <!-- LINKS:FIM -->.
Sem dependências: só a biblioteca padrão do Python.
"""
import json
import sys
import urllib.request
from pathlib import Path

FONTE = "https://services.gguerreiro232.com/go/links.json"
README = Path(__file__).resolve().parent.parent / "README.md"
INICIO, FIM = "<!-- LINKS:INICIO -->", "<!-- LINKS:FIM -->"


def celula(texto):
    """Texto seguro dentro de uma célula de tabela Markdown."""
    return " ".join(str(texto).split()).replace("|", "\\|")


def ler_links():
    pedido = urllib.request.Request(FONTE, headers={"User-Agent": "KCUuLAB-readme (+https://github.com/KCUuLAB/kcuulab)"})
    with urllib.request.urlopen(pedido, timeout=30) as r:
        dados = json.load(r)
    links = dados.get("links")
    if not isinstance(links, list) or not links:
        raise SystemExit("links.json sem links: o README fica como está")
    return links


def tabela(links):
    linhas = ["| Vídeo | O que é | Link |", "|---|---|---|"]
    for l in links:
        nome = celula(l["nome"])
        video = f"[{nome}]({l['youtube']})" if l.get("youtube") else nome
        url = l["url"]
        texto = url.replace("https://", "").rstrip("/")
        linhas.append(f"| {video} | {celula(l.get('descricao', ''))} | [{texto}]({url}) |")
    return "\n".join(linhas)


def main():
    links = ler_links()
    atual = README.read_text(encoding="utf-8")
    if INICIO not in atual or FIM not in atual:
        raise SystemExit("README sem os marcadores LINKS:INICIO / LINKS:FIM")
    antes, resto = atual.split(INICIO, 1)
    _, depois = resto.split(FIM, 1)
    novo = f"{antes}{INICIO}\n{tabela(links)}\n\n_{len(links)} links, do mais recente para o mais antigo._\n{FIM}{depois}"
    if novo == atual:
        print("README já está em dia")
        return 0
    README.write_text(novo, encoding="utf-8", newline="\n")
    print(f"README atualizado: {len(links)} links")
    return 0


if __name__ == "__main__":
    sys.exit(main())
