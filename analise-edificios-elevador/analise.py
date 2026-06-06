# -*- coding: utf-8 -*-
"""
Analise de edificios para midia de elevador — Buzzmonitor Brasil.

Abordagem BOTTOM-UP (decisao do usuario):
  1. Coletar empresas do ecossistema de marketing COM endereco (web + diretorios + CRM)
  2. VALIDAR na fonte oficial (Receita/BrasilAPI via MCP Brasil): situacao, endereco, CNAE, porte
  3. Clusterizar por endereco (mesma rua+numero = mesmo edificio)
  4. Pontuar e ranquear edificios pela densidade/qualidade de ICP
  5. (depois) midia de elevador + attribution

Confianca:
  oficial  = CNPJ verificado ATIVO na Receita, no eixo-alvo (endereco operacional confere)
  fonte    = endereco confirmado por fonte web real (site/Maps/diretorio), sem CNPJ validado
  baixada  = CNPJ existe mas situacao BAIXADA (entidade juridica encerrada/consolidada)

Saida: console + analise-edificios-elevador/edificios_buzzmonitor.xlsx
"""
import unicodedata
import re
import pandas as pd

# =====================================================================================
# DATASET CURADO — cada registro foi vetado (oficial = validado na Receita nesta sessao)
# Campos: empresa, grupo, tipo, logradouro, numero, bairro, regiao, edificio,
#         cnpj, situacao, cnae, porte, func_est, fonte, confianca, coworking
# regiao ∈ {faria_lima, itaim, berrini, paulista, vila_olimpia, pinheiros, fora}
# =====================================================================================
R = []
def add(**k): R.append(k)

# ---------- FARIA LIMA (corredor) ----------
add(empresa="Africa DDB (Africa Creative)", grupo="Omnicom/DDB", tipo="agencia_pub",
    logradouro="Av. Brigadeiro Faria Lima", numero="3477", bairro="Itaim Bibi", regiao="faria_lima",
    edificio="Patio Victor Malzoni", cnpj="60741303000197", situacao="ATIVA", cnae="7311-4/00 Ag. publicidade",
    porte="grande", func_est=250, fonte="Receita/BrasilAPI; africacreative.com.br", confianca="oficial", coworking=0)
add(empresa="Google Brasil", grupo="Alphabet", tipo="marca_inhouse",
    logradouro="Av. Brigadeiro Faria Lima", numero="3477", bairro="Itaim Bibi", regiao="faria_lima",
    edificio="Patio Victor Malzoni", cnpj="06990590000123", situacao="ATIVA", cnae="6319-4/00 Portais/internet",
    porte="grande", func_est=1000, fonte="Receita/BrasilAPI; about.google", confianca="oficial", coworking=0)
add(empresa="Dentsu Creative", grupo="Dentsu", tipo="agencia_pub",
    logradouro="Av. Brigadeiro Faria Lima", numero="949", bairro="Pinheiros", regiao="faria_lima",
    edificio="Faria Lima Plaza", cnpj="06275469000110", situacao="ATIVA", cnae="7311-4/00 Ag. publicidade",
    porte="grande", func_est=200, fonte="Receita/BrasilAPI; dentsu.com/br", confianca="oficial", coworking=0)
add(empresa="iProspect (Dentsu)", grupo="Dentsu", tipo="agencia_digital",
    logradouro="Av. Brigadeiro Faria Lima", numero="949", bairro="Pinheiros", regiao="faria_lima",
    edificio="Faria Lima Plaza", cnpj="09686917000166", situacao="ATIVA", cnae="7311-4/00 Ag. publicidade",
    porte="media", func_est=120, fonte="Receita/BrasilAPI", confianca="oficial", coworking=0)
add(empresa="Uber do Brasil", grupo="Uber", tipo="marca_inhouse",
    logradouro="Av. Brigadeiro Faria Lima", numero="949", bairro="Pinheiros", regiao="faria_lima",
    edificio="Faria Lima Plaza", cnpj="17895646000187", situacao="ATIVA", cnae="7490-1/04 Agenc. negocios",
    porte="grande", func_est=700, fonte="Receita/BrasilAPI; uber.com newsroom", confianca="oficial", coworking=0)
add(empresa="Shopee (Marketplace Shopee)", grupo="Sea", tipo="marca_inhouse",
    logradouro="Av. Brigadeiro Faria Lima", numero="3732", bairro="Itaim Bibi", regiao="faria_lima",
    edificio="Birmann 32", cnpj="57981711000101", situacao="ATIVA", cnae="7490-1/04 Agenc. negocios",
    porte="grande", func_est=1500, fonte="Receita/BrasilAPI; shopee blog", confianca="oficial", coworking=0)
add(empresa="Meta (Facebook) Brasil", grupo="Meta", tipo="marca_inhouse",
    logradouro="Av. Brigadeiro Faria Lima", numero="3732", bairro="Itaim Bibi", regiao="faria_lima",
    edificio="Birmann 32", cnpj="", situacao="—", cnae="—",
    porte="grande", func_est=1000, fonte="Foursquare; CBRE Birmann 32", confianca="fonte", coworking=0)
add(empresa="Stone", grupo="Stone", tipo="martech",
    logradouro="Av. Brigadeiro Faria Lima", numero="3064", bairro="Jardim Paulistano", regiao="faria_lima",
    edificio="Faria Lima (3064)", cnpj="16501555001048", situacao="ATIVA", cnae="6619-3/99 Aux. financeiro",
    porte="grande", func_est=1000, fonte="Receita/BrasilAPI", confianca="fonte", coworking=0)
add(empresa="RD Station", grupo="TOTVS", tipo="martech",
    logradouro="Av. Brigadeiro Faria Lima", numero="2055", bairro="Jardim Paulistano", regiao="faria_lima",
    edificio="Faria Lima (2055)", cnpj="", situacao="—", cnae="—",
    porte="media", func_est=300, fonte="rdstation.com/contato", confianca="fonte", coworking=0)
add(empresa="Suno United Creators", grupo="Suno", tipo="marca_inhouse",
    logradouro="Av. Brigadeiro Faria Lima", numero="1355", bairro="Jardim Paulistano", regiao="faria_lima",
    edificio="Faria Lima (1355)", cnpj="", situacao="—", cnae="—",
    porte="media", func_est=150, fonte="guiafacil", confianca="fonte", coworking=0)
# coworkings Faria Lima
add(empresa="WeWork Faria Lima 3729", grupo="WeWork", tipo="coworking",
    logradouro="Av. Brigadeiro Faria Lima", numero="3729", bairro="Itaim Bibi", regiao="faria_lima",
    edificio="WeWork 3729", cnpj="", situacao="—", cnae="—",
    porte="grande", func_est=300, fonte="wework.com", confianca="fonte", coworking=1)
add(empresa="WeWork Faria Lima 4055", grupo="WeWork", tipo="coworking",
    logradouro="Av. Brigadeiro Faria Lima", numero="4055", bairro="Itaim Bibi", regiao="faria_lima",
    edificio="WeWork 4055", cnpj="", situacao="—", cnae="—",
    porte="grande", func_est=300, fonte="wework.com", confianca="fonte", coworking=1)

# ---------- ITAIM / EIXO AV. JK ----------
add(empresa="WMcCann (McCann Erickson)", grupo="WPP/McCann", tipo="agencia_pub",
    logradouro="Av. Presidente Juscelino Kubitschek", numero="1909", bairro="V. Nova Conceicao/Itaim", regiao="itaim",
    edificio="JK 1909 (Torres)", cnpj="61416384000112", situacao="ATIVA", cnae="7311-4/00 Ag. publicidade",
    porte="grande", func_est=350, fonte="Receita/BrasilAPI; wmccann.com", confianca="oficial", coworking=0)
add(empresa="Espalhe MSL", grupo="Publicis", tipo="agencia_digital",
    logradouro="Av. Presidente Juscelino Kubitschek", numero="1909", bairro="V. Nova Conceicao/Itaim", regiao="itaim",
    edificio="JK 1909 (Torres)", cnpj="", situacao="—", cnae="—",
    porte="media", func_est=100, fonte="meioemensagem", confianca="fonte", coworking=0)
add(empresa="FSB Comunicacao", grupo="FSB", tipo="pr",
    logradouro="Av. Presidente Juscelino Kubitschek", numero="1400", bairro="V. Nova Conceicao/Itaim", regiao="itaim",
    edificio="JK 1400", cnpj="07148569000148", situacao="ATIVA", cnae="6204-0/00 Consultoria TI",
    porte="grande", func_est=200, fonte="Receita/BrasilAPI; fsb.com.br", confianca="oficial", coworking=0)
add(empresa="Adman Adtech Brasil", grupo="Adman", tipo="martech",
    logradouro="Rua Dr. Renato Paes de Barros", numero="33", bairro="Itaim Bibi", regiao="itaim",
    edificio="R. Renato Paes de Barros 33", cnpj="51915801000118", situacao="ATIVA", cnae="6201-5/01 Software",
    porte="pequena", func_est=30, fonte="Receita/BrasilAPI", confianca="oficial", coworking=0)
add(empresa="Fischer America (Fe/St)", grupo="Fischer", tipo="agencia_pub",
    logradouro="Rua Leopoldo Couto de Magalhaes Jr.", numero="758", bairro="Itaim Bibi", regiao="itaim",
    edificio="Leopoldo Couto 758", cnpj="", situacao="—", cnae="—",
    porte="media", func_est=120, fonte="apontador/foursquare", confianca="fonte", coworking=0)
add(empresa="Social Tailors", grupo="—", tipo="social",
    logradouro="Rua Tabapua", numero="82", bairro="Itaim Bibi", regiao="itaim",
    edificio="Tabapua 82", cnpj="", situacao="—", cnae="—",
    porte="pequena", func_est=25, fonte="socialtailors.com", confianca="fonte", coworking=0)
add(empresa="LEN Comunicacao e Branding", grupo="—", tipo="branding",
    logradouro="Rua Tabapua", numero="81", bairro="Itaim Bibi", regiao="itaim",
    edificio="Tabapua 81", cnpj="", situacao="—", cnae="—",
    porte="pequena", func_est=20, fonte="benditoguia/len.com.br", confianca="fonte", coworking=0)
add(empresa="TORO Comunicacao", grupo="—", tipo="agencia_pub",
    logradouro="Rua Urussui", numero="92", bairro="Itaim Bibi", regiao="itaim",
    edificio="Capital Offices (Urussui 92)", cnpj="", situacao="—", cnae="—",
    porte="media", func_est=60, fonte="brasilios.com", confianca="fonte", coworking=0)
add(empresa="Dois Pontos Comunicacao", grupo="—", tipo="agencia_pub",
    logradouro="Rua Urussui", numero="92", bairro="Itaim Bibi", regiao="itaim",
    edificio="Capital Offices (Urussui 92)", cnpj="", situacao="—", cnae="—",
    porte="media", func_est=50, fonte="encontraitaim.com.br", confianca="fonte", coworking=0)
add(empresa="Raca Marketing & Comunicacao", grupo="—", tipo="agencia_pub",
    logradouro="Rua Viradouro", numero="63", bairro="Itaim Bibi", regiao="itaim",
    edificio="Viradouro 63 (COW)", cnpj="", situacao="—", cnae="—",
    porte="media", func_est=60, fonte="raca.marketing", confianca="fonte", coworking=0)
add(empresa="COW Workspaces (Viradouro 63)", grupo="COW", tipo="coworking",
    logradouro="Rua Viradouro", numero="63", bairro="Itaim Bibi", regiao="itaim",
    edificio="Viradouro 63 (COW)", cnpj="", situacao="—", cnae="—",
    porte="grande", func_est=200, fonte="cowworkspaces.com.br", confianca="fonte", coworking=1)

# ---------- VILA OLIMPIA / PINHEIROS ----------
add(empresa="CP+B Brasil", grupo="Publicis", tipo="agencia_pub",
    logradouro="Alameda Vicente Pinzon", numero="51", bairro="Vila Olimpia", regiao="vila_olimpia",
    edificio="Vicente Pinzon 51", cnpj="13503980000197", situacao="ATIVA", cnae="7311-4/00 Ag. publicidade",
    porte="media", func_est=120, fonte="Receita/BrasilAPI; cpbbrasil.com.br", confianca="oficial", coworking=0)
add(empresa="Cubo Itau", grupo="Itau", tipo="coworking",
    logradouro="Alameda Vicente Pinzon", numero="54", bairro="Vila Olimpia", regiao="vila_olimpia",
    edificio="Cubo Itau (Vicente Pinzon 54)", cnpj="42267898000109", situacao="ATIVA", cnae="9499-5/00 Assoc.",
    porte="grande", func_est=500, fonte="Receita/BrasilAPI; cubo.network", confianca="oficial", coworking=1)
add(empresa="Gotcha Comunicacao", grupo="—", tipo="agencia_pub",
    logradouro="Rua Gomes de Carvalho", numero="1195", bairro="Vila Olimpia", regiao="vila_olimpia",
    edificio="Gomes de Carvalho 1195", cnpj="11388985000271", situacao="ATIVA", cnae="7311-4/00 Ag. publicidade",
    porte="media", func_est=80, fonte="Receita/BrasilAPI; gotcha.com.br", confianca="oficial", coworking=0)
add(empresa="Ole Brasil Publicidade", grupo="—", tipo="agencia_pub",
    logradouro="Rua Gomes de Carvalho", numero="911", bairro="Vila Olimpia", regiao="vila_olimpia",
    edificio="Gomes de Carvalho 911", cnpj="", situacao="—", cnae="—",
    porte="media", func_est=40, fonte="olebrasil.com.br", confianca="fonte", coworking=0)
add(empresa="Public Midia", grupo="—", tipo="agencia_digital",
    logradouro="Rua Gomes de Carvalho", numero="911", bairro="Vila Olimpia", regiao="vila_olimpia",
    edificio="Gomes de Carvalho 911", cnpj="", situacao="—", cnae="—",
    porte="pequena", func_est=15, fonte="agenciapublicmidia.com", confianca="fonte", coworking=0)
add(empresa="True Agency", grupo="—", tipo="agencia_pub",
    logradouro="Rua Funchal", numero="538", bairro="Vila Olimpia", regiao="vila_olimpia",
    edificio="Funchal 538", cnpj="", situacao="—", cnae="—",
    porte="media", func_est=40, fonte="trueagency.com.br", confianca="fonte", coworking=0)
add(empresa="Mestica Propaganda", grupo="—", tipo="agencia_pub",
    logradouro="Rua Funchal", numero="538", bairro="Vila Olimpia", regiao="vila_olimpia",
    edificio="Funchal 538", cnpj="", situacao="—", cnae="—",
    porte="pequena", func_est=12, fonte="meioemensagem", confianca="fonte", coworking=0)
add(empresa="Lola/TBWA (Lew'Lara)", grupo="Omnicom/TBWA", tipo="agencia_pub",
    logradouro="Rua Eugenio de Medeiros", numero="303", bairro="Pinheiros", regiao="pinheiros",
    edificio="WTorre / Eugenio de Medeiros 303", cnpj="09251692000115", situacao="ATIVA", cnae="7311-4/00 Ag. publicidade",
    porte="grande", func_est=200, fonte="Receita/BrasilAPI; lewlaratbwa.com.br", confianca="oficial", coworking=0)
add(empresa="David Brasil", grupo="Globo/David", tipo="agencia_pub",
    logradouro="Rua Pedroso de Morais", numero="1553", bairro="Pinheiros", regiao="pinheiros",
    edificio="Pedroso de Morais 1553", cnpj="10969880000162", situacao="ATIVA", cnae="7311-4/00 Ag. publicidade",
    porte="media", func_est=130, fonte="Receita/BrasilAPI", confianca="oficial", coworking=0)
add(empresa="GUT Sao Paulo", grupo="GUT", tipo="agencia_pub",
    logradouro="Rua Natingui", numero="862", bairro="Vila Madalena (Pinheiros)", regiao="pinheiros",
    edificio="Natingui 862", cnpj="29327911000100", situacao="ATIVA", cnae="7311-4/00 Ag. publicidade",
    porte="grande", func_est=120, fonte="Receita/BrasilAPI; gut.agency", confianca="oficial", coworking=0)
add(empresa="Galeria Estrategia e Comunicacao", grupo="—", tipo="agencia_pub",
    logradouro="Rua Mourato Coelho", numero="1404", bairro="Vila Madalena (Pinheiros)", regiao="pinheiros",
    edificio="Lab 1404 (Mourato Coelho 1404)", cnpj="42632634000107", situacao="ATIVA", cnae="7311-4/00 Ag. publicidade",
    porte="media", func_est=80, fonte="Receita/BrasilAPI; galeria.ag", confianca="oficial", coworking=0)
add(empresa="V2BMKT", grupo="—", tipo="agencia_digital",
    logradouro="Av. Brigadeiro Faria Lima", numero="2369", bairro="Pinheiros", regiao="pinheiros",
    edificio="Faria Lima 2369", cnpj="", situacao="—", cnae="—",
    porte="media", func_est=35, fonte="v2bmkt.com.br", confianca="fonte", coworking=0)

# ---------- BERRINI / BROOKLIN / CIDADE MONCOES ----------
add(empresa="DPZ Comunicacoes", grupo="Publicis (DPZ&T)", tipo="agencia_pub",
    logradouro="Rua Sansao Alves dos Santos", numero="400", bairro="Cidade Moncoes (Berrini)", regiao="berrini",
    edificio="Predio Grupo Publicis (Sansao A. Santos 400)", cnpj="73163529000108", situacao="ATIVA", cnae="7311-4/00 Ag. publicidade",
    porte="grande", func_est=200, fonte="Receita/BrasilAPI", confianca="oficial", coworking=0)
add(empresa="Publicis Brasil Comunicacao", grupo="Publicis", tipo="agencia_pub",
    logradouro="Rua Sansao Alves dos Santos", numero="400", bairro="Cidade Moncoes (Berrini)", regiao="berrini",
    edificio="Predio Grupo Publicis (Sansao A. Santos 400)", cnpj="74561580000122", situacao="BAIXADA", cnae="7311-4/00 Ag. publicidade",
    porte="grande", func_est=300, fonte="Receita/BrasilAPI (entidade baixada; grupo no local)", confianca="baixada", coworking=0)
add(empresa="The Group Comunicacao", grupo="—", tipo="agencia_pub",
    logradouro="Av. Eng. Luis Carlos Berrini", numero="1700", bairro="Cidade Moncoes (Berrini)", regiao="berrini",
    edificio="Berrini 1700", cnpj="00632911000131", situacao="ATIVA", cnae="7311-4/00 Ag. publicidade",
    porte="media", func_est=60, fonte="Receita/BrasilAPI; group.com.br", confianca="oficial", coworking=0)
add(empresa="Arabella Agencia de Publicidade", grupo="—", tipo="agencia_pub",
    logradouro="Av. Eng. Luis Carlos Berrini", numero="1461", bairro="Cidade Moncoes (Berrini)", regiao="berrini",
    edificio="Berrini 1461", cnpj="20086728000195", situacao="ATIVA", cnae="7311-4/00 Ag. publicidade",
    porte="pequena", func_est=25, fonte="Receita/BrasilAPI", confianca="oficial", coworking=0)
add(empresa="OUTMarketing Brasil", grupo="—", tipo="agencia_digital",
    logradouro="Av. das Nacoes Unidas", numero="12495", bairro="Brooklin", regiao="berrini",
    edificio="Nacoes Unidas 12495", cnpj="16640723000195", situacao="ATIVA", cnae="7319-0/03 Marketing direto",
    porte="media", func_est=35, fonte="Receita/BrasilAPI; outmarketing.com.br", confianca="oficial", coworking=0)
add(empresa="Daxx Omnimedia", grupo="—", tipo="agencia_pub",
    logradouro="Av. Nova Independencia", numero="87", bairro="Brooklin", regiao="berrini",
    edificio="Nova Independencia 87", cnpj="51311386000193", situacao="ATIVA", cnae="8299-7/99 Servicos a empresas",
    porte="pequena", func_est=25, fonte="Receita/BrasilAPI; daxxomnimedia.com.br", confianca="oficial", coworking=0)
add(empresa="Agencia Mestre", grupo="—", tipo="agencia_digital",
    logradouro="Av. Eng. Luis Carlos Berrini", numero="1681", bairro="Cidade Moncoes (Berrini)", regiao="berrini",
    edificio="Berrini 1681", cnpj="", situacao="—", cnae="—",
    porte="pequena", func_est=20, fonte="agenciamestre.com", confianca="fonte", coworking=0)
add(empresa="Coworking Smart Berrini", grupo="—", tipo="coworking",
    logradouro="Av. Eng. Luis Carlos Berrini", numero="1681", bairro="Cidade Moncoes (Berrini)", regiao="berrini",
    edificio="Berrini 1681", cnpj="43085666000100", situacao="ATIVA", cnae="8211-3/00 Apoio adm.",
    porte="media", func_est=30, fonte="Receita/BrasilAPI", confianca="oficial", coworking=1)

# ---------- AV. PAULISTA (+ Consolacao adjacente) ----------
add(empresa="MullenLowe Brasil", grupo="IPG/MullenLowe", tipo="agencia_pub",
    logradouro="Rua Frei Caneca", numero="1355", bairro="Consolacao (junto a Paulista)", regiao="paulista",
    edificio="Frei Caneca 1355", cnpj="61067377000152", situacao="ATIVA", cnae="7311-4/00 Ag. publicidade",
    porte="grande", func_est=200, fonte="Receita/BrasilAPI; mullenlowe", confianca="oficial", coworking=0)
add(empresa="Shout Agencia de Publicidade", grupo="—", tipo="agencia_pub",
    logradouro="Av. Paulista", numero="509", bairro="Paraiso", regiao="paulista",
    edificio="Paulista 509", cnpj="11363879000152", situacao="ATIVA", cnae="7311-4/00 Ag. publicidade",
    porte="pequena", func_est=20, fonte="Receita/BrasilAPI; shoutpublicidade.com.br", confianca="oficial", coworking=0)
add(empresa="Agencia Atentos", grupo="—", tipo="agencia_pub",
    logradouro="Av. Paulista", numero="302", bairro="Bela Vista", regiao="paulista",
    edificio="Paulista 302", cnpj="16882481000146", situacao="ATIVA", cnae="7311-4/00 Ag. publicidade",
    porte="micro", func_est=10, fonte="Receita/BrasilAPI", confianca="oficial", coworking=0)
add(empresa="Publicidade UP", grupo="—", tipo="agencia_digital",
    logradouro="Av. Paulista", numero="1636", bairro="Bela Vista", regiao="paulista",
    edificio="Paulista 1636", cnpj="13123482000119", situacao="ATIVA", cnae="6190-6/99 (mkt/telecom)",
    porte="pequena", func_est=15, fonte="Receita/BrasilAPI; publicidadeup.com.br", confianca="oficial", coworking=0)
add(empresa="Marketing Solutions Brasil", grupo="—", tipo="agencia_digital",
    logradouro="Av. Paulista", numero="1636", bairro="Bela Vista", regiao="paulista",
    edificio="Paulista 1636", cnpj="27300241000102", situacao="ATIVA", cnae="6311-9/00 Dados/internet",
    porte="micro", func_est=8, fonte="Receita/BrasilAPI", confianca="oficial", coworking=0)
add(empresa="ZAZ Producoes", grupo="—", tipo="eventos",
    logradouro="Av. Paulista", numero="807", bairro="Bela Vista", regiao="paulista",
    edificio="Paulista 807", cnpj="18376643000108", situacao="ATIVA", cnae="8230-0/01 Eventos",
    porte="pequena", func_est=15, fonte="Receita/BrasilAPI", confianca="oficial", coworking=0)
add(empresa="Bonafides Marketing e Eventos", grupo="—", tipo="eventos",
    logradouro="Av. Paulista", numero="726", bairro="Bela Vista", regiao="paulista",
    edificio="Paulista 726", cnpj="26049851000112", situacao="ATIVA", cnae="8230-0/01 Eventos",
    porte="micro", func_est=8, fonte="Receita/BrasilAPI", confianca="oficial", coworking=0)

# ---------- FORA DO EIXO (contexto/honestidade — NAO entram no ranking) ----------
FORA = [
    dict(empresa="Ogilvy Brasil", local="Mofarrej 971, Vila Leopoldina (WPP Campus)", cnpj="61067492000127", situacao="ATIVA",
         nota="WPP consolidou agencias em Vila Leopoldina (nov/2025) — saiu do eixo"),
    dict(empresa="AlmapBBDO", local="Roque Petroni Jr 999, Morumbi", cnpj="62050174000116", situacao="ATIVA",
         nota="Morumbi Office Tower — fora das 4 regioes"),
    dict(empresa="Artplan", local="Nacoes Unidas 14401, Vila Gertrudes", cnpj="33673286000710", situacao="ATIVA",
         nota="Parque da Cidade — sul de Berrini, fora do recorte"),
    dict(empresa="Soko", local="Nacoes Unidas 14401, Vila Gertrudes", cnpj="17765422000150", situacao="ATIVA",
         nota="Parque da Cidade — fora do recorte"),
    dict(empresa="Havas Health", local="Magalhaes de Castro 4800, Cidade Jardim", cnpj="09025223000188", situacao="ATIVA",
         nota="Continental Tower — fora do recorte"),
    dict(empresa="Leo Burnett", local="Brejo Alegre 93/99, Brooklin", cnpj="61151437000110", situacao="BAIXADA",
         nota="Entidade BAIXADA (consolidacao Publicis)"),
]

# =====================================================================================
# NORMALIZACAO DE ENDERECO + CLUSTERING
# =====================================================================================
def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')

def norm_street(s):
    s = strip_accents(s).lower()
    s = re.sub(r'[.,]', ' ', s)
    # remove tipo de logradouro no inicio
    s = re.sub(r'^\s*(av(enida)?|r(ua)?|al(ameda)?|praca|travessa)\s+', ' ', s)
    # normaliza abreviacoes comuns
    repl = {
        r'\bbrig\b': 'brigadeiro', r'\beng\b': 'engenheiro', r'\bdr\b': 'doutor',
        r'\bpres\b': 'presidente', r'\bjr\b': 'junior', r'\bluis\b': 'luiz',
        r'\bj\s*k\b': 'juscelino kubitschek', r'\bjk\b': 'juscelino kubitschek',
    }
    for pat, rep in repl.items():
        s = re.sub(pat, rep, s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s

df = pd.DataFrame(R)
df['rua_norm'] = df['logradouro'].apply(norm_street)
df['chave_endereco'] = df['rua_norm'] + ' | ' + df['numero'].astype(str)

# pesos
PORTE_W = {'grande': 5.0, 'media': 3.0, 'pequena': 1.5, 'micro': 1.0}
TIPO_W = {'agencia_pub': 1.0, 'agencia_digital': 1.0, 'pr': 0.85, 'branding': 0.85,
          'social': 0.8, 'eventos': 0.6, 'martech': 0.9, 'marca_inhouse': 0.55, 'coworking': 0.0}
CONF_W = {'oficial': 1.0, 'fonte': 0.6, 'baixada': 0.15}

def porte_w(p): return PORTE_W.get(p, 1.0)

def linha_peso(row):
    if row['tipo'] == 'coworking':
        # coworking = densidade transitoria; peso fixo moderado, tratado a parte
        return 2.0 * CONF_W.get(row['confianca'], 0.6)
    return porte_w(row['porte']) * TIPO_W.get(row['tipo'], 0.7) * CONF_W.get(row['confianca'], 0.6)

df['peso'] = df.apply(linha_peso, axis=1)
df['is_agencia'] = df['tipo'].isin(['agencia_pub', 'agencia_digital']).astype(int)
df['is_oficial'] = (df['confianca'] == 'oficial').astype(int)

# Agregacao por edificio (chave_endereco)
g = df.groupby('chave_endereco')
ed = g.agg(
    edificio=('edificio', lambda x: x.mode().iat[0] if len(x.mode()) else x.iat[0]),
    regiao=('regiao', lambda x: x.mode().iat[0]),
    logradouro=('logradouro', 'first'),
    numero=('numero', 'first'),
    n_empresas=('empresa', 'count'),
    n_agencias=('is_agencia', 'sum'),
    n_oficial=('is_oficial', 'sum'),
    n_coworking=('coworking', 'sum'),
    func_est_total=('func_est', 'sum'),
    score=('peso', 'sum'),
).reset_index()

# bonus: ter >=1 ancora grande oficial e diversidade
anchor = df[(df['porte'] == 'grande') & (df['confianca'] == 'oficial') &
            (df['tipo'].isin(['agencia_pub', 'agencia_digital']))].groupby('chave_endereco').size()
ed['ancora_grande'] = ed['chave_endereco'].map(anchor).fillna(0).astype(int)
ed['score'] = ed['score'] + ed['ancora_grande'] * 1.5 + (ed['n_empresas'] >= 3) * 1.0

ed = ed.sort_values('score', ascending=False).reset_index(drop=True)
ed['rank'] = ed.index + 1

# =====================================================================================
# SAIDAS
# =====================================================================================
pd.set_option('display.width', 200)
pd.set_option('display.max_columns', 30)
pd.set_option('display.max_colwidth', 40)

print("\n================ EDIFICIOS RANQUEADOS (todos) ================")
print(ed[['rank', 'edificio', 'regiao', 'numero', 'n_empresas', 'n_agencias',
          'n_oficial', 'ancora_grande', 'func_est_total', 'score']].to_string(index=False))

print("\n================ TOP 5 (excluindo coworking-puro como #1 alternativo) ================")
top5 = ed.head(8)
print(top5[['rank', 'edificio', 'regiao', 'n_empresas', 'n_agencias', 'score']].to_string(index=False))

print("\n================ POR REGIAO (melhor edificio) ================")
for reg in ['faria_lima', 'itaim', 'berrini', 'paulista', 'vila_olimpia', 'pinheiros']:
    sub = ed[ed['regiao'] == reg].head(3)
    print(f"\n[{reg}]")
    if len(sub):
        print(sub[['rank', 'edificio', 'numero', 'n_empresas', 'n_agencias', 'score']].to_string(index=False))
    else:
        print("  (sem cluster)")

print(f"\nTotal empresas no dataset: {len(df)} | edificios distintos: {len(ed)}")
print(f"Oficiais (Receita): {int(df['is_oficial'].sum())} | fonte-web: {int((df['confianca']=='fonte').sum())} | baixadas: {int((df['confianca']=='baixada').sum())}")

# =====================================================================================
# CAMADAS DE NEGOCIO (julgamento) — Top 5 recomendado, midia, attribution, metodologia
# =====================================================================================
# nº de elevadores (proxy de ALCANCE) e status de midia (fonte: pesquisa OOH 2025-2026)
ELEVADORES = {
    'juscelino kubitschek | 1909': 27, 'brigadeiro faria lima | 3477': 23,
    'brigadeiro faria lima | 949': 11,
}
ed['elevadores_aprox'] = ed['chave_endereco'].map(ELEVADORES)

TOP5_REC = pd.DataFrame([
    dict(rank=1, edificio="Faria Lima Plaza", regiao="Faria Lima", endereco="Av. Brig. Faria Lima 949 (Pinheiros)",
         ancoras="Dentsu Creative + iProspect (grupo Dentsu) + Uber", elevadores="11",
         porque="Cluster verificado mais DENSO (3 ancoras de marketing/tech no mesmo predio). Eixo Faria Lima."),
    dict(rank=2, edificio="Patio Victor Malzoni", regiao="Faria Lima/Itaim", endereco="Av. Brig. Faria Lima 3477 (Itaim Bibi)",
         ancoras="Africa DDB (top agencia, R$61M capital) + Google Brasil", elevadores="~23",
         porque="Prestigio AAA + maior reach + agencia top-tier + grande comprador de midia (Google). Itaim/Faria Lima."),
    dict(rank=3, edificio="Sao Paulo Corporate Towers", regiao="Itaim/JK", endereco="Av. Pres. Juscelino Kubitschek 1909 (V.Nova Conceicao/Itaim)",
         ancoras="WMcCann (R$211M — uma das maiores agencias do Brasil) + Espalhe MSL", elevadores="27",
         porque="MAIOR reach do Top 5 (27 elevadores) ancorado por uma das maiores agencias do pais. Eixo Itaim/JK."),
    dict(rank=4, edificio="Edificio do Grupo Publicis", regiao="Berrini/Brooklin", endereco="Rua Sansao Alves dos Santos 400 (Cidade Moncoes)",
         ancoras="DPZ (R$67M, ativa) + Publicis Brasil (sede do grupo no local)", elevadores="confirmar",
         porque="Predio-SEDE de holding de publicidade = altissima densidade de profissionais de marketing num so endereco. Berrini/Brooklin."),
    dict(rank=5, edificio="Eixo Vila Olimpia (Vicente Pinzon 51/54)", regiao="Vila Olimpia", endereco="Al. Vicente Pinzon 51 e 54",
         ancoras="CP+B (agencia, grupo Publicis) + Cubo Itau (hub com dezenas de startups/martech)", elevadores="multiplos",
         porque="Cobre a Vila Olimpia (epicentro de agencias). Densidade via hub Cubo + ancora CP+B. Escolha de equilibrio regional."),
])

ALT_PINHEIROS = ("Alternativas fortes (Pinheiros/V.Madalena, single-anchor de peso): TBWA (Eugenio de Medeiros 303), "
                 "GUT (Natingui 862, R$20M), David (Pedroso de Morais 1553), Galeria (Mourato Coelho 1404).")
NOTA_PAULISTA = ("Av. Paulista NAO entra no Top 5: agencias dispersas e majoritariamente micro/pequenas, sem predio "
                 "concentrador. Melhor opcao na regiao: Av. Paulista 1636 (2 agencias) ou MullenLowe em Frei Caneca 1355 "
                 "(Consolacao, adjacente a Paulista).")

MIDIA = pd.DataFrame([
    dict(vendor="Eletromidia (+ Elemidia)", cobertura="~12 mil edificios comerciais no Brasil (lider). Globo assumiu controle nov/2024.",
         corporativo="SIM", contato="comercial@eletromidia.com.br | (11) 99608-8598 | self-service: aqui.eletromidia.com.br (a partir de R$194/14 dias)",
         obs="Inventario por predio NAO e publico — pedir cobertura via RFP. HQ: Leopoldo Couto Magalhaes Jr 700, Itaim."),
    dict(vendor="NOALVO", cobertura="Marketplace OOH com MAPA PUBLICO de elevadores (filtra por endereco/edificio).",
         corporativo="SIM", contato="elevadores.midianoalvo.com.br | midianoalvo.com.br (form)",
         obs="Comercial ~1.155 insercoes/mes x15s. Melhor ponto de partida para checar disponibilidade por endereco."),
    dict(vendor="Helloo", cobertura="4-5 mil predios residenciais + 110+ shoppings.", corporativo="POUCO (foco residencial/varejo)",
         contato="anuncie.helloo.com.br (a partir de R$79,90/tela/30d)", obs="Menos aderente ao Top 5 corporativo."),
    dict(vendor="Remidia", cobertura="Elevador residencial exclusivamente.", corporativo="NAO",
         contato="remidia.com", obs="Fora do escopo corporativo."),
])

RFP = pd.DataFrame([
    dict(bloco="Inventario", pergunta="O predio [endereco] esta na rede? Quantas telas/elevadores? Localizacao (atrio, cabine)? Prazo de ativacao?"),
    dict(bloco="Formato", pergunta="Tela digital ou cartaz? Resolucao/tamanho? Duracao da insercao (s)? Frequencia/hora? Aceita QR code?"),
    dict(bloco="Financeiro", pergunta="CPM ou preco por tela/periodo? Minimo de telas e periodo? Producao do criativo inclusa? Desconto por volume/trimestre?"),
    dict(bloco="Audiencia", pergunta="Estimativa de passagem/dia no predio? Perfil? Comprovacao (relatorio de veiculacao)?"),
    dict(bloco="Mensuracao", pergunta="Suporta UTM/URL dedicada e QR? Relatorio semanal de veiculacao? Garantia de uptime/SLA?"),
])

ATTR_BASE = pd.DataFrame([
    dict(metrica="Total de deals (deals_comercial_prod)", valor="35.185"),
    dict(metrica="Deals com CNPJ preenchido", valor="66 (0,19%)"),
    dict(metrica="Deals com razao social", valor="66"),
    dict(metrica="Deals com endereco/bairro/municipio", valor="49 (0,14%)"),
    dict(metrica="Deals com 'como conheceu' preenchido", valor="60 (0,17%) — SEM opcao de OOH/elevador"),
    dict(metrica="Reunioes realizadas (total, base)", valor="2.559"),
    dict(metrica="Fechamentos (total, base)", valor="86"),
    dict(metrica="Match dos 24 CNPJs-ancora no CRM", valor="0 (nenhuma das grandes agencias e deal atual por CNPJ)"),
    dict(metrica="Deals nas regioes-alvo (por bairro preenchido)", valor="8 — com fechamentos em Itaim, Pinheiros, Vila Olimpia, Brooklin, Jardim Paulistano"),
    dict(metrica="CONCLUSAO baseline", valor="Atribuicao por localizacao HOJE e inviavel (dado firmografico <0,2%). Necessario implantar captura nova."),
])

ATTR_FRAME = pd.DataFrame([
    dict(passo=1, mecanismo="Campo 'como conheceu'", acao="Adicionar opcao 'Vi anuncio no elevador/predio (OOH)' em como_conheceu_bd e tornar obrigatorio na qualificacao SDR."),
    dict(passo=2, mecanismo="UTM dedicada", acao="utm_source=ooh, utm_medium=elevador, utm_campaign=elevador-{predio}. Cai nativo nas colunas utm_* do CRM."),
    dict(passo=3, mecanismo="LP/URL vanity + QR", acao="Uma URL/QR por predio (ex.: buzz.li/fl949) -> GA4 + formulario. QR no criativo do elevador."),
    dict(passo=4, mecanismo="Codigo/cupom", acao="Codigo citavel por predio ('ELEVADOR-FL949') logado pelo SDR na reuniao."),
    dict(passo=5, mecanismo="Firmografia na reuniao", acao="Preencher razao_social/CNPJ ja na reuniao (hoje so no contrato) OU enriquecer via BrasilAPI a partir do nome -> habilita match geografico."),
    dict(passo=6, mecanismo="Lista de contas-alvo", acao="Usar os inquilinos desta analise (aba Empresas) como target accounts; flag de inbound dessas contas."),
    dict(passo=7, mecanismo="Medicao de lift", acao="Janela pre/pos; comparar reunioes+fechamentos de contas-alvo vs controle. KPIs: nº reunioes/fechamentos OOH-atribuiveis, CAC vs canais, lift regional. OOH e direcional, nao deterministico."),
])

METODOLOGIA = pd.DataFrame([
    dict(item="Abordagem", detalhe="Bottom-up: coletar empresas do ecossistema de marketing COM endereco -> agrupar por endereco (mesma rua+numero = mesmo predio) -> ranquear por densidade/qualidade de ICP -> midia -> attribution."),
    dict(item="Fonte oficial", detalhe="Receita Federal via BrasilAPI (MCP Brasil): situacao cadastral, endereco, CNAE e porte por CNPJ. Validou/derrubou empresas (ex.: 1a coleta de Faria Lima era fabricada; varias empresas tinham endereco fiscal != operacional)."),
    dict(item="Outras fontes", detalhe="Google Maps, sites/contato das empresas, diretorios (Meio&Mensagem, ABRADi), noticias de mudanca de sede; CRM Buzzmonitor (Supabase, somente leitura)."),
    dict(item="Confianca", detalhe="oficial = CNPJ verificado ATIVO no eixo; fonte = endereco por fonte web real sem CNPJ validado; baixada = entidade encerrada."),
    dict(item="LIMITACOES", detalhe="(1) Amostra de ancoras verificadas, NAO censo de inquilinos. (2) Endereco fiscal != operacional (clusterizacao usa o operacional). (3) Inventario de midia por predio nao e publico. (4) Campos firmograficos do CRM <0,2% preenchidos. (5) WPP migrou para Vila Leopoldina (nov/2025) — fora do eixo."),
])

# ---- Excel ----
out = "analise-edificios-elevador/edificios_buzzmonitor.xlsx"
with pd.ExcelWriter(out, engine='openpyxl') as xw:
    TOP5_REC.to_excel(xw, sheet_name='Top5_Recomendado', index=False)
    ed_cols = ['rank', 'edificio', 'regiao', 'logradouro', 'numero', 'n_empresas', 'n_agencias',
               'n_oficial', 'n_coworking', 'ancora_grande', 'elevadores_aprox', 'func_est_total', 'score', 'chave_endereco']
    ed[ed_cols].to_excel(xw, sheet_name='Edificios_Ranking', index=False)
    emp_cols = ['empresa', 'grupo', 'tipo', 'regiao', 'edificio', 'logradouro', 'numero', 'bairro',
                'cnpj', 'situacao', 'cnae', 'porte', 'func_est', 'confianca', 'coworking', 'fonte', 'chave_endereco']
    df[emp_cols].sort_values(['regiao', 'chave_endereco', 'empresa']).to_excel(xw, sheet_name='Empresas', index=False)
    df[df['coworking'] == 1][['empresa', 'regiao', 'edificio', 'logradouro', 'numero', 'confianca', 'fonte']].to_excel(
        xw, sheet_name='Coworkings', index=False)
    MIDIA.to_excel(xw, sheet_name='Midia_Vendors', index=False)
    RFP.to_excel(xw, sheet_name='Checklist_RFP', index=False)
    ATTR_BASE.to_excel(xw, sheet_name='Attribution_Baseline', index=False)
    ATTR_FRAME.to_excel(xw, sheet_name='Attribution_Framework', index=False)
    pd.DataFrame(FORA).to_excel(xw, sheet_name='Fora_do_eixo', index=False)
    METODOLOGIA.to_excel(xw, sheet_name='Metodologia_Fontes', index=False)

print(f"\nExcel salvo em: {out}")
print("\nNOTA Pinheiros:", ALT_PINHEIROS)
print("NOTA Paulista:", NOTA_PAULISTA)

# ---- CSVs para upload nativo no Google Drive (sem base64) ----
import os
csvdir = "analise-edificios-elevador/csv"
os.makedirs(csvdir, exist_ok=True)
TOP5_REC.to_csv(f"{csvdir}/01_Top5_Recomendado.csv", index=False, encoding="utf-8")
ed[ed_cols].to_csv(f"{csvdir}/02_Edificios_Ranking.csv", index=False, encoding="utf-8")
df[emp_cols].sort_values(['regiao', 'chave_endereco', 'empresa']).to_csv(
    f"{csvdir}/03_Empresas_lista_attribution.csv", index=False, encoding="utf-8")
for f in os.listdir(csvdir):
    print("CSV:", f, os.path.getsize(os.path.join(csvdir, f)), "bytes")
