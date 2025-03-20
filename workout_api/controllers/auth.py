from fastapi import APIRouter, HTTPException

from workout_api.security import create_access_token, verify_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
def login(username: str, password: str):
    # Validação de usuário (exemplo simplificado)
    if username == "admin" and password == "password":
        token = create_access_token({"sub": username})
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Credenciais inválidas")


@router.get("/me")
def get_current_user(token: str):
    try:
        payload = verify_access_token(token)
        return {"user": payload["sub"]}
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
