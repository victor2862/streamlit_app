# Meu Primeiro App 🧊

Uma aplicação de apoio para gestão de projetos corporativos construída com Streamlit.

Este projeto, ainda em fase inicial, visa fornecer uma interface simples para gerenciar múltiplos projetos. A funcionalidade principal atualmente em desenvolvimento é a capacidade de criar e carregar projetos distintos, cada um com seu próprio "contexto" versionado. O contexto pode ser um texto em Markdown que descreve o escopo, objetivos ou qualquer outra informação relevante do projeto, e a aplicação permite restaurar versões anteriores desse contexto.

## Estado da Aplicação (`st.session_state`)

A aplicação utiliza o `st.session_state` do Streamlit para manter o estado entre as interações do usuário e as diferentes páginas. Abaixo está uma descrição das variáveis de estado utilizadas:

| Variável | Formato | Criação e Modificação |
| :--- | :--- | :--- |
| `db` | `AppDB` (objeto) | **Criação:** Na primeira execução da aplicação. **Modificação:** Nunca é modificado após a criação. Armazena a instância da classe de gerenciamento do banco de dados. |
| `projeto_atual` | `pd.Series` ou `None` | **Criação:** Na primeira execução, como `None`. **Modificação:** Quando um projeto é carregado na página "Projetos", esta variável armazena os dados do projeto (como uma linha de um DataFrame). |
| `contexto_atual` | `str` ou `None` | **Criação:** Na primeira execução, como `None`. **Modificação:** Quando um contexto é adicionado ou restaurado para o `projeto_atual`. Armazena o texto (Markdown) do contexto em vigor. |

### Variáveis de Escopo Específico

Estas variáveis são usadas para controlar o estado de componentes ou diálogos específicos.

| Variável | Formato | Criação e Modificação |
| :--- | :--- | :--- |
| `contexto_visualizado` | `str` ou `None` | **Criação:** Na primeira execução, como `None`. **Modificação:** Usado na caixa de diálogo "Restaurar contexto". Armazena temporariamente o texto de uma versão de contexto que o usuário seleciona para visualização, antes de decidir restaurá-la. |

### Variáveis de Mensagens e Sinalização

Estas variáveis funcionam como "flags" para sinalizar a ocorrência de eventos, como a exibição de mensagens de sucesso ou alerta.

| Variável | Formato | Criação e Modificação |
| :--- | :--- | :--- |
| `msg_projeto_criado` | `int` | **Criação:** Na primeira execução, como `0`. **Modificação:** Alterado para `1` (ou outro valor) para sinalizar que um novo projeto foi criado, possivelmente para exibir uma mensagem de sucesso. |
| `msg_projeto_carregado` | `int` | **Criação:** Na primeira execução, como `0`. **Modificação:** Alterado para `1` (ou outro valor) para sinalizar que um projeto foi carregado. |
| `msg_projeto_deletado` | `int` | **Criação:** Na primeira execução, como `0`. **Modificação:** Alterado para `1` (ou outro valor) para sinalizar que um projeto foi deletado. |