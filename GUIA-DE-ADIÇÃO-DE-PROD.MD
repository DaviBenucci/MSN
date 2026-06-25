# Sim, isso não só é perfeitamente possível como é a **melhor forma de estruturar automações**. A sua lógica de organizar por pastas utilizando o código do produto é o padrão ouro para não se perder no cadastro de e-commerces volumosos

Nós vamos criar um script que faz exatamente o que você descreveu: ele entra na sua pasta de extração, lê o código do produto, acha a imagem, recorta o fundo, centraliza em um quadrado branco perfeito de 800x800 e salva já em formato **WebP** lá no seu Desktop, dentro de `msn/products/[código do produto]`.

Aqui está o passo a passo de como vamos colocar isso para rodar.

---

## Passo 1: Instalar as Bibliotecas

Abra o **Terminal** (ou Prompt de Comando/CMD no Windows) e digite o seguinte comando para instalar a Inteligência Artificial que remove fundos e a biblioteca de manipulação de imagens:

```bash
pip install rembg pillow

```

*(Nota: O primeiro download do `rembg` pode demorar um pouquinho, pois ele baixa o modelo de IA treinado para reconhecer os objetos).*

## Passo 2: O Script de Automação

Abra o seu editor de código (ou o Bloco de Notas), copie o código abaixo e salve-o com o nome `otimizador_imagens.py`.

```python
import os
import io
from PIL import Image
from rembg import remove

# =====================================================================
# CONFIGURAÇÕES DE PASTAS (Altere a pasta_origem para o seu computador)
# =====================================================================
# Caminho onde você guarda os zips extraídos do Icecat.
pasta_origem = r"C:\Caminho\Para\Sua\Pasta\Produtos_Brutos" 

# Caminho de destino automático: Desktop/msn/products
pasta_destino = os.path.expanduser("~/Desktop/msn/products")
TAMANHO_FINAL = (800, 800)

# Garante que a pasta base no Desktop exista
os.makedirs(pasta_destino, exist_ok=True)

print("Iniciando o processamento em lote...")

# Percorre todas as pastas (códigos dos produtos) na pasta de origem
for codigo_produto in os.listdir(pasta_origem):
    caminho_produto = os.path.join(pasta_origem, codigo_produto)
    
    # Verifica se é realmente uma pasta (e não um arquivo solto)
    if os.path.isdir(caminho_produto):
        print(f"\n📦 Processando produto: {codigo_produto}")
        
        # Cria a pasta correspondente no destino
        destino_produto = os.path.join(pasta_destino, codigo_produto)
        os.makedirs(destino_produto, exist_ok=True)
        
        # Procura imagens dentro da pasta do produto
        for arquivo in os.listdir(caminho_produto):
            if arquivo.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                caminho_imagem = os.path.join(caminho_produto, arquivo)
                nome_sem_extensao = os.path.splitext(arquivo)[0]
                caminho_salvar = os.path.join(destino_produto, f"{nome_sem_extensao}_otimizado.webp")
                
                print(f"  ⏳ Tratando: {arquivo}...")
                
                try:
                    # 1. Lê a imagem original
                    with open(caminho_imagem, 'rb') as i:
                        input_bytes = i.read()
                    
                    # 2. Remove o fundo usando a IA (rembg)
                    output_bytes = remove(input_bytes)
                    img_sem_fundo = Image.open(io.BytesIO(output_bytes)).convert("RGBA")
                    
                    # 3. Redimensiona mantendo a proporção exata do produto
                    img_sem_fundo.thumbnail(TAMANHO_FINAL, Image.Resampling.LANCZOS)
                    
                    # 4. Cria um fundo quadrado branco perfeito (800x800)
                    fundo_branco = Image.new('RGB', TAMANHO_FINAL, (255, 255, 255))
                    
                    # 5. Calcula as coordenadas para centralizar a imagem
                    largura, altura = img_sem_fundo.size
                    pos_x = (TAMANHO_FINAL[0] - largura) // 2
                    pos_y = (TAMANHO_FINAL[1] - altura) // 2
                    
                    # 6. Cola o produto recortado no centro do quadrado branco
                    fundo_branco.paste(img_sem_fundo, (pos_x, pos_y), img_sem_fundo)
                    
                    # 7. Salva no formato otimizado WebP
                    fundo_branco.save(caminho_salvar, 'webp', quality=85)
                    print(f"  ✅ Salvo com sucesso!")
                    
                except Exception as e:
                    print(f"  ❌ Erro ao processar {arquivo}: {e}")

print("\n🚀 Processamento totalmente concluído!")

```

## Passo 3: Como utilizar

1. No script acima, encontre a linha `pasta_origem = r"C:\Caminho\Para\Sua\Pasta\Produtos_Brutos"` e substitua pelo endereço real de onde você extrai as pastas do Icecat.
2. Abra o terminal na mesma pasta onde você salvou o script.
3. Digite `python otimizador_imagens.py` e aperte Enter.
4. O script fará todo o trabalho sozinho e as pastas prontas mágicamente aparecerão no seu Desktop.

---
