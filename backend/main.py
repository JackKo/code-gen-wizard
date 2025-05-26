from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/start-codegen")
def start_codegen():
    result = subprocess.run(
        ["playwright", "codegen", "--target", "csharp"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    return {"code": result.stdout}

@app.post("/save-code")
async def save_code(request: Request):
    data = await request.json()
    code = data.get("code", "")
    os.makedirs("saved", exist_ok=True)
    with open("saved/edited_code.cs", "w", encoding="utf-8") as f:
        f.write(code)
    return {"status": "saved"}


from fastapi import Request
from page_object_generator import generate_all

@app.post("/generate-page-objects")
async def generate_objects(request: Request):
    data = await request.json()
    code = data.get("code", "")
    output_path = "generated_pages"
    generate_all(code, output_path)
    return {"status": "page objects generated", "output": output_path}
