from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/greet/{name}")
def greet(name: str):
    return f"Hello, {name}!"


if __name__ == "__main__":
    print("Listening 127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="warning")
