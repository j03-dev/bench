from oxapy import HttpServer, Request, Response, Router, Status  # type: ignore
from pathlib import Path

import re
import mimetypes
import matplotlib.pyplot as plt
import logging

# Constants
BENCH_FILE = "bench.txt"
IMAGE_PATH = Path("static/benchmark_rps.png")


def generate_benchmark_graph():
    logging.log(1000, "Generating benchmark graph...")

    # Read and parse benchmark file
    try:
        with open(BENCH_FILE) as f:
            content = f.read()
    except FileNotFoundError:
        logging.log(1000, f"Benchmark file {BENCH_FILE} not found.")
        return

    frameworks = re.findall(r"# (.+)", content)
    reqs_per_sec = [float(x) for x in re.findall(r"Requests/sec:\s+([\d.]+)", content)]

    if len(frameworks) != len(reqs_per_sec):
        logging.log(1000, "Mismatch between frameworks and requests/sec")
        return

    # Adjust figure height based on number of bars (limit min and max)
    bar_height = 0.4

    # type: ignore
    height = max(2, min(0.6 * len(frameworks), 6))

    # Plot horizontal bar chart
    plt.figure(figsize=(8, height))
    plt.barh(frameworks, reqs_per_sec, color="#4BA3C3", height=bar_height)
    plt.xlabel("Requests/sec")
    plt.title("Benchmark: Requests/sec per Framework")
    plt.grid(axis="x", linestyle="--", alpha=0.5)
    plt.tight_layout(pad=1)

    IMAGE_PATH.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(IMAGE_PATH, dpi=120)
    plt.close()

    logging.log(1000, f"Graph saved to {IMAGE_PATH}")


# Generate the graph before launching the server
generate_benchmark_graph()

router = Router()


@router.get("/bench")
def bench(request: Request):
    if not IMAGE_PATH.exists():
        return Response("Benchmark image not found", status=Status.NOT_FOUND)

    with open(IMAGE_PATH, "rb") as file:
        content = file.read()
        content_type, _ = mimetypes.guess_type(str(IMAGE_PATH))
        return Response(
            content, content_type=content_type or "application/octet-stream"
        )


logging.log(1000, "Launching server on http://localhost:5555/bench ...")

server = HttpServer(("0.0.0.0", 5555))
server.attach(router)
server.run()
