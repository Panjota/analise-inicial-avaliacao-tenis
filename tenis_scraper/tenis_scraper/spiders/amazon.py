import scrapy
import re
from urllib.parse import urljoin, urlencode, parse_qs, urlparse
from tenis_scraper.items import ProdutoItem


class AmazonSpider(scrapy.Spider):
    name = "amazon"
    allowed_domains = ["amazon.com.br"]

    # Configurações específicas para Amazon (mais conservadoras)
    custom_settings = {
        'DOWNLOAD_DELAY': 5.0,  # Delay maior para Amazon
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,  # Apenas 1 requisição por vez
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 3.0,
        'AUTOTHROTTLE_MAX_DELAY': 15.0,
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 0.5,
        'COOKIES_ENABLED': True,
        'DOWNLOADER_MIDDLEWARES': {
            'tenis_scraper.middlewares.AmazonUserAgentMiddleware': 400,
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
        }
    }

    def __init__(self, query=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if query:
            search_query = f"tenis corrida {query}"
            encoded_query = urlencode({'k': search_query, 'rh': 'n:16243890011'})  # Categoria Esportes
            self.start_urls = [f"https://www.amazon.com.br/s?{encoded_query}"]
        else:
            # URLs específicas para tênis de corrida na Amazon
            self.start_urls = [
                # Categoria principal de tênis de corrida
                "https://www.amazon.com.br/s?k=tenis+de+corrida&crid=DLJ5Z8MJX9ZM&sprefix=tenis+de+corrida%2Caps%2C739&ref=nb_sb_ss_ts-doa-p_2_16",
            ]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                callback=self.parse_listagem,
                meta={
                    'max_retry_times': 5,
                    'dont_cache': True,
                },
                headers={
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'DNT': '1',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                }
            )

    def parse_listagem(self, response):
        """Extrai links de produtos da página de listagem da Amazon"""
        
        self.logger.info(f"Processando página de listagem: {response.url}")
        
        # Debug extensivo dos seletores
        self.logger.debug("=== DEBUG SELETORES DE PRODUTOS ===")
        
        # Seletores principais para links de produtos na Amazon
        product_selectors = [
            "h2.a-size-mini.s-color-base.s-color-base a::attr(href)",
            "[data-component-type='s-search-result'] h2 a::attr(href)",
            ".s-result-item h2 a::attr(href)",
            "[data-cy='title-recipe-card'] a::attr(href)",
            ".a-link-normal::attr(href)",
            # Adicionando seletores mais genéricos
            "h2 a[href*='/dp/']::attr(href)",
            "a[href*='/dp/']::attr(href)",
            ".s-link-style a::attr(href)",
            "[data-asin] h2 a::attr(href)"
        ]
        
        product_links = []
        
        for i, selector in enumerate(product_selectors):
            links = response.css(selector).getall()
            self.logger.debug(f"Seletor {i} '{selector}': {len(links)} resultados")
            if links:
                self.logger.debug(f"Primeiros 3 links: {links[:3]}")
                product_links.extend(links)
        
        if not product_links:
            # Debug de fallback
            self.logger.warning("Nenhum seletor funcionou! Analisando estrutura...")
            all_divs = response.css('div[data-component-type]')
            self.logger.warning(f"Divs com data-component-type: {len(all_divs)}")
            
            all_h2 = response.css('h2')
            self.logger.warning(f"Total de H2s: {len(all_h2)}")
            
            dp_links = response.css('a[href*="/dp/"]')
            self.logger.warning(f"Links com /dp/: {len(dp_links)}")
            
            # Pegar qualquer link com /dp/
            product_links = [link for link in response.css('a::attr(href)').getall() if link and '/dp/' in link]
            self.logger.warning(f"Links /dp/ via fallback: {len(product_links)}")
        
        # Filtrar apenas links que parecem ser de produtos
        valid_links = []
        for link in product_links:
            if link and ('/dp/' in link or '/gp/product/' in link):
                if not link.startswith('http'):
                    link = urljoin(response.url, link)
                valid_links.append(link)
        
        # Remover duplicatas mantendo ordem
        seen = set()
        unique_links = []
        for link in valid_links:
            if link not in seen:
                seen.add(link)
                unique_links.append(link)
        
        self.logger.info(f"Encontrados {len(unique_links)} links únicos de produtos")
        
        for link in unique_links:
            yield scrapy.Request(
                link,
                callback=self.parse_produto,
                meta={
                    'max_retry_times': 3,
                    'dont_cache': True,
                },
                headers={
                    'Referer': response.url,
                }
            )
        
        # Paginação na Amazon
        next_page_selectors = [
            ".a-pagination .a-last a::attr(href)",
            "a[aria-label='Ir para a próxima página']::attr(href)",
            ".s-pagination-next::attr(href)"
        ]
        
        for selector in next_page_selectors:
            next_page = response.css(selector).get()
            if next_page:
                next_url = urljoin(response.url, next_page)
                self.logger.info(f"Seguindo para próxima página: {next_url}")
                yield scrapy.Request(
                    next_url,
                    callback=self.parse_listagem,
                    meta={'max_retry_times': 5},
                    headers={'Referer': response.url}
                )
                break  # Apenas uma página por vez

    def parse_produto(self, response):
        """Extrai dados do produto individual na Amazon"""
        
        # Verificar se é realmente um tênis de corrida
        page_text = response.text.lower()
        title_text = response.css('#productTitle::text').get() or ""
        title_text = title_text.lower()
        
        running_keywords = ['corrida', 'running', 'tênis', 'tenis', 'calçado esportivo']
        if not any(keyword in page_text or keyword in title_text for keyword in running_keywords):
            self.logger.info(f"Produto não parece ser tênis de corrida: {response.url}")
            return
        
        item = ProdutoItem()
        
        # Informações básicas
        item["loja"] = "Amazon"
        item["url_produto"] = response.url
        
        # Título/Modelo
        titulo = response.css('#productTitle::text').get()
        if titulo:
            item["modelo"] = titulo.strip()
        
        # Marca - Amazon tem estrutura específica
        marca = (
            response.css('#bylineInfo_feature_div a::text').get() or
            response.css('.a-row .a-size-small.a-link-normal::text').get() or
            response.css('[data-brand]::attr(data-brand)').get()
        )
        if marca:
            item["marca"] = marca.strip()
        
        # Preços - CORRIGIDO com base nos logs de debug
        preco_selectors = [
            '.a-price .a-offscreen::text',  # ESTE É O QUE FUNCIONA!
            '.a-price-current .a-offscreen::text',
            '.a-price.a-text-price.a-size-medium.apexPriceToPay .a-offscreen::text',
            '#price_inside_buybox::text',
            '.a-price-range .a-offscreen::text',
        ]
        
        for selector in preco_selectors:
            precos = response.css(selector).getall()
            for preco in precos:
                # Limpar espaços e caracteres especiais
                preco_limpo = preco.strip().replace('\xa0', ' ')
                if preco_limpo and 'R$' in preco_limpo and len(preco_limpo) > 3:
                    # Verificar se tem números (não só símbolo R$)
                    if any(char.isdigit() for char in preco_limpo):
                        item["preco"] = preco_limpo
                        self.logger.info(f"PREÇO CAPTURADO: {preco_limpo}")
                        break
            if item.get("preco"):
                break
        
        # Preço original (se houver desconto)
        preco_original = response.css('.a-price.a-text-price .a-offscreen::text').get()
        if preco_original and 'R$' in preco_original and preco_original != item.get("preco"):
            item["preco_original"] = preco_original.strip()
        
        # Avaliações - Amazon tem sistema específico
        avaliacao = response.css('.a-icon-alt::text').re_first(r'(\d+[,.]?\d*) de 5 estrelas')
        if avaliacao:
            item["avaliacao_media"] = avaliacao.replace(',', '.')
        
        # Quantidade de avaliações
        qtd_avaliacoes = response.css('#acrCustomerReviewText::text').re_first(r'(\d+)')
        if qtd_avaliacoes:
            item["qtd_avaliacoes"] = qtd_avaliacoes
        
        # Categoria via breadcrumb
        breadcrumb = response.css('#wayfinding-breadcrumbs_feature_div a::text').getall()
        if breadcrumb and len(breadcrumb) > 1:
            item["categoria"] = breadcrumb[-1].strip()
        
        # Gênero - procurar em especificações e título
        genero_text = None
        specs_section = response.css('#feature-bullets ul, #featurebullets_feature_div')
        if specs_section:
            specs_text = ' '.join(specs_section.css('::text').getall()).lower()
            
            if any(word in specs_text for word in ['masculino', 'homem', 'men\'s']):
                genero_text = 'Masculino'
            elif any(word in specs_text for word in ['feminino', 'mulher', 'women\'s']):
                genero_text = 'Feminino'
            elif 'unissex' in specs_text:
                genero_text = 'Unissex'
        
        # Também verificar no título
        if not genero_text and titulo:
            titulo_lower = titulo.lower()
            if any(word in titulo_lower for word in ['masculino', 'homem']):
                genero_text = 'Masculino'
            elif any(word in titulo_lower for word in ['feminino', 'mulher']):
                genero_text = 'Feminino'
        
        item["genero"] = genero_text
        
        # Especificações técnicas da Amazon
        specs_text = ""
        
        # Buscar em várias seções de especificações
        spec_sections = [
            '#feature-bullets ul li',
            '#featurebullets_feature_div li',
            '#productDetails_detailBullets_sections1 tr',
            '#productDetails_techSpec_section_1 tr'
        ]
        
        for section in spec_sections:
            specs = response.css(section + ' ::text').getall()
            if specs:
                specs_text += ' '.join(specs).lower()
        
        # Tipo de sola
        sola_keywords = {
            "eva": "EVA", "gel": "GEL", "air": "Air", "boost": "Boost",
            "zoom": "Zoom", "borracha": "Borracha", "carbono": "Carbono",
            "cloudfoam": "Cloudfoam", "bounce": "Bounce"
        }
        
        for keyword, sola_type in sola_keywords.items():
            if keyword in specs_text:
                item["tipo_sola"] = sola_type
                break
        
        # Material do cabedal
        cabedal_keywords = {
            "mesh": "Mesh", "flyknit": "Flyknit", "primeknit": "Primeknit",
            "textile": "Têxtil", "synthetic": "Sintético", "knit": "Knit",
            "tecido": "Tecido", "sintético": "Sintético"
        }
        
        for keyword, material in cabedal_keywords.items():
            if keyword in specs_text:
                item["material_cabedal"] = material
                break
        
        # Tecnologias
        tech_keywords = [
            "air zoom", "zoom air", "air max", "boost", "gel", "flyknit",
            "primeknit", "react", "vaporfly", "ultraboost", "cloudfoam",
            "bounce", "lightstrike", "wave", "fresh foam"
        ]
        
        found_techs = []
        for tech in tech_keywords:
            if tech in specs_text or tech in titulo.lower():
                found_techs.append(tech.title())
        
        if found_techs:
            item["tecnologia"] = ", ".join(list(set(found_techs)))
        
        # Imagem principal
        img_url = response.css('#landingImage::attr(src)').get()
        if not img_url:
            img_url = response.css('#imgBlkFront::attr(src)').get()
        
        if img_url:
            item["url_imagem"] = img_url
        
        # Disponibilidade
        availability_selectors = [
            '#availability span::text',
            '#buybox .a-alert-content::text',
            '#merchant-info::text'
        ]
        
        disponivel = False
        for selector in availability_selectors:
            avail_text = response.css(selector).get()
            if avail_text:
                avail_lower = avail_text.lower()
                if any(word in avail_lower for word in ['em estoque', 'disponível', 'available']):
                    disponivel = True
                    break
                elif any(word in avail_lower for word in ['fora de estoque', 'indisponível']):
                    disponivel = False
                    break
        
        item["em_estoque"] = "Disponível" if disponivel else "Verificar disponibilidade"
        
        # Verificar se item tem dados mínimos necessários
        if item.get("modelo") and (item.get("marca") or item.get("preco")):
            yield item
        else:
            self.logger.warning(f"Item com dados insuficientes descartado: {response.url}")

    def parse(self, response):
        """Método padrão que redireciona para parse_listagem"""
        return self.parse_listagem(response)
