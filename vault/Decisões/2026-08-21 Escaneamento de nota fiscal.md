---
data: 2026-08-21
status: parcial
tags: [decisão, custos, nota-fiscal, ocr]
---

# Escaneamento de nota fiscal: câmera sim, OCR ainda não

**Status:** 🟡 Parcialmente decidido · **PR:** #2 (`claude/custos-foto-nota`)

---

## Contexto

Pendência antiga, nunca decidida: como escanear nota fiscal no app de Custos. Duas perguntas
estavam em aberto:

1. Usar a câmera do iPhone?
2. Guardar só o cabeçalho da nota, ou os itens também?

---

## Decisão

**1. Câmera:** sim — `<input type="file" accept="image/*" capture="environment">`. No Safari do
iPhone isso abre a câmera direto, sem precisar de biblioteca nem permissão extra. É a solução
que funciona hoje, sem dependência nova.

**2. O que guardar:** a foto entra **junto** do cabeçalho e dos itens que já existiam — não
substitui nada. O formulário de NF já capturava número, série, data, fornecedor, categoria,
responsável, observações e a lista de itens; a foto é referência visual da nota original, para
conferência posterior.

Compressão: mesmo esquema já usado no RDO (`comprimirFoto`, máx. 1280px, qualidade 0.72).

**3. OCR — adiado.** Ler os dados automaticamente da foto depende de escolher uma API de visão
e de como cobrar por ela. Ficou fora do escopo deste PR.

---

## Consequências

- Uma NF com foto ocupa bem mais espaço no `localStorage`. Por isso a gravação passou a ter
  `try/catch`: se a cota estourar, o usuário é avisado em vez de perder a nota em silêncio.
  Ver [[Notas/Armazenamento Local]].
- Custos continua **só local** — o endpoint `custos/salvar` existe no backend mas nenhum
  front-end chama. Fotos ficam no aparelho, não no Drive (diferente do RDO). Se Custos for
  ligado à planilha um dia, a foto vai precisar ir para o Drive como as do RDO, não em base64
  na célula.

---

## Pendente

- Testar no iPhone real: confirmar que `capture="environment"` abre a câmera e não a galeria.
- Confirmar que a foto comprimida continua legível o bastante para reler a nota depois. Se não
  estiver, subir a qualidade — mas aí a pressão sobre a cota aumenta.
- Decidir sobre OCR (mesma dependência de API de IA do robô, que já usa Anthropic — pode ser o
  caminho natural).

---

## Relacionado

- [[Notas/Armazenamento Local]]
- [[Projetos/BUILDLy Premium]]
