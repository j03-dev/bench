import multiprocessing
from oxapy import HttpServer, Router, get


def main():
    cpu_count = multiprocessing.cpu_count()
    (
        HttpServer(("127.0.0.1", 5555))
        .max_connections(200)
        .channel_capacity(cpu_count * 450)
        .attach(
            Router().route(get("/hello/{name}", lambda _r, name: f"Hello, {name}!"))
        )
        .run(workers=cpu_count)
    )


if __name__ == "__main__":
    main()
