from fastapi import FastAPI
from routers import products, users, basic_auth_users, jwt_auth_users, users_db
from fastapi.staticfiles import StaticFiles

app = FastAPI()     #Crea una instancia de la aplicación FastAPI

app.include_router(products.router)  #Incluye el router en la aplicación principal
app.include_router(users.router)
app.include_router(basic_auth_users.router)
app.include_router(jwt_auth_users.router)
app.include_router(users_db.router)
app.mount("/static", StaticFiles(directory="static"), name="static")  #Monta un directorio estático para servir archivos estáticos

@app.get("/")       #Define la ruta raíz
async def root():   #Define la función que maneja las solicitudes GET a la ruta raíz de manera asíncrona
    return {"message": "Hola papus de las apis!"}

@app.get("/link")       
async def link():   
    return {"link": "https://www.youtube.com/watch?v=ZXIWU8GLsAc&list=RDZXIWU8GLsAc&start_radio=1"}