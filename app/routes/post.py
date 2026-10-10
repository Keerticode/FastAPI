from fastapi import (
    Response,
    status,
    HTTPException,
    Depends,
    APIRouter,
)
from .. import models, schemas, oauth2
from typing import Optional, List, Optional
from sqlalchemy.orm import Session
from ..database import get_db


router = APIRouter(
    prefix = "/posts",
    tags = ['Posts']
)


@router.get("/", response_model=List[schemas.Post])
async def get_posts(db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user), limit : int = 10, skip : int = 0, search : Optional[str] = ""):

    # cursor.execute("""SELECT * FROM "Posts" """)
    # posts = cursor.fetchall()

    #posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    print(limit)
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    

    #if not post :
    #    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
    #                        detail = f"post with id : {id} was not found")

    #if post.owner_id != current_user.id :
    #    raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,
    #                   detail = "Not authorized to perform required action")

    return posts


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.Post
)


async def create_posts(
    post: schemas.CreatePost,
    db: Session = Depends(get_db),
    current_user : int = Depends(oauth2.get_current_user)
):

    # post_dict = post.dict()
    # post_dict['id'] = randrange(0, 1000000)
    # my_posts.append(post_dict)

    # ---> using SQL
    # cursor.execute(
    #     """INSERT INTO "Posts" (title, content, published)
    #     VALUES (%s, %s, %s) RETURNING *""",
    #     (post.title, post.content, post.published)
    # )
    # new_post = cursor.fetchone()
    # conn.commit()

    # ----> Using SQL Alchemy

    print(current_user.id)
    new_post = models.Post(owner_id = current_user.id, **post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/{id}", response_model=schemas.Post)
async def get_post(
    id: int,
    db: Session = Depends(get_db),
    current_user : int = Depends(oauth2.get_current_user)
):

    # cursor.execute(
    #     """SELECT * FROM "Posts" WHERE id = %s """,
    #     (str(id))
    # )
    # test_post = cursor.fetchone()

    post = db.query(models.Post).filter(
        models.Post.id == id
    ).first()

    print(post)

    # post = find_posts(id)

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found"
        )

        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f"post with id: {id} was not found"}

    return post


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT
)
# async def delete_post(id: int):
async def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user : int = Depends(oauth2.get_current_user)
):

    # cursor.execute(
    #     """DELETE FROM "Posts" WHERE id = %s RETURNING *""",
    #     (str(id),)
    # )
    # delete_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(
        models.Post.id == id
    )

    # delete post
    # index = find_index_post(id)

    post = post_query.first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id : {id} doesn't exist"
        )

    if post.owner_id != current_user.id :
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "Not authorized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )


@router.put(
    "/{id}",
    response_model=schemas.Post
)
# async def update_post(id: int, post: Post):
async def update_post(
    id: int,
    post: schemas.CreatePost,
    db: Session = Depends(get_db),
    current_user : int = Depends(oauth2.get_current_user)
):

    post_query = db.query(models.Post).filter(
        models.Post.id == id
    )

    existing_post = post_query.first()

    if existing_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id : {id} doesn't exist"
        )

    if existing_post.owner_id != current_user.id :
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "Not authorized to perform requested action")

    post_query.update(post.model_dump(), synchronize_session = False)
    db.commit()

    return post_query.first()