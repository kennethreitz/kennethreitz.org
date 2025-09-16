#!/usr/bin/env python3
"""
Pre-build cache generation script for Docker builds.

This script generates all cache files as JSON during the Docker build process,
eliminating the need for runtime cache preloading and making the app instantly responsive.
Uses a unified single-sweep approach for maximum efficiency.
"""

import json
import time
from pathlib import Path

# Import the unified cache function from engine
from engine import _generate_all_caches_unified

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
    """Generate all cache files using unified single-sweep approach."""
    print("=== Pre-building caches for Docker image (unified approach) ===")
    
    # Create cache directory
    cache_dir = Path('.cache')
    cache_dir.mkdir(exist_ok=True)
    
    total_start = time.time()
    
    try:
        print("Generating unified cache data...")
        unified_cache = _generate_all_caches_unified()
        
        # Write each cache type to separate files for backward compatibility
        cache_configs = [
            ('blog_posts', unified_cache['blog_posts']),
            ('sidenotes', unified_cache['sidenotes']),
            ('outlines', unified_cache['outlines']),
            ('quotes', unified_cache['quotes']),
            ('connections', unified_cache['connections']),
            ('terms', unified_cache['terms']),
        ]
        
        for name, cache_data in cache_configs:
            output_path = cache_dir / f'{name}.json'
            
            try:
                # Serialize the data
                serializable_data = serialize_cache_data(cache_data)
                
                # Write to JSON file
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump({
                        'data': serializable_data,
                        'generated_at': time.time(),
                        'generation_time': time.time() - total_start
                    }, f, separators=(',', ':'))  # Compact JSON
                
                # Log appropriate stats based on cache type
                if name == 'blog_posts':
                    print(f"✓ Generated {name} cache: {len(serializable_data)} posts")
                elif name == 'sidenotes':
                    print(f"✓ Generated {name} cache: {serializable_data['total_count']} sidenotes from {len(serializable_data['articles'])} articles")
                elif name == 'outlines':
                    print(f"✓ Generated {name} cache: {serializable_data['total_count']} headings from {len(serializable_data['articles'])} articles")
                elif name == 'quotes':
                    print(f"✓ Generated {name} cache: {serializable_data['total_count']} quotes from {len(serializable_data['articles'])} articles")
                elif name == 'connections':
                    print(f"✓ Generated {name} cache: {serializable_data['total_count']} outgoing cross-references")
                elif name == 'terms':
                    print(f"✓ Generated {name} cache: {len(serializable_data['terms'])} terms with {serializable_data['total_occurrences']} total occurrences")
                    
            except Exception as e:
                print(f"✗ Error generating {name} cache: {e}")
                # Create empty cache file to prevent runtime errors
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump({
                        'data': None,
                        'generated_at': time.time(),
                        'generation_time': 0,
                        'error': str(e)
                    }, f)
        
    except Exception as e:
        print(f"✗ Error in unified cache generation: {e}")
        import traceback
        traceback.print_exc()
    
    total_time = time.time() - total_start
    print(f"\n=== Unified cache pre-build completed in {total_time:.2f}s ===")
    print("App will now start instantly with pre-built caches!")

if __name__ == '__main__':
    main()