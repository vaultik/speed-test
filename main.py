import argparse
import time

import requests


def measure_single_request(url: str) -> tuple[float, int]:
    """
    Make one GET request, wait for the full response body.

    Returns (elapsed seconds, downloaded bytes).
    """
    start = time.perf_counter()

    with requests.get(url, stream=True, timeout=10) as response:
        response.raise_for_status()

        downloaded_bytes = 0
        for piece in response.iter_content(chunk_size=8192):
            downloaded_bytes += len(piece)

    elapsed = time.perf_counter() - start
    return elapsed, downloaded_bytes


def measure_requests(url: str, count: int = 10) -> list[tuple[float, int]]:
    """Run several sequential requests, skip failed ones."""
    results = []

    for _ in range(count):
        try:
            result = measure_single_request(url)
            results.append(result)
        except requests.RequestException as error:
            print(f'Request failed: {error}')

    return results


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Measure average download speed for a URL'
    )
    parser.add_argument('url', help='URL to test')

    return parser.parse_args()


def format_size(size: float) -> str:
    if size >= 1024 * 1024:
        return f'{size / (1024 * 1024):.2f} MB'
    if size >= 1024:
        return f'{size / 1024:.0f} KB'

    return f'{size:.0f} B'


if __name__ == "__main__":
    args = parse_args()
    results = measure_requests(args.url)

    if not results:
        print('All requests failed, nothing to measure')
        raise SystemExit(1)

    times = [result[0] for result in results]
    sizes = [result[1] for result in results]

    average_time = sum(times) / len(times)
    average_size = sum(sizes) / len(sizes)
    speed = average_size / average_time / (1024 * 1024)

    print(f'Average time: {average_time:.2f}s')
    print(f'Average size: {format_size(average_size)}')
    print(f'Speed: {speed:.2f} MB/s')
