"""
Script para coletar dados do catálogo de tênis do RunRepeat
URL Base: https://runrepeat.com/catalog/running-shoes

Este script navega pelas 21 páginas do catálogo e extrai:
- Nome do tênis
- URL da página do produto
- URL da imagem

Resultado: runrepeat_all_shoes.json
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time


def configurar_driver():
    """
    Configura o driver do Selenium com Chrome em modo headless.
    
    Returns:
        webdriver: Driver configurado
    """
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    
    driver = webdriver.Chrome(options=chrome_options)
    return driver


def extrair_tenis_da_pagina(driver):
    """
    Extrai informações dos tênis de uma página específica.
    
    Args:
        driver: Driver do Selenium já posicionado na página
        
    Returns:
        list: Lista de dicionários com dados dos tênis
    """
    tenis_list = []
    
    try:
        # Aguardar carregamento dos cards de produtos
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.card-link, a[href*='/running-shoes/']"))
        )
        time.sleep(2)  # Aguardar JavaScript renderizar completamente
        
        # Localizar todos os cards de produtos
        # O site usa diferentes estruturas, vamos tentar múltiplos seletores
        cards = driver.find_elements(By.CSS_SELECTOR, "a.card-link, a[class*='product'], div.product-card a")
        
        if not cards:
            # Tentar seletor alternativo
            cards = driver.find_elements(By.XPATH, "//a[contains(@href, '/running-shoes/') or contains(@href, '/asics-') or contains(@href, '/nike-') or contains(@href, '/hoka-')]")
        
        print(f"  Encontrados {len(cards)} cards na página")
        
        for card in cards:
            try:
                # Extrair URL
                url = card.get_attribute('href')
                
                # Filtrar apenas URLs de produtos (não categorias ou filtros)
                if not url or '/catalog/' in url or url.endswith('/running-shoes'):
                    continue
                
                # Extrair nome do tênis
                # Tentar múltiplos seletores para o nome
                nome = None
                try:
                    nome_element = card.find_element(By.CSS_SELECTOR, "h3, h4, .product-name, .card-title")
                    nome = nome_element.text.strip()
                except:
                    try:
                        nome_element = card.find_element(By.TAG_NAME, "img")
                        nome = nome_element.get_attribute('alt')
                    except:
                        # Extrair do URL como fallback
                        nome = url.split('/')[-1].replace('-', ' ').title()
                
                # Extrair imagem
                imagem_url = None
                try:
                    img = card.find_element(By.TAG_NAME, "img")
                    imagem_url = img.get_attribute('src') or img.get_attribute('data-src')
                except:
                    pass
                
                if nome and url:
                    tenis = {
                        "name": nome,
                        "url": url,
                        "image": imagem_url
                    }
                    tenis_list.append(tenis)
                    
            except Exception as e:
                continue
        
    except Exception as e:
        print(f"  Erro ao extrair tênis da página: {e}")
    
    return tenis_list


def coletar_catalogo_completo(total_paginas=21):
    """
    Coleta dados de todas as páginas do catálogo.
    
    Args:
        total_paginas: Número total de páginas a serem coletadas
        
    Returns:
        list: Lista completa de tênis de todas as páginas
    """
    print("="*60)
    print("COLETA DE DADOS DO CATÁLOGO RUNREPEAT")
    print("="*60)
    
    driver = configurar_driver()
    todos_tenis = []
    
    try:
        for pagina in range(1, total_paginas + 1):
            # Construir URL da página
            if pagina == 1:
                url = "https://runrepeat.com/catalog/running-shoes"
            else:
                url = f"https://runrepeat.com/catalog/running-shoes?page={pagina}"
            
            print(f"\n[Página {pagina}/{total_paginas}] Acessando: {url}")
            
            # Acessar página
            driver.get(url)
            time.sleep(3)  # Aguardar carregamento
            
            # Extrair tênis da página
            tenis_pagina = extrair_tenis_da_pagina(driver)
            
            if tenis_pagina:
                todos_tenis.extend(tenis_pagina)
                print(f"  ✓ {len(tenis_pagina)} tênis extraídos desta página")
                print(f"  Total acumulado: {len(todos_tenis)} tênis")
            else:
                print(f"  ⚠ Nenhum tênis encontrado nesta página")
            
            # Pequeno delay entre páginas para não sobrecarregar o servidor
            time.sleep(2)
        
    finally:
        driver.quit()
    
    return todos_tenis


def salvar_dados(dados, arquivo='runrepeat_all_shoes.json'):
    """
    Salva os dados coletados em arquivo JSON.
    
    Args:
        dados: Lista de tênis coletados
        arquivo: Nome do arquivo de saída
    """
    with open(arquivo, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)
    
    print(f"\n✓ Dados salvos em: {arquivo}")


def main():
    """Função principal para executar a coleta do catálogo."""
    try:
        # Coletar dados de todas as páginas
        todos_tenis = coletar_catalogo_completo(total_paginas=21)
        
        # Remover duplicatas (baseado na URL)
        tenis_unicos = []
        urls_vistas = set()
        
        for tenis in todos_tenis:
            if tenis['url'] not in urls_vistas:
                tenis_unicos.append(tenis)
                urls_vistas.add(tenis['url'])
        
        print("\n" + "="*60)
        print("RESUMO DA COLETA")
        print("="*60)
        print(f"Total de tênis coletados: {len(todos_tenis)}")
        print(f"Tênis únicos: {len(tenis_unicos)}")
        print(f"Duplicatas removidas: {len(todos_tenis) - len(tenis_unicos)}")
        
        # Salvar dados
        salvar_dados(tenis_unicos)
        
        # Exibir primeiros resultados
        print("\n=== PRIMEIROS 5 TÊNIS ===")
        for i, tenis in enumerate(tenis_unicos[:5], 1):
            print(f"\n{i}. {tenis['name']}")
            print(f"   URL: {tenis['url']}")
        
        return tenis_unicos
        
    except Exception as e:
        print(f"\n✗ Erro durante a execução: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    dados = main()
