import time
import requests


def measure_single_request(url: str) -> tuple[float, int]:
    """
    Делаем один get запрос, дожидаемся полной загрузки ответа.

    Возвращаем (время сек, объём байт)
    """
    start = time.perf_counter()

    with requests.get(url, stream=True, timeout=10) as response:
        response.raise_for_status()

        downloaded_bytes = 0
        for piece in response.iter_content(chunk_size=8192):
            downloaded_bytes += len(piece)

    elapsed = time.perf_counter() - start
    return elapsed, downloaded_bytes


if __name__ == "__main__":
    elapsed, downloaded_bytes = measure_single_request('https://www.google.com/url?sa=t&source=web&rct=j&url=https%3A%2F%2Fwww.pexels.com%2Fsearch%2Fmoment%2F&ved=0CBYQjRxqFwoTCPieuqu1gpcDFQAAAAAdAAAAABA4&opi=89978449')
    print(f'Time: {elapsed:.3f}s, Bytes: {downloaded_bytes}')

