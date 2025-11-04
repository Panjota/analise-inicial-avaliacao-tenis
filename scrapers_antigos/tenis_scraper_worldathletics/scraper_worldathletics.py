"""
Script para coletar dados de tênis certificados pela World Athletics
URL: https://certcheck.worldathletics.org/FullList

Este script extrai informações sobre tênis aprovados para competições atléticas,
incluindo aprovação para diferentes modalidades (Track, Jumps, Throws, Road & RW, Cross).
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
import re


def extrair_dados_worldathletics():
    """
    Extrai dados do site World Athletics sobre tênis certificados.
    
    Returns:
        DataFrame: Dados limpos e estruturados dos tênis certificados
    """
    print("Iniciando coleta de dados do World Athletics...")
    
    # Configurar opções do Chrome (modo headless = sem interface gráfica)
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    
    # Iniciar navegador
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        # Acessar o site
        print("Acessando o site...")
        driver.get("https://certcheck.worldathletics.org/FullList")
        
        # Aguardar carregamento da página (JavaScript dinâmico)
        print("Aguardando carregamento dos dados...")
        time.sleep(8)
        
        # Extrair dados da tabela
        print("Extraindo dados da tabela...")
        table = driver.find_element(By.TAG_NAME, "table")
        tbody = table.find_element(By.TAG_NAME, "tbody")
        rows = tbody.find_elements(By.TAG_NAME, "tr")
        
        # Extrair cabeçalhos
        thead = table.find_element(By.TAG_NAME, "thead")
        header_row = thead.find_element(By.TAG_NAME, "tr")
        headers = [th.text for th in header_row.find_elements(By.TAG_NAME, "th")]
        
        # Extrair todas as linhas
        rows_data = []
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            row_data = [cell.text if cell.text else None for cell in cells]
            rows_data.append(row_data)
        
        print(f"Total de linhas extraídas: {len(rows_data)}")
        
        # Criar DataFrame
        df = pd.DataFrame(rows_data, columns=headers)
        
        return df
    
    finally:
        driver.quit()


def limpar_dados(df):
    """
    Limpa e estrutura os dados extraídos.
    
    Args:
        df: DataFrame bruto extraído do site
        
    Returns:
        DataFrame: Dados limpos e estruturados
    """
    print("\nLimpando e estruturando os dados...")
    
    # Identificar marcas (linhas onde Track é None)
    brands = []
    current_brand = None
    
    for idx, row in df.iterrows():
        if pd.isna(row['Track']):
            current_brand = row['Shoe']
        brands.append(current_brand)
    
    df['Brand'] = brands
    
    # Remover linhas separadoras de marca (onde Track é None)
    df_clean = df[df['Track'].notna()].copy()
    
    # Limpar nomes dos tênis (remover datas de validade)
    df_clean['Shoe_Clean'] = df_clean['Shoe'].apply(
        lambda x: re.sub(r'\n.*', '', x).strip() if pd.notna(x) else x
    )
    
    # Extrair informação sobre validade
    df_clean['Has_Validity_Date'] = df_clean['Shoe'].str.contains('VALID:', na=False)
    
    # Extrair datas de validade quando disponíveis
    def extract_validity_dates(text):
        if pd.isna(text) or 'VALID:' not in text:
            return None, None
        match = re.search(r'VALID:\s*(\d{2}\s+\w+\s+\d{4})\s*-\s*(\d{2}\s+\w+\s+\d{4})', text)
        if match:
            return match.group(1), match.group(2)
        return None, None
    
    df_clean[['Validity_Start', 'Validity_End']] = df_clean['Shoe'].apply(
        lambda x: pd.Series(extract_validity_dates(x))
    )
    
    # Converter aprovações para booleano (Y -> True, N -> False)
    approval_columns = ['Track', 'Jumps', 'Throws', 'Road & RW', 'Cross']
    for col in approval_columns:
        df_clean[col] = df_clean[col].map({'Y': True, 'N': False})
    
    # Reorganizar colunas
    columns_order = [
        'Brand', 'Shoe_Clean', 'Track', 'Jumps', 'Throws', 'Road & RW', 'Cross',
        'Has_Validity_Date', 'Validity_Start', 'Validity_End', 'Shoe'
    ]
    df_clean = df_clean[columns_order]
    
    # Renomear colunas para nomes mais descritivos
    df_clean.columns = [
        'Marca', 'Modelo', 'Aprovado_Pista', 'Aprovado_Saltos', 'Aprovado_Arremessos',
        'Aprovado_Estrada_Marcha', 'Aprovado_Cross_Country', 'Tem_Data_Validade',
        'Validade_Inicio', 'Validade_Fim', 'Nome_Original_Completo'
    ]
    
    # Resetar índice
    df_clean.reset_index(drop=True, inplace=True)
    
    print(f"Dados limpos! Total de tênis: {len(df_clean)}")
    print(f"Total de marcas: {df_clean['Marca'].nunique()}")
    
    return df_clean


def main():
    """Função principal para executar a coleta e limpeza de dados."""
    try:
        # Extrair dados
        df_raw = extrair_dados_worldathletics()
        
        # Limpar dados
        df_clean = limpar_dados(df_raw)
        
        # Salvar dados limpos
        output_file = 'dados_tenis_worldathletics.csv'
        df_clean.to_csv(output_file, index=False, encoding='utf-8')
        print(f"\n✓ Dados salvos com sucesso em: {output_file}")
        
        # Exibir resumo
        print("\n=== RESUMO DOS DADOS ===")
        print(f"Total de tênis: {len(df_clean)}")
        print(f"Total de marcas: {df_clean['Marca'].nunique()}")
        print(f"\nTop 10 marcas:")
        print(df_clean['Marca'].value_counts().head(10))
        print(f"\nAprovações por modalidade:")
        for col in ['Aprovado_Pista', 'Aprovado_Saltos', 'Aprovado_Arremessos', 
                    'Aprovado_Estrada_Marcha', 'Aprovado_Cross_Country']:
            count = df_clean[col].sum()
            print(f"  {col}: {count} tênis ({count/len(df_clean)*100:.1f}%)")
        
        return df_clean
        
    except Exception as e:
        print(f"\n✗ Erro durante a execução: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    df = main()
