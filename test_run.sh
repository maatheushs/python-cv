#!/bin/bash
# Script de teste rápido do Resume Builder

echo "=== TESTE DO RESUME BUILDER ==="
echo ""
echo "Este script vai gerar um currículo usando a descrição de vaga de exemplo."
echo ""

# Ativar virtual environment se existir
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Criar um input automatizado para teste
echo "2" > /tmp/resume_input.txt  # Opção 2: carregar de arquivo
echo "example_job_description.txt" >> /tmp/resume_input.txt  # Arquivo de exemplo
echo "1" >> /tmp/resume_input.txt  # Selecionar versão 1 (default)

# Executar o resume builder com input do arquivo
python resume_builder.py < /tmp/resume_input.txt

# Limpar arquivo temporário
rm /tmp/resume_input.txt

echo ""
echo "=== TESTE CONCLUÍDO ==="
echo "Verifique o arquivo .docx gerado no diretório atual!"
