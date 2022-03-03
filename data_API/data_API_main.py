
from typing import Any
import uvicorn
from fastapi import FastAPI

import pandas as pd
from datetime import datetime

import os
from dotenv import load_dotenv

load_dotenv()
PWD = os.getenv("PWD")
import sys
sys.path.insert(1, f'{PWD}\\modules')

from api_modules.open_binance_api import OpenBinanceApi

from pydantic import BaseModel

class DFModel(BaseModel):
    df: pd.DataFrame
    class Config:
        arbitrary_types_allowed = True

class InputData(BaseModel):
    df: str

app = FastAPI()
DFModel.df = OpenBinanceApi.get_df(
            pair = 'RVNUSDT', # pair
            interval = '1m', # Interval
            limit = 1000,   # limit
    )
# df = pd.DataFrame([])
time_ = datetime.now()

# === test api routes ===
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/server_time")
async def get_server_time():
    return {"message": f"{time_}"}

@app.post("/server_time")
async def update_server_time():
    time_ = datetime.now()
    return {"message": f"{time_}"}

# === normal api ===

@app.get("/df")
async def get_data_frame():
    return {"df": DFModel.df.to_json()}

@app.post("/df")
async def change_data_frame(new_df: InputData):

    DFModel.df = pd.read_json(new_df.df)
    
    return {"df": DFModel.df.to_json()}


if __name__ == "__main__":
    uvicorn.run(app, debug=1, host="0.0.0.0", port=8000)