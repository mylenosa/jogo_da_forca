# 🎮 Jogo da Forca - Aplicação Web com Django

Aplicação web do clássico jogo da forca, desenvolvida com Django e baseada em Class Based Views.

## ✅ Funcionalidades Implementadas

- Professores podem se cadastrar, criar **temas** e **palavras** com **dica**.
- Alunos podem jogar livremente (com ou sem login).
- Tela interativa do jogo da forca, com contador de erros e dica.
- Registro de jogadas dos alunos (palavra, acertos, erros, data).
- Interface separada para professores e alunos.
- Filtragem por tema para iniciar um jogo.
- Layout simples e funcional com Bootstrap.
- Projeto pronto para deploy no PythonAnywhere.

## 📌 A fazer (próximas etapas)

- Filtro por professor e tema antes do jogo.
- Relatório visual de jogadas para professores.
- Geração de PDF da atividade por tema.
- Opção de exigir login do aluno para jogar certos temas.
- Melhorias visuais no jogo (desenho da forca, responsividade).

## 🧩 Estrutura

- `tema/` - Temas criados por professores.
- `palavra/` - Palavras com dicas associadas aos temas.
- `jogada/` - Histórico de jogadas dos alunos.
- `templates/` - Páginas HTML do jogo, login, cadastro e listagens.

## 👥 Requisitos de Usuário

### Professores
- Criam temas e palavras
- Visualizam jogadas
- Podem gerar PDF (futuramente)

### Alunos
- Jogam sem login (ou com, se necessário)
- Podem escolher tema
- Resultados são registrados

## 🚀 Como rodar localmente

```bash
git clone https://github.com/seu-usuario/jogo_da_forca.git
cd jogo_da_forca
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
