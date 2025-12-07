from oxapy import HttpServer, Router, get


greet = get("/greet/{name}", lambda _r, name: f"Hello, {name}!")
HttpServer(("127.0.0.1", 5555)).attach(Router().route(greet)).run()
