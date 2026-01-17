"""
Gemini API Key Manager
Handles automatic fallback and rotation across multiple API keys
"""
import google.generativeai as genai
from config.settings import GEMINI_API_KEYS
from typing import Optional, Callable, Any
import asyncio
import time


class GeminiKeyManager:
    """
    Manages multiple Gemini API keys with automatic fallback.
    
    Features:
    - Automatic rotation when a key fails (rate limit, quota exceeded, etc.)
    - Tracks which keys are currently working
    - Cooldown period for failed keys
    - Thread-safe key rotation
    """
    
    def __init__(self, api_keys: list[str]):
        self.api_keys = api_keys
        self.current_key_index = 0
        self.failed_keys = {}  # {key_index: timestamp_when_failed}
        self.cooldown_period = 60  # Retry failed keys after 60 seconds
        
        if not self.api_keys:
            raise ValueError("No API keys provided to GeminiKeyManager")
        
        print(f"🔑 GeminiKeyManager initialized with {len(self.api_keys)} key(s)")
    
    def get_current_key(self) -> str:
        """Get the currently active API key"""
        # Clean up old failures (past cooldown period)
        current_time = time.time()
        self.failed_keys = {
            idx: timestamp 
            for idx, timestamp in self.failed_keys.items()
            if current_time - timestamp < self.cooldown_period
        }
        
        # Find next available key (not in failed_keys)
        for _ in range(len(self.api_keys)):
            if self.current_key_index not in self.failed_keys:
                return self.api_keys[self.current_key_index]
            self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
        
        # All keys failed recently - use the oldest failure
        print("⚠️ All API keys failed recently. Using least-recently-failed key...")
        oldest_failure_idx = min(self.failed_keys.keys(), key=lambda k: self.failed_keys[k])
        self.current_key_index = oldest_failure_idx
        del self.failed_keys[oldest_failure_idx]  # Give it another chance
        return self.api_keys[self.current_key_index]
    
    def mark_key_failed(self, key_index: Optional[int] = None):
        """Mark a key as failed and rotate to the next one"""
        if key_index is None:
            key_index = self.current_key_index
        
        self.failed_keys[key_index] = time.time()
        next_index = (key_index + 1) % len(self.api_keys)
        
        print(f"❌ API Key #{key_index + 1} failed. Rotating to key #{next_index + 1}...")
        self.current_key_index = next_index
    
    def create_model(self, model_name: str = 'gemini-2.5-flash'):
        """Create a GenerativeModel with the current API key"""
        current_key = self.get_current_key()
        genai.configure(api_key=current_key)
        return genai.GenerativeModel(model_name)
    
    async def execute_with_fallback(
        self, 
        func: Callable, 
        *args, 
        max_retries: int = None,
        **kwargs
    ) -> Any:
        """
        Execute a function with automatic API key fallback.
        
        Args:
            func: The function to execute (can be sync or async)
            max_retries: Maximum number of keys to try (default: all keys)
            *args, **kwargs: Arguments to pass to func
        
        Returns:
            The result of func
        
        Raises:
            Exception: If all keys fail
        """
        if max_retries is None:
            max_retries = len(self.api_keys)
        
        last_exception = None
        
        for attempt in range(max_retries):
            try:
                # Get fresh model with current key
                model = self.create_model()
                
                # Execute the function
                if asyncio.iscoroutinefunction(func):
                    result = await func(model, *args, **kwargs)
                else:
                    result = func(model, *args, **kwargs)
                
                # Success!
                if attempt > 0:
                    print(f"✅ Succeeded with API Key #{self.current_key_index + 1} after {attempt} fallback(s)")
                
                return result
                
            except Exception as e:
                error_message = str(e).lower()
                
                # Check if it's a rate limit / quota error
                is_key_issue = any(term in error_message for term in [
                    'rate limit',
                    'quota',
                    'resource exhausted',
                    '429',
                    'too many requests',
                    'invalid api key',
                    'api_key_invalid'
                ])
                
                if is_key_issue:
                    print(f"⚠️ API Key #{self.current_key_index + 1} hit limit: {str(e)[:100]}")
                    self.mark_key_failed()
                    last_exception = e
                    
                    # If we have more keys to try, continue
                    if attempt < max_retries - 1:
                        print(f"🔄 Retrying with next API key...")
                        continue
                else:
                    # Not a key issue - probably a real error (bad input, etc.)
                    print(f"❌ Non-key error: {str(e)[:200]}")
                    raise e
        
        # All keys failed
        raise Exception(
            f"All {max_retries} API key(s) failed. Last error: {last_exception}"
        )
    
    def get_stats(self) -> dict:
        """Get statistics about key usage"""
        return {
            "total_keys": len(self.api_keys),
            "current_key_index": self.current_key_index,
            "failed_keys_count": len(self.failed_keys),
            "failed_keys": list(self.failed_keys.keys()),
            "available_keys": len(self.api_keys) - len(self.failed_keys)
        }


# Global singleton instance
key_manager = GeminiKeyManager(GEMINI_API_KEYS) if GEMINI_API_KEYS else None
