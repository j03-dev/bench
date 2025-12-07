from oxapy import HttpServer, Router, static_file
from pathlib import Path

import re
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

    bar_height = 0.4

    height = max(2, min(0.6 * len(frameworks), 6))

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


def main():
    generate_benchmark_graph()
    (
        HttpServer(("0.0.0.0", 5555))
        .attach(Router().route(static_file("/bench", "./static")))
        .run()
    )


if __name__ == "__main__":
    main()
