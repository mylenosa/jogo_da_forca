# Jogo da Forca - Aplicação Web Educacional

**Autores:**
* Mylena Viana Nunes
* Higor Rodrigues Lauer
* Luís Eduardo Barros Rodrigues

## 1. Visão Geral do Projeto

Este projeto consiste em uma aplicação web do clássico "Jogo da Forca", desenvolvida como um desafio acadêmico. A plataforma foi criada com um foco educacional, permitindo que usuários do tipo "Professor" criem e gerenciem jogos (temas e palavras) para que os "Alunos" possam jogar.

A aplicação implementa um sistema completo de autenticação, gerenciamento de conteúdo, jogabilidade interativa e geração de relatórios, atendendo a todos os requisitos propostos.

**Link da Aplicação:** [https://mylenosa.pythonanywhere.com/](https://mylenosa.pythonanywhere.com/) 

## 2. Tecnologias Utilizadas

* **Backend:** Python 3, Django Framework
* **Frontend:** HTML5, CSS3, JavaScript
* **Banco de Dados:** SQLite 3 (padrão do Django)
* **Geração de PDF:** Biblioteca `reportlab`
* **Servidor de Deploy:** PythonAnywhere

## 3. Dados de Acesso para Testes

Para facilitar a avaliação da aplicação, os seguintes usuários de teste foram pré-cadastrados no sistema.

| Usuário | Tipo | Senha |
| --- | --- | --- |
| marcos.faino | professor | alunoifro |
| andrey.alencar | professor | alunoifro |
| higor.lauer | aluno | alunoifro |
| mylena.nunes | aluno | alunoifro |
| luis.rodrigues| aluno | alunoifro |

## 4. Cumprimento dos Requisitos

A seguir, detalhamos como cada requisito do desafio foi implementado na aplicação.

### a. Padrão Class-Based Views (CBV)

Todo o projeto foi estruturado utilizando **Class-Based Views (CBVs)** do Django, garantindo um código mais organizado, reutilizável e escalável.

* **Exemplos Notáveis:**
    * `HomeView(View)`: Controla a página inicial e a lógica de filtragem dos jogos.
    * `TemaListView(ListView)` e `PalavraListView(ListView)`: Listam os temas e palavras cadastrados.
    * `TemaCreateView(CreateView)` e `PalavraCreateView(CreateView)`: Gerenciam os formulários de criação.
    * `RelatorioView(View)` e `gerar_pdf_view(View)`: Views customizadas para funcionalidades específicas de relatório e PDF.

### b. Cadastro e Gerenciamento por Professores

A aplicação possui um sistema de papéis bem definido, onde os **Professores** têm privilégios elevados para gerenciar o conteúdo do jogo.

* **Implementação:**
    * O `models.py` define o modelo `Professor` que estende o `User` padrão do Django, permitindo um cadastro seguro.
    * As views de criação, edição e exclusão de `Tema` e `Palavra` (ex: `TemaCreateView`, `PalavraUpdateView`) utilizam o `LoginRequiredMixin`, restringindo o acesso apenas a usuários autenticados.
    * Os formulários, como `TemaForm` e `PalavraForm`, garantem que ao salvar um novo item, ele seja automaticamente associado ao professor que está logado.

### c. Área de Gerenciamento de Conteúdo

Professores possuem uma área exclusiva e intuitiva para administrar temas, palavras, dicas e textos de apoio.

* **Implementação:**
    * A view `TemaGerenciarView` serve como um painel central para o professor.
    * A partir dela, o professor pode listar, criar, editar e deletar **Temas**.
    * Ao selecionar um tema, o professor pode gerenciar as **Palavras** associadas, cada uma podendo conter um `texto` e uma `dica` opcionais, conforme definido no `models.py`.

### d. Experiência do Aluno e Acesso

O aluno tem uma experiência fluida, podendo jogar de forma anônima ou se cadastrando, caso o professor exija.

* **Implementação:**
    * A `HomeView` é acessível a todos os usuários (logados ou não) e exibe os jogos disponíveis. Ela contém filtros para que o aluno possa encontrar jogos por **tema** ou por **professor**.
    * O modelo `Tema` possui um campo booleano `login_obrigatorio`. Na `JogoView`, antes de iniciar uma partida, o sistema verifica este campo. Se for `True` e o usuário não estiver logado, ele é redirecionado para a página de `login`.

### e. Geração de PDF da Atividade

Professores podem exportar as atividades em formato PDF para impressão e uso em sala de aula.

* **Implementação:**
    * A view `gerar_pdf_view` foi criada especificamente para esta finalidade.
    * Utilizando a biblioteca `reportlab` (listada em `requirements.txt`), a view busca as palavras de um determinado tema e as desenha em um documento PDF, que é disponibilizado para download.

### f. Relatório de Desempenho

A plataforma oferece uma poderosa ferramenta de relatórios para que os professores possam acompanhar o engajamento dos alunos.

* **Implementação:**
    * O modelo `Jogada` em `models.py` registra cada vez que um usuário joga, salvando qual usuário, qual palavra e a data.
    * A `RelatorioView` exibe um formulário (`FiltroRelatorioForm`) onde o professor pode filtrar as jogadas por **tema** e por um **período de tempo** (data de início e fim).
    * O resultado é exibido em uma tabela clara, mostrando os dados solicitados.

### g. Deploy da Aplicação

A aplicação está funcional e disponível na internet, hospedada na plataforma PythonAnywhere.

* **Implementação:**
    * O código foi configurado para produção, com `DEBUG=False` e `SECRET_KEY` gerenciadas por variáveis de ambiente, garantindo a segurança.
    * Os arquivos estáticos (`CSS`, `JS`) são servidos corretamente através da configuração do `collectstatic`.
    * O arquivo de configuração WSGI foi ajustado no PythonAnywhere para carregar a aplicação Django e seu ambiente virtual.