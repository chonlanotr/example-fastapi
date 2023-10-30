from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)



# @router.get("/")
@router.get("/", response_model=List[schemas.PostOut])
# @router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):

    # ORM
    print(limit)
    # posts = db.query(models.Post).all()
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
    #     models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id)
    posts =  db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
            models.Post.title.contains(search)).limit(limit).offset(skip).all()

    # Print SQL Statement
    # print (results)

    # #SQL 
    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()
    # print(posts)
    return posts
    # return results

# @router.post("/createposts")
# # def create_posts(payLoad: dict = Body(...)):
# #     print(payLoad)
# #     return {"new_post" : f"title {payLoad['title']} content: {payLoad['content']}"}

# def create_posts(post: Post):
#     print(post)
#     print(post.model_dump(mode="unchanged"))
#     # print(post.dict()) #duplicate use model_dump instead
#     return {"data": post}

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # print(post)
    # print(post.model_dump(mode="unchanged"))
    # post_dict = post.model_dump(mode="unchanged")
    # post_dict['id'] = randrange(0,1000000)
    # my_posts.append(post_dict)
    # my_posts.append(post.dict())
    # return {"data": post_dict}

    # แบบ f string ทำให้เกิด sql injection ได้
    # cursor.execute( f" INSERT INTO posts (title, content, published ) VALUES ( {post.title}, {post.content}, {post.published} )")
    
    # # SQL Pattern
    # cursor.execute( """ INSERT INTO posts (title, content, published ) VALUES (%s, %s, %s ) RETURNING * """, 
    #                                     (post.title, post.content, post.published) )
    # new_post = cursor.fetchone()
    # conn.commit()

    # ORM Pattern
    # print(**post.model_dump(mode="unchanged"))


    # new_post = models.Post(title=post.title, content=post.content, published=post.published)

    print(current_user.email)
    new_post = models.Post(owner_id=current_user.id, **post.model_dump(mode="unchanged"))
    db.add(new_post)
    db.commit()
    # เท่ากับ RETURNING ของ SQL Pattern
    db.refresh(new_post)

    return new_post

# # การเรียงลำดับ path สำคัญไม่งั้นอันนี้จะไปหา path /posts/{id} เพราะมันหาจากบนลงล่าง
# @router.get("/posts/latest")
# def get_latest_post():
#     post = my_posts[len(my_posts)-1]
#     return{"detail": post}




@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int,  db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # # SQL Pattern
    #ถ้าเกิด error ที่ sql string ลองตามด้วย comma น่าจะเป็น bug
    # cursor.execute ( """ SELECT * FROM posts WHERE id = %s """ , (str(id),) )
    # post = cursor.fetchone()

    # ORM Pattern
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    
    print(post)
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found.")
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,  db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    # # SQL
    # cursor.execute( """ DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    # delete_post = cursor.fetchone()
    # conn.commit()

    # ORM
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post = post_query.first()


    if post == None:
    # if delete_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with: {id} does not exist.")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")



    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate,  db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # # SQL
    # cursor.execute ( """ UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, 
    #                 (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()

    # ORM
    post_query =    db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    print(post.owner_id)
    print(current_user.id)
    if post == None:
    # if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with: {id} does not exist.")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")


    # post_query.update( {'title': 'hey 5', 'content': 'content5'}, synchronize_session=False)

    post_query.update( updated_post.model_dump(mode="unchanged"), synchronize_session=False)

    db.commit()

    return post_query.first()
