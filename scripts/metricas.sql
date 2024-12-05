SELECT *
from dim_aeroporto ;

SELECT *
from main.dim_empresas e
where e.ICAO  = 'ABJ';

SELECT *
from main.ft_venda_passagem fvp ;

SELECT *
from read_csv('/home/rodrigo/Documentos/projetos/assistente_ia_sql_passagens_aereas/banco/fato.csv') ft
WHERE ft.ANO = 2023
AND ft.MES = 1
AND ft.EMPRESA = 'GLO';
-- Destinos mais procurados no mês


SELECT da.municipio, SUM(ft.ASSENTOS) as total_passageiros
from read_csv('/home/rodrigo/Documentos/projetos/assistente_ia_sql_passagens_aereas/banco/fato.csv') ft
INNER JOIN main.dim_aeroporto da on da.oaci = ft.DESTINO
WHERE ft.ANO = 2023
AND ft.MES = 2
AND ft.EMPRESA = 'GLO'
GROUP BY da.municipio
order by 2 desc
LIMIT  10;