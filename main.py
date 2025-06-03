from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the static directory
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def serve_homepage():
    try:
        with open("static/index.html", "r",encoding="utf-8") as file:
            return HTMLResponse(content=file.read(), status_code=200)
    except FileNotFoundError:
        return HTMLResponse(content="<h1>404 - Page Not Found</h1>", status_code=404)


@app.post("/calculate_bmi")
async def calculate(
        weight: float = Query(..., gt=20, le=200, description="Enter your weight in KG"),
        height: float = Query(..., gt=1, le=3, description="Enter your height in M")
):
    bmi = weight / (height ** 2)
    if bmi < 18.5:
        m = "you need to get more weight"
    elif 18.5 <= bmi < 25:
        m = "you are normal"
    elif 25 <= bmi < 30:
        m = "you need to lose weight"
    else:
        m = "You are overweight, and need to visit doctor"
    return {
        "BMI": bmi,
        "Message": m
    }
