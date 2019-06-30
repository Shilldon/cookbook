import os
from flask import Flask, render_template
import json

app=Flask(__name__)

@app.route("/")

def index():
    return "<h1>Hello world.</h1><h2>This is a recipe book.</h2>"
    
    
if __name__ =="__main__":
    app.run(host=os.environ.get("IP"), port=int(os.environ.get("PORT")), debug=True)    
    