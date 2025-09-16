#!/usr/bin/env python3
"""
Pre-build cache generation script for Docker builds.

This script generates all cache files as JSON during the Docker build process,
eliminating the need for runtime cache preloading and making the app instantly responsive.
"""

import json
import time
from pathlib import Path

# Import the cache functions from engine
from engine import (
    _collect_all_blog_posts_cached,
    _extract_all_sidenotes_cached,
    _extract_all_outlines_cached,
    _extract_all_quotes_cached,
    _extract_all_connections_cached,
    _extract_all_terms_cached,
)

def serialize_cache_data(data):
    """Convert cache data to JSON-serializable format."""
    from datetime import datetime
    
    def convert_item(item):
        if isinstance(item, datetime):
            return item.isoformat()
        elif isinstance(item, dict):
            return {k: convert_item(v) for k, v in item.items()}
        elif isinstance(item, (list, tuple)):
            return [convert_item(i) for i in item]
        else:
            return item
    
    if isinstance(data, tuple):
        return convert_item(list(data))
    return convert_item(data)

def generate_cache_file(name, cache_function, output_path):
    """Generate a single cache file."""
    print(f"Generating {name} cache...")
    start_time = time.time()
    
    try:
        # Call the cache function to get the data
        cache_data = cache_function()
        
        # Serialize the data
        serializable_data = serialize_cache_data(cache_data)
        
        # Write to JSON file
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump({
                'data': serializable_data,
                'generated_at': time.time(),
                'generation_time': time.time() - start_time
            }, f, separators=(',', ':'))  # Compact JSON
        
        load_time = time.time() - start_time
        
        # Log appropriate stats based on cache type
        if name == 'blog_posts':
            print(f"✓ Generated {name} cache: {len(serializable_data)} posts in {load_time:.2f}s")
        elif name == 'sidenotes':
            print(f"✓ Generated {name} cache: {serializable_data['total_count']} sidenotes from {len(serializable_data['articles'])} articles in {load_time:.2f}s")
        elif name == 'outlines':
            print(f"✓ Generated {name} cache: {serializable_data['total_count']} headings from {len(serializable_data['articles'])} articles in {load_time:.2f}s")
        elif name == 'quotes':
            print(f"✓ Generated {name} cache: {serializable_data['total_count']} quotes from {len(serializable_data['articles'])} articles in {load_time:.2f}s")
        elif name == 'connections':
            print(f"✓ Generated {name} cache: {serializable_data['total_count']} cross-references in {load_time:.2f}s")
        elif name == 'terms':
            print(f"✓ Generated {name} cache: {len(serializable_data['terms'])} terms with {serializable_data['total_occurrences']} total occurrences in {load_time:.2f}s")
        else:
            print(f"✓ Generated {name} cache in {load_time:.2f}s")
            
    except Exception as e:
        print(f"✗ Error generating {name} cache: {e}")
        import traceback
        traceback.print_exc()
        # Create empty cache file to prevent runtime errors
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump({
                'data': None,
                'generated_at': time.time(),
                'generation_time': 0,
                'error': str(e)
            }, f)

def main():
    """Generate all cache files."""
    print("=== Pre-building caches for Docker image ===")
    
    # Create cache directory
    cache_dir = Path('.cache')
    cache_dir.mkdir(exist_ok=True)
    
    # Define cache generations
    cache_configs = [
        ('blog_posts', _collect_all_blog_posts_cached, cache_dir / 'blog_posts.json'),
        ('sidenotes', _extract_all_sidenotes_cached, cache_dir / 'sidenotes.json'),
        ('outlines', _extract_all_outlines_cached, cache_dir / 'outlines.json'),
        ('quotes', _extract_all_quotes_cached, cache_dir / 'quotes.json'),
        ('connections', _extract_all_connections_cached, cache_dir / 'connections.json'),
        ('terms', _extract_all_terms_cached, cache_dir / 'terms.json'),
    ]
    
    total_start = time.time()
    
    # Generate each cache file
    for name, cache_function, output_path in cache_configs:
        generate_cache_file(name, cache_function, output_path)
    
    total_time = time.time() - total_start
    print(f"\n=== Cache pre-build completed in {total_time:.2f}s ===")
    print("App will now start instantly with pre-built caches!")

if __name__ == '__main__':
    main()