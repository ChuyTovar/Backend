from fastapi import APIRouter

router = APIRouter(prefix="/products", responses={404: {"message": "No encontrado"}}, tags=["products"])

products_list = [{"nombre": "fabuloso","categoria": "multiusos","descripcion": "fabuloso!", "precio": 14},]

@router.get("/")       
async def products():   
    return [{"nombre": "fabuloso","categoria": "multiusos","descripcion": "fabuloso!", "precio": 14},
            ]
    
@router.get("/{id_product}")       
async def products(id_product: int):   
    return products_list