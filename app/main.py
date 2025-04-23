from fastapi import FastAPI
from datetime import datetime
app = FastAPI()
start_time  = datetime.now()



@app.get("/")
def test():
    return {"message": "This is an API for health check"}
@app.get("/check")
def health_check():
    current_time = datetime.now()
    return {"status": "OK",
            "uptime": current_time - start_time,
            "current time": current_time,
            "started at ": start_time}