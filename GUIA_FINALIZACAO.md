# 🚀 Guia de Finalização — Mission Control AI

Este documento NÃO entra na entrega final — é só para você seguir o
passo-a-passo de finalização do projeto até estar pronto para submeter.

---

## Checklist macro (na ordem)

- [ ] 1. Testar o projeto rodando localmente
- [ ] 2. Capturar os 2 prints obrigatórios
- [ ] 3. Criar repositório no GitHub
- [ ] 4. Subir o projeto no GitHub
- [ ] 5. Gravar o vídeo de demonstração (3 min)
- [ ] 6. Subir o vídeo no YouTube como "Não listado"
- [ ] 7. Atualizar o README com o link real do vídeo
- [ ] 8. Atualizar o .txt com os links reais
- [ ] 9. Submeter o .txt no portal da FIAP

⏱️ Tempo total estimado: **~2 horas** (a parte do código já está feita).

---

## 1️⃣ Testar o projeto rodando localmente (15 min)

### 1.1. Descompactar e entrar na pasta

Descompacte o ZIP em algum lugar do seu PC. Abra o **Visual Studio Code**
(ou outro editor) na pasta `mission-control-ai/`.

### 1.2. Criar ambiente virtual e instalar dependências

Abra o terminal integrado do VS Code (Ctrl+`) e rode:

**Windows:**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Se a ativação der erro sobre "execution policy", rode antes:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 1.3. Configurar o .env

Copia o arquivo de exemplo:
```powershell
copy .env.example .env
```

Abre o arquivo `.env` no editor e cola sua chave real da Ollama Cloud:
```
OLLAMA_API_KEY=sua_chave_real_que_voce_gerou_no_ollama_dot_com
```

⚠️ **Confirma que o arquivo `.env` (sem o `.example`) está listado no `.gitignore`.**
Eu já configurei isso, mas vale conferir antes do primeiro commit.

### 1.4. Rodar

```powershell
python main.py
```

**O que deve acontecer:**
1. Banner ASCII ciano "Mission Control AI" aparece
2. Painel de boas-vindas mostra "Status do engine: ONLINE" em verde
3. Aparece o prompt `>` aguardando input

### 1.5. Testar a IA

Digita pergunta livre:
```
> Como está a missão?
```

Deve aparecer um spinner "Mission Control AI processando..." e em 5-15 segundos
um painel com 3 seções: **Diagnóstico técnico**, **Impacto terrestre**,
**Recomendação operacional**.

Se aparecer erro `[ERRO] Falha ao consultar Ollama Cloud:`, verifica:
- Sua chave no `.env` está correta (sem espaços, sem aspas)?
- Você tem conexão com a internet?
- O Ollama Cloud não está fora do ar?

### 1.6. Testar os 3 cenários

```
> /cenario nominal
[deve mostrar painel com borda VERDE, IA falando que está tudo OK]

> /cenario atencao
[deve mostrar painel com borda AMARELA/AMBAR, IA explicando 3 parâmetros degradados]

> /cenario critico
[deve mostrar painel com borda VERMELHA, IA explicando falha múltipla
 e mencionar que o Modo de Segurança foi ativado automaticamente]
```

### 1.7. Outros comandos para testar

```
> /status      → resumo da telemetria sem chamar IA
> /help        → tabela de comandos
> /about       → informações da equipe
> /clear       → limpa a tela
> /exit        → encerra
```

---

## 2️⃣ Capturar os 2 prints obrigatórios (5 min)

O briefing exige **pelo menos 2 prints reais** do sistema funcionando
(Frente 2, README completo, vale parte dos 1,5 pts).

### Print 1 — Operação nominal

1. Rode `/cenario nominal`
2. Espera a resposta da IA aparecer
3. Use **Win + Shift + S** para recortar a janela do terminal inteira
4. Cola no Paint, salva como **`screenshot_normal.png`**
5. Coloca o arquivo em `mission-control-ai/assets/`

### Print 2 — Cenário crítico

1. Rode `/cenario critico`
2. Espera a resposta da IA aparecer (deve mencionar "Modo de Segurança")
3. Use **Win + Shift + S** para recortar
4. Salva como **`screenshot_alerta.png`**
5. Coloca em `mission-control-ai/assets/`

> **Importante:** o README já está configurado para procurar essas duas
> imagens com esses nomes. Se você usar nomes diferentes, edita o README
> antes de subir.

---

## 3️⃣ Criar repositório no GitHub (5 min)

1. Acessa **github.com** e loga
2. Clica no botão **+** no topo direito → **New repository**
3. Preenche:
   - **Repository name:** `mission-control-ai` (ou nome de sua preferência)
   - **Description:** `Sistema de monitoramento IoT de satélite GNSS com IA generativa - GS 2026.1 FIAP`
   - **Visibility:** **Public** (obrigatório pelo briefing — repositório privado perde 1,5 pts)
   - ❌ **NÃO marque** "Add README" (você já tem um)
   - ❌ **NÃO marque** "Add .gitignore"
4. Clica **Create repository**

---

## 4️⃣ Subir o projeto no GitHub (10 min)

### Opção A — Pela interface web (mais fácil)

1. Na página do repo recém-criado (que está vazio), clica em
   **"uploading an existing file"** (link azul no meio da página).
2. **CRÍTICO:** antes de arrastar, certifica que **o arquivo `.env` NÃO está na pasta**.
   Se estiver, deleta ele (você sempre pode recriar copiando de `.env.example`).
3. Arrasta a pasta `mission-control-ai/` inteira para a área indicada.
4. Em **Commit changes**:
   - **Commit message:** `Entrega final - GS 2026.1 Mission Control AI / MobilitySat`
5. Clica **Commit changes**.

### Opção B — Por linha de comando (mais profissional)

```bash
cd mission-control-ai
git init
git config user.name "João Pedro Quagliano"
git config user.email "joaopedroquagliano@gmail.com"

# CRÍTICO: confirmar que .env NÃO está sendo trackado
git status
# Se aparecer .env na lista, ALGO ERRADO. Confere o .gitignore.

git add .
git commit -m "Entrega final - GS 2026.1 Mission Control AI / MobilitySat"
git branch -M main
git remote add origin https://github.com/SEU-USUARIO/mission-control-ai.git
git push -u origin main
```

### Verificação crítica

Depois do upload, **abre o repositório em uma janela anônima do navegador** e
**procura por "OLLAMA_API_KEY="** na barra de busca do GitHub.
**Se aparecer sua chave real, você commitou o `.env` por engano:**
- Penalidade automática: -2,0 pontos
- **Revoga sua chave AGORA mesmo na Ollama Cloud** (Settings → API Keys → Delete)
- Gera nova chave
- Limpa o histórico do Git (procura "BFG Repo-Cleaner" no Google) ou cria
  um novo repositório do zero sem o `.env`

---

## 5️⃣ Gravar o vídeo de demonstração (20 min)

### Requisitos do briefing:
- ✅ Máximo **3 minutos** (acima disso: -0,5 pt)
- ✅ Apresentar integrantes no início (rosto, voz ou texto)
- ✅ Sistema rodando ao vivo (não slides parados)
- ✅ Mostrar IA respondendo em tempo real
- ✅ Demonstrar pelo menos um cenário de alerta
- ✅ Áudio e tela legíveis

### Roteiro sugerido (3 minutos)

**[00:00–00:15] Apresentação da equipe**
- Texto sobre frame: "João Pedro Quagliano - RM 570233 / Matheus Levi Dagel - RM 571961 / Turma 1CCPH"
- Voz em off (ou narrando): "Mission Control AI, trilha MobilitySat, Global Solution 2026.1"

**[00:15–00:45] Contexto e apresentação do projeto**
- Tela inicial do sistema (banner ASCII + painel de boas-vindas)
- Narração:
  > "Construímos um sistema de monitoramento de satélite GNSS — o tipo
  > de satélite que sustenta toda a logística rodoviária, agricultura
  > de precisão e aviação regional no Brasil. Quando o satélite degrada,
  > frotas perdem rota, tratores autônomos param, aviões abortam pouso.
  > O sistema avisa o engenheiro antes do impacto."

**[00:45–01:30] Demonstração — cenário nominal**
- Digita `/cenario nominal`
- Mostra a IA respondendo com diagnóstico técnico + impacto terrestre + recomendação
- Narração:
  > "Em operação nominal, a IA confirma que frotas e tratores estão
  > recebendo posicionamento centimétrico sem degradação."

**[01:30–02:30] Demonstração — cenário crítico**
- Digita `/cenario critico`
- Mostra a IA respondendo, destaque o painel vermelho
- Aponta com o mouse para a linha "MODO DE SEGURANÇA ATIVADO automaticamente"
- Narração:
  > "Aqui o sistema detectou falha múltipla — drift atômico fora do
  > limite, sinais L1 e L5 degradados. **Antes** de a IA responder, o
  > código Python já tinha executado a resposta automatizada: migrou
  > tráfego para o canal de segurança L5. A IA agora explica o que
  > aconteceu, qual o impacto na Terra, e o que o engenheiro deve fazer
  > nas próximas horas."

**[02:30–02:55] Fechamento — proposta de valor**
- Volta para o painel do README ou mostra a seção "Proposta de valor"
- Narração:
  > "Se este satélite operar saudável por um ano, são R$ 26 milhões
  > economizados em combustível de frotas, R$ 87 milhões em fertilizantes
  > para 350 mil hectares de agricultura de precisão, e 2.500 toneladas
  > de CO₂ evitadas. Esse é o impacto terrestre que justifica monitorar
  > satélites com IA."

**[02:55–03:00] Encerramento**
- "Obrigado pela atenção."

### Ferramentas

- **Gravação de tela:** OBS Studio (gratuito) ou Loom (mais simples)
- **Áudio:** microfone do notebook serve, só fala perto
- **Edição:** não precisa — gravação em uma tomada com pausas naturais funciona melhor que vídeo super-editado

---

## 6️⃣ Subir o vídeo no YouTube como "Não listado" (5 min)

1. Vai em **youtube.com** logado
2. Clica em **Criar** (ícone de câmera com +) → **Enviar vídeo**
3. Seleciona o arquivo do vídeo
4. Em **Detalhes:**
   - Título: `Mission Control AI - MobilitySat | GS 2026.1 FIAP`
   - Descrição: cola o link do GitHub
5. Em **Visibilidade:**
   - Seleciona **"Não listado"** (importante! Não é privado, é não listado)
6. Publica
7. **Copia o link do vídeo** que aparece (algo tipo `https://www.youtube.com/watch?v=ABC123`)

---

## 7️⃣ Atualizar o README com o link real do vídeo (2 min)

No arquivo `README.md` local, encontra essa linha:

```
🔗 **[Assistir demonstração no YouTube](https://www.youtube.com/watch?v=SUBSTITUIR_AQUI)**
```

Substitui pela URL real. Salva o arquivo.

Sobe o README atualizado no GitHub (commit novo) ou edita direto pela
interface web do GitHub.

---

## 8️⃣ Atualizar o .txt com os links reais (2 min)

Abre o arquivo `GS_2026_1_Grupo_1CCPH.txt`. Substitui as 2 linhas:

**De:**
```
Link do repositório GitHub: https://github.com/SUBSTITUIR_USUARIO/mission-control-ai
Link do vídeo de demonstração: https://www.youtube.com/watch?v=SUBSTITUIR_ID_VIDEO
```

**Para os links reais que você acabou de obter.**

Salva.

---

## 9️⃣ Submeter o .txt no portal da FIAP

1. Acessa o portal institucional
2. Vai na seção da GS 2026.1 - Prompt Engineering and AI
3. **Upload do arquivo `GS_2026_1_Grupo_1CCPH.txt`**

### Checklist final antes de clicar "enviar":

- [ ] O `.txt` tem nomes, RMs, modalidade, GitHub e YouTube preenchidos
- [ ] O GitHub está **público** (testa em janela anônima)
- [ ] O vídeo do YouTube está **não listado** e o link funciona
- [ ] O **link do YouTube aparece em DOIS lugares**: no .txt **e** no README
- [ ] A pasta `assets/` no GitHub tem os 2 prints
- [ ] O arquivo `.env` **NÃO está no GitHub** (verifica de novo!)
- [ ] O `requirements.txt` está presente

Se todos os itens estão ok, **submete**. Não espera o último dia.

---

## 🆘 Solução de problemas

### "ImportError: No module named 'rich'"
Você esqueceu de ativar o ambiente virtual antes de rodar. Roda
`.venv\Scripts\Activate.ps1` (Windows) ou `source .venv/bin/activate` (Linux/Mac).

### "[ERRO] Falha ao consultar Ollama Cloud"
- Confere a chave no `.env`
- Testa a chave manualmente em https://ollama.com no playground
- Verifica conexão com a internet

### Banner ASCII aparece "quebrado" no Windows
O `cmd.exe` antigo não renderiza Unicode bem. Use o **Windows Terminal**
(vem com Windows 10/11) ou **PowerShell 7**.

### Acentuação aparece quebrada
O código usa só ASCII no terminal por segurança. Se quiser acentos,
configura o terminal pra UTF-8 com `chcp 65001` antes de rodar.

---

## 📊 Como estamos contra a rubrica (estimativa)

| Frente | Peso | O que entreguei | Estimativa |
|---|---|---|---|
| 1 - Entrega correta | 1,0 | Tudo organizado, .txt completo | 1,0 |
| 2 - README completo | 1,5 | README detalhado com Frente 6 | 1,4-1,5 |
| 3 - Uso de IA via Ollama | 3,0 | System prompt com few-shot, dados injetados dinamicamente | 2,8-3,0 |
| 4 - Funcionalidades | 2,5 | 5 parâmetros, alertas em Python, ação automatizada | 2,3-2,5 |
| 5 - Vídeo | 1,0 | Depende de você gravar bem | 0,8-1,0 |
| 6 - Proposta de valor | 1,0 | Frente 6 do README com dados reais do Brasil | 0,9-1,0 |
| **TOTAL** | **10,0** | | **9,2-10,0** |

Frente 5 (vídeo) é o item mais sensível — se você gravar lendo roteiro
ou pular algum critério, a nota dessa frente cai. Segue o roteiro acima
e ensaia umas 2 vezes antes de gravar pra valer.

Boa apresentação! 🚀
