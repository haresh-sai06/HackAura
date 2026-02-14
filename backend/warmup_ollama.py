"""
Warm up the Ollama model so the first real request isn't delayed by model load.

Usage examples:

# Single warm-up ping:
python warmup_ollama.py --model rapid-triage

# Warm up then keep model alive every 5 minutes (daemon mode):
python warmup_ollama.py --model rapid-triage --loop --interval 300

# Run N warm-up pings:
python warmup_ollama.py --model rapid-triage --iterations 3 --interval 10

Notes:
- The script tries to use the `ollama` Python package. If it's not available,
  it falls back to a direct HTTP POST to OLLAMA_HOST (default http://127.0.0.1:11434).
- Adjust `--timeout` if your environment has slow disk/GPU cold-starts.

"""

import time
import json
import logging
import argparse
import os

logger = logging.getLogger("warmup_ollama")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

try:
    import ollama
    HAS_OLLAMA_PKG = True
except Exception:
    HAS_OLLAMA_PKG = False
    import requests


def warmup_once(model: str, timeout: int = 300):
    """Send a single warm-up request to Ollama and return elapsed seconds and response."""
    prompt = "Warmup ping. Reply briefly with 'pong'."
    start = time.monotonic()

    try:
        if HAS_OLLAMA_PKG:
            # Use the ollama Python client
            resp = ollama.chat(model=model, format='text', messages=[{'role': 'user', 'content': prompt}], stream=False, timeout=timeout)
            # Response shape: {'message': {'role': 'assistant', 'content': '...'}}
            content = resp.get('message', {}).get('content', '')
        else:
            host = os.getenv('OLLAMA_HOST', 'http://127.0.0.1:11434')
            url = host.rstrip('/') + '/api/chat'
            payload = {
                'model': model,
                'messages': [{'role': 'user', 'content': prompt}],
                'format': 'text'
            }
            r = requests.post(url, json=payload, timeout=timeout)
            r.raise_for_status()
            content = r.json().get('message', {}).get('content', '')

        elapsed = time.monotonic() - start
        return elapsed, content

    except Exception as e:
        elapsed = time.monotonic() - start
        logger.error(f"Warmup failed: {e}")
        return elapsed, None


def main():
    parser = argparse.ArgumentParser(description='Warm up Ollama model to avoid cold starts')
    parser.add_argument('--model', type=str, default='rapid-triage', help='Ollama model name to warm')
    parser.add_argument('--iterations', type=int, default=1, help='Number of warmup pings to send')
    parser.add_argument('--interval', type=int, default=300, help='Seconds between pings when looping')
    parser.add_argument('--loop', action='store_true', help='Keep warmup running in a loop')
    parser.add_argument('--timeout', type=int, default=300, help='Request timeout in seconds')
    args = parser.parse_args()

    logger.info(f"Warmup script started. model={args.model} iterations={args.iterations} loop={args.loop} interval={args.interval}s")

    try:
        # Run initial iterations
        for i in range(max(1, args.iterations)):
            logger.info(f"Warmup ping {i+1}/{args.iterations} -> model: {args.model}")
            elapsed, content = warmup_once(args.model, timeout=args.timeout)
            if content:
                logger.info(f"Warmup success in {elapsed:.2f}s; response preview: {str(content)[:200]!s}")
            else:
                logger.warning(f"Warmup attempt returned no content (elapsed {elapsed:.2f}s)")

            # If not looping and multiple iterations requested, sleep between them
            if args.iterations > 1 and i < args.iterations - 1:
                time.sleep(args.interval)

        # If loop requested, keep pinging at interval
        if args.loop:
            logger.info("Entering keep-alive loop. Press Ctrl+C to stop.")
            while True:
                elapsed, content = warmup_once(args.model, timeout=args.timeout)
                if content:
                    logger.info(f"Keep-alive ping successful in {elapsed:.2f}s")
                else:
                    logger.warning(f"Keep-alive ping failed (elapsed {elapsed:.2f}s)")
                time.sleep(args.interval)

    except KeyboardInterrupt:
        logger.info("Warmup script stopped by user")


if __name__ == '__main__':
    main()
