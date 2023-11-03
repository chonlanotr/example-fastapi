
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import Settings


# เอาไว้ generate table โดยไม่มี alembic 
# models.Base.metadata.create_all(bind=engine)

#  uvicorn app.main:app --reload
app = FastAPI(
    title="API Tutorial",
    description="Demo purpose",
    contact={
        "name": "chonlanotr supharoekrat",
        "url": "http://www.google.com",
        "email": "chonlanotr@gamil.com",
    }
)

# origins = ["https://www.google.com", "https://www.youtube.com"]
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
#             {"title": "favorite foods", "content": "I like pizza", "id": 2}
#             ]


# def find_post(id):
#     for p in my_posts:
#         if p["id"] == id:
#             return p

# def find_index_post(id):
#     for i, p in enumerate(my_posts):
#         if p['id'] == id:
#             return i


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


# request Get method url: "/"
@app.get("/")
async def root():
    return {"message": "Hello World"}


# @app.get("/sqlalchemy")
# def test_posts(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     #print - sql statement
#     print(posts)
#     return posts



