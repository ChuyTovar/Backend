#! Users db
from fastapi import APIRouter, HTTPException, status
from Db.models.user import User
from Db.client import db_client
from Db.schemas.user import user_schema, users_schema
from bson import ObjectId

router = APIRouter()
    
@router.get("/users_db", response_model=list[User])       
async def users():   
    return users_schema(db_client.users.find())

#Path
@router.get("/user_db/{id_user}")       
async def user(id_user: str):
    return search_user("_id", ObjectId(id_user))

#Query
@router.get("/userquery_db/")       
async def userquery(id_user: str):
    return search_user("_id", ObjectId(id_user))
    
def search_user(field: str, key):
    
    try:
        user = db_client.users.find_one({field: key})
        return User(**user_schema(user))
    except:
        return {"error": "Usuario desconocido"}
    
#!Post
@router.post("/user_db/",response_model=User ,status_code=status.HTTP_201_CREATED)       
async def create_user(user: User):
    if  type(search_user("email", user.email)) == User:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario ya existe")
        
    user_dict = dict(user)
    del user_dict["id"]
    
    id = db_client.users.insert_one(user_dict).inserted_id
    
    new_user = user_schema(db_client.users.find_one({"_id": id}))
    
    return User(**new_user)

#!Put
@router.put("/user_db/", response_model=User)
async def update_user(user: User):
    user_dict = dict(user)
    del user_dict["id"]
    
    try:
        db_client.users.find_one_and_update({"_id": ObjectId(user.id)},        
                                                {"$set": user_dict},
                                                return_document=True)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    
    return search_user("_id", ObjectId(user.id))
    
#!Delete
@router.delete("/user_db/{id_user}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id_user: str):
    found = db_client.users.find_one_and_delete({"_id": ObjectId(id_user)})
    
    if not found:
        return {"message": "No se ha eliminado el usuario"}
    