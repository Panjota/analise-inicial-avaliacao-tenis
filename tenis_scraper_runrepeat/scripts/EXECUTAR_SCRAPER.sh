#!/bin/bash

# ============================================================================
# SCRIPT DE EXECUÇÃO - EXTRAÇÃO DE DADOS DOS 625 TÊNIS
# ============================================================================
# 
# Este script executa a extração dos 20 campos principais de TODOS os 625
# tênis do catálogo RunRepeat.
#
# TEMPO ESTIMADO: ~30 minutos
# 
# REQUISITOS:
# - Python 3.x instalado
# - Bibliotecas: selenium, beautifulsoup4, pandas
# - ChromeDriver instalado
#
# RESULTADOS:
# - runrepeat_shoes_complete.json (625 tênis com dados completos)
# - runrepeat_shoes_complete.csv (formato tabular)
# - runrepeat_temp_X.json (backups a cada 50 tênis)
#
# ============================================================================

echo "============================================================================"
echo "EXTRAÇÃO DE DADOS - 625 TÊNIS RUNREPEAT"
echo "============================================================================"
echo ""
echo "📊 Este script irá processar TODOS os 625 tênis do catálogo"
echo "⏱️  Tempo estimado: ~30 minutos"
echo "💾 Progresso salvo a cada 50 tênis"
echo ""
echo "Pressione CTRL+C para cancelar a qualquer momento"
echo "============================================================================"
echo ""

# Verificar se o arquivo de entrada existe
if [ ! -f "runrepeat_all_shoes.json" ]; then
    echo "❌ ERRO: Arquivo runrepeat_all_shoes.json não encontrado!"
    echo "Execute primeiro o script 01_scraper_runrepeat_catalogo.py"
    exit 1
fi

# Contar tênis no arquivo
TOTAL_SHOES=$(python3 -c "import json; print(len(json.load(open('runrepeat_all_shoes.json'))))")
echo "✓ Arquivo de entrada encontrado: $TOTAL_SHOES tênis"
echo ""

# Verificar dependências
echo "🔍 Verificando dependências..."
python3 -c "import selenium, bs4, pandas" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ ERRO: Bibliotecas necessárias não instaladas!"
    echo ""
    echo "Instale com:"
    echo "  pip install selenium beautifulsoup4 pandas"
    exit 1
fi
echo "✓ Todas as dependências instaladas"
echo ""

echo ""
echo "🚀 Iniciando extração (progresso será retomado automaticamente se houver)..."
echo "============================================================================"
echo ""

# Executar o script
python3 02_scraper_runrepeat_detalhes.py

# Verificar resultado
if [ $? -eq 0 ]; then
    echo ""
    echo "============================================================================"
    echo "✅ EXTRAÇÃO CONCLUÍDA COM SUCESSO!"
    echo "============================================================================"
    echo ""
    echo "Arquivos gerados:"
    
    if [ -f "runrepeat_shoes_complete.json" ]; then
        SIZE_JSON=$(ls -lh runrepeat_shoes_complete.json | awk '{print $5}')
        echo "  ✓ runrepeat_shoes_complete.json ($SIZE_JSON)"
    fi
    
    if [ -f "runrepeat_shoes_complete.csv" ]; then
        SIZE_CSV=$(ls -lh runrepeat_shoes_complete.csv | awk '{print $5}')
        echo "  ✓ runrepeat_shoes_complete.csv ($SIZE_CSV)"
    fi
    
    # Listar arquivos temporários
    TEMP_FILES=$(ls runrepeat_temp_*.json 2>/dev/null | wc -l)
    if [ $TEMP_FILES -gt 0 ]; then
        echo "  ✓ $TEMP_FILES arquivos temporários de backup"
    fi
    
    echo ""
    echo "Próximo passo: Execute 03_analise_exploratoria.py para analisar os dados"
    echo "============================================================================"
else
    echo ""
    echo "============================================================================"
    echo "❌ ERRO durante a execução"
    echo "============================================================================"
    echo ""
    echo "Verifique os arquivos temporários para recuperar o progresso:"
    ls -lh runrepeat_temp_*.json 2>/dev/null
    exit 1
fi
