from database import SessionDep, create_db_and_tables, get_session
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from models import Post, PostCreate, PostPatch
import logging

app = FastAPI()

# Configurar logging para exibir informações no console
logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

# Rota de criação de posts
@app.post("/posts/")
def create_post(post: PostCreate, session: SessionDep):

    new_post = Post.model_validate(post)    # Converte o objeto PostCreate em um objeto Post
    session.add(new_post)                   # Adiciona o objeto ao banco de dados
    session.commit()                        # Realiza o commit da transação
    session.refresh(new_post)               # Atualiza o objeto com os dados do banco de dados

    return new_post

# Rota de listagem de posts
@app.get("/posts/{ong_id}")
def read_posts(ong_id: int, session: Session = Depends(get_session)):

    # Tenta buscar os posts no banco de dados, caso não encontre, retorna um erro 404
    try:

        logger.info(f"Fetching posts for ONG ID: {ong_id}")                 # Loga a requisição
        posts = session.exec(select(Post).where(Post.ong == ong_id)).all()  # Busca todos os posts da ONG no banco de dados por meio do id da ONG

        # Se não houver posts, retorna um erro 404
        if not posts:
            raise HTTPException(status_code = 404, detail = "Posts not found")
        
        return posts
    
    except Exception as e: # Caso ocorra um erro, loga o erro e retorna um erro 500

        logger.error(f"Error fetching posts: {e}")
        raise HTTPException(status_code = 500, detail = "Internal Server Error")

# Rota de atualização de posts
@app.patch("/posts/{ong_id}/{id}")
def update_post(ong_id: int, id: int, post: PostPatch, session: Session = Depends(get_session)):

    db_post = session.get(Post, id) # Busca o post no banco de dados

    # Se não encontrar o post ou o post não pertencer à ONG, retorna um erro 404
    if not db_post or db_post.ong != ong_id:
        raise HTTPException(status_code = 404, detail = "Post not found")
    
    # Atualiza os campos do post com os valores do objeto PostPatch recebido
    for key, value in post.model_dump(exclude_unset = True).items():
        setattr(db_post, key, value)

    session.add(db_post)        # Adiciona o post ao banco de dados
    session.commit()            # Realiza o commit da transação
    session.refresh(db_post)    # Atualiza o objeto com os dados do banco de dados

    return db_post

# Rota de deleção de posts
@app.delete("/posts/{ong_id}/{id}")
def delete_post(ong_id: int, id: int, session: Session = Depends(get_session)):

    db_post = session.get(Post, id) # Busca o post no banco de dados

    # Se não encontrar o post ou o post não pertencer à ONG, retorna um erro 404
    if not db_post or db_post.ong != ong_id:
        raise HTTPException(status_code = 404, detail = "Post not found")
    
    session.delete(db_post) # Deleta o post do banco de dados
    session.commit()        # Realiza o commit da transação

    return {"detail": "Post deleted"}