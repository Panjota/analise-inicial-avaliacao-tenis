# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ProdutoItem(scrapy.Item):
    # Informações básicas do produto
    loja = scrapy.Field()
    url_produto = scrapy.Field()
    modelo = scrapy.Field()
    marca = scrapy.Field()
    preco = scrapy.Field()
    preco_original = scrapy.Field()
    desconto_percentual = scrapy.Field()
    
    # Avaliações
    avaliacao_media = scrapy.Field()
    qtd_avaliacoes = scrapy.Field()
    
    # Categorização
    categoria = scrapy.Field()
    genero = scrapy.Field()
    
    # Especificações técnicas
    tipo_sola = scrapy.Field()
    material_cabedal = scrapy.Field()
    tipo_fecho = scrapy.Field()  # Novo campo específico para tipo de fecho
    drop = scrapy.Field()
    peso = scrapy.Field()
    tecnologia = scrapy.Field()
    
    # Disponibilidade
    tamanhos_disponiveis = scrapy.Field()
    cores_disponiveis = scrapy.Field()
    em_estoque = scrapy.Field()
    
    # Metadados
    data_coleta = scrapy.Field()
    url_imagem = scrapy.Field()
