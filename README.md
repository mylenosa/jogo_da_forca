# Jogo da Forca - Projeto Django

## Descrição

Este projeto é uma aplicação web de um jogo da forca, desenvolvido em Django utilizando Class Based Views (CBV). 

O sistema contempla dois tipos de usuários principais: **professores** e **alunos**. Professores podem criar temas e adicionar palavras com dicas, enquanto alunos podem jogar escolhendo temas ou professores, mesmo sem estar logados.

---

## O que foi implementado

- **Autenticação e cadastro:**  
  - Professores (usuários staff) podem se cadastrar e acessar área restrita.  
  - Alunos podem se cadastrar e jogar sem login, ou com login caso exigido.

- **Gerenciamento de temas e palavras (somente professores):**  
  - Professores criam, editam e excluem temas.  
  - Podem adicionar palavras a temas, com texto, dicas e informações extras opcionais.

- **Jogabilidade:**  
  - Alunos escolhem tema ou professor para jogar.  
  - Palavra é selecionada aleatoriamente para o jogo da forca.  
  - Sistema registra erros e acertos do aluno.  
  - API simples para obter palavra e salvar jogadas.

- **Interface:**  
  - Uso do Bootstrap 5 para o front-end.  
  - Layout responsivo e navegação básica.

- **Relatórios e PDF (parcial):**  
  - Área para professores visualizarem temas criados.  
  - (Implementação do PDF e relatórios completos pendente).

---

## O que falta para cumprir todos os requisitos

- **Cadastro obrigatório para alunos, quando exigido pelo professor.**  
- **Geração de PDFs das atividades para impressão.**  
- **Relatórios detalhados:**  
  - Visualizar quais alunos jogaram por tema e por período (datas).  
- **Deploy:**  
  - Publicar a aplicação em servidor como PythonAnywhere, Heroku ou similar.  
- **Testes automatizados e validação completa dos formulários e views.**  
- **Melhorias na UI/UX do jogo, incluindo feedbacks visuais mais claros.**  
- **Sistema de permissões refinado, garantindo que somente professores possam criar/editar/excluir.**

---

## Usuários de teste incluídos

| Usuário       | Tipo      | Senha       |
| ------------- | --------- | ----------- |
| higor.lauer   | aluno     | alunoifro   |
| marcos.faino  | professor | alunoifro   |

---

## Como rodar o projeto

```bash
python -m venv venv
source venv/bin/activate  # ou `venv\Scripts\activate` no Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser  # se desejar criar administrador
python manage.py runserver
