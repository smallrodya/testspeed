#!/usr/bin/env python3
"""Sequential download speed probe: 10 GETs, then average time and MB/s."""

from __future__ import annotations

import argparse
import sys
import time
import urllib.error
import urllib.request
from typing import List, Tuple

DEFAULT_REQUESTS = 10
USER_AGENT = "speedtest.py/1.0 (+https://github.com)"
# 1 MB = 1_000_000 bytes (SI megabyte, usual for network speeds)
BYTES_PER_MB = 1_000_000


def fetch_once(url: str, timeout: float) -> Tuple[float, int]:
    """Download `url` once. Returns (elapsed_seconds, bytes_received)."""
    request = urllib.request.Request(
        url,
        headers={"User-Agent": USER_AGENT},
        method="GET",
    )
    started = time.perf_counter()
    with urllib.request.urlopen(request, timeout=timeout) as response:
        payload = response.read()
    elapsed = time.perf_counter() - started
    return elapsed, len(payload)


def run_probe(url: str, count: int, timeout: float) -> List[Tuple[float, int]]:
    results: List[Tuple[float, int]] = []
    for index in range(1, count + 1):
        print(f"[{index}/{count}] GET {url} ...", end=" ", flush=True)
        try:
            elapsed, size = fetch_once(url, timeout)
        except urllib.error.HTTPError as exc:
            print(f"HTTP {exc.code} {exc.reason}")
            raise SystemExit(1) from exc
        except urllib.error.URLError as exc:
            print(f"failed: {exc.reason}")
            raise SystemExit(1) from exc
        except TimeoutError as exc:
            print("timed out")
            raise SystemExit(1) from exc
        except Exception as exc:  # noqa: BLE001 — show any unexpected network error
            print(f"failed: {exc}")
            raise SystemExit(1) from exc

        speed = (size / BYTES_PER_MB) / elapsed if elapsed > 0 else 0.0
        print(f"{elapsed:.3f} s, {size} bytes, {speed:.2f} MB/s")
        results.append((elapsed, size))
    return results


def print_summary(results: List[Tuple[float, int]]) -> None:
    times = [item[0] for item in results]
    sizes = [item[1] for item in results]
    total_time = sum(times)
    total_bytes = sum(sizes)
    avg_time = total_time / len(times)
    avg_bytes = total_bytes / len(sizes)
    # Average throughput: all downloaded bytes over wall time of the 10 GETs
    mbps = (total_bytes / BYTES_PER_MB) / total_time if total_time > 0 else 0.0

    print()
    print("--- summary ---")
    print(f"requests:           {len(results)}")
    print(f"avg request time:   {avg_time:.3f} s")
    print(f"avg payload:        {avg_bytes:.0f} bytes")
    print(f"total downloaded:   {total_bytes} bytes ({total_bytes / BYTES_PER_MB:.2f} MB)")
    print(f"total time:         {total_time:.3f} s")
    print(f"average speed:      {mbps:.2f} MB/s")


def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Hit a URL sequentially (default 10 times), wait for each response, "
            "then print average request time, downloaded volume, and MB/s."
        )
    )
    parser.add_argument(
        "url",
        help="Address to download, preferably a reasonably large file/image",
    )
    parser.add_argument(
        "-n",
        "--count",
        type=int,
        default=DEFAULT_REQUESTS,
        help=f"How many sequential requests to run (default: {DEFAULT_REQUESTS})",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=60.0,
        help="Per-request timeout in seconds (default: 60)",
    )
    args = parser.parse_args(argv)
    if args.count < 1:
        parser.error("--count must be at least 1")
    if args.timeout <= 0:
        parser.error("--timeout must be greater than 0")
    if not args.url.startswith(("http://", "https://")):
        parser.error("url must start with http:// or https://")
    return args


def main(argv: List[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    results = run_probe(args.url, args.count, args.timeout)
    print_summary(results)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
