from fastapi import (
    Response,
    status,
    HTTPException,
    Depends,
    APIRouter
)
from .. import models, schemas
from typing import Optional, List
from sqlalchemy.orm import Session
from ..database import get_db


router = APIRouter()


@router.get("/posts", response_model=List[schemas.Post])
async def get_posts(db: Session = Depends(get_db)):

    # cursor.execute("""SELECT * FROM "Posts" """)
    # posts = cursor.fetchall()

    posts = db.query(models.Post).all()

    return posts


@router.post(
    "/posts",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.Post
)
async def create_posts(
    post: schemas.CreatePost,
    db: Session = Depends(get_db)
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

    new_post = models.Post(**post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/posts/{id}", response_model=schemas.Post)
async def get_post(
    id: int,
    db: Session = Depends(get_db)
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
    "/posts/{id}",
    status_code=status.HTTP_204_NO_CONTENT
)
# async def delete_post(id: int):
async def delete_post(
    id: int,
    db: Session = Depends(get_db)
):

    # cursor.execute(
    #     """DELETE FROM "Posts" WHERE id = %s RETURNING *""",
    #     (str(id),)
    # )
    # delete_post = cursor.fetchone()
    # conn.commit()

    post = db.query(models.Post).filter(
        models.Post.id == id
    )

    # delete post
    # index = find_index_post(id)

    if post.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id : {id} doesn't exist"
        )

    post.delete(synchronize_session=False)
    db.commit()

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )


@router.put(
    "/posts/{id}",
    response_model=schemas.Post
)
# async def update_post(id: int, post: Post):
async def update_post(
    id: int,
    post: schemas.CreatePost,
    db: Session = Depends(get_db)
):

    # cursor.execute(
    #     """UPDATE "Posts"
    #     SET title = %s, content = %s, published = %s
    #     WHERE id = %s RETURNING *""",
    #     (
    #         post.title,
    #         post.content,
    #         post.published,
    #         str(id)
    #     )
    # )
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(
        models.Post.id == id
    )

    existing_post = post_query.first()

    if existing_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id : {id} doesn't exist"
        )

    post_query.update(
        post.model_dump(),
        synchronize_session=False
    )

    db.commit()

    return post_query.first()

