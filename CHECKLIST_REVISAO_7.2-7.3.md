# Checklist de revisão — seções 7.2, 7.2.2, 7.2.3 e 7.3

**Data de geração:** alinhada ao commit que contém o script `scripts/apply_sections_72_73_images.py` e o `MC-AMADEU ELIAS R0.docx` atualizado.  
**Fonte dos ficheiros:** pasta `WhatsApp Chat - PONTE AMADEU/` (prefixos `00000xxx-PHOTO-…jpg`).

Use esta lista para rever no Word: ordem das figuras, leitura das imagens, legendas e quebras de página.

---

## Resumo numérico

| Zona | Parágrafos com imagem substituídos | Prefixos WhatsApp (ordem) |
|------|------------------------------------|---------------------------|
| 7.2.1 Paredes (Encontros 1 e 2) | 4 | `00000281`, `00000282`, `00000285`, `00000286` |
| 7.2.2 Transversinas (apoios entre tabuleiros) | 24 | `00000290` + `00000292`…`00000296` + `00000298`…`00000303` + `00000305`…`00000310` + `00000312`…`00000317` |
| 7.2.3 Pilares | 36 | `00000320`…`00000325`, `00000327`…`00000332`, `00000334`…`00000339`, `00000341`…`00000346`, `00000348`…`00000350`, `00000352`…`00000354`, `00000356`…`00000361` |
| 7.3 Infraestrutura | 54 | ver secção abaixo (ordem exata) |

**Total de imagens substituídas nesta operação:** 4 + 24 + 36 + 54 = **118**.

---

## Texto alterado (instrução explícita do chat)

| O quê | De | Para |
|--------|----|--------|
| Legenda da **Figura 232** (Bloco Encontro 1, permanentes) | `Reações nas estacas do Bloco do Encontro 1.` | `Reações Rz nas estacas do Bloco do Encontro 1.` |

Nenhum outro parágrafo de título ou lista foi reescrito.

---

## O que **não** foi alterado no texto (e porquê)

- **7.2 `MESOESTRUTURA` → `SUPERESTRUTURA`:** no documento atual, o título de secção ao nível do bloco 7.2 já está como **SUPERESTRUTURA** (não existia `MESOESTRUTURA` a corrigir nessa posição).
- **Item a) “horizontais e verticais” → só “horizontais”:** o item listado **já** está como `Diagramas dos momentos característicos horizontais.` (sem “e verticais”).
- **Remoção do item b) momentos verticais:** **não** foi encontrado parágrafo com “momentos … verticais” nessa subsecção; não houve conteúdo a apagar.
- **Quadro “ajustar” / print `00000435`:** é instrução visual; **não** foi aplicada automaticamente (rever se pretende ajuste manual de formatação).

---

## 7.3 — Ordem dos 54 ficheiros aplicada aos 54 parágrafos com imagem

Ordem = ordem de leitura do chat (excluindo o **55.º** ficheiro da lista completa: `00000434` — ver nota abaixo).

1. `00000364` … `00000365`  
2. `00000368` … `00000371`  
3. `00000372` … `00000373`  
4. `00000375` … `00000379`  
5. `00000381` … `00000382`  
6. `00000384` … `00000388`  
7. `00000390` … `00000391`  
8. `00000393`, `00000395` … `00000399`  
9. `00000401` … `00000402`  
10. `00000404` … `00000408`  
11. `00000410` … `00000411`  
12. `00000413` … `00000418`  
13. `00000420` … `00000421`  
14. `00000423` … `00000427`  
15. `00000429` … `00000430`  
16. `00000432` … `00000433`  

**Nota:** no chat existem **55** anexos numerados até `00000434` (após `00000433`). O memorial tem **54** parágrafos com imagem nesta secção; **não** se aplicou o ficheiro `00000434-PHOTO-…jpg` (ficou de fora para manter 1:1 com parágrafos existentes). Reveja no Word se falta inserir uma figura extra ou se o ficheiro `00000434` é redundante.

O anexo `00000435` (“ajustar”) **não** entra no mapeamento de substituição de imagens.

---

## Conferência técnica executada

- `unzip -t "MC-AMADEU ELIAS R0.docx"` — estrutura do pacote **sem erros** após gravação.

---

## Pontos para revisão visual obrigatória

1. **Todas as legendas** continuam com **Figura N:** coerente com o sumário (atualizar campos no Word se usar lista automática).
2. **7.2.2 e 7.2.3:** confirmar que cada imagem corresponde ao par de tabuleiros / pilares indicado na legenda à frente.
3. **7.3:** blocos com **várias imagens seguidas** entre uma legenda e outra — conferir se a ordem das capturas do SCIA corresponde ao texto “Para as cargas permanentes / acidentais”.
4. **Ficheiro `00000434` não aplicado** — decisão do revisor.

---

## Script de reprodução

```bash
python3 scripts/apply_sections_72_73_images.py
```

(Requer `python-docx` e ficheiros JPG na pasta do chat.)
