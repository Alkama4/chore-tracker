from fastapi import APIRouter

router = APIRouter()


@router.get("/hello-world")
async def hello_world():
    """
    Hello world!
    """
    return {"msg": "Hello world!"}
