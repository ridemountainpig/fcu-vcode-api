from typing import Union
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles 
import uvicorn
import os
from script import validateCode as vc
from script import validateImg as vi

app = FastAPI()

origins = [
    '*'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/validate")
async def validate_image(file: UploadFile = File(...)):
    if not os.path.exists("images"):
        os.makedirs("images")

    file_list = os.listdir("images")
    file_count = len(file_list)

    file_location = os.path.join("images", f"{file_count}.png")
    with open(file_location, "wb") as f:
        f.write(file.file.read())

    result = vc.validateCodeLite(file_location)

    os.remove(file_location)

    return JSONResponse({"vcode": result})


@app.get("/validateImg")
async def get_validate_image():
    fileName = vi.downLoadImage("https://course.fcu.edu.tw/validateCode.aspx")
    vcodeNum = vc.validateCodeLite(f"images/{fileName}")
    return JSONResponse({"fileName": fileName, "vcode": vcodeNum})

app.mount("/images", app=StaticFiles(directory="images"), name="images")

# @app.post("/upload")
# async def upload_image(file: UploadFile = File(...)):
#     if not os.path.exists("images"):
#         os.makedirs("images")

#     file_list = os.listdir("images")
#     file_count = len(file_list)

#     file_location = os.path.join("images", f"{file_count}.png")
#     with open(file_location, "wb") as f:
#         f.write(file.file.read())

#     return JSONResponse({"message": "File uploaded successfully"})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
