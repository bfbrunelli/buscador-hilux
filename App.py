from flask import Flask, render_template_string, request
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time

app = Flask(__name__)

PALAVRA_PADRAO = "hilux"
MAX_PAGINAS = 20
TIMEOUT = 10

sites = [
"https://www.emleilao.com.br/",
"https://www.pimentelleiloes.com.br/",
"https://www.webleiloes.com.br/",
"https://alfaleiloes.com/leiloes/",
"https://www.leiloesfederal.com.br/externo/",
"https://www.amazonasleiloes.com.br/",
"https://leiloesrionegro.com.br/",
"https://milanleiloes.com.br/",
"https://satoleiloes.com.br/",
"https://www.aragaoleiloes.com.br/",
"https://www.ricoleiloes.com.br/",
"https://www.victordortaleiloes.com.br/",
"https://www.danielgarcialeiloes.com.br/",
"https://www.grleiloes.com/",
"https://www.flexleiloes.com.br/",
"https://www.nossoleilao.com.br/",
"https://www.leiloespb.com.br/",
"https://mullerleiloes.com.br/",
"https://www.casadeleiloes.com.br/",
"https://www.snleiloes.com.br/",
"https://spencerleiloes.com.br/"
]

headers = {"User-Agent": "Mozilla/5.0"}

def buscar(site, palavra):
    visitados = set()
    fila = [site]
    encontrados = []
    dominio = urlparse(site).netloc
    paginas = 0

    while fila and paginas < MAX_PAGINAS:
        url = fila.pop(0)

        if url in visitados:
            continue

        try:
            r = requests.get(url, headers=headers, timeout=TIMEOUT)
            soup = BeautifulSoup(r.text, "html.parser")
            texto = soup.get_text().lower()

            if palavra.lower() in texto:
                encontrados.append(url)

            visitados.add(url)
            paginas += 1

            for link in soup.find_all("a", href=True):
                novo = urljoin(url, link["href"])
                if dominio in urlparse(novo).netloc:
                    fila.append(novo)

            time.sleep(0.5)

        except:
            pass

    return encontrados


@app.route("/", methods=["GET", "POST"])
def index():
    resultados = {}
    palavra = PALAVRA_PADRAO

    if request.method == "POST":
        palavra = request.form.get("palavra")

        for site in sites:
            encontrados = buscar(site, palavra)
            if encontrados:
                resultados[site] = encontrados

    return render_template_string("""
    <html>
    <head>
        <title>Busca de Veículos</title>
        <style>
            body { font-family: Arial; padding: 20px; }
            button { padding: 10px; font-size: 16px; }
            input { padding: 8px; font-size: 16px; }
        </style>
    </head>
    <body>
        <h2>🔎 Buscar Palavra nos Sites</h2>
        <form method="POST">
            <input type="text" name="palavra" value="{{palavra}}" />
            <button type="submit">Buscar</button>
        </form>
        <hr>
        {% for site, paginas in resultados.items() %}
            <h3>{{site}}</h3>
            <ul>
                {% for p in paginas %}
                    <li><a href="{{p}}" target="_blank">{{p}}</a></li>
                {% endfor %}
            </ul>
        {% endfor %}
    </body>
    </html>
    """, resultados=resultados, palavra=palavra)


if __name__ == "__main__":
    app.run(debug=True)
