from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from parser import CodeTreeBuilder

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic модель для входных данных
class CodeInput(BaseModel):
    code: str


# Маршрут для обработки кода
@app.post("/parse/")
def parse_code(input: CodeInput):
    try:
        # Получаем код и передаём его парсеру
        builder = CodeTreeBuilder()
        ast_tree = builder.build_tree(input.code)

        return ast_tree
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Parsing failed: {str(e)}")


# uvicorn server:app --reload