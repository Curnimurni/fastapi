






from .. import models, schemas, oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func
router = APIRouter(
     prefix="/posts" ,
     tags= ['Posts']
)




@router.get("/", response_model = List[schemas.PostOut])
#@router.get("/")
def get_post(db: Session = Depends(get_db),
                                   current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] =""):
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    #cursor.execute("""SELECT * FROM public."posts " """)
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes") ).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()
    #cursor.execute("""SELECT * FROM public."posts " """)
 
    return posts
     

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)

def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), 
                                                                current_user: int = Depends(oauth2.get_current_user)):

    #cursor.execute("""INSERT INTO public."posts " (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
    #                (post.title, post.content, post.published))
    #new_post = cursor.fetchone()
    #conn.commit()
    #cursor.execute("""SELECT * FROM public."posts " """)
    new_post = models.Post(owner_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


#@router.get("/posts/latest")
#def latest_post():
 #   latest = my_post[len(my_post) -1]
  #  return latest

@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db),
                                            current_user: int = Depends(oauth2.get_current_user)):
   # cursor.execute("""SELECT * FROM public."posts " WHERE id = %s """, (str(id)))
   # post = cursor.fetchone()
   
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    #post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                             detail=f"your id: {id} is not found" )
    
    #print(post)
    return  post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),
                                                current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    #cursor.execute("""DELETE  FROM public."posts " WHERE id = %s Returning * """, (str(id),))
    #delete_post = cursor.fetchone()
    #conn.commit()
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail = f"this id: {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db),
                                    current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute(""" UPDATE public."posts " SET title = %s, content = %s, published = %s Where id = %s RETURNING *""",
     #               ( post.title, post.content, post.published,str(id)))
    
    #updated_post = cursor.fetchone()
    #conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail = f"this id: {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
    
    
