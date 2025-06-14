import multiprocessing

from sanic import Sanic
from sanic.response import text

app = Sanic("my-hello-world-app")


@app.route("/greet/<name:str>", methods=["GET"])
async def greet(request, name):
    return text(f"Hello {name}")


if __name__ == "__main__":
    workers = multiprocessing.cpu_count()
    app.run(host="0.0.0.0", port=3000, workers=workers, debug=False, access_log=False)
