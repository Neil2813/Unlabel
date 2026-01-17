"""
In-Memory Cache for AI Analysis Results
Uses LRU (Least Recently Used) cache strategy
"""
from functools import lru_cache
from typing import Optional, Dict, Any
import hashlib
import json
import time
from datetime import datetime, timedelta


class AnalysisCache:
    """
    In-memory cache for ingredient analyses.
    Uses hash of ingredient text as cache key.
    """
    
    def __init__(self, max_size: int = 1000, ttl_seconds: int = 3600):
        """
        Args:
            max_size: Maximum number of cached items
            ttl_seconds: Time-to-live in seconds (default: 1 hour)
        """
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds
        self.hits = 0
        self.misses = 0
    
    def _generate_key(self, text: str) -> str:
        """Generate cache key from text using SHA256 hash"""
        normalized_text = text.lower().strip()
        return hashlib.sha256(normalized_text.encode()).hexdigest()
    
    def _is_expired(self, timestamp: datetime) -> bool:
        """Check if cache entry has expired"""
        return datetime.now() - timestamp > timedelta(seconds=self.ttl_seconds)
    
    def _evict_oldest(self):
        """Remove oldest cache entry when max size is reached"""
        if len(self.cache) >= self.max_size:
            oldest_key = min(self.cache.keys(), key=lambda k: self.cache[k]['timestamp'])
            del self.cache[oldest_key]
            print(f"Cache evicted: {oldest_key[:8]}...")
    
    def get(self, text: str) -> Optional[Any]:
        """
        Retrieve cached analysis result.
        Returns None if not found or expired.
        """
        key = self._generate_key(text)
        
        if key not in self.cache:
            self.misses += 1
            return None
        
        entry = self.cache[key]
        
        # Check if expired
        if self._is_expired(entry['timestamp']):
            del self.cache[key]
            self.misses += 1
            return None
        
        # Cache hit
        self.hits += 1
        entry['access_count'] += 1
        entry['last_accessed'] = datetime.now()
        
        print(f"✅ Cache hit: {key[:8]}... (hit rate: {self.get_hit_rate():.1%})")
        return entry['data']
    
    def set(self, text: str, data: Any):
        """Store analysis result in cache"""
        key = self._generate_key(text)
        
        # Evict oldest if necessary
        self._evict_oldest()
        
        self.cache[key] = {
            'data': data,
            'timestamp': datetime.now(),
            'last_accessed': datetime.now(),
            'access_count': 0
        }
        
        print(f"💾 Cache stored: {key[:8]}... (total: {len(self.cache)})")
    
    def invalidate(self, text: str):
        """Remove specific entry from cache"""
        key = self._generate_key(text)
        if key in self.cache:
            del self.cache[key]
            print(f"🗑️ Cache invalidated: {key[:8]}...")
    
    def clear(self):
        """Clear entire cache"""
        self.cache.clear()
        self.hits = 0
        self.misses = 0
        print("🧹 Cache cleared")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        return {
            'size': len(self.cache),
            'max_size': self.max_size,
            'hits': self.hits,
            'misses': self.misses,
            'hit_rate': self.get_hit_rate(),
            'ttl_seconds': self.ttl_seconds
        }
    
    def get_hit_rate(self) -> float:
        """Calculate cache hit rate"""
        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0.0


# Global cache instances
ingredient_analysis_cache = AnalysisCache(max_size=1000, ttl_seconds=3600)  # 1 hour TTL
decision_cache = AnalysisCache(max_size=500, ttl_seconds=1800)  # 30 min TTL
