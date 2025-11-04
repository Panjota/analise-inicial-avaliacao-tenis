# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import re
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class CleanAndValidatePipeline:
    """Pipeline para limpar e validar dados"""
    
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        # Limpar e validar campos obrigatórios
        if not adapter.get('modelo') or not adapter.get('url_produto'):
            raise DropItem(f"Item sem modelo ou URL: {item}")
        
        # Limpar modelo
        if adapter.get('modelo'):
            adapter['modelo'] = self.clean_text(adapter['modelo'])
        
        # Limpar marca
        if adapter.get('marca'):
            adapter['marca'] = self.clean_text(adapter['marca'])
        
        # Limpar e converter preço
        if adapter.get('preco'):
            adapter['preco'] = self.extract_price(adapter['preco'])
        
        # Limpar e converter preço original
        if adapter.get('preco_original'):
            adapter['preco_original'] = self.extract_price(adapter['preco_original'])
        
        # Calcular desconto se não existir
        if adapter.get('preco') and adapter.get('preco_original') and not adapter.get('desconto_percentual'):
            try:
                preco = float(adapter['preco'])
                preco_original = float(adapter['preco_original'])
                if preco_original > preco:
                    desconto = ((preco_original - preco) / preco_original) * 100
                    adapter['desconto_percentual'] = round(desconto, 2)
            except (ValueError, ZeroDivisionError):
                pass
        
        # Limpar avaliação
        if adapter.get('avaliacao_media'):
            adapter['avaliacao_media'] = self.extract_rating(adapter['avaliacao_media'])
        
        # Limpar quantidade de avaliações
        if adapter.get('qtd_avaliacoes'):
            adapter['qtd_avaliacoes'] = self.extract_number(adapter['qtd_avaliacoes'])
        
        # Padronizar gênero
        if adapter.get('genero'):
            adapter['genero'] = self.standardize_gender(adapter['genero'])
        
        return item
    
    def clean_text(self, text):
        """Remove caracteres especiais e espaços extras"""
        if not text:
            return text
        return re.sub(r'\s+', ' ', str(text).strip())
    
    def extract_price(self, price_text):
        """Extrai preço numérico do texto"""
        if not price_text:
            return None
        
        # Remove caracteres não numéricos exceto vírgula e ponto
        price_clean = re.sub(r'[^\d,.]', '', str(price_text))
        
        # Converte vírgula para ponto se for decimal brasileiro
        if ',' in price_clean and '.' not in price_clean:
            price_clean = price_clean.replace(',', '.')
        elif ',' in price_clean and '.' in price_clean:
            # Remove pontos de milhares e mantém vírgula como decimal
            price_clean = price_clean.replace('.', '').replace(',', '.')
        
        try:
            return float(price_clean)
        except ValueError:
            return None
    
    def extract_rating(self, rating_text):
        """Extrai nota numérica do texto"""
        if not rating_text:
            return None
        
        rating_match = re.search(r'(\d+[,.]?\d*)', str(rating_text))
        if rating_match:
            rating = rating_match.group(1).replace(',', '.')
            try:
                return float(rating)
            except ValueError:
                return None
        return None
    
    def extract_number(self, text):
        """Extrai número inteiro do texto"""
        if not text:
            return None
        
        number_match = re.search(r'(\d+)', str(text))
        if number_match:
            try:
                return int(number_match.group(1))
            except ValueError:
                return None
        return None
    
    def standardize_gender(self, gender_text):
        """Padroniza texto de gênero"""
        if not gender_text:
            return None
        
        gender_lower = str(gender_text).lower()
        
        if any(word in gender_lower for word in ['masculino', 'homem', 'men', 'male']):
            return 'Masculino'
        elif any(word in gender_lower for word in ['feminino', 'mulher', 'women', 'female']):
            return 'Feminino'
        elif any(word in gender_lower for word in ['unissex', 'unisex']):
            return 'Unissex'
        else:
            return gender_text


class DuplicatesPipeline:
    """Pipeline para remover itens duplicados"""
    
    def __init__(self):
        self.urls_seen = set()
    
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        url = adapter.get('url_produto')
        
        if url in self.urls_seen:
            raise DropItem(f"Item duplicado encontrado: {url}")
        else:
            self.urls_seen.add(url)
            return item


class TenisScraperPipeline:
    def process_item(self, item, spider):
        return item
