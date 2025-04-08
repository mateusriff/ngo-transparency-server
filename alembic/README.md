# Passo a Passo para Alterar o Banco de Dados com Alembic

Este guia descreve como realizar alterações no banco de dados usando o Alembic, incluindo a criação de novas colunas, alteração de tipos de dados e remoção de colunas.

---

## 1. Atualizar o Modelo no Código

1. Abra o arquivo `models.py`.

2. Faça a alteração desejada no modelo. Exemplos:
   - **Adicionar uma nova coluna**:
     ```python
      class Post(PostBase, table=True):
          id: int | None = Field(default=None, primary_key=True)
          created_at: datetime = Field(default_factory=datetime.now)
          teste: Optional[str] = Field(default=None)  # Nova coluna adicionada
     ```

   - **Alterar o tipo de uma coluna existente**:
     ```python
     class Post(PostBase, table=True):
         transaction: str = Field()  # Alterando de float para string
     ```

   - **Remover uma coluna**:
     Basta remover a coluna do modelo:
     ```python
     class Post(PostBase, table=True):
         # Removendo a coluna 'teste'
         pass
     ```

---

## 2. Criar uma Nova Migração

Após atualizar o modelo, gere uma nova migração para refletir a alteração no banco de dados.

1. Execute o comando:
   ```sh
   alembic revision --autogenerate -m "Descrição da alteração"
   ```

2. O Alembic gerará um arquivo de migração na pasta `versions`. Por exemplo:
    ```
    alembic/versions/984cbb036182_add_teste_column_post.py
    ```

3. Abra o arquivo gerado e revise o conteúdo. Ele deve conter os comandos para aplicar (`upgrade`) e reverter (`downgrade`) a alteração.

   Exemplo de migração para adicionar uma coluna:
   ```python
   def upgrade() -> None:
       op.add_column('post', sa.Column('teste', sa.String(), nullable=True))

   def downgrade() -> None:
       op.drop_column('post', 'teste')
   ```

---

## 3. Aplicar a Migração

Aplique a migração ao banco de dados para que a alteração seja refletida.

1. Execute o comando:
   ```sh
   alembic upgrade head
   ```

2. O Alembic executará o método `upgrade()` da migração gerada e aplicará as alterações no banco de dados.

---

## 4. Verificar a Alteração no Banco de Dados
Após aplicar a migração, verifique se a alteração foi feita corretamente no banco de dados. Você pode fazer isso tanto pelo `pgAdmin` quanto pelo `psql`:

1. psql:

    -  Conecte-se ao banco de dados:
       ```sh
       docker exec -it postgres-ngo psql -U postgres -d postgres
       ```
    
    -  Liste a estrutura da tabela alterada:
       ```sql
       \d post
       ```
    
    -  Verifique se a alteração está refletida (por exemplo, a nova coluna `teste`).

2. pgAdmin:

    - Abra o pgAdmin na sua máquina
    - Clique com o botão direito em **Servers** e selecione **Register > Server**.
    - Na aba **General**, insira um nome para o servidor (por exemplo, `Postgres Docker`).
    - Na aba **Connection**, preencha os campos:
        - **Host name/address**: `localhost` (ou `127.0.0.1`).
        - **Port**: `5433` (ou a porta configurada no `docker-compose.yml`).
        - **Maintenance database**: `postgres`.
        - **Username**: `postgres`.
        - **Password**: `insira a senha neste campo`.
    - Clique em **Save**.

3. **Verificar a Tabela Alterada**:
   - No painel esquerdo, expanda o servidor conectado.
   - Navegue até **Databases > postgres > Schemas > public > Tables**.
   - Clique com o botão direito na tabela alterada (por exemplo, `post`) e selecione **View/Edit Data > All Rows** para visualizar os dados.
   - Para verificar a estrutura da tabela, clique com o botão direito na tabela e selecione **Properties > Columns**.

---

## 5. Testar a Alteração na Aplicação
Certifique-se de que a aplicação está funcionando corretamente com a alteração feita.

1. Reinicie o servidor FastAPI:
   ```sh
   uvicorn main:app --reload
   ```
    ou
    ```sh
   docker-compose up --build
   ```

2. Acesse o Swagger UI em [http://localhost:8000/docs](http://localhost:8000/docs) e teste as rotas relacionadas à tabela alterada.

---

## 6. Reverter a Migração (Se Necessário)
Se algo deu errado e você precisa desfazer a alteração, pode reverter a migração.

1. Execute o comando:
   ```sh
   alembic downgrade -1
   ```

2. Isso executará o método `downgrade()` da última migração e reverterá a alteração.

---