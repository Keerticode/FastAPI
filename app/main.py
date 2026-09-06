from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True 
    rating: Optional[int] = None


try:
    conn = psycopg2.connect(host = 'localhost', database = 'fastapi',user = 'postgres', password = 'keerti@1009', cursor_factory= RealDictCursor)
    cursor = conn.cursor()
    print("Database:", conn.info.dbname)
    print("Host:", conn.info.host)
    print("Port:", conn.info.port)
    print("User:", conn.info.user)
    print("Database connection was succesfull")

except Exception as error:
    print("Connecting to database failed")
    print("Error :", error)
    time.sleep(2)

my_posts = [{"title" : "title of posts 1", "content" : "content of post 1", "id" : 1}, {"title": "favourite foods", "content": "I like pizza", "id": 2}]


def find_posts(id):
    for p in my_posts:
        if p["id"] == id:
            return p


def find_index_post(id: int):
    for i, p in enumerate(my_posts) :
        if p['id'] == id :
            return i
        

@app.get("/")
async def root():
    return{"message" : "Hello World"}


@app.get("/posts")
async def get_posts():
    cursor.execute("""SELECT * FROM "Posts" """)
    posts = cursor.fetchall()
    return{"data" : posts}


@app.post("/posts", status_code = status.HTTP_201_CREATED)
async def create_posts(post : Post):
    #post_dict = post.dict()
    #post_dict['id'] = randrange(0, 1000000)
    #my_posts.append(post_dict)
    cursor.execute("""INSERT INTO "Posts" (title, content, published) VALUES (%s, %s, %s) RETURNING *""",(post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return{"data": new_post}


@app.get("/posts/{id}")
def get_post(id : int, response : Response):

    cursor.execute("""SELECT * FROM "Posts" WHERE id = %s """, (str(id)))
    test_post = cursor.fetchone()
    print(test_post)


    post = find_posts(id)
    if not post :
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} was not found")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {'message': f"post with id: {id} was not found"}
    return {"post_details": post}


@app.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_post(id:int):

    cursor.execute("""DELETE FROM "Posts" WHERE id = %s RETURNING *""", (str(id),))
    delete_post = cursor.fetchone()
    conn.commit()



    #delete post
    #index = find_index_post(id)

    if delete_post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail = f"post with id : {id} doesn't exist")
    return Response(status_code = status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
async def update_post(id : int, post : Post):

    cursor.execute("""UPDATE "Posts" SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail = f"post with id : {id} doesn't exist")

    return{"data" : updated_post}