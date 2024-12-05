import requests
import os
from dotenv import load_dotenv
import duckdb
load_dotenv()
# aeroportos = [
#     "SBCH", "SBIL", "SBPJ", "SBPS", "SBRP", "SBSN", "SBUR", "SSKW", "SSOU", "SWLC",
#     "SBDB", "SNTO", "SBCN", "SBPO", "SBAU", "SBCY", "SBIP", "SBKP", "SBRF", "SBVT",
#     "SNBR", "SBHT", "SBGV", "SBSO", "SBPB", "SBCB", "SBTT", "SBCG", "SBFI", "SBFN",
#     "SBFZ", "SBIZ", "SBSL", "SBSP", "SBPV", "SBRB", "SBZM", "SBJE", "SBMS", "SBPP",
#     "SBJI", "SBJR", "SNGI", "SBAX", "SNPD", "SWMW", "SBCA", "SBCF", "SBGL", "SBMA",
#     "SBMO", "SBRJ", "SBSR", "SWSI", "SNCP", "SBAE", "SBAT", "SBLE", "SBBR", "SBFL",
#     "SBGR", "SBMQ", "SBNF", "SBPA", "SBUL", "SBVC", "SBBW", "SBCP", "SBGO", "SBJV",
#     "SBPG", "SBPL", "SBEG", "SBLO", "SBCJ", "SBUG", "SBCX", "SBTG", "SSGG", "SBBE",
#     "SBCT", "SBJP", "SBKG", "SBMG", "SBMK", "SBPF", "SBSG", "SBSI", "SBCZ", "SBNM",
#     "SBRD", "SBVG", "SBAR", "SBBV", "SBSV", "SBTE", "SBDN", "SBJA", "SBJU", "SBML",
#     "SBVH", "SBCR", "SNEB", "SBIH", "SWPI"
# ]

aeroportos = [
    "SBCH"

]

con = duckdb.connect(
    '/home/rodrigo/Documentos/projetos/assistente_ia_sql_passagens_aereas/banco/dados_passagens.duckdb')

for aeroporto in aeroportos:

    url = "https://aiport-data.p.rapidapi.com/getAirportByICAO"

    querystring = {"icaoCode": aeroporto}

    headers = {
        "x-rapidapi-key": os.environ['x-rapidapi-key'],
        "x-rapidapi-host": os.environ['x-rapidapi-host']
    }

    response = requests.get(url, headers=headers, params=querystring)

    print(response.json())
    con.execute(
        """
        INSERT INTO 

    """
    )
