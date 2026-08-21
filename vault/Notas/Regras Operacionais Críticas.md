---
criado: 2026-08-21
tags: [nota, regras, crítico]
---

# Regras Operacionais Críticas

Cada item aqui vem de um erro que já aconteceu de verdade e custou tempo ou dado. Não são
preferências de estilo.

---

## Dados do usuário

1. **Nunca recomendar limpar dados do site / Safari como solução de cache.** Isso apaga o
   `localStorage` inteiro — cadastro e histórico. Já foi violado uma vez por engano no app
   antigo e causou a pior crise daquela sessão. Se o app não atualizar visualmente: fechar e
   reabrir, e aguardar a propagação do GitHub Pages (1–2 min).

2. **Nunca pedir para o usuário redigitar cadastro por causa de bug.** Se dados sumirem ou
   aparecerem misturados depois de uma atualização, a correção é restaurar do backup
   (nuvem ou arquivo) automaticamente — nunca mandar apagar colaborador por colaborador.

3. **Nunca inventar dado operacional** (efetivo, quantidade, atividade) em RDO. É documento
   contratual. Faltou dado, fica em branco ou marcado como pendente — nunca estimado, nunca
   inferido.

4. **Nunca deixar o app cair silenciosamente em estado vazio / obra sem nome.** No app antigo,
   `backupNuvem()` usava `state.obra.nome || 'Obra'` como nome de pasta: toda vez que o nome
   vinha vazio, criava uma pasta nova no Drive — resultado, 11+ pastas duplicadas "Suzano -
   ETA". Nome vazio é sinal de perda de estado: deve alertar, não seguir em frente.

5. **Nunca limpar uma aba da planilha que já tem dados.** Um `clearContents()` incondicional em
   `salvarDiario()` já apagou histórico inteiro de RDO em produção. Cabeçalho só se cria quando
   a aba está genuinamente vazia (`getLastRow() === 0`).

---

## Publicação e teste

6. **Integrações não funcionam em arquivo local.** Abrir o `.html` direto (`file://`) bloqueia
   POST — planilha, fotos e backup só funcionam no endereço publicado (GitHub Pages).

7. **Atualizar o Apps Script exige nova implantação.** Colar o código e salvar não põe nada no
   ar: Implantar → Gerenciar implantações → editar (lápis) → Nova versão → Implantar. Sem esse
   passo final, o `/exec` continua servindo a versão anterior.

8. **Scripts de entrega precisam ser idempotentes.** As mudanças chegam ao usuário como scripts
   Python que editam os HTML por trechos exatos. Rodar duas vezes não pode duplicar a alteração.

---

## Código

9. **O backend Apps Script não é versionado por git.** O que roda é o que está colado no projeto
   Google. Se for apagado, git não recupera — só a Lixeira do Drive (~30 dias). Ver
   [[Decisões/2026-08-21 Backend recuperado da Lixeira]].

10. **Não presumir simetria entre front-end e backend.** Existem `fetch()` sem endpoint
    correspondente (`foto&action=base64`) e endpoints que ninguém chama (`custos/salvar`).
    Reconstruir backend a partir do front-end perde tudo que nenhum `fetch()` exercita.

11. **Toda escrita no backend é upsert.** A sincronização automática de 2 em 2 minutos reenvia
    os mesmos registros; sem upsert, cada ciclo duplica linha.

12. **Elemento que precisa aparecer em toda aba tem que ser flutuante.** As 10 telas fora da
    Home têm cabeçalho próprio e não reservam espaço para o cabeçalho do shell. Ver
    [[Decisões/2026-08-21 Robô de IA visível em todas as abas]].

13. **Gravação que pode conter imagem precisa de `try/catch`.** Cota de `localStorage` estoura
    sem aviso e o registro se perde em silêncio. Ver [[Notas/Armazenamento Local]].

---

## Relacionado

- [[Notas/Armazenamento Local]]
- [[Notas/Contrato do Backend]]
- [[Projetos/BUILDLy Premium]]
