from fastapi import APIRouter


router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/register", status_code=201)
async def register():
    return {'data': 'Registered'}
