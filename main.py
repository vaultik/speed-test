import argparse
import time

import requests

# IMG_URL = 'https://www.google.com/url?sa=t&source=web&rct=j&url=https%3A%2F%2Fwww.pexels.com%2Fsearch%2Fmoment%2F&ved=0CBYQjRxqFwoTCPieuqu1gpcDFQAAAAAdAAAAABA4&opi=89978449'


def measure_single_request(url: str) -> tuple[float, int]:
    """
    Делаем один get запрос, дожидаемся полной загрузки ответа.

    Возвращаем (время сек, объём байт).
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
    """Делаем несколько последовательных запросов."""
    results = []

    for _ in range(count):
        result = measure_single_request(url)
        results.append(result)

    return results


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('url')

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    results = measure_requests(args.url)

    times = [result[0] for result in results]
    sizes = [result[1] for result in results]

    average_time = sum(times) / len(times)
    average_size = sum(sizes) / len(sizes)
    speed = average_size / average_time / (1024 * 1024)

    print(f'Average time: {average_time:.3f}s, Average size {average_size}, Speed {speed}МБ/с')
