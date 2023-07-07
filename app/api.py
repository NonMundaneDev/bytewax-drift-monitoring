from typing import Optional
from fastapi import Body, FastAPI,BackgroundTasks,Response,Depends
from app.predict_model import predict_d
from app.db import insert_data,data_from_s3
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from starlette.responses import FileResponse
import json


app = FastAPI()


from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates










origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)


# class Result:
#     prediction: str






# @app.post("/predict/")
# async def predict_route(input_str: str) -> dict:
#     # Call the predict function
#     prediction = predict(input_str)
#     # Return the result as a JSON response
#     return {"prediction": prediction}





@app.post("/d_predict")
async def pred(input_value: list):
    result = predict_d(input_value)
    return result
    






@app.get("/monitoring", response_class=HTMLResponse)
async def read_item(request: Request):
    file_path = "app/static/file.html"
    data_from_s3(method="get")
    return HTMLResponse(content=open(file_path, "r").read())
