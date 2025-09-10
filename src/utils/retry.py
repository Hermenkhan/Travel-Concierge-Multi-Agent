import time
import requests

def call_api_with_retries(api_func, max_retries=2, backoff_factor=1.5):
    """
    Generic retry wrapper for API calls.
    api_func: function to execute (no args).
    """
    for attempt in range(max_retries + 1):
        try:
            return api_func()
        except Exception as e:
            if attempt < max_retries:
                sleep_time = backoff_factor ** attempt
                print(f"[Retry] Attempt {attempt+1} failed: {e}. Retrying in {sleep_time:.1f}s...")
                time.sleep(sleep_time)
            else:
                print(f"[Fallback] API failed after {max_retries} retries: {e}")
                return {"error": str(e), "fallback": True}
