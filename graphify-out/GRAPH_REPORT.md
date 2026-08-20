# Graph Report - .  (2026-08-16)

## Corpus Check
- 69 files · ~110,484 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 682 nodes · 1699 edges · 70 communities (67 shown, 3 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 81 edges (avg confidence: 0.54)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Supabase Backend
- Utility Functions
- Supabase Backend
- Community 3
- Meeting Management
- Utility Functions
- Site Management
- Community 7
- Utility Functions
- Testing & Validation
- Data Schema
- Community 11
- Community 12
- Community 13
- Community 14
- Community 15
- Testing & Validation
- Testing & Validation
- Testing & Validation
- Community 19
- Testing & Validation
- Community 21
- Community 22
- Meeting Management
- Community 24
- Community 25
- Supabase Backend
- Community 27
- Community 28
- Community 29
- Community 30
- Meeting Management
- Supabase Backend
- Community 33
- Supabase Backend
- Supabase Backend
- Community 36
- Community 41
- Community 61

## God Nodes (most connected - your core abstractions)
1. `F()` - 77 edges
2. `Y()` - 61 edges
3. `t()` - 60 edges
4. `_returnResult()` - 48 edges
5. `constructor()` - 47 edges
6. `n()` - 42 edges
7. `join()` - 30 edges
8. `handleOperation()` - 30 edges
9. `push()` - 29 edges
10. `toString()` - 28 edges

## Surprising Connections (you probably didn't know these)
- `BUILDLy Premium v2` --rationale_for--> `Design Pattern: Content Aligned to Tabs Width`  [EXTRACTED]
  README.md → LEIA-ME.txt
- `BUILDLy Premium v2` --rationale_for--> `Two-Column Form Layout for Obra`  [EXTRACTED]
  README.md → LEIA-ME.txt
- `BUILDLy Premium v2` --rationale_for--> `Responsive Layout: Mobile and Desktop`  [EXTRACTED]
  README.md → LEIA-ME.txt
- `App Supabase (Next Generation)` --conceptually_related_to--> `Gestão de Equipes (Team Management)`  [EXTRACTED]
  MANIFEST.md → app-supabase/README.md
- `Ata de Reunião (Meeting Minutes App)` --conceptually_related_to--> `Shared Header Pattern (Company, Work, Logo)`  [EXTRACTED]
  reuniao.html → resumo-tempo.html

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Gestão de Equipes Complete Implementation (6 Phases)** — fase_1_database, fase_2_backend_api, fase_3_frontend_form, fase_4_list_view_advanced, fase_5_testes_integrados, fase_6_documentacao_final [EXTRACTED 1.00]
- **Complete CRUD Operations Test Suite** — ct_001_novo_colaborador, ct_005_editar_colaborador, ct_006_detalhes_colaborador, ct_007_remover_colaborador [EXTRACTED 1.00]
- **Filters, Search, and Sorting Capabilities** — ct_008_busca_nome, ct_009_filtro_empresa, ct_010_filtro_situacao, ct_011_filtro_frente, ct_012_ordenacao, ct_013_filtros_combinados [EXTRACTED 1.00]
- **Weather Data Collection & Reporting** — resumo_tempo_html_mapa_mensal, resumo_tempo_html_resumo_chuva, resumo_tempo_html_calcular_resumo_chuva, resumo_tempo_html_texto_tempo [EXTRACTED 1.00]
- **Meeting Documentation & Action Tracking** — reuniao_html_dados_reuniao, reuniao_html_participantes, reuniao_html_pauta, reuniao_html_topicos_discutidos, reuniao_html_plano_acao [EXTRACTED 1.00]
- **Shared PWA Architecture Across Apps** — shared_header_pattern, shared_navigation_tabs, shared_toast_notifications, resumo_tempo_html_concrete_design_system, reuniao_html_concrete_design_system [INFERRED 0.85]

## Communities (70 total, 3 thin omitted)

### Community 0 - "Supabase Backend"
Cohesion: 0.08
Nodes (89): _acquireLock(), _adminDeletePasskey(), _adminListPasskeys(), _approveAuthorization(), _authenticate(), _challenge(), _challengeAndVerify(), _createCustomProvider() (+81 more)

### Community 1 - "Utility Functions"
Cohesion: 0.05
Nodes (73): applyTransformOptsToQuery(), copy(), createBucket(), createIndex(), createSignedUploadUrl(), createSignedUrl(), createSignedUrls(), deleteBucket() (+65 more)

### Community 3 - "Community 3"
Cohesion: 0.09
Nodes (35): bn(), Bt(), catch(), Cn(), cr(), createNamespace(), createNamespaceIfNotExists(), fetchRequest() (+27 more)

### Community 4 - "Meeting Management"
Cohesion: 0.08
Nodes (28): Calculate Rain Summary Function, Rustic Concrete Design System, RDO Historical Data, Mapa Mensal do Tempo, Mobile-First Responsive Design, Progressive Web App Capabilities, Render Daily List Function, Render Monthly Map Function (+20 more)

### Community 5 - "Utility Functions"
Cohesion: 0.09
Nodes (26): channel(), clone(), constructor(), getChannel(), getChannels(), _getPayloadRecords(), getSocket(), _handleTokenChanged() (+18 more)

### Community 6 - "Site Management"
Cohesion: 0.11
Nodes (22): areaModulo, atualizarObraAtiva(), btnLogout, btnRecolherSidebar, carregarObras(), entrarNoApp(), formLogin, loginErro (+14 more)

### Community 7 - "Community 7"
Cohesion: 0.20
Nodes (20): _autoRefreshTokenTick(), _callRefreshToken(), _debug(), dispose(), _emitInitialSession(), gr(), _handleVisibilityChange(), initialize() (+12 more)

### Community 8 - "Utility Functions"
Cohesion: 0.12
Nodes (19): cloneRequestState(), containedBy(), contains(), delete(), explain(), _getSessionFromURL(), ilikeAllOf(), ilikeAnyOf() (+11 more)

### Community 9 - "Testing & Validation"
Cohesion: 0.11
Nodes (19): test-checklist.html Interactive Test Tracker, CT-001: New Collaborator Flow, CT-002: Name Validation, CT-003: Date Validation, CT-004: Unique Matricula Validation, CT-005: Edit Collaborator, CT-006: View Details, CT-007: Delete Collaborator (+11 more)

### Community 10 - "Data Schema"
Cohesion: 0.17
Nodes (17): ai(), assertFieldSize(), _binaryDecode(), binaryEncode(), _binaryEncodeUserBroadcastPush(), decode(), decodeBroadcast(), decodePush() (+9 more)

### Community 11 - "Community 11"
Cohesion: 0.24
Nodes (16): clearHeartbeats(), _handleNodeJsRaceCondition(), hasLogger(), heartbeatCallback(), heartbeatTimeout(), isClosed(), isErrored(), onConnClose() (+8 more)

### Community 12 - "Community 12"
Cohesion: 0.23
Nodes (15): build(), connectWithFallback(), makeRef(), off(), on(), onClose(), onError(), onMessage() (+7 more)

### Community 13 - "Community 13"
Cohesion: 0.25
Nodes (15): _cancelPendingDisconnect(), connect(), disconnect(), isConnecting(), isDisconnecting(), _isManualToken(), log(), remove() (+7 more)

### Community 14 - "Community 14"
Cohesion: 0.14
Nodes (14): add(), eq(), gt(), gte(), ilike(), imatch(), in(), is() (+6 more)

### Community 15 - "Community 15"
Cohesion: 0.21
Nodes (12): canPush(), _fetchWithTimeout(), hasReceived(), httpSend(), isJoined(), isJoining(), leave(), leaveOpenTopic() (+4 more)

### Community 16 - "Testing & Validation"
Cohesion: 0.18
Nodes (10): description, devDependencies, @playwright/test, name, scripts, test, test:debug, test:ui (+2 more)

### Community 17 - "Testing & Validation"
Cohesion: 0.20
Nodes (11): BUILDLy Premium v2, Check-in (Task Derivation App), Custos (Invoice Control), Local Data Persistence via localStorage, Design Pattern: Content Aligned to Tabs Width, Two-Column Form Layout for Obra, GitHub Pages Single Page Application (SPA), Google Sheets Integration via Google Apps Script (+3 more)

### Community 18 - "Testing & Validation"
Cohesion: 0.20
Nodes (10): 0004_expand_colaborador_operacional.sql, Matrícula (Employee ID), Nome (Full Name), Triggers for Collaborator Validation, validar_datas_colaborador PL/pgSQL Function, validar_matricula_unica PL/pgSQL Function, validar_nome_colaborador PL/pgSQL Function, v_colaboradores_ativos_por_frente View (+2 more)

### Community 19 - "Community 19"
Cohesion: 0.22
Nodes (10): cancelRefEvent(), cancelTimeout(), destroy(), filterBindings(), isMember(), joinRef(), matchReceive(), reset() (+2 more)

### Community 20 - "Testing & Validation"
Cohesion: 0.20
Nodes (10): CT-018: Integration with Efetivo Module, Efetivo Module (Daily Presence), equipes.js Frontend Module, Fase 2: Backend API & Validations, Fase 3: Frontend Form with 3 Tabs, Fase 4: Advanced List View with Filters, Fase 6: Documentation Consolidation, Gestão de Equipes (Team Management) (+2 more)

### Community 21 - "Community 21"
Cohesion: 0.31
Nodes (9): ajax(), batchSend(), close(), closeAndRetry(), endpointURL(), isActive(), ontimeout(), poll() (+1 more)

### Community 22 - "Community 22"
Cohesion: 0.22
Nodes (9): appendParams(), Fn(), jr(), match(), Nn(), processResponse(), serialize(), vr() (+1 more)

### Community 23 - "Meeting Management"
Cohesion: 0.25
Nodes (8): 20 Campos Operacionais de Canteiro, Cargo (Job Title), Colaborador Data Model with 20 Operational Fields, Data de Admissão, Frente de Serviço (Work Front), Operational Canteiro vs RH/eSocial Distinction, Situação (Status: ativo/inativo/afastado/licença), Tipo Mão de Obra (MOI/MOD/Terceirizado)

### Community 24 - "Community 24"
Cohesion: 0.29
Nodes (8): createTable(), createTableIfNotExists(), dropTable(), listTables(), loadTable(), O(), tableExists(), updateTable()

### Community 25 - "Community 25"
Cohesion: 0.25
Nodes (8): detectEnvironment(), dt(), ft(), getWebSocketConstructor(), _initializeOptions(), isWebSocketSupported(), onHeartbeat(), _wrapHeartbeatCallback()

### Community 26 - "Supabase Backend"
Cohesion: 0.25
Nodes (8): isFilterValueEqual(), _notThisChannelEvent(), _performAuth(), qe(), subscribe(), _updateFilterMessage(), updateJoinPayload(), _updatePostgresBindings()

### Community 27 - "Community 27"
Cohesion: 0.57
Nodes (6): abrirFormularioEdicao(), limparFormulario(), mostrarDetalhes(), removerColaborador(), renderModuloEquipes(), salvarColaborador()

### Community 28 - "Community 28"
Cohesion: 0.33
Nodes (6): carregarOuCriarRdo(), RDO_ABAS, RDO_CONDICOES_CLIMA, RDO_PERIODOS, RDO_STATUS_ROTULO, renderModuloRDO()

### Community 29 - "Community 29"
Cohesion: 0.33
Nodes (7): ae(), b(), ie(), ne(), re(), sr(), te()

### Community 30 - "Community 30"
Cohesion: 0.38
Nodes (7): He(), onJoinPayload(), onLeavePayload(), state(), transformState(), Ve(), We()

### Community 31 - "Meeting Management"
Cohesion: 0.47
Nodes (5): diasUteisEntre(), formatarDataCurta(), RDO_DASH_CORES_CLIMA, RDO_DASH_STATUS_ROTULO, renderRdoDashboard()

### Community 32 - "Supabase Backend"
Cohesion: 0.40
Nodes (5): 0001_schema_inicial.sql Migration, 0002_rls_autenticado.sql RLS Policies, 0003_seed_obra_inicial.sql Initial Data, Fase 1: Database Expansion, Supabase Backend (PostgreSQL + Auth + RLS)

### Community 33 - "Community 33"
Cohesion: 0.40
Nodes (5): ci(), hi(), li(), Si(), xi()

### Community 34 - "Supabase Backend"
Cohesion: 0.40
Nodes (5): connectionState(), flushSendBuffer(), isConnected(), _reconnectAuth(), _waitForAuthIfNeeded()

### Community 35 - "Supabase Backend"
Cohesion: 0.40
Nodes (5): App Supabase (Next Generation), Buidly (Supabase Development), Buildly2 (Legacy Production), Buildly3 Consolidated Repository, Multi-Tenancy via Obra Table

### Community 36 - "Community 36"
Cohesion: 0.67
Nodes (4): Ct(), St(), Tt(), wt()

## Knowledge Gaps
- **74 isolated node(s):** `TITULOS_MODULO`, `obras`, `telaLogin`, `telaApp`, `formLogin` (+69 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Gestão de Equipes (Team Management)` connect `Testing & Validation` to `Supabase Backend`, `Testing & Validation`, `Supabase Backend`, `Meeting Management`?**
  _High betweenness centrality (0.005) - this node is a cross-community bridge._
- **Why does `F()` connect `Supabase Backend` to `Utility Functions`, `Supabase Backend`, `Community 3`, `Community 7`, `Utility Functions`, `Community 12`?**
  _High betweenness centrality (0.004) - this node is a cross-community bridge._
- **Why does `Fase 5: Integrated E2E Tests` connect `Testing & Validation` to `Testing & Validation`?**
  _High betweenness centrality (0.004) - this node is a cross-community bridge._
- **Are the 26 inferred relationships involving `t()` (e.g. with `bn()` and `_emitInitialSession()`) actually correct?**
  _`t()` has 26 INFERRED edges - model-reasoned connections that need verification._
- **What connects `TITULOS_MODULO`, `obras`, `telaLogin` to the rest of the system?**
  _74 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Supabase Backend` be split into smaller, more focused modules?**
  _Cohesion score 0.07533197139938713 - nodes in this community are weakly interconnected._
- **Should `Utility Functions` be split into smaller, more focused modules?**
  _Cohesion score 0.0502283105022831 - nodes in this community are weakly interconnected._