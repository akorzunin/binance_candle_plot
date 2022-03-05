
import json
import uvicorn
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.responses import RedirectResponse

import pandas as pd
from datetime import datetime

import os
from dotenv import load_dotenv

load_dotenv()
PWD = os.getenv("PWD")
import sys
sys.path.insert(1, f'{PWD}\\modules')

# from api_modules.open_binance_api import OpenBinanceApi
from pydantic import BaseModel

class DashboardModel(BaseModel):
    MA_lines: tuple
    trade_data: pd.DataFrame
    df: pd.DataFrame
    p_trdr: pd.DataFrame

    class Config:
        arbitrary_types_allowed = True

class InputData(BaseModel):
    new_item: str



app = FastAPI()

time_ = datetime.now()

# === test api routes ===
@app.get("/")
async def root():
    return RedirectResponse(url='/docs')


@app.get("/server_time")
async def get_server_time():
    return {"message": f"{datetime.now()}"}

# === base api routes===

@app.get("/ma_lines")
async def get_ma_lines():
    try:
        DashboardModel.MA_lines
    except AttributeError:
        DashboardModel.MA_lines = ()
    return {"ma_lines": DashboardModel.MA_lines}

@app.post("/ma_lines")
async def change_ma_lines(item: list):
    DashboardModel.MA_lines = item
    return {"ma_lines": DashboardModel.MA_lines}

@app.get("/trade_data")
async def get_trade_data():
    try:
        return {"trade_data": DashboardModel.trade_data.to_json()}
    except AttributeError as e: 
        raise HTTPException(status_code=404, detail="Item not found") from e

@app.post("/trade_data")
async def change_trade_data(new_df: InputData):

    DashboardModel.trade_data = pd.read_json(new_df.new_item)
    
    return {"trade_data": DashboardModel.trade_data.to_json()}

@app.get("/df")
async def get_df():
    try:
        return {"df": DashboardModel.df.to_json()}
    except AttributeError as e: 
        raise HTTPException(status_code=404, detail="Item not found") from e

@app.post("/df")
async def change_df(new_df: InputData):

    DashboardModel.df = pd.read_json(new_df.new_item)
    
    return {"df": DashboardModel.df.to_json()}

@app.get("/p_trdr")
async def get_p_trdr():
    try:
        return {"p_trdr": DashboardModel.p_trdr.to_json()}
    except AttributeError as e: 
        raise HTTPException(status_code=404, detail="Item not found") from e

@app.post("/p_trdr")
async def change_p_trdr(new_df: InputData):

    DashboardModel.p_trdr = pd.read_json(new_df.new_item)
    
    return {"p_trdr": DashboardModel.p_trdr.to_json()}


if __name__ == "__main__":
    uvicorn.run(app, debug=1, host="0.0.0.0", port=8000)