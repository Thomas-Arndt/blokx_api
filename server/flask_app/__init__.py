from flask import Flask
from flask_app.models.model_miner import Miner

DATABASE='blokx_schema'

# MINER=Miner()


app=Flask(__name__)
app.secret_key="fd77e312-fabf-49e5-9a9f-ed9c8fb77c1e"

