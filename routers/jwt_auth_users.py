from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone

router = APIRouter(prefix="", responses={404: {"message": "No encontrado"}}, tags=["jwt_auth_users"])

oauth2 = OAuth2PasswordBearer(tokenUrl="/login_jwt")

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1
SECRET_KEY = "410acef3c480b951ba5028d132a7348bdcef9ba7267fc7ae73926c46e4234375"

crypt = CryptContext(schemes=["argon2"])

class User(BaseModel):
    username: str
    fullname: str 
    email: str 
    disabled: bool
    
class UserInDB(User):
    password: str
    
users_db = {
    "tovar": {"username": "tovar",
            "fullname": "Tovar Gomez", 
            "email": "inventado23@gmail.com", 
            "disabled": False, 
            "password": "$argon2i$v=19$m=16,t=2,p=1$RENTMUNsb3hvb095OWVMdQ$wLhxMPvx0q4bsM4jEYsh1A"},    #mypapu123
    "chuy": {"username": "chuy", 
            "fullname": "Chuy Gomez", 
            "email": "inv55@gmail.com", 
            "disabled": True, 
            "password": "$argon2i$v=19$m=16,t=2,p=1$a2RpdFZJTDJBNDhqcU5PNA$4/9vVDZ0M1cfKeBbDUFTqA"},    #chuyspapu
}

def search_user_db(username: str):
    if username in users_db:
        return UserInDB(**users_db[username])
    
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])

@router.post("/login_jwt")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no existe")
    
    user = search_user_db(form.username)
    
    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Contraseña incorrecta")
    
    expiration = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_DURATION)
    
    access_token = {"sub": user.username, "exp": expiration}
    
    return {"access_token": jwt.encode(access_token, SECRET_KEY, algorithm=ALGORITHM), "token_type": "bearer"}

async def auth_user(token: str = Depends(oauth2)):
    error_401 = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Credenciales de autenticación inválidas",
                                headers={"WWW-Authenticate": "Bearer"})
    
    try:
        username = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise error_401
        
    except JWTError:
        raise error_401
    
    return search_user(username)

async def current_user(user: User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario inactivo")
    
    return user

@router.get("/users/me_jwt")
async def me(user: User = Depends(current_user)):
    return user
