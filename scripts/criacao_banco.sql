CREATE TABLE dim_empresas (
    ICAO VARCHAR(6) PRIMARY KEY,
    IATA VARCHAR(3),
    NOME_EMPRESA TEXT
);

CREATE TABLE dim_aeroporto (
    OACI VARCHAR(4) PRIMARY KEY,
    NOME TEXT,
    MUNICIPIO TEXT,
    UF TEXT
);


ALTER TABLE dim_aeroporto
ADD CONSTRAINT pk_dim_aeroporto PRIMARY KEY (OACI);

SELECT *
FROM  dim;


CREATE TABLE dim_data (
    ano_mes VARCHAR(8) PRIMARY KEY,
    ano INT,
    mes INT,
    nome_mes VARCHAR(15)
);

CREATE TABLE ft_venda_passagem (
    ano_mes VARCHAR(8) ,
    oaci_origem VARCHAR(4),
    oaci_destino VARCHAR(4),
    ICAO VARCHAR(6),
    tarifa REAL,
    assentos INT,

    FOREIGN KEY (ano_mes) REFERENCES dim_data(ano_mes) ,
    FOREIGN KEY (oaci_origem) REFERENCES dim_aeroporto(OACI) ,
    FOREIGN KEY (oaci_destino) REFERENCES dim_aeroporto(OACI),
    FOREIGN KEY (ICAO) REFERENCES dim_empresas(ICAO)
);


SELECT *
FROM dim_aeroporto da 
where da.UF  = 'PA';

TRUNCATE TABLE dim_aeroporto;

INSERT INTO dim_aeroporto
values ('SBFE', 'Aeroporto de Sobral - Coronel Virgílio Távora', 'Sobral', 'CE', '-3.6808775', '-40.3432025', 1)


INSERT INTO dim_data

 SELECT * 
 FROM read_csv_auto('/home/rodrigo/Documentos/projetos/assistente_ia_sql_passagens_aereas/docs/dim_data_202411282124_depara_video.csv')


INSERT INTO dim_aeroporto

SELECT 
	CodigoOACI as OACI, Nome as NOME, Município AS MUNICIPIO, UF, null as latitude, null as longitude, null as tipo_aeroporto
FROM read_csv('/home/rodrigo/Documentos/projetos/assistente_ia_sql_passagens_aereas/docs/dimaeroporto.csv')
WHERE  CodigoOACI = 'SDZG'



INSERT INTO dim_empresas

 SELECT * 
 FROM read_csv_auto('/home/rodrigo/Documentos/projetos/assistente_ia_sql_passagens_aereas/docs/dim_empresas_202411282124_depara_video.csv')


SELECT COUNT(*) 
from ft_venda_passagem

 SELECT 
*
 FROM read_csv_auto('/home/rodrigo/Documentos/projetos/assistente_ia_sql_passagens_aereas/docs/fato.csv');


INSERT INTO ft_venda_passagem
 SELECT 
 	ano_mes ,  origem as oaci_origem, destino as oaci_destino, empresa as icao, tarifa, assentos
 FROM read_csv_auto('/home/rodrigo/Documentos/projetos/assistente_ia_sql_passagens_aereas/docs/fato.csv')
where ano_mes = '2024-10'
and icao = 'AZU'
AND oaci_origem = 'SBAE'

SELECT 
 	DISTINCT  ORIGEM
 FROM read_csv_auto('/home/rodrigo/Documentos/projetos/assistente_ia_sql_passagens_aereas/docs/fato.csv')
where  origem NOT IN (
	SELECT oaci
	FROM dim_aeroporto
)


SELECT 
 	DISTINCT  DESTINO
 FROM read_csv_auto('/home/rodrigo/Documentos/projetos/assistente_ia_sql_passagens_aereas/docs/fato.csv')
where  origem NOT IN (
	SELECT oaci
	FROM dim_aeroporto
)


 
 
 INSERT INTO ft_venda_passagem
SELECT 
    ano_mes,
    origem AS oaci_origem,
    destino AS oaci_destino,
    empresa AS icao,
    tarifa,
    assentos
FROM TRY(read_csv_auto('/home/rodrigo/Documentos/projetos/assistente_ia_sql_passagens_aereas/docs/fato.csv'))


SELECT * 
FROM read_csv('/home/rodrigo/Documentos/projetos/assistente_ia_sql_passagens_aereas/docs/aeroportos/AerodromosPublicos_utf8.csv', 
              delim=';',
              header=TRUE);


 
  2023-1;2023;1;ABJ;SBSV;SIRI;650,0;17






