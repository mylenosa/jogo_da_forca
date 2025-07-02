# Jogo da Forca

Aplicação web Django para um jogo da forca com gerenciamento de temas e palavras por professores, e acesso para alunos jogarem com ou sem cadastro.

---

## Funcionalidades principais

- Cadastro e login para professores (usuários staff) para criação/edição/exclusão de temas e palavras.
- Alunos podem jogar sem cadastro, ou se cadastrar para ter histórico.
- Escolha de temas e palavras para jogar, filtrando por tema ou professor.
- Interface responsiva com Bootstrap.
- Professores podem gerar PDFs das atividades para imprimir.
- Relatórios para professores com dados de jogadas por aluno, tema e período.
- Deploy simples para servidores como PythonAnywhere.

---

## Requisitos

- Python 3.8+
- Django 5.2.3
- Bootstrap 5 (via CDN)
- Pacotes listados em `requirements.txt`

---

## Instalação rápida

```bash
git clone <URL_DO_REPOSITORIO>
cd jogo-da-forca
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

## Usuários de teste incluídos

| Usuário       | Tipo      | Senha       |
| ------------- | --------- | ----------- |
| higor.lauer   | aluno     | alunoifro   |
| marcos.faino  | professor | alunoifro   |

---

## Estrutura do projeto

- `forca/` — App principal do jogo e gerenciamento.
- `templates/` — Templates HTML baseados em Bootstrap.
- `static/` — Arquivos estáticos (CSS, JS, imagens).
- `models.py` — Modelos para Tema, Palavra, Aluno, Partida e Jogada.
- `views.py` — Views baseadas em Classes (Class-Based Views).
- `urls.py` — Rotas da aplicação.
- `forms.py` — Formulários customizados.
- `requirements.txt` — Dependências do projeto.

---

## Regras e fluxos

- Professores criam temas e adicionam palavras com dicas e textos extras.
- Alunos escolhem tema ou professor para jogar.
- Jogo da forca com sistema de erros, dicas e palavras randomizadas.
- Professores visualizam relatórios e geram PDFs para impressão.

---

## Deploy

Projeto pode ser facilmente implantado em servidores como PythonAnywhere, Heroku, etc., seguindo a documentação oficial de deploy do Django.

---

## Contato

Para dúvidas ou sugestões, entre em contato com o professor ou mantenedor do projeto.
