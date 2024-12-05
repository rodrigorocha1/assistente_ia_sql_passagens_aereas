SELECT *
from dim_aeroporto ;

SELECT *
from main.dim_empresas e
where e.ICAO  = 'ABJ';

SELECT *
from main.ft_venda_passagem fvp ;

SELECT DISTINCT EMPRESA
from read_csv('/home/rodrigo/Documentos/projetos/assistente_ia_sql_passagens_aereas/banco/fato.csv') ft
WHERE ft.ANO = 2023
AND ft.MES = 1
AND ft.EMPRESA = 'GLO';
-- Destinos mais procurados no mês


SELECT 
	da.municipio, 
	SUM(ft.ASSENTOS) as total_passageiros
from read_csv('/home/rodrigo/Documentos/projetos/assistente_ia_sql_passagens_aereas/banco/fato.csv') ft
INNER JOIN main.dim_aeroporto da on da.oaci = ft.DESTINO
WHERE ft.ANO = 2023
AND ft.MES = 2
AND ft.EMPRESA = 'GLO'
GROUP BY da.municipio
order by 2 desc
LIMIT  10;


SELECT
	da.municipio, 
	SUM(ft.ASSENTOS) as total_passageiros
from read_csv('/home/rodrigo/Documentos/projetos/assistente_ia_sql_passagens_aereas/banco/fato.csv') ft
INNER JOIN main.dim_aeroporto da on da.oaci = ft.DESTINO
WHERE ft.ANO = 2023
AND ft.MES = 2
AND ft.EMPRESA = 'AZU'
AND da.UF = 'SP'
GROUP BY da.municipio
order by 2 desc;



SELECT 
	da.UF, 
	SUM(ft.ASSENTOS) as total_passageiros
from read_csv('/home/rodrigo/Documentos/projetos/assistente_ia_sql_passagens_aereas/banco/fato.csv') ft
INNER JOIN main.dim_aeroporto da on da.oaci = ft.DESTINO
WHERE ft.ANO = 2023
AND ft.MES = 2
AND ft.EMPRESA = 'GLO'
GROUP BY da.UF
order by 2 desc
LIMIT  10;

---- Total de Assentos Vendidos por rota

SELECT 
	da_origem.oaci || '-' || da_destino.oaci  , 
	SUM(ft.ASSENTOS) as total_passageiros
from read_csv('/home/rodrigo/Documentos/projetos/assistente_ia_sql_passagens_aereas/banco/fato.csv') ft
INNER JOIN main.dim_aeroporto da_destino on da_destino.oaci = ft.DESTINO
INNER JOIN main.dim_aeroporto da_origem on da_origem.oaci = ft.ORIGEM
WHERE ft.ANO = 2023
AND ft.MES = 2
AND ft.EMPRESA = 'GLO'
GROUP BY da_origem.oaci || '-' || da_destino.oaci
order by 2 desc
LIMIT  10;


SELECT 
	ft.ANO , 
	ft.MES  , 
	SUM(ft.ASSENTOS) as total_passageiros
from read_csv('/home/rodrigo/Documentos/projetos/assistente_ia_sql_passagens_aereas/banco/fato.csv') ft
INNER JOIN main.dim_aeroporto da_destino on da_destino.oaci = ft.DESTINO
INNER JOIN main.dim_aeroporto da_origem on da_origem.oaci = ft.ORIGEM
WHERE  ft.EMPRESA = 'TAM'
AND ANO = 2023
AND da_origem.oaci || '-' || da_destino.oaci = 'SBRJ-SBSP'
GROUP BY ft.ANO , ft.MES 
order by 2 ASC ;


SELECT 
	ft.ANO , 
	ft.MES, 
	SUM(ft.ASSENTOS) as total_passageiros
from read_csv('/home/rodrigo/Documentos/projetos/assistente_ia_sql_passagens_aereas/banco/fato.csv') ft
INNER JOIN main.dim_aeroporto da_destino on da_destino.oaci = ft.DESTINO
INNER JOIN main.dim_aeroporto da_origem on da_origem.oaci = ft.ORIGEM
WHERE  ft.EMPRESA = 'GLO'
AND ANO = 2023
AND da_origem.oaci || '-' || da_destino.oaci = 'SBRJ-SBSP'
GROUP BY ft.ANO , ft.MES 
order by 2 ASC ;


---- Taxa de Crescimento de Assentos Vendidos



WITH cte_passageiros AS (
    SELECT 
        ft.ANO, 
        ft.MES, 
        SUM(ft.ASSENTOS) AS total_passageiros
    FROM read_csv('/home/rodrigo/Documentos/projetos/assistente_ia_sql_passagens_aereas/banco/fato.csv') ft
    INNER JOIN main.dim_aeroporto da_destino ON da_destino.oaci = ft.DESTINO
    INNER JOIN main.dim_aeroporto da_origem ON da_origem.oaci = ft.ORIGEM
    WHERE ft.EMPRESA = 'GLO'
      AND ANO = 2023
      AND da_origem.oaci || '-' || da_destino.oaci = 'SBRJ-SBSP'
    GROUP BY ft.ANO, ft.MES
)
SELECT 
    ANO,
    MES,
    total_passageiros,
    LAG(total_passageiros) OVER (PARTITION BY ANO ORDER BY MES) AS total_passageiros_mes_anterior,
  ROUND(((  total_passageiros - LAG(total_passageiros) OVER (PARTITION BY ANO ORDER BY MES)) / LAG(total_passageiros) OVER (PARTITION BY ANO ORDER BY MES) ) * 100, 2) AS TAXA_CRESCIMENTO
FROM cte_passageiros
ORDER BY MES ASC;

---- RECEITA por rota 

SELECT 
	da_origem.MUNICIPIO || '-' || da_destino.MUNICIPIO  , 
	ROUND(SUM(ft.TARIFA * FT.ASSENTOS), 2) as total_passageiros
from read_csv('/home/rodrigo/Documentos/projetos/assistente_ia_sql_passagens_aereas/banco/fato.csv') ft
INNER JOIN main.dim_aeroporto da_destino on da_destino.oaci = ft.DESTINO
INNER JOIN main.dim_aeroporto da_origem on da_origem.oaci = ft.ORIGEM
WHERE ft.ANO = 2023
AND ft.MES = 2
AND ft.EMPRESA = 'GLO'
GROUP BY da_origem.MUNICIPIO || '-' || da_destino.MUNICIPIO 
order by 2 desc
LIMIT  10;


SELECT   
	ft.ANO, 
    ft.MES,  
    ROUND(SUM(ft.TARIFA * FT.ASSENTOS), 2) as total_passageiros
from read_csv('/home/rodrigo/Documentos/projetos/assistente_ia_sql_passagens_aereas/banco/fato.csv') ft
INNER JOIN main.dim_aeroporto da_destino on da_destino.oaci = ft.DESTINO
INNER JOIN main.dim_aeroporto da_origem on da_origem.oaci = ft.ORIGEM
WHERE ft.ANO = 2023
AND ft.EMPRESA = 'GLO'
AND da_origem.oaci || '-' || da_destino.oaci = 'SBRJ-SBSP'
GROUP BY ft.ANO, FT.MES
order by 2 ASC
;


---------------
Análise de Retorno

Definição: Identificar rotas onde os voos de ida e volta têm padrões distintos de vendas ou tarifas.
Exemplo: Comparar as vendas entre GRU-JFK e JFK-GRU.



-----------Faturamento por mês

SELECT 
        ft.ANO,
        ft.MES,
        ROUND(SUM(ft.TARIFA * ft.ASSENTOS), 2) AS total_passageiros
    FROM 
        read_csv('/home/rodrigo/Documentos/projetos/assistente_ia_sql_passagens_aereas/banco/fato.csv') ft
    INNER JOIN 
        main.dim_aeroporto da_destino ON da_destino.oaci = ft.DESTINO
    INNER JOIN 
        main.dim_aeroporto da_origem ON da_origem.oaci = ft.ORIGEM
    WHERE  
        ft.EMPRESA = 'GLO'
        AND ft.ANO IN (2023, 2024) -- Inclui dados de ambos os anos
        AND da_origem.oaci || '-' || da_destino.oaci = 'SBRJ-SBSP'
    GROUP BY 
        ft.ANO, ft.MES 
     ORDER BY 1, 2

----------Faturamento acumulado Atual X período anterior

WITH faturamento_mensal AS (
    SELECT 
        ft.ANO,
        ft.MES,
        ROUND(SUM(ft.TARIFA * ft.ASSENTOS), 2) AS total_passageiros
    FROM 
        read_csv('/home/rodrigo/Documentos/projetos/assistente_ia_sql_passagens_aereas/banco/fato.csv') ft
    INNER JOIN 
        main.dim_aeroporto da_destino ON da_destino.oaci = ft.DESTINO
    INNER JOIN 
        main.dim_aeroporto da_origem ON da_origem.oaci = ft.ORIGEM
    WHERE  
        ft.EMPRESA = 'GLO'
        AND ft.ANO IN (2023, 2024) -- Inclui dados de ambos os anos
        AND da_origem.oaci || '-' || da_destino.oaci = 'SBRJ-SBSP'
    GROUP BY 
        ft.ANO, ft.MES
)
SELECT 
    ANO,
    MES,
    total_passageiros,
    ROUND(SUM(total_passageiros) OVER (PARTITION BY ANO ORDER BY MES ASC), 2) AS faturamento_acumulado -- Calcula acumulado por ano
FROM 
    faturamento_mensal
ORDER BY 
    ANO ASC, MES ASC;

-----------Participação de Mercado por Origem/Destino

Definição: Percentual de vendas de uma rota em relação ao total de vendas em todos os destinos.
Exemplo: GRU-JFK representa 20% das vendas totais do aeroporto de GRU.

SELECT   
	
    da_origem.MUNICIPIO || '-' || da_destino.MUNICIPIO ,
    ROUND(SUM(ft.TARIFA * FT.ASSENTOS), 2) as total_passageiros,
    ROUND(SUM(SUM(ft.TARIFA * FT.ASSENTOS)) OVER (), 2) AS total_mes
from read_csv('/home/rodrigo/Documentos/projetos/assistente_ia_sql_passagens_aereas/banco/fato.csv') ft
INNER JOIN main.dim_aeroporto da_destino on da_destino.oaci = ft.DESTINO
INNER JOIN main.dim_aeroporto da_origem on da_origem.oaci = ft.ORIGEM
WHERE ft.ANO = 2023
AND ft.MES = 1
AND ft.EMPRESA = 'GLO'

GROUP BY da_origem.MUNICIPIO || '-' || da_destino.MUNICIPIO
order by 2 DESC 
;

SELECT   
    da_origem.MUNICIPIO || '-' || da_destino.MUNICIPIO AS rota,
    ROUND(SUM(ft.TARIFA * FT.ASSENTOS), 2) AS FATURAMENTO,
	ROUND(SUM(SUM(ft.TARIFA * FT.ASSENTOS)) OVER (), 2) AS total_mes,
    ROUND((SUM(ft.TARIFA * FT.ASSENTOS)  * 100) / ROUND(SUM(SUM(ft.TARIFA * FT.ASSENTOS)) OVER (), 2), 3)  as porcentagem_participacao
FROM read_csv('/home/rodrigo/Documentos/projetos/assistente_ia_sql_passagens_aereas/banco/fato.csv') ft
INNER JOIN main.dim_aeroporto da_destino ON da_destino.oaci = ft.DESTINO
INNER JOIN main.dim_aeroporto da_origem ON da_origem.oaci = ft.ORIGEM
WHERE ft.ANO = 2023
AND ft.MES = 2
AND ft.EMPRESA = 'AZU'
GROUP BY  da_origem.MUNICIPIO || '-' || da_destino.MUNICIPIO
ORDER BY 4 DESC;

