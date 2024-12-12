SELECT *
from dim_aeroporto ;

SELECT *
from main.dim_empresas e
where e.ICAO  IN (
	'GLO',
	'AZU',
	'TAM',
	'PTB',
	'ABJ',
	'CQB'
);

SELECT *
from main.ft_venda_passagem fvp ;

/*
	CQB-APUÍ TÁXI AÉREO S/A
	ABJ-ATA AEROTÁXI ABAETÉ LTDA.
	AZU-AZUL LINHAS AÉREAS BRASILEIRAS S/A
	GLO-GOL LINHAS AÉREAS S.A. (EX- VRG LINHAS AÉREAS S.A.)
	PTB-PASSAREDO TRANSPORTES AÉREOS S.A.
	TAM-TAM LINHAS AÉREAS S.A.
 */

SELECT DISTINCT EMPRESA
from read_csv('/home/rodrigo/Documentos/projetos/assistente_ia_sql_passagens_aereas/banco/fato.csv') ft
WHERE ft.ANO = 2023
AND ft.MES = 1
AND ft.EMPRESA = 'GLO';
--Destinos mais procurados no mês
--- Geral 1
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

--- são paulo 2
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

--- Total passageiros por estado 3

SELECT 
	da.UF, 
	SUM(ft.ASSENTOS) as total_passageiros
from read_csv('/home/rodrigo/Documentos/projetos/assistente_ia_sql_passagens_aereas/banco/fato.csv') ft
INNER JOIN main.dim_aeroporto da on da.oaci = ft.DESTINO
WHERE ft.ANO = 2023
AND ft.MES = 2
AND ft.EMPRESA = 'GLO'
GROUP BY da.UF
order by 2 desc;


--- Variação de procura de destino em relação ao mês anterior  4

SELECT 
    ft.MES,
    SUM(ft.ASSENTOS) AS total_passageiros,
    ROUND(
        (SUM(ft.ASSENTOS) - LAG(SUM(ft.ASSENTOS)) OVER (ORDER BY ft.MES ASC)) 
        / NULLIF(LAG(SUM(ft.ASSENTOS)) OVER (ORDER BY ft.MES ASC), 0) * 100, 
        2
    ) AS variacao_percentual
FROM read_csv('/home/rodrigo/Documentos/projetos/assistente_ia_sql_passagens_aereas/banco/fato.csv') ft
INNER JOIN main.dim_aeroporto da 
    ON da.oaci = ft.DESTINO
WHERE ft.ANO = 2023
AND ft.EMPRESA = 'GLO'
AND da.MUNICIPIO = 'SÃO PAULO'
GROUP BY ft.MES
ORDER BY ft.MES ASC;

select DISTINCT  MUNICIPIO || '-' || UF as MUNICIPIO 
from main.dim_aeroporto 


===============================================
-- Total de Assentos Vendidos por rota
---  ROTA GERAL 1
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

 -- Período por rota 2
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

--- Taxa de Crescimento de Assentos Vendidos 3

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
============================================

-- Faturamento
--- Faturamento por rota  1

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

--- Faturamento Período E rota 2
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
order by 2 ASC;

--- Faturamento por mês 3

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
     ORDER BY 1, 2 -- Até aqui tabs 

--- Faturamento acumulado Atual X período anterior --4

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
   
   
   
--- Receita por destino 

SELECT   
    da_destino.MUNICIPIO AS rota,
    ROUND(SUM(ft.TARIFA * FT.ASSENTOS), 2) AS FATURAMENTO
FROM read_csv('/home/rodrigo/Documentos/projetos/assistente_ia_sql_passagens_aereas/banco/fato.csv') ft
INNER JOIN main.dim_aeroporto da_destino ON da_destino.oaci = ft.DESTINO
WHERE ft.ANO = 2023
AND ft.MES = 2
AND ft.EMPRESA = 'AZU'
GROUP BY  da_destino.MUNICIPIO
ORDER BY 2 DESC;

--- Receita por origem
SELECT   
    da_origem.MUNICIPIO AS rota,
    ROUND(SUM(ft.TARIFA * FT.ASSENTOS), 2) AS FATURAMENTO
FROM read_csv('/home/rodrigo/Documentos/projetos/assistente_ia_sql_passagens_aereas/banco/fato.csv') ft
INNER JOIN main.dim_aeroporto da_origem ON da_origem.oaci = ft.ORIGEM
WHERE ft.ANO = 2023
AND ft.MES = 2
AND ft.EMPRESA = 'AZU'
GROUP BY  da_origem.MUNICIPIO
ORDER BY 2 DESC;
=============================================================================

-- Participação de Mercado por Origem/Destino


--- Geral 

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
--- 
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




