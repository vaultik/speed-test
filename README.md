# Speed Test

A small Python script for checking download speed for a given URL.

The script makes 10 sequential requests and calculates:

* average response time;
* average downloaded data size;
* average download speed.

## Requirements

* Python 3.12+
* uv

## Installation

Install the project dependencies:

```bash
uv sync
```

## Usage

Run the script with a URL:

```bash
uv run python main.py "https://httpbin.org/bytes/1000000"
```

Example output:

```text
Average time: 1.95s
Average size: 100 KB
Speed: 0.05 MB/s
```

If a request fails, the error is displayed and the script continues with the remaining requests.

If all requests fail, the script exits without calculating the statistics.
