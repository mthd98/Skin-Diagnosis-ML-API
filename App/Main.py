from fastapi import FastAPI
from Routers.MakePrediction import ml_router

description = """"""
contact_us= """"""
app = FastAPI(
            description=description, 
            title="Skin Cancer ML API", 
            version="0.0.1",contact=contact_us,         
            )



app.include_router(ml_router)

