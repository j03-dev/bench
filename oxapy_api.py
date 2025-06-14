from oxapy import HttpServer, Router  # type: ignore

router = Router()


@router.get("/greet/{name}")
def greet(request, name: str):
    return f"Hello, {name}!"


app = HttpServer(("127.0.0.1", 5555))
app.attach(router)
app.run()
