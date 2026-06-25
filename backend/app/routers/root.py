from fastapi import APIRouter

router = APIRouter()


@router.put("/hello-world")
async def hello_world():
    """
    Hello world!
    """
    return {"msg": "Hello world!"}
