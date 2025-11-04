"""
Script para extrair os 20 CAMPOS PRINCIPAIS de todos os 625 tênis do RunRepeat

Versão otimizada que processa TODOS os 625 tênis, extraindo apenas os dados
mais importantes para análise rápida e eficiente.

Campos extraídos (Top 20):
- price, weight, drop, heel stack, forefoot stack
- arch support, pace, terrain, strike pattern
- cushioning, stability, flexibility, responsiveness
- breathability, durability, audience score
- midsole, outsole, upper, category
- brand (do JSON-LD)

Características:
- Processa TODOS os 625 tênis do runrepeat_all_shoes.json
- Extração focada nos 20 campos mais relevantes
- Salva progresso a cada 50 tênis
- Tempo estimado: ~30 minutos para 625 tênis
- Resultados salvos em JSON e CSV

Arquivos de saída:
- runrepeat_shoes_complete.json (todos os 625 tênis)
- runrepeat_shoes_complete.csv (formato tabular)
- runrepeat_temp_X.json (progresso a cada 50 tênis)
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json
import pandas as pd
import time
import re


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
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    # Configurar timeouts mais longos
    chrome_options.add_argument('--dns-prefetch-disable')
    chrome_options.page_load_strategy = 'normal'
    
    driver = webdriver.Chrome(options=chrome_options)
    # Timeouts MUITO mais generosos para evitar problemas
    driver.set_page_load_timeout(180)  # 3 minutos para carregar página
    driver.implicitly_wait(15)  # 15 segundos para encontrar elementos
    
    return driver


def extrair_numero(texto):
    """
    Extrai número de um texto.
    
    Args:
        texto: String contendo número
        
    Returns:
        float: Número extraído ou None
    """
    if not texto:
        return None
    
    # Remover caracteres não numéricos exceto ponto e vírgula
    numeros = re.findall(r'[\d.,]+', texto)
    if numeros:
        # Pegar o primeiro número encontrado
        numero_str = numeros[0].replace(',', '.')
        try:
            return float(numero_str)
        except:
            return None
    return None


def extrair_texto_limpo(element):
    """Extrai texto limpo de um elemento."""
    try:
        return element.text.strip() if element.text else None
    except:
        return None


def extrair_atributo_elemento(driver, seletores, atributo='text'):
    """
    Tenta extrair informação usando múltiplos seletores.
    
    Args:
        driver: Driver do Selenium
        seletores: Lista de seletores CSS para tentar
        atributo: 'text' para texto ou nome de atributo HTML
        
    Returns:
        Valor extraído ou None
    """
    for seletor in seletores:
        try:
            element = driver.find_element(By.CSS_SELECTOR, seletor)
            if atributo == 'text':
                return extrair_texto_limpo(element)
            else:
                return element.get_attribute(atributo)
        except:
            continue
    return None


def extrair_specs_estruturadas(driver, soup):
    """
    Extrai especificações técnicas de forma estruturada.
    """
    specs = {}
    
    # Procurar por tabelas de especificações
    try:
        # Procurar elementos dt/dd (definition list)
        dt_elements = soup.find_all('dt')
        dd_elements = soup.find_all('dd')
        
        if dt_elements and dd_elements:
            for dt, dd in zip(dt_elements, dd_elements):
                key = dt.get_text().strip().lower()
                value = dd.get_text().strip()
                specs[key] = value
        
        # Procurar por divs/spans com classes específicas
        spec_divs = soup.find_all(['div', 'span', 'li'], class_=re.compile(r'spec|attribute|feature|detail', re.I))
        for spec in spec_divs:
            text = spec.get_text().strip()
            if ':' in text:
                parts = text.split(':', 1)
                if len(parts) == 2:
                    key = parts[0].strip().lower()
                    value = parts[1].strip()
                    specs[key] = value
        
        # Procurar por tabelas
        tables = soup.find_all('table')
        for table in tables:
            rows = table.find_all('tr')
            for row in rows:
                cells = row.find_all(['td', 'th'])
                if len(cells) >= 2:
                    key = cells[0].get_text().strip().lower()
                    value = cells[1].get_text().strip()
                    specs[key] = value
    
    except Exception as e:
        pass
    
    return specs


def extrair_texto_limpo(element):
    """Extrai texto limpo de um elemento."""
    try:
        return element.text.strip() if element.text else None
    except:
        return None


def extrair_atributo_elemento(driver, seletores, atributo='text'):
    """
    Tenta extrair informação usando múltiplos seletores.
    
    Args:
        driver: Driver do Selenium
        seletores: Lista de seletores CSS para tentar
        atributo: 'text' para texto ou nome de atributo HTML
        
    Returns:
        Valor extraído ou None
    """
    for seletor in seletores:
        try:
            element = driver.find_element(By.CSS_SELECTOR, seletor)
            if atributo == 'text':
                return extrair_texto_limpo(element)
            else:
                return element.get_attribute(atributo)
        except:
            continue
    return None


def extrair_specs_estruturadas(driver, soup):
    """
    Extrai especificações técnicas de forma estruturada.
    """
    specs = {}
    
    # Procurar por tabelas de especificações
    try:
        # Procurar elementos dt/dd (definition list)
        dt_elements = soup.find_all('dt')
        dd_elements = soup.find_all('dd')
        
        if dt_elements and dd_elements:
            for dt, dd in zip(dt_elements, dd_elements):
                key = dt.get_text().strip().lower()
                value = dd.get_text().strip()
                specs[key] = value
        
        # Procurar por divs/spans com classes específicas
        spec_divs = soup.find_all(['div', 'span', 'li'], class_=re.compile(r'spec|attribute|feature|detail', re.I))
        for spec in spec_divs:
            text = spec.get_text().strip()
            if ':' in text:
                parts = text.split(':', 1)
                if len(parts) == 2:
                    key = parts[0].strip().lower()
                    value = parts[1].strip()
                    specs[key] = value
        
        # Procurar por tabelas
        tables = soup.find_all('table')
        for table in tables:
            rows = table.find_all('tr')
            for row in rows:
                cells = row.find_all(['td', 'th'])
                if len(cells) >= 2:
                    key = cells[0].get_text().strip().lower()
                    value = cells[1].get_text().strip()
                    specs[key] = value
    
    except Exception as e:
        pass
    
    return specs


def extrair_detalhes_tenis(driver, url, max_tentativas=3):
    """
    Extrai os 20 campos mais importantes de um tênis para análise rápida.
    
    Args:
        driver: Driver do Selenium
        url: URL da página do tênis
        max_tentativas: Número máximo de tentativas em caso de erro
        
    Returns:
        tuple: (dict com campos extraídos, driver atualizado se foi recriado)
    """
    detalhes = {}
    driver_recriado = False
    
    # Lista dos 20 campos mais importantes que queremos extrair
    CAMPOS_PRIORITARIOS = [
        'price', 'weight', 'drop', 'heel stack', 'forefoot stack',
        'arch support', 'pace', 'terrain', 'strike pattern', 'cushioning',
        'stability', 'flexibility', 'responsiveness', 'breathability',
        'durability', 'audience score', 'midsole', 'outsole', 'upper', 'category'
    ]
    
    for tentativa in range(max_tentativas):
        try:
            # Tentar carregar a página com timeout aumentado
            driver.get(url)
            time.sleep(3)  # Aumentado para 3 segundos
            
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            
            # ===== EXTRAIR CAMPOS PRIORITÁRIOS DAS TABELAS =====
            tables = soup.find_all('table')
            campos_extraidos = 0
            
            for table in tables:
                if campos_extraidos >= 20:  # Parar após extrair 20 campos
                    break
                    
                rows = table.find_all('tr')
                for row in rows:
                    if campos_extraidos >= 20:  # Parar após extrair 20 campos
                        break
                        
                    cells = row.find_all(['td', 'th'])
                    if len(cells) >= 2:
                        key = cells[0].get_text().strip()
                        value = cells[1].get_text().strip()
                        
                        if key and value and len(key) < 150:
                            # Normalizar nome da chave
                            key_normalized = key.lower().replace(':', '').replace('  ', ' ').strip()
                            
                            # Verificar se é um campo prioritário
                            if any(campo in key_normalized for campo in CAMPOS_PRIORITARIOS):
                                detalhes[key_normalized] = value
                                campos_extraidos += 1
            
            # ===== EXTRAIR JSON-LD DO PRODUTO (dados essenciais) =====
            scripts = soup.find_all('script', type='application/ld+json')
            for script in scripts:
                try:
                    data = json.loads(script.string)
                    if data.get('@type') == 'Product':
                        # Nome e marca (essenciais)
                        if 'brand' in data and isinstance(data['brand'], dict):
                            detalhes['brand'] = data['brand'].get('name')
                        
                        break
                except:
                    continue
            
            # ===== EXTRAIR SCORE PRINCIPAL =====
            try:
                score_elem = driver.find_element(By.CSS_SELECTOR, ".corescore-big__score, .corescore__score")
                score_text = score_elem.text.strip()
                detalhes['audience_score'] = score_text
            except:
                pass
            
            # ===== PROCESSAR CAMPOS NUMÉRICOS (apenas os mais importantes) =====
            # Extrair peso em gramas
            if 'weight' in detalhes:
                weight_text = detalhes['weight']
                weight_match = re.search(r'\((\d+)g\)', weight_text)
                if weight_match:
                    detalhes['weight_grams'] = int(weight_match.group(1))
                else:
                    oz_match = re.search(r'([\d.]+)\s*oz', weight_text)
                    if oz_match:
                        oz = float(oz_match.group(1))
                        detalhes['weight_grams'] = int(oz * 28.35)
            
            # Extrair preço em USD
            if 'price' in detalhes:
                price_text = detalhes['price']
                usd_match = re.search(r'\$\s*(\d+)', price_text)
                if usd_match:
                    detalhes['price_usd'] = float(usd_match.group(1))
            
            # Extrair drop numérico
            if 'drop' in detalhes:
                drop_text = detalhes['drop']
                drop_match = re.search(r'([\d.]+)\s*mm', drop_text)
                if drop_match:
                    detalhes['drop_mm'] = float(drop_match.group(1))
            
            # Se chegou aqui e extraiu dados, sucesso!
            if len(detalhes) > 0:
                break
                
        except Exception as e:
            error_msg = str(e)
            if tentativa < max_tentativas - 1:
                # Aumentar o tempo de espera entre tentativas exponencialmente
                wait_time = (tentativa + 1) * 5  # 5s, 10s, 15s...
                print(f"    ⚠️  Tentativa {tentativa + 1} falhou, aguardando {wait_time}s...")
                time.sleep(wait_time)
                
                # Se for timeout, SEMPRE recriar o driver
                if 'timed out' in error_msg.lower() or 'timeout' in error_msg.lower() or 'read timed out' in error_msg.lower():
                    try:
                        print(f"    🔄 Timeout detectado. Recriando driver do navegador...")
                        driver.quit()
                        time.sleep(3)
                        driver = configurar_driver()
                        driver_recriado = True
                    except Exception as restart_error:
                        print(f"    ⚠️  Erro ao recriar driver: {restart_error}")
            else:
                print(f"    ⚠️  Erro após {max_tentativas} tentativas: {error_msg[:100]}")
    
    return detalhes, driver if driver_recriado else None


def processar_todos_tenis(arquivo_entrada='runrepeat_all_shoes.json'):
    """
    Processa TODOS os 625 tênis do arquivo de entrada e extrai os 20 campos principais.
    
    Args:
        arquivo_entrada: Arquivo JSON com lista de tênis básicos
        
    Returns:
        list: Lista de tênis com detalhes completos
    """
    print("="*80)
    print("EXTRAÇÃO RÁPIDA - TOP 20 CAMPOS MAIS IMPORTANTES")
    print("="*80)
    
    # Carregar dados básicos
    print(f"\n📂 Carregando dados de: {arquivo_entrada}")
    with open(arquivo_entrada, 'r', encoding='utf-8') as f:
        tenis_basicos = json.load(f)
    
    total_tenis = len(tenis_basicos)
    print(f"✓ Total de tênis a processar: {total_tenis}")
    
    # Tentar recuperar progresso anterior
    tenis_completos, start_index = recuperar_progresso()
    
    if start_index > 0:
        print(f"\n🔄 Continuando do tênis #{start_index + 1}")
    
    # Estimativa de tempo (mais rápida agora)
    tenis_restantes = total_tenis - start_index
    tempo_por_tenis = 3  # segundos (reduzido de 4 para 3)
    tempo_total_estimado = (tenis_restantes * tempo_por_tenis) / 60
    print(f"⏱️  Tempo estimado para os {tenis_restantes} tênis restantes: {tempo_total_estimado:.0f} minutos ({tempo_total_estimado/60:.1f} horas)")
    print(f"\n🚀 Iniciando extração dos 20 campos principais...")
    print(f"💾 Progresso será salvo a cada 5 tênis (arquivo anterior será removido)")
    print("="*80)
    
    driver = configurar_driver()
    tempo_inicio = time.time()
    erros_consecutivos = 0
    
    try:
        for i in range(start_index, total_tenis):
            tenis = tenis_basicos[i]
            print(f"\n[{i+1}/{total_tenis}] Processando: {tenis['name']}")
            
            # Se houver muitos erros consecutivos, recriar o driver
            if erros_consecutivos >= 3:
                print(f"    🔄 Muitos erros consecutivos. Reiniciando driver...")
                try:
                    driver.quit()
                    time.sleep(5)
                    driver = configurar_driver()
                    erros_consecutivos = 0
                except Exception as e:
                    print(f"    ⚠️  Erro ao recriar driver: {e}")
            
            # Extrair detalhes
            detalhes, novo_driver = extrair_detalhes_tenis(driver, tenis['url'])
            
            # Atualizar driver se foi recriado
            if novo_driver:
                driver = novo_driver
            
            # Verificar se houve sucesso na extração
            if len(detalhes) == 0:
                erros_consecutivos += 1
            else:
                erros_consecutivos = 0
            
            # Combinar dados básicos com detalhes
            tenis_completo = {
                'name': tenis['name'],
                'url': tenis['url'],
                'image': tenis['image'],
                **detalhes
            }
            
            tenis_completos.append(tenis_completo)
            
            # Mostrar progresso resumido
            campos_preenchidos = sum(1 for v in detalhes.values() if v is not None and v != '')
            print(f"  ✓ {campos_preenchidos} campos extraídos", end='')
            
            # Mostrar campos principais se disponíveis
            info_parts = []
            if 'brand' in detalhes and detalhes['brand']:
                info_parts.append(f"Marca: {detalhes['brand']}")
            if 'price_usd' in detalhes and detalhes['price_usd']:
                info_parts.append(f"${detalhes['price_usd']}")
            if 'weight_grams' in detalhes and detalhes['weight_grams']:
                info_parts.append(f"{detalhes['weight_grams']}g")
            if 'drop_mm' in detalhes and detalhes['drop_mm']:
                info_parts.append(f"Drop {detalhes['drop_mm']}mm")
            
            if info_parts:
                print(f" | {' | '.join(info_parts)}")
            else:
                print()
            
            # Estimativa de tempo restante (a cada 10 tênis)
            tenis_processados = i + 1 - start_index
            if tenis_processados % 10 == 0 and tenis_processados >= 10:
                tempo_decorrido = time.time() - tempo_inicio
                tempo_medio = tempo_decorrido / tenis_processados
                tempo_restante = tempo_medio * (total_tenis - i - 1)
                horas = int(tempo_restante // 3600)
                minutos = int((tempo_restante % 3600) // 60)
                total_processados = i + 1
                sucesso_count = sum(1 for t in tenis_completos[-tenis_processados:] if len(t) > 3)
                sucesso_rate = (sucesso_count / tenis_processados) * 100
                if horas > 0:
                    print(f"  ⏱️  Tempo restante: ~{horas}h {minutos}min | Taxa de sucesso: {sucesso_rate:.1f}%")
                else:
                    print(f"  ⏱️  Tempo restante: ~{minutos}min | Taxa de sucesso: {sucesso_rate:.1f}%")
            
            # Delay reduzido para não sobrecarregar
            time.sleep(2)  # Aumentado para 2 segundos
            
            # Salvar progresso a cada 5 tênis (mais frequente!)
            if (i + 1) % 5 == 0:
                salvar_progresso(tenis_completos, i + 1)
        
    finally:
        driver.quit()
    
    return tenis_completos


def salvar_progresso(dados, contador):
    """
    Salva progresso parcial durante a coleta e remove arquivo anterior.
    
    Args:
        dados: Lista de tênis processados até o momento
        contador: Número de tênis processados
    """
    import glob
    import os
    
    # Salvar novo arquivo
    arquivo_temp = f'runrepeat_temp_{contador}.json'
    with open(arquivo_temp, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)
    print(f"\n  💾 Progresso salvo em: {arquivo_temp}")
    
    # Excluir arquivos temporários anteriores
    temp_files = glob.glob('runrepeat_temp_*.json')
    for temp_file in temp_files:
        if temp_file != arquivo_temp:
            try:
                os.remove(temp_file)
                print(f"  🗑️  Removido arquivo antigo: {temp_file}")
            except:
                pass


def recuperar_progresso():
    """
    Tenta recuperar progresso de execução anterior AUTOMATICAMENTE.
    
    Returns:
        tuple: (lista de tênis já processados, índice do último processado) ou ([], 0)
    """
    import glob
    import os
    
    # Procurar arquivos temporários
    temp_files = glob.glob('runrepeat_temp_*.json')
    if not temp_files:
        return [], 0
    
    # Encontrar o arquivo mais recente
    temp_files.sort(key=lambda x: int(x.split('_')[-1].replace('.json', '')), reverse=True)
    latest_file = temp_files[0]
    
    # Extrair o número do arquivo
    last_index = int(latest_file.split('_')[-1].replace('.json', ''))
    
    print(f"\n📂 Progresso anterior encontrado: {latest_file}")
    print(f"   Último tênis processado: {last_index}")
    
    # Carregar automaticamente
    with open(latest_file, 'r', encoding='utf-8') as f:
        dados = json.load(f)
    print(f"✓ Carregados {len(dados)} tênis já processados - CONTINUANDO AUTOMATICAMENTE")
    return dados, last_index


def salvar_dados_finais(dados):
    """
    Salva os dados finais em JSON e CSV.
    
    Args:
        dados: Lista completa de tênis com detalhes
    """
    # Salvar JSON
    arquivo_json = 'runrepeat_shoes_complete.json'
    with open(arquivo_json, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)
    print(f"\n✓ Dados salvos em JSON: {arquivo_json}")
    
    # Converter para DataFrame e salvar CSV
    df = pd.DataFrame(dados)
    arquivo_csv = 'runrepeat_shoes_complete.csv'
    df.to_csv(arquivo_csv, index=False, encoding='utf-8')
    print(f"✓ Dados salvos em CSV: {arquivo_csv}")
    
    return df


def main():
    """Função principal para executar a extração de detalhes dos 625 tênis."""
    try:
        # Processar todos os tênis
        tenis_completos = processar_todos_tenis()
        
        # Salvar dados finais
        df = salvar_dados_finais(tenis_completos)
        
        # Exibir resumo
        print("\n" + "="*80)
        print("RESUMO DOS DADOS COLETADOS - 625 TÊNIS")
        print("="*80)
        print(f"✓ Total de tênis processados: {len(df)}")
        print(f"✓ Total de campos coletados: {len(df.columns)}")
        
        print(f"\n📊 Completude dos Dados (top 20 campos):")
        campos_principais = [
            'brand', 'price', 'price_usd', 'weight', 'weight_grams', 'drop', 'drop_mm',
            'heel stack', 'forefoot stack', 'arch support', 'pace', 'terrain',
            'cushioning', 'stability', 'flexibility', 'responsiveness',
            'breathability', 'durability', 'audience_score', 'category'
        ]
        
        for campo in campos_principais:
            if campo in df.columns:
                nao_nulos = df[campo].notna().sum()
                percentual = (nao_nulos / len(df)) * 100
                if nao_nulos > 0:  # Só mostrar campos com dados
                    print(f"  • {campo}: {nao_nulos}/{len(df)} ({percentual:.1f}%)")
        
        if 'brand' in df.columns and df['brand'].notna().any():
            print(f"\n🏷️  Top 10 marcas:")
            print(df['brand'].value_counts().head(10))
        
        if 'price_usd' in df.columns and df['price_usd'].notna().any():
            print(f"\n💰 Estatísticas de preço (USD):")
            print(f"  Média: ${df['price_usd'].mean():.2f}")
            print(f"  Mediana: ${df['price_usd'].median():.2f}")
            print(f"  Mínimo: ${df['price_usd'].min():.2f}")
            print(f"  Máximo: ${df['price_usd'].max():.2f}")
        
        if 'weight_grams' in df.columns and df['weight_grams'].notna().any():
            print(f"\n⚖️  Estatísticas de peso (gramas):")
            print(f"  Média: {df['weight_grams'].mean():.0f}g")
            print(f"  Mediana: {df['weight_grams'].median():.0f}g")
            print(f"  Mínimo: {df['weight_grams'].min():.0f}g")
            print(f"  Máximo: {df['weight_grams'].max():.0f}g")
        
        if 'drop_mm' in df.columns and df['drop_mm'].notna().any():
            print(f"\n📐 Distribuição de Drop (mm):")
            print(df['drop_mm'].value_counts().sort_index().head(10))
        
        print("\n" + "="*80)
        print("✅ COLETA COMPLETA! Dados salvos em:")
        print("   • runrepeat_shoes_complete.json")
        print("   • runrepeat_shoes_complete.csv")
        print("="*80)
        
        return df
        
    except Exception as e:
        print(f"\n❌ Erro durante a execução: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    df = main()
