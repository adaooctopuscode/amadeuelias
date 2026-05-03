# Agente Para Atualizacao Do Memorial Tecnico

Este repositório contém o documento principal `MC-AMADEU ELIAS R0.docx`.
Qualquer agente que trabalhe neste projeto deve tratar esse arquivo como um relatório técnico já diagramado e preservar o layout existente.

---

## Contexto Do Projeto

- **Documento:** `MC-AMADEU ELIAS R0.docx` (~70 MB)
- **Repositório GitHub:** `adaooctopuscode/amadeuelias`
- **Ferramenta de cálculo:** Software SCIA Engineer
- **Estrutura:** Memorial técnico de ponte com 7 tabuleiros

### Estrutura De Seções Do Documento

| Seção | Conteúdo |
|-------|----------|
| C.4 | Trem Tipo TB-50 — 21 imagens (3 por tabuleiro × 7 tabuleiros) |
| C.5 | Frenagem — 7 imagens (1 por tabuleiro) + tabelas de carga |
| C.6 | Vento Longitudinal — 3 imagens (grupos de tabuleiros) |
| C.7 | Empuxos — 4 imagens (sobrecarga e solo nos Encontros 1 e 2) |

### Tabuleiros E Trilhos De Referência

| Tabuleiro | Trilhos | Obs |
|-----------|---------|-----|
| 1 | TR1, TR2, TR3 | Reto |
| 2 | TR4, TR5, TR6 | Reto |
| 3 | TR7, TR8, TR9 | Reto |
| 4 | TR10, TR11, TR12 | Curvo |
| 5 | TR13, TR14, TR15 | Curvo |
| 6 | TR16, TR17, TR18 | Curvo |
| 7 | TR19, TR20, TR21 | Curvo |

---

## Papel Do Agente

O agente atua como editor técnico de documentos Word. Ele deve:

- Substituir, inserir, remover e reposicionar imagens
- Criar, editar e formatar tabelas
- Ajustar textos preservando estilo
- Ler imagens enviadas pelo usuário e extrair conteúdo relevante
- Manter histórico claro do que foi alterado
- Validar o arquivo após cada modificação

---

## Regras Obrigatórias

- Nunca alterar layout, margens, cabeçalhos, rodapés, estilos globais, numeração, sumário, tamanho de página sem pedido explícito.
- Fazer alterações pequenas e localizadas no trecho solicitado.
- Preservar fontes, alinhamento, espaçamento, estilos de legenda, bordas, cores e dimensões existentes.
- Não criar arquivos `.docx` de backup permanentes.
- **Antes de qualquer modificação:** verificar se o Word está aberto e fechá-lo via AppleScript.
- **Após qualquer modificação:** reabrir o Word com o arquivo atualizado e **obrigatoriamente saltar para a secção alterada** (não basta abrir no início do ficheiro): Localizar via AppleScript com texto único que exista só nessa zona (título da subsecção, subtítulo ou primeira legenda tocada), para conferência imediata pelo utilizador.
- Quando o usuário disser `salvar`, executar o fluxo Git completo.
- **Sempre confirmar imagens antes de substituir:** localizar os arquivos em `~/Downloads/`, visualizar cada um, apresentar tabela de mapeamento (arquivo → legenda) e aguardar confirmação do usuário antes de aplicar qualquer alteração.
- **Sempre perguntar sobre legendas quando houver dúvida:** nem toda imagem tem legenda. Imagens de tabelas/listas do software geralmente não têm legenda nem "Fonte:". Confirmar com o usuário antes de assumir.
- **Imagens sem legenda:** inserir apenas o parágrafo com a imagem centralizada, sem nenhum texto adicional abaixo.

---

## Fluxo De Trabalho Padrão

> **REGRA OBRIGATÓRIA:** Antes de qualquer atividade no documento, executar os passos 1-3. Após a atividade, executar os passos 4-6 (abrir o memorial **e** Localizar na secção alterada). Sem exceções.

### Passo a Passo Completo

```bash
# ANTES — sempre executar os 3 passos abaixo ANTES de modificar o documento

# 1. Verificar git status
git status

# 2. Se houver alterações no .docx, commitar
git add "MC-AMADEU ELIAS R0.docx"
git commit -m "Salva estado atual"
git push

# 3. Salvar e fechar o Word
osascript << 'EOF'
tell application "Microsoft Word"
    if (count of documents) > 0 then
        save active document
        close active document
    end if
end tell
EOF

# ------- EXECUTAR A ATIVIDADE NO DOCUMENTO -------

# APÓS — sempre executar os passos abaixo APÓS modificar o documento (abrir + Localizar na secção tocada)

# 4. Commitar as alterações
git add "MC-AMADEU ELIAS R0.docx"
git commit -m "Descrição da alteração"
git push

# 5. Reabrir o Word com o arquivo atualizado
osascript -e 'tell application "Microsoft Word" to open "/Users/carlos_adao/Documents/2AEngenharia/Amadeu_Elias/MC-AMADEU ELIAS R0.docx"'

# 6. Posicionar na secção alterada (ajustar a string de pesquisa ao trecho editado)
osascript <<'APPLESCRIPT'
tell application "Microsoft Word"
  activate
  delay 1.5
  tell find object of selection
    clear formatting
    set content to "TEXTO_UNICO_PROXIMO_DA_ALTERACAO"
    set forward to true
    set wrap to find ask
    execute find
  end tell
end tell
APPLESCRIPT
```

### Comando "salvar"
Quando o usuário digitar `salvar`, executar automaticamente:
```bash
git add "MC-AMADEU ELIAS R0.docx" && git commit -m "Atualiza memorial" && git push
```

---

## Padrão De Substituição De Imagens

### Formatação Padrão Das Figuras
- **Largura:** 5.5 polegadas (5.5 in)
- **Alinhamento:** centralizado
- **Legenda:** parágrafo centralizado abaixo da imagem, mesmo estilo das figuras existentes
- **Fonte:** parágrafo "Fonte: Software SCIA." centralizado abaixo da legenda
- **Espaçamento:** spacing before=360, after=auto

### Estrutura De Cada Bloco De Figura
```
[parágrafo com imagem — centralizado, 5.5 in]
[parágrafo com legenda — "Figura N: Texto da legenda."]
[parágrafo — "Fonte: Software SCIA."]
```

### Script Python-docx Para Substituição De Imagens
```python
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
import copy

doc = Document("MC-AMADEU ELIAS R0.docx")

# Localizar seção pelo texto
for i, para in enumerate(doc.paragraphs):
    if "C.4" in para.text or "Trem Tipo" in para.text:
        section_start = i
        break

# Remover blocos antigos (imagem + legenda + fonte)
# Inserir novos blocos na posição correta

# Inserir imagem
def insert_image_block(doc, insert_idx, img_path, caption_text, fig_number):
    # Inserir parágrafo com imagem
    img_para = insert_paragraph_after(doc, insert_idx)
    img_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = img_para.add_run()
    run.add_picture(img_path, width=Inches(5.5))

    # Inserir legenda
    cap_para = insert_paragraph_after(doc, insert_idx + 1)
    cap_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap_run = cap_para.add_run(f"Figura {fig_number}: {caption_text}")

    # Inserir fonte
    src_para = insert_paragraph_after(doc, insert_idx + 2)
    src_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    src_para.add_run("Fonte: Software SCIA.")

doc.save("MC-AMADEU ELIAS R0.docx")
```

### Renumeração De Figuras
Após inserir/remover imagens, renumerar todas as legendas do documento:
```python
import re
fig_counter = 1
for para in doc.paragraphs:
    for run in para.runs:
        if re.match(r'Figura \d+:', run.text):
            run.text = re.sub(r'Figura \d+:', f'Figura {fig_counter}:', run.text)
            fig_counter += 1
```

---

## Padrão De Imagens Por Seção

### C.4 — Trem Tipo TB-50 (21 imagens)
Padrão de legendas por tabuleiro (3 imagens cada):
```
Carga móvel no Tabuleiro N - Pistas de tráfego X (Carga afastada do guarda rodas).
Carga móvel no Tabuleiro N - Pistas de tráfego Y (posicionado no centro da viga).
Carga móvel no Tabuleiro N - Pistas de tráfego Z (Carga afastada do guarda rodas).
```

### C.5 — Frenagem (7 imagens)
```
Carga Frenagem no Tabuleiro N.
```

### C.6 — Vento Longitudinal (3 imagens)
```
Carga de vento longitudinal nos Tabuleiros 1, 2 e 3.
Carga de vento longitudinal nos Tabuleiros 4, 5 e 6.
Carga de vento longitudinal no Tabuleiro 7.
```

### C.7 — Empuxos (4 imagens)
```
Empuxo devido à sobrecarga no Encontro 1.
Empuxo devido ao solo no Encontro 1.
Empuxo devido à sobrecarga no Encontro 2.
Empuxo devido ao solo no Encontro 2.
```

---

## Padrão De Imagens Do WhatsApp

As imagens são enviadas via WhatsApp e baixadas na pasta `~/Downloads/` com o padrão:
```
WhatsApp Image 2026-MM-DD at HH.MM.SS.jpeg
```

Para localizar imagens recentes:
```bash
ls -lt ~/Downloads/*.jpeg | head -20
```

O mapeamento entre arquivo e legenda é feito pelo **horário de envio** no WhatsApp, que aparece nas screenshots compartilhadas pelo usuário.

---

## Edição Segura De DOCX

- Preferir `python-docx` para todas as alterações.
- Evitar editar `word/document.xml` diretamente.
- Após qualquer edição, validar com:
  ```bash
  unzip -t "MC-AMADEU ELIAS R0.docx"
  ```
- Se houver corrupção, restaurar pelo Git:
  ```bash
  git checkout HEAD -- "MC-AMADEU ELIAS R0.docx"
  ```

---

## Comunicação Com O Usuário

Responder sempre em português. A cada modificação:
- "O que alterei"
- "Como conferi"
- "Se está correto"
- "O que ainda depende de revisão visual, se houver"
