#! Users
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

class User(BaseModel):
    id_user: int
    name: str 
    level: str 
    papu_message: str 
    age: int

users_list = [User(id_user=1, name="Tovar", level="avanzado", papu_message="hola users del papuverso!", age=32),
            User(id_user=2, name="Chuy", level="de piso", papu_message="hi users del papuverso!", age=20),
            User(id_user=3, name="Lalo", level="intermedio", papu_message="hello users del papuverso!", age=25)]

@router.get("/users_manual")       
async def users_manual():   
    return [{"User": "Chuy","Nivel": "de piso","papu mensaje": "hi users del papuverso!", "age": 20},
            {"User": "Lalo","Nivel": "intermedio","papu mensaje": "hello users del papuverso!", "age": 25},
            {"User": "Tovar","Nivel": "avanzado","papu mensaje": "hola users del papuverso!", "age": 30}]
    
@router.get("/users")       
async def users():   
    return users_list

#Path
@router.get("/user/{id_user}")       
async def user(id_user: int):
    return search_user(id_user)

#Query
@router.get("/userquery/")       
async def userquery(id_user: int):
    return search_user(id_user)
    
def search_user(id_user: int):
    users = filter(lambda user: user.id_user == id_user, users_list)
    try:
        return list(users)[0]
    except:
        return {"error": "Usuario desconocido"}
    
#!Post
@router.post("/user/",response_model=User ,status_code=201)       
async def create_user(user: User):
    result = search_user(user.id_user)
    if "error" not in result:
        raise HTTPException(status_code=204, detail="El usuario ya existe")
        #return {"error": "El usuario ya existe"}
    users_list.append(user)
    return user

#!Put
@router.put("/user/")
async def update_user(user: User):
    update = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id_user == user.id_user:
            users_list[index] = user
            update = True
    
    if update:
        return user
    else:
        return {"error": "Usuario no encontrado"}
    
#!Delete
@router.delete("/user/{id_user}")
async def delete_user(id_user: int):
    delete = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id_user == id_user:
            del users_list[index]
            delete = True
    
    if delete:
        return {"message": "Usuario eliminado correctamente"}
    else:
        return {"error": "Usuario no encontrado"}
