# Enable gevent async I/O optimizations
import gevent
from gevent import monkey
monkey.patch_all()  # Patch standard library for async I/O
from gevent.pool import Pool

import os
import mistune
from flask import Flask, render_template, abort, request, url_for, jsonify, redirect, Response
from pathlib import Path
import re
from datetime import datetime
from urllib.parse import quote
import json
import time
from xml.sax.saxutils import escape
import html
from collections import defaultdict
import hashlib
import base64
import math

app = Flask(__name__, template_folder='templates')

# Configuration
app.config['DISABLE_ANALYTICS'] = os.environ.get('DISABLE_ANALYTICS', 'false').lower() == 'true'

# Add custom Jinja2 filters
@app.template_filter('strftime')
def strftime_filter(date, fmt='%Y-%m-%d'):
    """Format a datetime object using strftime."""
    if date is None:
        return ''
    if isinstance(date, str) and date.lower() == 'now':
        date = datetime.now()
    return date.strftime(fmt)

@app.template_filter('unescape')
def unescape_filter(text):
    """Unescape HTML entities in text."""
    if text is None:
        return ''
    return html.unescape(text)

def _process_single_file(file_path):
    """Process a single file for cache generation. Returns data structure for the file."""
    try:
        full_path = Path(file_path)
        
        # Read raw content directly for processing
        with open(full_path, 'r', encoding='utf-8') as f:
            raw_content = f.read()
        
        # Get processed content data
        content_data = render_markdown_file(full_path)
        html_content = content_data['content']
        
        result = {
            'file_path': file_path,
            'full_path': full_path,
            'raw_content': raw_content,
            'content_data': content_data,
            'html_content': html_content,
            'success': True
        }
        
        return result
    except Exception as e:
        return {
            'file_path': file_path,
            'error': str(e),
            'success': False
        }


def _generate_all_caches_unified():
    """Generate all caches in a single sweep through the data."""
    import glob
    from collections import defaultdict
    import re
    
    def simple_extract_excerpt(content, max_words=50):
        """Simple excerpt extraction for unified cache generation."""
        # Remove front matter
        content = re.sub(r'^---\s*\n.*?\n---\s*\n', '', content, flags=re.DOTALL)
        # Remove title (first # line)
        content = re.sub(r'^# .+?$', '', content, flags=re.MULTILINE)
        # Remove date lines
        content = re.sub(r'^\*[A-Za-z]+ \d{4}\*\s*$', '', content, flags=re.MULTILINE)
        # Remove sidenotes (label + input + span structure)
        content = re.sub(r'<label[^>]*class="margin-toggle sidenote-number"[^>]*></label><input[^>]*class="margin-toggle"[^>]*/>(<span class="sidenote">.*?</span>)', '', content, flags=re.DOTALL)
        # Remove any remaining HTML tags
        content = re.sub(r'<[^>]+>', '', content)
        # Remove markdown links but keep the text
        content = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', content)
        # Remove markdown emphasis
        content = re.sub(r'[*_`]', '', content)
        # Get first paragraph
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        if lines:
            first_para = lines[0]
            words = first_para.split()[:max_words]
            excerpt = ' '.join(words)
            if len(words) == max_words:
                excerpt += '...'
            return excerpt
        return ''
    
    # Initialize all data structures
    sidenotes_data = defaultdict(list)
    outlines_data = defaultdict(list)
    quotes_data = defaultdict(list)
    connections_outgoing = defaultdict(list)
    connections_incoming = defaultdict(list)
    terms_data = defaultdict(list)
    blog_posts = []
    
    # Get all markdown files from /data/ directory
    all_files = glob.glob('data/**/*.md', recursive=True)
    all_files = [f for f in all_files if not f.endswith('index.md')]
    
    print(f"Unified cache generation: Processing {len(all_files)} files...")
    
    # Use gevent pool for parallel file processing
    pool = Pool(20)  # Process up to 20 files concurrently
    file_results = pool.map(_process_single_file, all_files)
    
    # Process results from parallel file processing
    for result in file_results:
        if not result['success']:
            print(f"Error processing {result['file_path']}: {result['error']}")
            continue
            
        file_path = result['file_path']
        full_path = result['full_path']
        raw_content = result['raw_content']
        content_data = result['content_data']
        html_content = result['html_content']
        
        # Generate blog post entry if this is an essay
        if full_path.parent.name == 'essays':
            # Use the robust extract_intelligent_date function
            date_obj = extract_intelligent_date(full_path, content_data)
            
            if date_obj is not None:
                blog_posts.append({
                    'title': content_data['title'],
                    'path': f"/{full_path.relative_to(Path('data')).with_suffix('')}",
                    'url': f"/{full_path.relative_to(Path('data')).with_suffix('')}",
                    'file_path': str(full_path),  # Add actual file path for mapping
                    'pub_date': date_obj,
                    'date_str': date_obj.strftime('%Y-%m-%d'),
                    'excerpt': simple_extract_excerpt(raw_content),
                    'description': simple_extract_excerpt(raw_content),
                    'word_count': len(raw_content.split()),
                    'category': full_path.parent.name,
                    'unique_icon': generate_unique_svg_icon(content_data['title'], size=24)
                })
            else:
                print(f"DEBUG: Could not extract date from {full_path.name} in unified cache")
            
            # Extract sidenotes with their IDs
            # Pattern matches the full sidenote structure: input + span
            sidenote_pattern = r'<input[^>]*id="([^"]*)"[^>]*class="margin-toggle"[^>]*/>.*?<span class="sidenote">(.*?)</span>'
            sidenotes = re.findall(sidenote_pattern, html_content, re.DOTALL)
            if sidenotes:
                for sidenote_id, sidenote_content in sidenotes:
                    clean_sidenote = re.sub(r'<[^>]+>', '', sidenote_content).strip()
                    if clean_sidenote:
                        sidenotes_data[file_path].append({
                            'text': clean_sidenote,
                            'html': sidenote_content.strip(),
                            'id': sidenote_id
                        })
            
            # Extract outlines (headings)
            heading_pattern = r'(<h([1-6])[^>]*>.*?</h[1-6]>)'
            headings = re.findall(heading_pattern, html_content)
            if headings:
                for full_tag, level in headings:
                    # Extract just the inner content for text
                    inner_pattern = r'<h[1-6][^>]*>(.*?)</h[1-6]>'
                    inner_match = re.search(inner_pattern, full_tag)
                    if inner_match:
                        clean_heading = re.sub(r'<[^>]+>', '', inner_match.group(1)).strip()
                        if clean_heading and not clean_heading.startswith('fn:'):
                            outlines_data[file_path].append({
                                'level': int(level),
                                'text': clean_heading,
                                'html': full_tag.strip()
                            })
            
            # Extract quotes (blockquotes)
            quote_pattern = r'<blockquote[^>]*>(.*?)</blockquote>'
            quotes = re.findall(quote_pattern, html_content, re.DOTALL)
            if quotes:
                for quote in quotes:
                    clean_quote = re.sub(r'<[^>]+>', '', quote).strip()
                    if clean_quote:
                        quotes_data[file_path].append({
                            'text': clean_quote,
                            'html': quote.strip()
                        })
            
            # Extract connections (cross-references)
            connection_pattern = r'\[([^\]]+)\]\((/[^)]+)\)'
            connections = re.findall(connection_pattern, raw_content)
            if connections:
                for link_text, link_url in connections:
                    # Include all internal links (starting with /) except external ones
                    if link_url.startswith('/') and not link_url.startswith('//'):
                        connections_outgoing[file_path].append({
                            'text': link_text,
                            'url': link_url,
                            'target_file': link_url
                        })
                        # Track incoming references
                        connections_incoming[link_url].append({
                            'text': link_text,
                            'source_file': file_path,
                            'context': link_text
                        })
            
            # Extract terms for index
            # Simple approach: extract words that appear in multiple files
            words = re.findall(r'\b[A-Z][a-zA-Z]{3,}\b', raw_content)
            for word in set(words):
                if len(word) > 3 and word not in ['This', 'That', 'They', 'When', 'Where', 'What', 'Which']:
                    terms_data[word].append({
                        'file': file_path,
                        'context': word
                    })
    
    # Sort blog posts by date (newest first)
    blog_posts.sort(key=lambda x: x['pub_date'], reverse=True)
    
    # Create URL and metadata mappings for terms processing
    url_metadata = {}
    file_to_url = {}
    for post in blog_posts:
        url_metadata[post['url']] = post
        file_path = post.get('file_path') or post.get('path')
        if file_path:
            file_to_url[file_path] = post['url']
    
    # Process terms to only include ones that appear in multiple files
    filtered_terms = {term: refs for term, refs in terms_data.items() if len(refs) >= 2}
    final_terms = {}
    total_term_occurrences = 0
    for term, refs in sorted(filtered_terms.items()):
        # Convert refs to articles format expected by template
        # Group by file to get counts per article
        file_counts = {}
        for ref in refs:
            file_path = ref['file']
            if file_path not in file_counts:
                file_counts[file_path] = 0
            file_counts[file_path] += 1
        
        articles = []
        for file_path, count in file_counts.items():
            # Map file path to article URL and title
            url = file_to_url.get(file_path, '')
            if url:
                metadata = url_metadata.get(url, {})
                title = metadata.get('title', '')
                if title:  # Only include articles with valid titles
                    articles.append({
                        'url': url,
                        'title': title,
                        'count': count
                    })
        
        if articles:  # Only include terms that have valid articles
            final_terms[term] = {
                'articles': articles,
                'total_count': sum(file_counts.values()),
                'article_count': len(articles)
            }
            total_term_occurrences += sum(file_counts.values())
    
    # Build final cache structures
    total_sidenotes = sum(len(notes) for notes in sidenotes_data.values())
    
    unified_cache = {
        'blog_posts': blog_posts,
        'sidenotes': {
            'articles': dict(sidenotes_data),
            'total_count': total_sidenotes
        },
        'outlines': {
            'articles': dict(outlines_data),
            'total_count': sum(len(headings) for headings in outlines_data.values())
        },
        'quotes': {
            'articles': dict(quotes_data),
            'total_count': sum(len(quotes) for quotes in quotes_data.values())
        },
        'connections': {
            'outgoing_refs': dict(connections_outgoing),
            'incoming_refs': dict(connections_incoming),
            'total_count': sum(len(refs) for refs in connections_outgoing.values())
        },
        'terms': {
            'terms': final_terms,
            'total_occurrences': total_term_occurrences
        }
    }
    
    return unified_cache

@app.context_processor
def inject_index_counts():
    """Make index counts available to all templates."""
    try:
        # Use optimized MetadataCache instead of old cached functions
        sidenotes_data = metadata_cache.get_sidenotes()
        outlines_data = metadata_cache.get_outlines()
        quotes_data = metadata_cache.get_quotes()
        connections_data = metadata_cache.get_connections()
        terms_data = metadata_cache.get_terms()
        
        return {
            'index_counts': {
                'sidenotes': sidenotes_data.get('total_count', 0),
                'outlines': outlines_data.get('total_count', 0),
                'quotes': quotes_data.get('total_count', 0),
                'connections_outgoing': connections_data.get('total_outgoing', 0),
                'connections_incoming': connections_data.get('total_incoming', 0),
                'terms': terms_data.get('total_terms', 0),
                'terms_total_refs': terms_data.get('total_occurrences', 0)
            }
        }
    except Exception:
        # Fallback to prevent template errors
        return {
            'index_counts': {
                'sidenotes': 0,
                'outlines': 0,
                'quotes': 0,
                'connections_outgoing': 0,
                'connections_incoming': 0,
                'terms': 0,
                'terms_total_refs': 0
            }
        }

DATA_DIR = Path('data')

# Import the clean SVG icon generator
from svg_icon_generator import generate_unique_svg_icon

def generate_unique_svg_icon_OLD(title, size=24):
    """Generate a sophisticated unique SVG icon based on the title string."""
    # Create multiple hashes for more entropy
    hash_obj = hashlib.md5(title.encode())
    hash_bytes = hash_obj.digest()
    
    # Use SHA256 for additional entropy
    sha_hash = hashlib.sha256(title.encode()).digest()
    
    # Extract values from hash for various parameters
    hue1 = (hash_bytes[0] * 360) // 256
    hue2 = (hash_bytes[1] * 360) // 256
    saturation = 50 + (hash_bytes[2] * 30) // 256  # 50-80% saturation
    lightness = 40 + (hash_bytes[3] * 35) // 256   # 40-75% lightness
    
    # Choose pattern type - expanded to 20 different patterns for much more diversity
    pattern_type = hash_bytes[4] % 20
    
    # Create gradient colors
    color1 = f"hsl({hue1}, {saturation}%, {lightness}%)"
    color2 = f"hsl({hue2}, {saturation + 10}%, {lightness + 15}%)"
    
    # Generate gradient definition
    gradient_angle = (sha_hash[0] * 360) // 256
    gradient_id = f"grad_{abs(hash(title)) % 10000}"
    
    shapes = []
    defs = []
    
    if pattern_type == 0:  # Layered circles with gradients
        defs.append(f'''<linearGradient id="{gradient_id}" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="{color1}"/>
            <stop offset="100%" stop-color="{color2}"/>
        </linearGradient>''')
        
        # Multiple concentric circles
        for i in range(3):
            radius = size // 3 - i * (size // 12)
            opacity = 0.7 + i * 0.1
            shapes.append(f'<circle cx="{size//2}" cy="{size//2}" r="{radius}" fill="url(#{gradient_id})" opacity="{opacity}"/>')
            
    elif pattern_type == 1:  # Flower of Life
        defs.append(f'''<radialGradient id="{gradient_id}" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stop-color="{color1}"/>
            <stop offset="100%" stop-color="{color2}"/>
        </radialGradient>''')
        
        # Sacred Flower of Life pattern - 6 surrounding circles around center
        center_x, center_y = size // 2, size // 2
        radius = size // 5
        
        # Center circle
        shapes.append(f'<circle cx="{center_x}" cy="{center_y}" r="{radius}" fill="none" stroke="url(#{gradient_id})" stroke-width="2" opacity="0.8"/>')
        
        # Six surrounding circles
        for i in range(6):
            angle = (i * 60) * math.pi / 180
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            shapes.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{radius}" fill="none" stroke="url(#{gradient_id})" stroke-width="2" opacity="0.7"/>')
        
        # Outer petals for extended flower
        for i in range(12):
            angle = (i * 30) * math.pi / 180
            x = center_x + radius * 1.732 * math.cos(angle)  # sqrt(3) spacing
            y = center_y + radius * 1.732 * math.sin(angle)
            shapes.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{radius//2}" fill="none" stroke="{color2}" stroke-width="1" opacity="0.5"/>')
        
    elif pattern_type == 2:  # Crystalline line art
        defs.append(f'''<linearGradient id="{gradient_id}" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="{color1}"/>
            <stop offset="50%" stop-color="{color2}"/>
            <stop offset="100%" stop-color="{color2}"/>
        </linearGradient>''')
        
        # Create elegant crystal structure in line art
        center_x, center_y = size // 2, size // 2
        points = []
        for i in range(6):
            angle = (i * 60) * math.pi / 180
            x = center_x + (size // 3) * math.cos(angle)
            y = center_y + (size // 3) * math.sin(angle)
            points.append(f"{x:.1f},{y:.1f}")
        
        # Main hexagonal outline with elegant stroke
        shapes.append(f'<polygon points="{" ".join(points)}" fill="none" stroke="url(#{gradient_id})" stroke-width="2.5" opacity="0.8"/>')
        
        # Inner crystalline structure with delicate lines
        for i in range(6):
            angle = (i * 60) * math.pi / 180
            x = center_x + (size // 6) * math.cos(angle)
            y = center_y + (size // 6) * math.sin(angle)
            shapes.append(f'<line x1="{center_x}" y1="{center_y}" x2="{x:.1f}" y2="{y:.1f}" stroke="{color2}" stroke-width="1.5" opacity="0.6"/>')
        
        # Central sacred point
        shapes.append(f'<circle cx="{center_x}" cy="{center_y}" r="2" fill="none" stroke="{color1}" stroke-width="1.5" opacity="0.9"/>')
            
    elif pattern_type == 3:  # Flowing wave interference - line art
        defs.append(f'''<linearGradient id="{gradient_id}" x1="0%" y1="50%" x2="100%" y2="50%">
            <stop offset="0%" stop-color="{color1}"/>
            <stop offset="30%" stop-color="{color2}"/>
            <stop offset="70%" stop-color="{color2}"/>
            <stop offset="100%" stop-color="{color1}"/>
        </linearGradient>''')
        
        # Create flowing wave-like paths with graceful curves
        for wave in range(3):
            path_data = f"M 0,{size//2}"
            for x in range(0, size, 1):
                frequency = 0.15 + wave * 0.08
                amplitude = size // 8
                phase_shift = wave * 1.5
                y = size // 2 + amplitude * math.sin(x * frequency + phase_shift)
                path_data += f" L {x},{y:.1f}"
            
            stroke_width = 2.5 - wave * 0.5
            opacity = 0.85 - wave * 0.15
            shapes.append(f'<path d="{path_data}" stroke="url(#{gradient_id})" stroke-width="{stroke_width:.1f}" fill="none" opacity="{opacity:.2f}" stroke-linecap="round"/>')
            
    elif pattern_type == 4:  # Sacred Golden Ratio Spiral - refined line art
        defs.append(f'''<linearGradient id="{gradient_id}" x1="20%" y1="20%" x2="80%" y2="80%">
            <stop offset="0%" stop-color="{color2}"/>
            <stop offset="40%" stop-color="{color2}"/>
            <stop offset="100%" stop-color="{color1}"/>
        </linearGradient>''')
        
        # Sacred golden ratio spiral with elegant curves
        center_x, center_y = size // 2, size // 2
        golden_ratio = 1.618033988749
        
        # Create smooth logarithmic spiral based on golden ratio
        path_data = f"M {center_x},{center_y}"
        for t in range(0, 400, 2):  # Smoother curve with more points
            angle = t * math.pi / 180
            # Golden ratio growth with refined scaling
            radius = (size // 10) * math.pow(golden_ratio, angle / (math.pi / 1.8))
            if radius > size // 2 - 2:
                break
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            path_data += f" L {x:.1f},{y:.1f}"
        
        shapes.append(f'<path d="{path_data}" stroke="url(#{gradient_id})" stroke-width="3" fill="none" opacity="0.85" stroke-linecap="round"/>')
        
        # Subtle Fibonacci rectangle outlines
        fib_sizes = [2, 3, 5, 8]
        for i, fib in enumerate(fib_sizes):
            if fib * 2 > size // 4:
                break
            square_size = fib * 2
            x = center_x - square_size // 2 + i * 1.5
            y = center_y - square_size // 2 + i * 1.5
            opacity = 0.4 - i * 0.08
            shapes.append(f'<rect x="{x}" y="{y}" width="{square_size}" height="{square_size}" fill="none" stroke="{color2}" stroke-width="1" opacity="{opacity:.2f}"/>')
            
        # Sacred center - golden ratio point
        shapes.append(f'<circle cx="{center_x}" cy="{center_y}" r="1.5" fill="none" stroke="{color1}" stroke-width="2" opacity="0.9"/>')
        
    elif pattern_type == 5:  # Tessellation pattern
        defs.append(f'''<pattern id="{gradient_id}" x="0" y="0" width="8" height="8" patternUnits="userSpaceOnUse">
            <rect width="8" height="8" fill="{color1}"/>
            <circle cx="4" cy="4" r="2" fill="{color2}" opacity="0.7"/>
        </pattern>''')
        
        # Create tessellated hexagon
        points = []
        for i in range(6):
            angle = (i * 60) * 3.14159 / 180
            x = size // 2 + (size // 2.5) * math.cos(angle)
            y = size // 2 + (size // 2.5) * math.sin(angle)
            points.append(f"{x:.1f},{y:.1f}")
        
        shapes.append(f'<polygon points="{" ".join(points)}" fill="url(#{gradient_id})" stroke="{color2}" stroke-width="1"/>')
        
    elif pattern_type == 6:  # Fractal tree
        defs.append(f'''<linearGradient id="{gradient_id}" x1="0%" y1="100%" x2="0%" y2="0%">
            <stop offset="0%" stop-color="{color1}"/>
            <stop offset="100%" stop-color="{color2}"/>
        </linearGradient>''')
        
        def draw_branch(x, y, angle, length, depth):
            if depth == 0 or length < 2:
                return []
            end_x = x + length * math.cos(angle)
            end_y = y + length * math.sin(angle)
            branches = [f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{end_x:.1f}" y2="{end_y:.1f}" stroke="url(#{gradient_id})" stroke-width="{depth}" opacity="{0.8 if depth > 1 else 0.6}"/>']
            branches.extend(draw_branch(end_x, end_y, angle - 0.5, length * 0.7, depth - 1))
            branches.extend(draw_branch(end_x, end_y, angle + 0.5, length * 0.7, depth - 1))
            return branches
        
        shapes.extend(draw_branch(size//2, size*0.9, -math.pi/2, size//3, 4))
        
    elif pattern_type == 7:  # Dot matrix
        dot_size = size // 12
        spacing = size // 6
        for x in range(spacing, size - spacing + 1, spacing):
            for y in range(spacing, size - spacing + 1, spacing):
                opacity = 0.4 + (hash(f"{x},{y}") % 6) * 0.1
                color = color1 if (x + y) % 2 == 0 else color2
                shapes.append(f'<circle cx="{x}" cy="{y}" r="{dot_size}" fill="{color}" opacity="{opacity}"/>')
                
    elif pattern_type == 8:  # Triangular mosaic
        defs.append(f'''<linearGradient id="{gradient_id}" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="{color1}"/>
            <stop offset="50%" stop-color="{color2}"/>
            <stop offset="100%" stop-color="{color1}"/>
        </linearGradient>''')
        
        # Create triangular pattern
        tri_size = size // 3
        for i in range(3):
            for j in range(3):
                x = j * tri_size
                y = i * tri_size
                if (i + j) % 2 == 0:
                    shapes.append(f'<polygon points="{x},{y} {x+tri_size},{y} {x+tri_size//2},{y+tri_size}" fill="url(#{gradient_id})" opacity="0.8"/>')
                else:
                    shapes.append(f'<polygon points="{x},{y+tri_size} {x+tri_size},{y+tri_size} {x+tri_size//2},{y}" fill="{color2}" opacity="0.6"/>')
                    
    elif pattern_type == 9:  # Organic bubbles
        defs.append(f'''<radialGradient id="{gradient_id}" cx="30%" cy="30%" r="70%">
            <stop offset="0%" stop-color="{color2}"/>
            <stop offset="100%" stop-color="{color1}"/>
        </radialGradient>''')
        
        # Create organic bubble pattern
        bubble_positions = [
            (size * 0.3, size * 0.25, size // 6),
            (size * 0.7, size * 0.4, size // 8),
            (size * 0.5, size * 0.7, size // 5),
            (size * 0.2, size * 0.6, size // 10),
            (size * 0.8, size * 0.8, size // 7),
            (size * 0.6, size * 0.2, size // 9)
        ]
        
        for i, (x, y, radius) in enumerate(bubble_positions):
            opacity = 0.7 - (i % 3) * 0.15
            bubble_color = f"url(#{gradient_id})" if i % 2 == 0 else color2
            shapes.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{radius}" fill="{bubble_color}" opacity="{opacity}"/>')
            
    elif pattern_type == 10:  # Metatron's Cube
        defs.append(f'''<linearGradient id="{gradient_id}" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="{color1}"/>
            <stop offset="100%" stop-color="{color2}"/>
        </radialGradient>''')
        
        # Sacred Metatron's Cube - 13 circles of creation
        center_x, center_y = size // 2, size // 2
        radius = size // 8
        
        # Center circle
        shapes.append(f'<circle cx="{center_x}" cy="{center_y}" r="{radius//2}" fill="url(#{gradient_id})" opacity="0.9"/>')
        
        # Inner 6 circles (hexagonal pattern)
        for i in range(6):
            angle = (i * 60) * math.pi / 180
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            shapes.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{radius//3}" fill="none" stroke="url(#{gradient_id})" stroke-width="2" opacity="0.8"/>')
        
        # Outer 6 circles
        for i in range(6):
            angle = (i * 60) * math.pi / 180
            x = center_x + radius * 2 * math.cos(angle)
            y = center_y + radius * 2 * math.sin(angle)
            shapes.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{radius//4}" fill="none" stroke="{color2}" stroke-width="1" opacity="0.6"/>')
        
        # Connect with sacred lines (Fruit of Life pattern)
        for i in range(6):
            angle1 = (i * 60) * math.pi / 180
            angle2 = ((i + 1) * 60) * math.pi / 180
            x1 = center_x + radius * math.cos(angle1)
            y1 = center_y + radius * math.sin(angle1)
            x2 = center_x + radius * math.cos(angle2)
            y2 = center_y + radius * math.sin(angle2)
            shapes.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color2}" stroke-width="1" opacity="0.4"/>')
            
    elif pattern_type == 11:  # Flower petals
        defs.append(f'''<radialGradient id="{gradient_id}" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stop-color="{color2}"/>
            <stop offset="100%" stop-color="{color1}"/>
        </radialGradient>''')
        
        num_petals = 6 + (hash_bytes[6] % 6)  # 6-12 petals
        for i in range(num_petals):
            angle = (i * 360 / num_petals) * math.pi / 180
            x = size // 2 + (size // 3) * math.cos(angle)
            y = size // 2 + (size // 3) * math.sin(angle)
            shapes.append(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{size//8}" ry="{size//6}" fill="url(#{gradient_id})" opacity="0.8" transform="rotate({i * 360 / num_petals} {x:.1f} {y:.1f})"/>')
        
        # Center
        shapes.append(f'<circle cx="{size//2}" cy="{size//2}" r="{size//10}" fill="{color1}"/>')
        
    elif pattern_type == 12:  # Diamond lattice
        diamond_size = size // 6
        for x in range(diamond_size, size, diamond_size * 2):
            for y in range(diamond_size, size, diamond_size * 2):
                points = [
                    f"{x},{y - diamond_size//2}",
                    f"{x + diamond_size//2},{y}",
                    f"{x},{y + diamond_size//2}",
                    f"{x - diamond_size//2},{y}"
                ]
                color = color1 if (x + y) % 4 == 0 else color2
                shapes.append(f'<polygon points="{" ".join(points)}" fill="{color}" opacity="0.7"/>')
                
    elif pattern_type == 13:  # Sine wave pattern
        defs.append(f'''<linearGradient id="{gradient_id}" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stop-color="{color1}"/>
            <stop offset="100%" stop-color="{color2}"/>
        </linearGradient>''')
        
        for wave in range(5):
            path_data = f"M 0,{size//2}"
            for x in range(0, size, 2):
                frequency = 0.3 + wave * 0.1
                amplitude = size // 8
                phase = wave * math.pi / 3
                y = size // 2 + amplitude * math.sin(x * frequency + phase)
                path_data += f" L {x},{y:.1f}"
            shapes.append(f'<path d="{path_data}" stroke="url(#{gradient_id})" stroke-width="2" fill="none" opacity="{0.9 - wave * 0.15}"/>')
            
    elif pattern_type == 14:  # Hexagonal grid
        hex_size = size // 8
        for row in range(4):
            for col in range(4):
                x = col * hex_size * 1.5 + (row % 2) * hex_size * 0.75
                y = row * hex_size * 0.866
                if x < size and y < size:
                    points = []
                    for i in range(6):
                        angle = (i * 60) * math.pi / 180
                        px = x + hex_size * math.cos(angle)
                        py = y + hex_size * math.sin(angle)
                        points.append(f"{px:.1f},{py:.1f}")
                    color = color1 if (row + col) % 2 == 0 else color2
                    shapes.append(f'<polygon points="{" ".join(points)}" fill="{color}" opacity="0.6" stroke="{color2}" stroke-width="1"/>')
                    
    elif pattern_type == 15:  # Sri Yantra
        defs.append(f'''<radialGradient id="{gradient_id}" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stop-color="{color1}"/>
            <stop offset="100%" stop-color="{color2}"/>
        </radialGradient>''')
        
        # Sacred Sri Yantra - 9 interlocking triangles
        center_x, center_y = size // 2, size // 2
        outer_radius = size // 2.5
        
        # 4 upward pointing triangles (Shiva)
        for i in range(4):
            scale = 1 - i * 0.2
            triangle_size = outer_radius * scale
            
            # Calculate triangle points
            x1 = center_x
            y1 = center_y - triangle_size
            x2 = center_x - triangle_size * 0.866  # sin(60°)
            y2 = center_y + triangle_size * 0.5
            x3 = center_x + triangle_size * 0.866
            y3 = center_y + triangle_size * 0.5
            
            opacity = 0.7 - i * 0.1
            shapes.append(f'<polygon points="{x1:.1f},{y1:.1f} {x2:.1f},{y2:.1f} {x3:.1f},{y3:.1f}" fill="none" stroke="url(#{gradient_id})" stroke-width="2" opacity="{opacity}"/>')
        
        # 5 downward pointing triangles (Shakti)
        for i in range(5):
            scale = 0.9 - i * 0.15
            triangle_size = outer_radius * scale
            rotation = i * 8  # Slight rotation for interlocking effect
            
            # Calculate inverted triangle points
            x1 = center_x
            y1 = center_y + triangle_size
            x2 = center_x - triangle_size * 0.866
            y2 = center_y - triangle_size * 0.5
            x3 = center_x + triangle_size * 0.866
            y3 = center_y - triangle_size * 0.5
            
            opacity = 0.6 - i * 0.08
            shapes.append(f'<polygon points="{x1:.1f},{y1:.1f} {x2:.1f},{y2:.1f} {x3:.1f},{y3:.1f}" fill="none" stroke="{color2}" stroke-width="1" opacity="{opacity}"/>')
        
        # Central bindu (divine point)
        shapes.append(f'<circle cx="{center_x}" cy="{center_y}" r="{size//20}" fill="{color1}" opacity="0.9"/>')
        
        # Outer protective circles
        shapes.append(f'<circle cx="{center_x}" cy="{center_y}" r="{outer_radius * 1.1}" fill="none" stroke="{color2}" stroke-width="1" opacity="0.5"/>')
        shapes.append(f'<circle cx="{center_x}" cy="{center_y}" r="{outer_radius * 1.25}" fill="none" stroke="{color1}" stroke-width="1" opacity="0.3"/>')
            
    elif pattern_type == 16:  # Mosaic tiles
        tile_size = size // 5
        for x in range(0, size, tile_size):
            for y in range(0, size, tile_size):
                # Random tile pattern based on position
                tile_hash = hash(f"{x}-{y}-{title}") % 4
                if tile_hash == 0:
                    shapes.append(f'<rect x="{x}" y="{y}" width="{tile_size}" height="{tile_size}" fill="{color1}" opacity="0.8"/>')
                elif tile_hash == 1:
                    shapes.append(f'<circle cx="{x + tile_size//2}" cy="{y + tile_size//2}" r="{tile_size//3}" fill="{color2}" opacity="0.7"/>')
                elif tile_hash == 2:
                    points = f"{x},{y+tile_size} {x+tile_size//2},{y} {x+tile_size},{y+tile_size}"
                    shapes.append(f'<polygon points="{points}" fill="{color1}" opacity="0.6"/>')
                else:
                    shapes.append(f'<rect x="{x}" y="{y}" width="{tile_size}" height="{tile_size}" fill="{color2}" opacity="0.5" rx="{tile_size//4}"/>')
                    
    elif pattern_type == 17:  # Orbital rings
        defs.append(f'''<linearGradient id="{gradient_id}" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="{color1}"/>
            <stop offset="100%" stop-color="{color2}"/>
        </linearGradient>''')
        
        for i in range(4):
            radius = size // 6 + i * size // 12
            rotation = i * 45
            shapes.append(f'<circle cx="{size//2}" cy="{size//2}" r="{radius}" fill="none" stroke="url(#{gradient_id})" stroke-width="2" opacity="{0.8 - i*0.15}" transform="rotate({rotation} {size//2} {size//2})"/>')
            # Small planet
            planet_x = size // 2 + radius
            planet_y = size // 2
            shapes.append(f'<circle cx="{planet_x}" cy="{planet_y}" r="3" fill="{color2}" transform="rotate({rotation} {size//2} {size//2})"/>')
            
    elif pattern_type == 18:  # Woven pattern
        defs.append(f'''<pattern id="{gradient_id}" x="0" y="0" width="6" height="6" patternUnits="userSpaceOnUse">
            <rect width="6" height="6" fill="{color1}"/>
            <rect x="0" y="0" width="3" height="3" fill="{color2}"/>
            <rect x="3" y="3" width="3" height="3" fill="{color2}"/>
        </pattern>''')
        
        # Create woven effect with overlapping rectangles
        for i in range(6):
            x = i * size // 6
            shapes.append(f'<rect x="{x}" y="0" width="{size//12}" height="{size}" fill="url(#{gradient_id})" opacity="0.7"/>')
            shapes.append(f'<rect x="0" y="{x}" width="{size}" height="{size//12}" fill="{color2}" opacity="0.5"/>')
            
    else:  # pattern_type == 19: Platonic Tetrahedron 
        defs.append(f'''<linearGradient id="{gradient_id}" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="{color1}"/>
            <stop offset="50%" stop-color="{color2}"/>
            <stop offset="100%" stop-color="{color1}"/>
        </radialGradient>''')
        
        # Sacred Tetrahedron - representing Fire element and divine trinity
        center_x, center_y = size // 2, size // 2
        tet_size = size // 2.8
        
        # Main large triangle (upward - divine masculine)
        x1 = center_x
        y1 = center_y - tet_size * 0.7
        x2 = center_x - tet_size * 0.866
        y2 = center_y + tet_size * 0.5
        x3 = center_x + tet_size * 0.866
        y3 = center_y + tet_size * 0.5
        
        shapes.append(f'<polygon points="{x1:.1f},{y1:.1f} {x2:.1f},{y2:.1f} {x3:.1f},{y3:.1f}" fill="none" stroke="url(#{gradient_id})" stroke-width="3" opacity="0.9"/>')
        
        # Inverted triangle (downward - divine feminine)
        y1_inv = center_y + tet_size * 0.4
        y2_inv = center_y - tet_size * 0.3
        y3_inv = center_y - tet_size * 0.3
        x2_inv = center_x - tet_size * 0.5
        x3_inv = center_x + tet_size * 0.5
        
        shapes.append(f'<polygon points="{center_x:.1f},{y1_inv:.1f} {x2_inv:.1f},{y2_inv:.1f} {x3_inv:.1f},{y3_inv:.1f}" fill="none" stroke="{color2}" stroke-width="2" opacity="0.8"/>')
        
        # Inner sacred triangles (tetraktys pattern)
        for i in range(3):
            scale = 0.6 - i * 0.15
            inner_size = tet_size * scale
            x1_i = center_x
            y1_i = center_y - inner_size * 0.4
            x2_i = center_x - inner_size * 0.5
            y2_i = center_y + inner_size * 0.2
            x3_i = center_x + inner_size * 0.5
            y3_i = center_y + inner_size * 0.2
            
            opacity = 0.7 - i * 0.15
            shapes.append(f'<polygon points="{x1_i:.1f},{y1_i:.1f} {x2_i:.1f},{y2_i:.1f} {x3_i:.1f},{y3_i:.1f}" fill="none" stroke="{color1}" stroke-width="1" opacity="{opacity}"/>')
        
        # Central point of unity
        shapes.append(f'<circle cx="{center_x}" cy="{center_y}" r="{size//25}" fill="{color1}" opacity="1.0"/>')
        
        # Corner vertices (tetraktys dots)
        vertex_radius = size // 30
        shapes.append(f'<circle cx="{x1:.1f}" cy="{y1:.1f}" r="{vertex_radius}" fill="{color2}" opacity="0.8"/>')
        shapes.append(f'<circle cx="{x2:.1f}" cy="{y2:.1f}" r="{vertex_radius}" fill="{color2}" opacity="0.8"/>')
        shapes.append(f'<circle cx="{x3:.1f}" cy="{y3:.1f}" r="{vertex_radius}" fill="{color2}" opacity="0.8"/>')
    
    # Compose SVG
    defs_content = "\n        ".join(defs) if defs else ""
    shapes_content = "\n        ".join(shapes)
    
    svg = f'''<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" xmlns="http://www.w3.org/2000/svg">
        <defs>
            {defs_content}
        </defs>
        {shapes_content}
    </svg>'''
    
    # Convert to data URL
    svg_b64 = base64.b64encode(svg.encode()).decode()
    return f"data:image/svg+xml;base64,{svg_b64}"

def generate_folder_icon(title, size=24):
    """Generate a folder icon with unique accent color based on title."""
    hash_obj = hashlib.md5(title.encode())
    hash_bytes = hash_obj.digest()
    
    # Generate accent color
    hue = (hash_bytes[0] * 360) // 256
    saturation = 60 + (hash_bytes[1] * 20) // 256  # 60-80%
    lightness = 45 + (hash_bytes[2] * 20) // 256   # 45-65%
    
    accent_color = f"hsl({hue}, {saturation}%, {lightness}%)"
    folder_base = "#e8e8e8"
    
    svg = f'''<svg width="{size}" height="{size}" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="folder_grad_{abs(hash(title)) % 1000}" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="{folder_base}"/>
                <stop offset="100%" stop-color="{accent_color}"/>
            </linearGradient>
        </defs>
        <path d="M10 4H4c-1.11 0-2 .89-2 2v12c0 1.11.89 2 2 2h16c1.11 0 2-.89 2-2V8c0-1.11-.89-2-2-2h-8l-2-2z" 
              fill="url(#folder_grad_{abs(hash(title)) % 1000})" 
              stroke="{accent_color}" 
              stroke-width="0.5"/>
        <circle cx="18" cy="7" r="2" fill="{accent_color}" opacity="0.8"/>
    </svg>'''
    
    svg_b64 = base64.b64encode(svg.encode()).decode()
    return f"data:image/svg+xml;base64,{svg_b64}"

def get_directory_structure(path):
    """Get the directory structure for a given path."""
    items = []
    if not path.exists() or not path.is_dir():
        return items

    # Separate directories and files for better organization
    dirs = []
    files = []

    for item in sorted(path.iterdir(), reverse=True):
        if item.name.startswith('.') or item.name.lower() == 'index.md':
            continue

        # Create display name without extension for files
        display_name = item.stem if item.is_file() and item.suffix else item.name
        display_name = display_name.replace('-', ' ').replace('_', ' ').title()

        # Create clean URL path without .md extension
        if item.is_dir():
            url_path = '/' + str(item.relative_to(DATA_DIR)) + '/'
        elif item.suffix == '.md':
            # Remove .md extension for clean URLs
            relative_path = str(item.relative_to(DATA_DIR))
            url_path = '/' + relative_path[:-3]  # Remove .md extension
        else:
            url_path = '/' + str(item.relative_to(DATA_DIR))

        # Extract date from markdown files
        file_date = None
        if item.is_file() and item.suffix == '.md':
            try:
                with open(item, 'r', encoding='utf-8') as f:
                    # Read first few lines to find date
                    for i, line in enumerate(f):
                        if i > 10:  # Only check first 10 lines
                            break
                        # Look for date patterns like *January 2009* or *2014*
                        date_match = re.match(r'^\*([A-Za-z]+ \d{4}|\d{4})\*\s*$', line.strip())
                        if date_match:
                            file_date = date_match.group(1)
                            break
            except:
                pass

        # Generate unique SVG icon based on actual content title for consistency
        icon_title = display_name  # Default to filename-based display name
        
        # For markdown files, try to extract the actual H1 title from content
        if item.is_file() and item.suffix == '.md':
            try:
                content_data = render_markdown_file(item)
                if content_data and 'title' in content_data:
                    icon_title = content_data['title']
                    # Also update display_name to use the actual title
                    display_name = content_data['title']
            except:
                # Fallback to filename-based display name if parsing fails
                pass
        
        if item.is_dir():
            unique_icon = generate_folder_icon(icon_title, size=32)
        else:
            unique_icon = generate_unique_svg_icon(icon_title, size=32)
        
        item_info = {
            'name': item.name,
            'display_name': display_name,
            'path': str(item.relative_to(DATA_DIR)),
            'url_path': url_path,
            'is_dir': item.is_dir(),
            'is_markdown': item.suffix == '.md',
            'is_image': item.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.webp'],
            'size': item.stat().st_size if item.is_file() else None,
            'created': datetime.fromtimestamp(item.stat().st_ctime),
            'modified': datetime.fromtimestamp(item.stat().st_mtime),
            'file_date': file_date,  # Date extracted from file content
            'file_type': item.suffix.lower() if item.is_file() else 'directory',
            'static_path': f"/static/data/{item.relative_to(DATA_DIR)}" if not item.is_dir() else None,
            'unique_icon': unique_icon  # Generated SVG icon
        }

        if item.is_dir():
            dirs.append(item_info)
        else:
            files.append(item_info)

    # Return directories first, then files
    return dirs + files



def calculate_reading_time(text):
    """Calculate estimated reading time based on word count."""
    # Remove HTML tags for more accurate word count
    clean_text = re.sub(r'<[^>]+>', '', text)
    # Average reading speed is 200-250 words per minute, using 225 as middle ground
    word_count = len(clean_text.split())
    reading_time = max(1, round(word_count / 225))  # Minimum 1 minute
    return reading_time, word_count



def find_series_posts(metadata, current_path):
    """Find all posts in the same series as the current post."""
    series_posts = []
    if not metadata.get('series'):
        return series_posts

    series_name = metadata['series']

    # Search through all markdown files to find posts in the same series
    for root, dirs, files in os.walk(DATA_DIR):
        for file in files:
            if file.endswith('.md') and file != 'index.md':
                file_path = Path(root) / file

                # Skip the current file
                if str(file_path) == str(current_path):
                    continue

                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # Extract metadata
                    yaml_pattern = r'^---\s*\n(.*?)\n---\s*\n'
                    yaml_match = re.match(yaml_pattern, content, re.DOTALL)
                    if yaml_match:
                        import yaml
                        post_metadata = yaml.safe_load(yaml_match.group(1)) or {}

                        if post_metadata.get('series') == series_name:
                            # Create URL path for this post
                            relative_path = str(file_path.relative_to(DATA_DIR))
                            url_path = '/' + relative_path[:-3]  # Remove .md

                            # Get title from metadata or filename
                            title = post_metadata.get('title') or file_path.stem.replace('-', ' ').title()

                            series_posts.append({
                                'title': title,
                                'url': url_path,
                                'order': post_metadata.get('series_order', 999),
                                'description': post_metadata.get('description', '')
                            })
                except:
                    continue

    # Sort by series_order
    series_posts.sort(key=lambda x: x['order'])
    return series_posts

def extract_tags_from_content(content, metadata, file_path):
    """Extract tags from content and metadata for categorization."""
    tags = set()

    # Only use explicitly defined tags from YAML front matter
    if metadata.get('tags'):
        if isinstance(metadata['tags'], list):
            tags.update(tag.lower().strip() for tag in metadata['tags'])
        else:
            tags.update(tag.lower().strip() for tag in str(metadata['tags']).split(','))

    return list(tags)


def render_markdown_file(file_path):
    """Render a markdown file to HTML."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract YAML front matter if it exists
        metadata = {}
        yaml_pattern = r'^---\s*\n(.*?)\n---\s*\n'
        yaml_match = re.match(yaml_pattern, content, re.DOTALL)
        if yaml_match:
            try:
                import yaml
                metadata = yaml.safe_load(yaml_match.group(1)) or {}
                content = content[yaml_match.end():]
            except:
                pass

        # Extract first h1 header if it exists
        first_h1 = None
        # Look for the first H1 at the start of the file (must be on first line or after blank line)
        h1_match = re.search(r'^# (.+?)$', content, re.MULTILINE)
        if h1_match:
            first_h1 = h1_match.group(1).strip()
            # Remove only the first h1 line from content to avoid duplication
            content = re.sub(r'^# .+?$', '', content, count=1, flags=re.MULTILINE)

        # Extract date from italic date pattern (e.g., "*August 2025*") 
        # Only match dates that look like month/year patterns, not quotes or long text
        date_match = re.search(r'^\*([A-Za-z]+ \d{4}|\d{4})\*\s*$', content, re.MULTILINE)
        if date_match and not metadata.get('date'):
            date_text = date_match.group(1).strip()
            # Skip only if it's "January 2025" (current year placeholder)
            if not (date_text.lower().startswith('january') and '2025' in date_text):
                # Format "January YYYY" (not 2025) as just "YYYY" for cleaner display
                if re.match(r'^january\s+(\d{4})$', date_text.lower()) and '2025' not in date_text:
                    year_match = re.search(r'(\d{4})', date_text)
                    if year_match:
                        date_text = year_match.group(1)
                # Keep other months like "August 2025" as full format
                metadata['date'] = date_text
            # Remove the date line from content
            content = re.sub(r'^\*([A-Za-z]+ \d{4}|\d{4})\*\s*$', '', content, count=1, flags=re.MULTILINE)

        # Configure mistune renderer with URL plugin for bare links
        markdown = mistune.create_markdown(
            escape=False,
            plugins=['strikethrough', 'footnotes', 'table', 'task_lists', 'def_list', 'url']
        )

        # Process content to HTML
        html_content = markdown(content.strip())
        
        # Add anchor IDs to headings using post-processing on HTML
        def add_heading_anchor_ids(html_content):
            def replace_heading(match):
                tag = match.group(1)  # h1, h2, etc.
                level = int(tag[1])  # 1, 2, etc.
                classes = match.group(2) or ''  # existing classes if any
                text = match.group(3)
                
                # Generate anchor ID from heading text (remove HTML tags first)
                clean_text = re.sub(r'<[^>]+>', '', text)
                anchor_id = re.sub(r'[^\w\s-]', '', clean_text.lower()).replace(' ', '-')
                anchor_id = re.sub(r'-+', '-', anchor_id).strip('-')  # Clean up multiple dashes
                
                # Add id attribute, preserving any existing classes
                if classes:
                    return f'<{tag} id="{anchor_id}"{classes}>{text}</{tag}>'
                else:
                    return f'<{tag} id="{anchor_id}">{text}</{tag}>'
            
            # Match h1-h6 tags with optional class attributes
            return re.sub(r'<(h[1-6])(\s+[^>]*)?>([^<]+)</h[1-6]>', replace_heading, html_content)
        
        html_content = add_heading_anchor_ids(html_content)

        # Post-processing for poetry line breaks
        # Check if this is likely a poetry file based on file path
        if file_path and 'poetry' in str(file_path):
            # For poetry, convert single line breaks within paragraphs to <br> tags
            html_content = re.sub(r'<p>(.*?)</p>',
                                lambda m: '<p>' + m.group(1).replace('\n', '<br>\n') + '</p>',
                                html_content, flags=re.DOTALL)

        # Add classes to headers to prevent conflicts with page headers
        html_content = html_content.replace('<h1>', '<h1 class="content-header">')
        html_content = html_content.replace('<h2>', '<h2 class="content-header">')
        html_content = html_content.replace('<h3>', '<h3 class="content-header">')
        html_content = html_content.replace('<h4>', '<h4 class="content-header">')
        html_content = html_content.replace('<h5>', '<h5 class="content-header">')
        html_content = html_content.replace('<h6>', '<h6 class="content-header">')

        # Use the first h1 as title if available, otherwise fallback to metadata or filename
        if first_h1:
            title = first_h1
        elif 'title' in metadata:
            title = metadata['title']
        else:
            title = file_path.stem.replace('-', ' ').replace('_', ' ').title()

        # Calculate reading time
        reading_time, word_count = calculate_reading_time(html_content)

        # Extract tags
        tags = extract_tags_from_content(html_content, metadata, file_path)

        # Find series posts if this post is part of a series
        series_posts = find_series_posts(metadata, file_path)
        
        # Generate unique icon for this content
        unique_icon = generate_unique_svg_icon(title, size=32)

        return {
            'content': html_content,
            'title': title,
            'metadata': metadata,
            'reading_time': reading_time,
            'word_count': word_count,
            'tags': tags,
            'series_posts': series_posts,
            'series_name': metadata.get('series'),
            'unique_icon': unique_icon
        }
    except Exception as e:
        return {
            'content': f'<p>Error reading file: {str(e)}</p>',
            'title': 'Error',
            'metadata': {}
        }

@app.route('/')
def index():
    """Homepage showcasing download statistics."""
    return render_template('homepage.html',
                         current_year=datetime.now().year,
                         title="Home")


@app.route('/health')
def health_check():
    """Simple health check endpoint for monitoring."""
    return {'status': 'healthy', 'timestamp': datetime.now().isoformat()}


@app.route('/search')
def search_page():
    """Search page with interactive search functionality."""
    return render_template('search.html',
                         title='Search',
                         breadcrumbs=[],
                         current_year=datetime.now().year,
                         current_page='Search')


def _convert_unified_outlines_cache(unified_cache):
    """Convert unified cache outlines format to template-expected format."""
    articles_list = []
    
    for file_path, outlines in unified_cache.get('articles', {}).items():
        if not outlines:
            continue
            
        try:
            full_path = Path(file_path)
            content_data = render_markdown_file(full_path)
            pub_date = extract_intelligent_date(full_path, content_data)
            relative_path = str(full_path.relative_to(DATA_DIR))
            url_path = '/' + relative_path[:-3]
            
            processed_outlines = []
            for outline in outlines:
                if isinstance(outline, dict) and 'text' in outline:
                    processed_outlines.append(outline)
            
            if processed_outlines:
                articles_list.append({
                    'title': content_data['title'],
                    'url': url_path,
                    'date': pub_date,
                    'category': full_path.parent.name.replace('-', ' ').title(),
                    'outlines': processed_outlines
                })
        except Exception:
            continue
    
    articles_list.sort(key=lambda x: x['date'] if x['date'] else datetime(1900, 1, 1), reverse=True)
    return {
        'articles': articles_list,
        'total_count': unified_cache.get('total_count', sum(len(article['outlines']) for article in articles_list))
    }

def _convert_unified_quotes_cache(unified_cache):
    """Convert unified cache quotes format to template-expected format."""
    articles_list = []
    
    for file_path, quotes in unified_cache.get('articles', {}).items():
        if not quotes:
            continue
            
        try:
            full_path = Path(file_path)
            content_data = render_markdown_file(full_path)
            pub_date = extract_intelligent_date(full_path, content_data)
            relative_path = str(full_path.relative_to(DATA_DIR))
            url_path = '/' + relative_path[:-3]
            
            processed_quotes = []
            for quote in quotes:
                if isinstance(quote, dict) and 'text' in quote:
                    processed_quotes.append(quote)
            
            if processed_quotes:
                articles_list.append({
                    'title': content_data['title'],
                    'url': url_path,
                    'date': pub_date,
                    'category': full_path.parent.name.replace('-', ' ').title(),
                    'quotes': processed_quotes
                })
        except Exception:
            continue
    
    articles_list.sort(key=lambda x: x['date'] if x['date'] else datetime(1900, 1, 1), reverse=True)
    return {
        'articles': articles_list,
        'total_count': unified_cache.get('total_count', sum(len(article['quotes']) for article in articles_list))
    }

def _convert_unified_connections_cache(unified_cache):
    """Convert unified cache connections format to template-expected format."""
    return {
        'outgoing_refs': unified_cache.get('outgoing_refs', {}),
        'incoming_refs': unified_cache.get('incoming_refs', {}),
        'total_count': unified_cache.get('total_count', 0)
    }

def _convert_unified_terms_cache(unified_cache):
    """Convert unified cache terms format to template-expected format."""
    return {
        'terms': unified_cache.get('terms', []),
        'total_occurrences': unified_cache.get('total_occurrences', 0)
    }

def _convert_unified_sidenotes_cache(unified_cache):
    """Convert unified cache sidenotes format to template-expected format."""
    articles_list = []
    
    # The unified cache has structure: {'articles': {file_path: [sidenotes]}, 'total_count': int}
    articles_data = unified_cache.get('articles', {})
    
    for file_path, sidenotes in articles_data.items():
        if not sidenotes:
            continue
            
        try:
            # Get file info
            full_path = Path(file_path)
            content_data = render_markdown_file(full_path)
            
            # Extract date for sorting
            pub_date = extract_intelligent_date(full_path, content_data)
            
            # Create URL for this file
            relative_path = str(full_path.relative_to(DATA_DIR))
            url_path = '/' + relative_path[:-3]  # Remove .md extension
            
            # Convert sidenotes to expected format
            processed_sidenotes = []
            for sidenote in sidenotes:
                if isinstance(sidenote, dict) and 'text' in sidenote:
                    processed_sidenotes.append({
                        'text': sidenote['text'],
                        'id': sidenote.get('id')  # May be None
                    })
            
            if processed_sidenotes:
                articles_list.append({
                    'title': content_data['title'],
                    'url': url_path,
                    'date': pub_date,
                    'category': full_path.parent.name.replace('-', ' ').title(),
                    'sidenotes': processed_sidenotes
                })
                
        except Exception as e:
            # Skip files that can't be processed
            continue
    
    # Sort by date (most recent first)
    articles_list.sort(key=lambda x: x['date'] if x['date'] else datetime(1900, 1, 1), reverse=True)
    
    print(f"Sidenotes conversion: {len(articles_list)} articles processed from {len(unified_cache.get('articles', {}))} files")
    return {
        'articles': articles_list,
        'total_count': unified_cache.get('total_count', sum(len(article['sidenotes']) for article in articles_list))
    }

def _extract_all_sidenotes_cached():
    """Return pre-loaded sidenotes cache data (pure RAM, no TTL)."""
    # Return pre-loaded cache data if available
    if _sidenotes_cache['data'] is not None:
        return _sidenotes_cache['data']
    
    # Fallback to rebuild if cache somehow wasn't initialized
    import glob
    from collections import defaultdict
    
    articles_with_sidenotes = defaultdict(list)
    
    # Get all markdown files from /data/ directory
    all_files = glob.glob('data/**/*.md', recursive=True)
    
    # Filter out index files
    all_files = [f for f in all_files if not f.endswith('index.md')]
    
    for file_path in all_files:
        try:
            # Read the file and render it
            full_path = Path(file_path)
            content_data = render_markdown_file(full_path)
            html_content = content_data['content']
            
            # Extract sidenotes from the HTML using regex
            # Pattern matches <span class="sidenote">content</span>
            sidenote_pattern = r'<span class="sidenote">(.*?)</span>'
            file_sidenotes = re.findall(sidenote_pattern, html_content, re.DOTALL)
            
            if file_sidenotes:
                # Create URL for this file
                relative_path = str(full_path.relative_to(DATA_DIR))
                url_path = '/' + relative_path[:-3]  # Remove .md extension
                
                # Extract date for sorting
                pub_date = extract_intelligent_date(full_path, content_data)
                
                # Clean up sidenotes and add to article group with IDs
                cleaned_sidenotes = []
                
                # Also extract sidenote IDs from the HTML
                # Pattern to match the full sidenote structure with ID
                full_pattern = r'<input type="checkbox" id="(sn-[^"]+)"[^>]*\/><span class="sidenote">(.*?)</span>'
                full_matches = re.findall(full_pattern, html_content, re.DOTALL)
                
                if full_matches:
                    # We have IDs for the sidenotes
                    for sidenote_id, sidenote_text in full_matches:
                        # Remove HTML links but keep the link text
                        sidenote_text = re.sub(r'<a[^>]*?>(.*?)</a>', r'\1', sidenote_text)
                        # Clean up the sidenote text (remove extra whitespace)
                        sidenote_text = re.sub(r'\s+', ' ', sidenote_text).strip()
                        cleaned_sidenotes.append({
                            'text': sidenote_text,
                            'id': sidenote_id
                        })
                else:
                    # Fallback for sidenotes without IDs
                    for i, sidenote in enumerate(file_sidenotes):
                        # Remove HTML links but keep the link text
                        sidenote_text = re.sub(r'<a[^>]*?>(.*?)</a>', r'\1', sidenote)
                        # Clean up the sidenote text (remove extra whitespace)
                        sidenote_text = re.sub(r'\s+', ' ', sidenote_text).strip()
                        cleaned_sidenotes.append({
                            'text': sidenote_text,
                            'id': None
                        })
                
                articles_with_sidenotes[content_data['title']].append({
                    'sidenotes': cleaned_sidenotes,
                    'url': url_path,
                    'date': pub_date,
                    'category': full_path.parent.name.replace('-', ' ').title()
                })
        except Exception as e:
            # Skip files that can't be processed
            continue
    
    # Convert to list and sort by date (most recent first)
    articles_list = []
    for title, article_data in articles_with_sidenotes.items():
        # Should only be one entry per article
        data = article_data[0]
        articles_list.append({
            'title': title,
            'url': data['url'],
            'date': data['date'],
            'category': data['category'],
            'sidenotes': data['sidenotes']
        })
    
    articles_list.sort(key=lambda x: x['date'] if x['date'] else datetime(1900, 1, 1), reverse=True)
    
    # Count total sidenotes
    total_count = sum(len(article['sidenotes']) for article in articles_list)
    
    # Update cache
    result = {
        'articles': articles_list,
        'total_count': total_count
    }
    _sidenotes_cache['data'] = result
    
    return result


@app.route('/sidenotes')
def sidenotes_index():
    """Extract and display all sidenotes from across the site as an index."""
    # Use clean MetadataCache interface
    sidenotes_data = metadata_cache.get_sidenotes()
    
    return render_template('sidenotes.html',
                         articles=sidenotes_data['articles'],
                         total_count=sidenotes_data['total_count'],
                         title='Sidenotes Index',
                         breadcrumbs=[],
                         current_year=datetime.now().year,
                         current_page='Sidenotes')


def _extract_all_outlines_cached():
    """Return pre-loaded outlines cache data (pure RAM, no TTL)."""
    # Return pre-loaded cache data if available
    if _outlines_cache['data'] is not None:
        return _outlines_cache['data']
    
    # Fallback to rebuild if cache somehow wasn't initialized
    import glob
    from collections import defaultdict
    
    articles_with_outlines = defaultdict(list)
    
    # Get all markdown files from /data/ directory
    all_files = glob.glob('data/**/*.md', recursive=True)
    
    # Filter out index files
    all_files = [f for f in all_files if not f.endswith('index.md')]
    
    for file_path in all_files:
        try:
            # Read the file and render it
            full_path = Path(file_path)
            content_data = render_markdown_file(full_path)
            html_content = content_data['content']
            
            # Extract headings from the HTML using regex
            # Pattern matches <h1>, <h2>, <h3>, etc. with optional IDs and content
            heading_pattern = r'<h([1-6])(?:[^>]*id="([^"]*)")?[^>]*>([^<]+)</h[1-6]>'
            headings = re.findall(heading_pattern, html_content)
            
            if headings:
                # Create URL for this file
                relative_path = str(full_path.relative_to(DATA_DIR))
                url_path = '/' + relative_path[:-3]  # Remove .md extension
                
                # Extract date for sorting
                pub_date = extract_intelligent_date(full_path, content_data)
                
                # Clean up headings and create outline structure
                cleaned_headings = []
                for level, heading_id, heading_text in headings:
                    # Skip h1 if it matches the title (avoid duplication)
                    if level == '1' and heading_text.strip() == content_data['title'].strip():
                        continue
                    
                    cleaned_headings.append({
                        'level': int(level),
                        'text': heading_text.strip(),
                        'id': heading_id if heading_id else None,
                        'anchor_url': f"{url_path}#{heading_id}" if heading_id else url_path
                    })
                
                if cleaned_headings:  # Only add if there are headings after filtering
                    articles_with_outlines[content_data['title']].append({
                        'headings': cleaned_headings,
                        'url': url_path,
                        'date': pub_date,
                        'category': full_path.parent.name.replace('-', ' ').title()
                    })
        except Exception as e:
            # Skip files that can't be processed
            continue
    
    # Convert to list and sort by date (most recent first)
    articles_list = []
    for title, article_data in articles_with_outlines.items():
        # Should only be one entry per article
        data = article_data[0]
        articles_list.append({
            'title': title,
            'url': data['url'],
            'date': data['date'],
            'category': data['category'],
            'headings': data['headings']
        })
    
    articles_list.sort(key=lambda x: x['date'] if x['date'] else datetime(1900, 1, 1), reverse=True)
    
    # Count total headings
    total_count = sum(len(article['headings']) for article in articles_list)
    
    # Update cache
    result = {
        'articles': articles_list,
        'total_count': total_count
    }
    _outlines_cache['data'] = result
    
    return result


@app.route('/outlines')
def outlines_index():
    """Extract and display all essay outlines from across the site as an index."""
    # Use clean MetadataCache interface
    outlines_data = metadata_cache.get_outlines()
    
    return render_template('outlines.html',
                         articles=outlines_data['articles'],
                         total_count=outlines_data['total_count'],
                         title='Outlines Index',
                         breadcrumbs=[],
                         current_year=datetime.now().year,
                         current_page='Outlines')


def _extract_all_quotes_cached():
    """Return pre-loaded quotes cache data (pure RAM, no TTL)."""
    # Return pre-loaded cache data if available
    if _quotes_cache['data'] is not None:
        return _quotes_cache['data']
    
    # Fallback to rebuild if cache somehow wasn't initialized
    import glob
    from collections import defaultdict
    
    articles_with_quotes = defaultdict(list)
    
    # Get all markdown files from /data/ directory
    all_files = glob.glob('data/**/*.md', recursive=True)
    
    # Filter out index files
    all_files = [f for f in all_files if not f.endswith('index.md')]
    
    for file_path in all_files:
        try:
            # Read the file and render it
            full_path = Path(file_path)
            content_data = render_markdown_file(full_path)
            html_content = content_data['content']
            
            # Extract blockquotes from the HTML using regex
            # Pattern matches <blockquote>content</blockquote>
            quote_pattern = r'<blockquote[^>]*>(.*?)</blockquote>'
            quotes = re.findall(quote_pattern, html_content, re.DOTALL)
            
            if quotes:
                # Create URL for this file
                relative_path = str(full_path.relative_to(DATA_DIR))
                url_path = '/' + relative_path[:-3]  # Remove .md extension
                
                # Extract date for sorting
                pub_date = extract_intelligent_date(full_path, content_data)
                
                # Clean up quotes
                cleaned_quotes = []
                for quote in quotes:
                    # Skip quotes that start with bold labels (like "Note:", "Analysis:", "The Prompt:", etc.)
                    # Pattern matches: <p><strong>Label</strong>: content or similar
                    if re.match(r'^\s*<p[^>]*><(?:strong|b)[^>]*>[^<]*</(?:strong|b)>:', quote):
                        continue
                    
                    # Remove inner HTML tags but preserve basic formatting
                    quote_text = re.sub(r'<(?!/?(?:em|strong|i|b)\b)[^>]*>', '', quote)
                    quote_text = re.sub(r'\s+', ' ', quote_text).strip()
                    
                    # Skip very short quotes (likely not substantive)
                    if len(quote_text) > 20:
                        cleaned_quotes.append(quote_text)
                
                if cleaned_quotes:
                    articles_with_quotes[content_data['title']].append({
                        'quotes': cleaned_quotes,
                        'url': url_path,
                        'date': pub_date,
                        'category': full_path.parent.name.replace('-', ' ').title()
                    })
        except Exception as e:
            # Skip files that can't be processed
            continue
    
    # Convert to list and sort by date (most recent first)
    articles_list = []
    for title, article_data in articles_with_quotes.items():
        # Should only be one entry per article
        data = article_data[0]
        articles_list.append({
            'title': title,
            'url': data['url'],
            'date': data['date'],
            'category': data['category'],
            'quotes': data['quotes']
        })
    
    articles_list.sort(key=lambda x: x['date'] if x['date'] else datetime(1900, 1, 1), reverse=True)
    
    # Count total quotes
    total_count = sum(len(article['quotes']) for article in articles_list)
    
    # Update cache
    result = {
        'articles': articles_list,
        'total_count': total_count
    }
    _quotes_cache['data'] = result
    
    return result


@app.route('/quotes')
def quotes_index():
    """Extract and display all blockquotes from across the site as an index."""
    # Use clean MetadataCache interface
    quotes_data = metadata_cache.get_quotes()
    
    return render_template('quotes.html',
                         articles=quotes_data['articles'],
                         total_count=quotes_data['total_count'],
                         title='Quotes Index',
                         breadcrumbs=[],
                         current_year=datetime.now().year,
                         current_page='Quotes')


def _extract_all_connections_cached():
    """Return pre-loaded connections cache data (pure RAM, no TTL)."""
    # Return pre-loaded cache data if available
    if _connections_cache['data'] is not None:
        return _connections_cache['data']
    
    # Fallback to rebuild if cache somehow wasn't initialized
    import glob
    from collections import defaultdict
    
    # Track both outgoing and incoming connections
    articles_data = {}  # url -> {title, date, category, outgoing_connections}
    incoming_connections = defaultdict(list)  # target_url -> [source connections]
    
    # Get all markdown files from /data/ directory
    all_files = glob.glob('data/**/*.md', recursive=True)
    
    # Filter out index files
    all_files = [f for f in all_files if not f.endswith('index.md')]
    
    # First pass: collect all articles and their outgoing connections
    for file_path in all_files:
        try:
            # Read the file and render it
            full_path = Path(file_path)
            content_data = render_markdown_file(full_path)
            html_content = content_data['content']
            
            # Create URL for this file
            relative_path = str(full_path.relative_to(DATA_DIR))
            source_url = '/' + relative_path[:-3]  # Remove .md extension
            
            # Extract date for sorting
            pub_date = extract_intelligent_date(full_path, content_data)
            
            # Initialize article data
            articles_data[source_url] = {
                'title': content_data['title'],
                'url': source_url,
                'date': pub_date,
                'category': full_path.parent.name.replace('-', ' ').title(),
                'outgoing_connections': []
            }
            
            # Extract internal links from the HTML
            # Pattern matches <a href="/internal/path">link text</a>
            link_pattern = r'<a[^>]*href="(/[^"]*)"[^>]*>(.*?)</a>'
            links = re.findall(link_pattern, html_content, re.DOTALL)
            
            # Collect outgoing connections for this article
            for link_url, link_text in links:
                if (link_url.startswith('/') and 
                    not link_url.startswith('//') and 
                    not link_url.startswith('/static') and
                    link_url != source_url):  # Don't include self-references
                    
                    # Clean up link text
                    link_text = re.sub(r'<[^>]*>', '', link_text)
                    link_text = re.sub(r'\s+', ' ', link_text).strip()
                    
                    connection = {
                        'target_url': link_url,
                        'link_text': link_text,
                        'source_url': source_url,
                        'source_title': content_data['title']
                    }
                    
                    # Add to outgoing connections
                    articles_data[source_url]['outgoing_connections'].append({
                        'target_url': link_url,
                        'link_text': link_text
                    })
                    
                    # Add to incoming connections map
                    incoming_connections[link_url].append({
                        'source_url': source_url,
                        'source_title': content_data['title'],
                        'link_text': link_text
                    })
                    
        except Exception as e:
            # Skip files that can't be processed
            continue
    
    # Second pass: add incoming connections to each article
    for url, article in articles_data.items():
        article['incoming_connections'] = incoming_connections.get(url, [])
    
    # Convert to list format and filter articles with connections
    articles_list = []
    for url, article in articles_data.items():
        # Only include articles that have outgoing OR incoming connections
        if article['outgoing_connections'] or article['incoming_connections']:
            articles_list.append({
                'title': article['title'],
                'url': article['url'],
                'date': article['date'],
                'category': article['category'],
                'connections': article['outgoing_connections'],  # Keep for backward compatibility
                'outgoing_connections': article['outgoing_connections'],
                'incoming_connections': article['incoming_connections']
            })
    
    articles_list.sort(key=lambda x: x['date'] if x['date'] else datetime(1900, 1, 1), reverse=True)
    
    # Count total connections (both directions)
    total_outgoing = sum(len(article['outgoing_connections']) for article in articles_list)
    total_incoming = sum(len(article['incoming_connections']) for article in articles_list)
    
    # Update cache
    result = {
        'articles': articles_list,
        'total_count': total_outgoing,  # Keep backward compatibility
        'total_outgoing': total_outgoing,
        'total_incoming': total_incoming
    }
    _connections_cache['data'] = result
    
    return result


@app.route('/connections')
def connections_index():
    """Extract and display all cross-references between essays."""
    # Use clean MetadataCache interface
    connections_data = metadata_cache.get_connections()
    
    return render_template('connections.html',
                         articles=connections_data['articles'],
                         total_count=connections_data['total_count'],
                         total_outgoing=connections_data.get('total_outgoing'),
                         total_incoming=connections_data.get('total_incoming'),
                         title='Connections Index',
                         breadcrumbs=[],
                         current_year=datetime.now().year,
                         current_page='Connections')


@app.route('/graph/data')
def graph_data():
    """API endpoint that returns graph data for network visualization."""
    # Use clean MetadataCache interface
    connections_data = metadata_cache.get_connections()
    
    nodes = []
    edges = []
    node_ids = set()
    
    # Create nodes and edges from connections
    for article in connections_data['articles']:
        source_id = article['url']
        node_ids.add(source_id)
        
        # Use outgoing_connections for graph edges (backward compatibility: also check connections)
        connections_list = article.get('outgoing_connections', article.get('connections', []))
        for connection in connections_list:
            target_id = connection['target_url']
            node_ids.add(target_id)
            
            edges.append({
                'source': source_id,
                'target': target_id,
                'link_text': connection['link_text']
            })
    
    # Create node objects with titles using MetadataCache
    posts = metadata_cache.get_blog_posts()
    post_lookup = {post['url']: post for post in posts}
    
    for node_id in node_ids:
        post = post_lookup.get(node_id)
        nodes.append({
            'id': node_id,
            'title': post['title'] if post else node_id.split('/')[-1],
            'category': post['category'] if post else 'Unknown',
            'url': node_id
        })
    
    return jsonify({
        'nodes': nodes,
        'edges': edges,
        'stats': {
            'total_nodes': len(nodes),
            'total_edges': len(edges)
        }
    })


@app.route('/graph')
def graph_visualization():
    """Interactive network graph of cross-references."""
    return render_template('graph.html',
                         title='Cross-Reference Graph',
                         breadcrumbs=[],
                         current_year=datetime.now().year,
                         current_page='Cross-Reference Graph')



@app.route('/terms')
def terms_index():
    """Extract and display all significant terms like a book index."""
    # Use clean MetadataCache interface
    terms_data = metadata_cache.get_terms()
    
    return render_template('terms.html',
                         terms=terms_data['terms'],
                         total_terms=terms_data['total_terms'],
                         total_occurrences=terms_data['total_occurrences'],
                         title='Term Index',
                         breadcrumbs=[],
                         current_year=datetime.now().year,
                         current_page='Term Index')



@app.route('/random')
def random_post():
    """Redirect to a random document from anywhere in /data/."""
    import random
    import glob
    
    # Get all markdown files from /data/ directory
    all_files = glob.glob('data/**/*.md', recursive=True)
    
    # Filter out index files
    all_files = [f for f in all_files if not f.endswith('index.md')]
    
    if not all_files:
        return redirect('/directory')
    
    # Choose random file and convert to URL
    random_file = random.choice(all_files)
    # Convert data/essays/2010-01-example.md -> /essays/2010-01-example
    url_path = '/' + random_file.replace('data/', '').replace('.md', '')
    return redirect(url_path)


def get_random_personality_from_collection(collection_path):
    """Helper function to get a random personality from a collection."""
    import random
    import glob

    if collection_path:
        # Get files from specific collection
        pattern = f'data/artificial-intelligence/personalities/{collection_path}/*.md'
        fallback_url = f'/artificial-intelligence/personalities/{collection_path}'
    else:
        # Get all personality files
        pattern = 'data/artificial-intelligence/personalities/**/*.md'
        fallback_url = '/artificial-intelligence/personalities'

    personality_files = glob.glob(pattern, recursive=True)
    # Filter out index files
    personality_files = [f for f in personality_files if not f.endswith('index.md')]

    if not personality_files:
        return redirect(fallback_url)

    # Choose random personality and convert to URL
    random_file = random.choice(personality_files)
    # Convert data/artificial-intelligence/personalities/major-arcana/the-fool.md -> /artificial-intelligence/personalities/major-arcana/the-fool
    url_path = '/' + random_file.replace('data/', '').replace('.md', '')
    return redirect(url_path)


@app.route('/random/personality')
@app.route('/random/personality/')
def random_personality():
    """Redirect to a random AI personality from any collection."""
    return get_random_personality_from_collection(None)


@app.route('/random/<collection>')
def random_from_collection(collection):
    """Redirect to a random personality from a specific collection."""
    # Validate collection exists
    valid_collections = [
        'major-arcana', 'seven-virtues', 'programming-languages',
        'greek-pantheon', 'roman-pantheon', 'hindu-pantheon',
        'operating-systems', 'supporting-cast', 'goddess-archetypes',
        'biblical-characters', 'biblical-anthology'
    ]

    if collection not in valid_collections:
        return redirect('/artificial-intelligence/personalities')

    return get_random_personality_from_collection(collection)


@app.route('/archive')
def archive_index():
    """Archive index showing all posts by year."""
    posts = metadata_cache.get_blog_posts()

    # Group posts by year
    grouped_posts = {}
    for post in posts:
        year = post['pub_date'].year
        if year not in grouped_posts:
            grouped_posts[year] = []
        grouped_posts[year].append(post)

    # Sort each year's posts by date (most recent first) and years in descending order
    for year in grouped_posts:
        grouped_posts[year].sort(key=lambda x: x['pub_date'], reverse=True)

    grouped_posts = dict(sorted(grouped_posts.items(), reverse=True))

    return render_template('archive.html',
                         archive_title='Complete',
                         archive_description=None,
                         grouped_posts=grouped_posts,
                         breadcrumbs=[],
                         current_year=datetime.now().year,
                         current_page='Archive')


@app.route('/archive/<int:year>')
def archive_year(year):
    """Archive for a specific year."""
    posts = metadata_cache.get_blog_posts()

    # Filter posts for the specific year
    year_posts = [post for post in posts if post['pub_date'].year == year]

    if not year_posts:
        abort(404)

    # Group posts by month
    grouped_posts = {}
    month_names = ['', 'January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']

    for post in year_posts:
        month_name = month_names[post['pub_date'].month]
        if month_name not in grouped_posts:
            grouped_posts[month_name] = []
        grouped_posts[month_name].append(post)

    # Sort posts within each month by date (most recent first)
    for month in grouped_posts:
        grouped_posts[month].sort(key=lambda x: x['pub_date'], reverse=True)

    # Sort months in chronological order (most recent first)
    month_order = {name: idx for idx, name in enumerate(month_names[1:], 1)}
    grouped_posts = dict(sorted(grouped_posts.items(),
                               key=lambda x: month_order[x[0]], reverse=True))

    breadcrumbs = [{'name': 'Archive', 'url': '/archive'}]

    return render_template('archive.html',
                         archive_title=str(year),
                         archive_description=f'Essays and AI writings from {year}.',
                         grouped_posts=grouped_posts,
                         breadcrumbs=breadcrumbs,
                         current_year=datetime.now().year,
                         current_page=f'{year} Archive')


@app.route('/archive/<int:year>/<int:month>')
def archive_month(year, month):
    """Archive for a specific month and year."""
    posts = metadata_cache.get_blog_posts()

    # Filter posts for the specific month and year
    month_posts = [post for post in posts
                   if post['pub_date'].year == year and post['pub_date'].month == month]

    if not month_posts:
        abort(404)

    # Group by category (single level for monthly view)
    grouped_posts = {}
    for post in month_posts:
        category = post['category']
        if category not in grouped_posts:
            grouped_posts[category] = []
        grouped_posts[category].append(post)

    month_names = ['', 'January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']
    month_name = month_names[month]

    breadcrumbs = [
        {'name': 'Archive', 'url': '/archive'},
        {'name': str(year), 'url': f'/archive/{year}'}
    ]

    return render_template('archive.html',
                         archive_title=f'{month_name} {year}',
                         archive_description=f'Essays and AI writings from {month_name} {year}.',
                         grouped_posts=grouped_posts,
                         breadcrumbs=breadcrumbs,
                         current_year=datetime.now().year,
                         current_page=f'{month_name} {year} Archive')


@app.route('/themes')
def themes_index():
    """Themes page - just displays the index.md content."""
    themes_path = DATA_DIR / 'themes'
    
    # Check for index.md in the themes directory
    index_file = themes_path / 'index.md'
    if index_file.exists():
        content_data = render_markdown_file(index_file)
        return render_template('post.html',
                             content=content_data['content'],
                             title='Themes',
                             metadata=content_data.get('metadata', {}),
                             breadcrumbs=[],
                             current_year=datetime.now().year,
                             current_page='Themes',
                             unique_icon=content_data.get('unique_icon'),
                             parent_directory=None)
    else:
        # Fallback to directory listing if no index.md
        return serve_path('themes')


@app.route('/directory')
def directory_index():
    """Directory listing that was previously the homepage."""
    items = get_directory_structure(DATA_DIR)

    # Check for index.md in the root data directory
    index_file = DATA_DIR / 'index.md'
    index_content = None
    content_position = 'top'  # Default position
    if index_file.exists():
        index_content = render_markdown_file(index_file)

        # Determine content position based on length
        # Count words in the HTML content (after stripping HTML tags)
        content_text = re.sub(r'<[^>]+>', '', index_content['content'])
        word_count = len(content_text.split())

        # If content is longer than 150 words, put it at the bottom
        if word_count > 150:
            content_position = 'bottom'

    # Check if root directory is an image gallery
    image_items = [item for item in items if item['is_image']]
    total_files = [item for item in items if not item['is_dir']]
    is_image_gallery = len(image_items) >= 3 and len(total_files) > 0 and (len(image_items) / len(total_files)) >= 0.5

    return render_template('directory.html',
                         items=items,
                         current_path='',
                         title='Kenneth Reitz',
                         breadcrumbs=[],
                         index_content=index_content,
                         content_position=content_position,
                         is_image_gallery=is_image_gallery,
                         image_items=image_items,
                         current_year=datetime.now().year)

@app.route('/<path:path>')
def serve_path(path):
    """Serve files and directories from the data folder."""
    full_path = DATA_DIR / path

    # If the path doesn't exist, try adding .md extension for markdown files
    if not full_path.exists():
        md_path = DATA_DIR / (path + '.md')
        if md_path.exists() and md_path.suffix == '.md':
            full_path = md_path
        else:
            abort(404)

    # Generate breadcrumbs
    # For clean URLs, we need to handle the case where path might not include .md
    original_path = path
    if full_path.suffix == '.md' and not path.endswith('.md'):
        # This is a clean URL for a markdown file
        path_parts = path.split('/')
    else:
        path_parts = path.split('/')

    breadcrumbs = []
    current = ''
    for part in path_parts[:-1]:  # Exclude the current page
        current = f"{current}/{part}" if current else part
        breadcrumbs.append({
            'name': part.replace('-', ' ').replace('_', ' ').title(),
            'url': f"/{current}"
        })

    if full_path.is_dir():
        # Directory listing
        items = get_directory_structure(full_path)

        # Check if this is an image gallery (50% or more images)
        image_items = [item for item in items if item['is_image']]
        total_files = [item for item in items if not item['is_dir']]
        is_image_gallery = len(image_items) >= 3 and len(total_files) > 0 and (len(image_items) / len(total_files)) >= 0.5

        # Check for index.md in the directory
        index_file = full_path / 'index.md'
        index_content = None
        content_position = 'top'  # Default position
        if index_file.exists():
            index_content = render_markdown_file(index_file)

            # Determine content position based on length
            # Count words in the HTML content (after stripping HTML tags)
            content_text = re.sub(r'<[^>]+>', '', index_content['content'])
            word_count = len(content_text.split())

            # If content is longer than 150 words, put it at the bottom
            if word_count > 150:
                content_position = 'bottom'

        # Use title from index.md if available, otherwise fall back to directory name
        if index_content and index_content.get('title'):
            title = index_content['title']
        else:
            title = path_parts[-1].replace('-', ' ').replace('_', ' ').title()

        # Generate parent directory information for back link
        parent_directory = None
        if full_path.parent != DATA_DIR:  # Don't show parent for root-level content
            parent_path = full_path.parent
            parent_display_name = parent_path.name.replace('-', ' ').replace('_', ' ').title()
            parent_url = '/' + str(parent_path.relative_to(DATA_DIR))
            if parent_url == '/':
                parent_url = '/directory'
            parent_icon = generate_folder_icon(parent_display_name, size=20)
            
            parent_directory = {
                'display_name': parent_display_name,
                'url': parent_url,
                'icon': parent_icon
            }

        return render_template('directory.html',
                             items=items,
                             current_path=original_path,
                             title=title,
                             breadcrumbs=breadcrumbs,
                             index_content=index_content,
                             content_position=content_position,
                             is_image_gallery=is_image_gallery,
                             image_items=image_items,
                             parent_directory=parent_directory,
                             current_year=datetime.now().year,
                             current_page=title)

    elif full_path.suffix == '.md':
        # Markdown file
        content_data = render_markdown_file(full_path)

        # Find related posts for essays and AI writings
        related_posts = []
        prev_post = None
        next_post = None
        if 'essays' in path or ('artificial-intelligence' in path and 'writings' in path):
            related_posts = find_related_posts(str(full_path.relative_to(DATA_DIR)))
            prev_post, next_post = find_adjacent_posts(str(full_path.relative_to(DATA_DIR)))

        # Generate description from content for social sharing
        content_text = re.sub(r'<[^>]+>', '', content_data['content'])
        content_text = content_text.strip()
        description = ""
        if content_text:
            # Get first paragraph or first 200 chars
            first_para = content_text.split('\n\n')[0]
            description = first_para[:200] + '...' if len(first_para) > 200 else first_para

        # Generate parent directory information
        parent_directory = None
        if full_path.parent != DATA_DIR:  # Don't show parent for root-level content
            parent_path = full_path.parent
            parent_display_name = parent_path.name.replace('-', ' ').replace('_', ' ').title()
            parent_url = '/' + str(parent_path.relative_to(DATA_DIR))
            parent_icon = generate_folder_icon(parent_display_name, size=20)
            
            parent_directory = {
                'display_name': parent_display_name,
                'url': parent_url,
                'icon': parent_icon
            }

        return render_template('post.html',
                             content=content_data['content'],
                             title=content_data['title'],
                             metadata=content_data['metadata'],
                             description=description,
                             breadcrumbs=breadcrumbs,
                             current_path=path,
                             current_year=datetime.now().year,
                             current_page=content_data['title'],
                             related_posts=related_posts,
                             reading_time=content_data.get('reading_time'),
                             word_count=content_data.get('word_count'),
                             prev_post=prev_post,
                             next_post=next_post,
                             tags=content_data.get('tags', []),
                             series_posts=content_data.get('series_posts', []),
                             series_name=content_data.get('series_name'),
                             unique_icon=content_data.get('unique_icon'),
                             parent_directory=parent_directory)

    elif full_path.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
        # Image file - check if it's in a gallery directory
        parent_dir = full_path.parent
        gallery_images = []

        if parent_dir.exists():
            for img in sorted(parent_dir.iterdir()):
                if img.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
                    gallery_images.append({
                        'name': img.name,
                        'path': f"/static/data/{img.relative_to(DATA_DIR)}",
                        'url': f"/{img.relative_to(DATA_DIR)}",
                        'is_current': img == full_path
                    })

        return render_template('photo.html',
                             image_path=f"/static/data/{path}",
                             title=full_path.stem.replace('-', ' ').replace('_', ' ').title(),
                             breadcrumbs=breadcrumbs,
                             gallery_images=gallery_images,
                             current_path=path,
                             current_year=datetime.now().year,
                             current_page=full_path.stem.replace('-', ' ').replace('_', ' ').title())

    else:
        # Other files - serve directly
        from flask import send_file
        return send_file(full_path)

@app.route('/static/data/<path:path>')
def serve_data_file(path):
    """Serve static files from the data directory."""
    full_path = DATA_DIR / path
    if not full_path.exists() or not full_path.is_file():
        abort(404)
    from flask import send_file
    return send_file(full_path)



@app.route('/api/search')
def api_search():
    """API endpoint for full-text search across the knowledge base."""
    query = request.args.get('q', '').lower()
    if not query:
        return jsonify([])

    results = []

    def search_path(current_path: Path, display_path: str = ""):
        """Recursively search files and directories under ``current_path``.

        This replaces the previous implementation that searched an in-memory
        tree representation but never actually scanned the filesystem,
        resulting in an empty search index. We now walk the ``data`` directory
        directly so queries return real results.
        """
        for item in current_path.iterdir():
            if item.name.startswith('.'):
                continue

            relative_path = str(item.relative_to(DATA_DIR))
            node_name = item.name.lower()
            node_path = relative_path.lower()
            node_content = ""

            if item.is_file() and item.suffix == '.md':
                try:
                    node_content = item.read_text(encoding='utf-8').lower()
                except Exception:
                    node_content = ""

            item_display_path = f"{display_path}/{item.name}" if display_path else item.name

            if query in node_name or query in node_path or query in node_content:
                # Generate snippet with highlighted search terms for markdown files
                snippet = ""
                if item.suffix == '.md' and node_content and query in node_content:
                    # Find the first occurrence of the query in content
                    query_pos = node_content.find(query)
                    if query_pos != -1:
                        # Extract context around the query (200 chars before and after)
                        start = max(0, query_pos - 100)
                        end = min(len(node_content), query_pos + len(query) + 100)
                        snippet_text = node_content[start:end]
                        
                        # Clean up the snippet (remove markdown syntax)
                        import re
                        snippet_text = re.sub(r'[#*`_\[\]()]', '', snippet_text)
                        snippet_text = re.sub(r'\s+', ' ', snippet_text).strip()
                        
                        # Highlight the search term (case-insensitive)
                        snippet = re.sub(f'({re.escape(query)})', r'<mark>\1</mark>', snippet_text, flags=re.IGNORECASE)
                        
                        # Add ellipsis if snippet is truncated
                        if start > 0:
                            snippet = "..." + snippet
                        if end < len(node_content):
                            snippet = snippet + "..."
                
                result = {
                    'name': item.name,
                    'type': 'directory' if item.is_dir() else ('article' if item.suffix == '.md' else 'file'),
                    'path': relative_path,
                    'display_path': item_display_path,
                    'snippet': snippet,
                    'relevance': 0,
                }
                
                # Add unique_icon for articles
                if item.suffix == '.md':
                    try:
                        # Convert path to URL for lookup in blog_posts
                        clean_url = '/' + relative_path[:-3]  # Remove .md extension
                        blog_posts = metadata_cache.get_blog_posts()
                        for post in blog_posts:
                            if post['url'] == clean_url:
                                if 'unique_icon' in post:
                                    result['unique_icon'] = post['unique_icon']
                                break
                    except Exception:
                        pass

                relevance = 0
                if query in node_name:
                    relevance += 10
                    if node_name.startswith(query):
                        relevance += 5
                if query in node_path:
                    relevance += 3
                if query in node_content:
                    relevance += 1
                    relevance += node_content.count(query) * 0.1

                result['relevance'] = relevance
                results.append(result)

            if item.is_dir():
                search_path(item, item_display_path)

    # Start searching from the data directory
    search_path(DATA_DIR)

    results.sort(key=lambda x: x['relevance'], reverse=True)
    return jsonify(results)



def collect_blog_posts():
    """Collect blog posts from essays and AI writings for RSS feed."""
    posts = []

    # Define blog post directories
    blog_dirs = [
        DATA_DIR / 'essays',
        DATA_DIR / 'artificial-intelligence'  # This will pick up root AI posts and scan subdirs
    ]

    def scan_for_posts(path, category=""):
        if not path.exists() or not path.is_dir():
            return

        for item in sorted(path.iterdir(), reverse=True):  # Most recent first
            if item.name.startswith('.') or item.name.lower() == 'index.md':
                continue

            if item.is_file() and item.suffix == '.md':
                # Get post data
                try:
                    content_data = render_markdown_file(item)

                    # Extract publication date using intelligent extraction
                    pub_date = extract_intelligent_date(item, content_data)

                    # Skip posts without determinable dates (no filename date, no YAML date, no content date)
                    if pub_date is None:
                        continue

                    # Create clean URL
                    relative_path = str(item.relative_to(DATA_DIR))
                    clean_url = '/' + relative_path[:-3]  # Remove .md extension

                    # Extract description (first paragraph or first 200 chars)
                    # Strip HTML tags for description
                    content_text = re.sub(r'<[^>]+>', '', content_data['content'])
                    content_text = content_text.strip()

                    # Get first paragraph or first 200 chars
                    description = ""
                    if content_text:
                        first_para = content_text.split('\n\n')[0]
                        description = first_para[:300] + '...' if len(first_para) > 300 else first_para

                    posts.append({
                        'title': content_data['title'],
                        'url': clean_url,
                        'description': description,
                        'pub_date': pub_date,
                        'category': category or item.parent.name.replace('-', ' ').title(),
                        'content': content_data['content'][:1000] + '...' if len(content_data['content']) > 1000 else content_data['content']
                    })
                except Exception:
                    continue
            elif item.is_dir():
                # Recursively scan subdirectories
                scan_for_posts(item, category or item.name.replace('-', ' ').title())

    # Scan each blog directory
    for blog_dir in blog_dirs:
        if blog_dir.exists():
            category = blog_dir.name.replace('-', ' ').title()
            if 'artificial-intelligence' in str(blog_dir):
                category = 'AI & Consciousness'
            scan_for_posts(blog_dir, category)

    # Sort by publication date (most recent first)
    posts.sort(key=lambda x: x['pub_date'], reverse=True)

    return posts[:20]  # Return most recent 20 posts


# Cache with TTL - cleared when date extraction logic changes
_blog_posts_cache = {'data': None, 'timestamp': 0}
_sidenotes_cache = {'data': None, 'timestamp': 0}
_outlines_cache = {'data': None, 'timestamp': 0}
_quotes_cache = {'data': None, 'timestamp': 0}
_connections_cache = {'data': None, 'timestamp': 0}
_external_links_cache = {'data': None, 'timestamp': 0}
_terms_cache = {'data': None, 'timestamp': 0}
CACHE_TTL = 36000  # 10 hours cache

# Force cache invalidation for filename change
import time
_force_cache_clear = time.time()

def load_prebuild_cache(cache_name):
    """Load a pre-built cache file if it exists."""
    from datetime import datetime
    
    def convert_datetime_strings(item):
        """Convert ISO datetime strings back to datetime objects."""
        if isinstance(item, str):
            # Try to parse as ISO datetime
            try:
                return datetime.fromisoformat(item)
            except ValueError:
                return item
        elif isinstance(item, dict):
            return {k: convert_datetime_strings(v) for k, v in item.items()}
        elif isinstance(item, list):
            return [convert_datetime_strings(i) for i in item]
        else:
            return item
    
    cache_file = Path(f'.cache/{cache_name}.json')
    if cache_file.exists():
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
                if cache_data.get('data') is not None:
                    # Convert datetime strings back to datetime objects
                    restored_data = convert_datetime_strings(cache_data['data'])
                    print(f"Loaded pre-built {cache_name} cache from Docker build")
                    return restored_data, cache_data.get('generated_at', time.time())
        except Exception as e:
            print(f"Warning: Failed to load pre-built {cache_name} cache: {e}")
    return None, 0

def initialize_prebuild_caches():
    """Initialize all caches from pre-built files if available."""
    global _blog_posts_cache, _sidenotes_cache, _outlines_cache
    global _quotes_cache, _connections_cache, _terms_cache
    
    cache_mappings = [
        ('blog_posts', _blog_posts_cache),
        ('sidenotes', _sidenotes_cache),
        ('outlines', _outlines_cache),
        ('quotes', _quotes_cache),
        ('connections', _connections_cache),
        ('terms', _terms_cache),
    ]
    
    loaded_count = 0
    for cache_name, cache_dict in cache_mappings:
        data, timestamp = load_prebuild_cache(cache_name)
        if data is not None:
            cache_dict['data'] = tuple(data) if cache_name == 'blog_posts' else data
            cache_dict['timestamp'] = timestamp
            loaded_count += 1
    
    if loaded_count > 0:
        print(f"Loaded {loaded_count} pre-built caches - app ready instantly!")
    
    return loaded_count

# Initialize unified cache on module load
class MetadataCache:
    """Clean interface to site metadata cache."""
    
    def __init__(self):
        self._data = None
    
    def initialize(self):
        """Load all site metadata in a single scan."""
        print("Starting unified cache generation...")
        self._data = _generate_all_caches_unified()
        print("Unified cache generation completed!")
    
    def get_sidenotes(self):
        """Get all sidenotes with metadata."""
        if not self._data:
            return {'articles': [], 'total_count': 0}
        
        sidenotes_data = self._data['sidenotes']['articles']  # {file_path: [sidenotes]}
        
        # Create file metadata lookup from blog_posts (fast dictionary lookup)
        file_metadata = {}
        for post in self._data.get('blog_posts', []):
            # Convert URL back to file path for lookup
            file_path = 'data' + post['url'] + '.md'
            file_metadata[file_path] = post
        
        articles = []
        for file_path, sidenotes in sidenotes_data.items():
            if not sidenotes:
                continue
                
            # Use pre-computed metadata instead of re-processing files
            metadata = file_metadata.get(file_path)
            if metadata:
                articles.append({
                    'title': metadata['title'],
                    'url': metadata['url'],
                    'date': metadata.get('pub_date'),
                    'category': metadata['category'].replace('-', ' ').title(),
                    'sidenotes': [{'text': s['text'], 'id': s.get('id')} for s in sidenotes],
                    'unique_icon': metadata.get('unique_icon')
                })
        
        # Sort by date (most recent first)
        articles.sort(key=lambda x: x['date'] if x['date'] else datetime(1900, 1, 1), reverse=True)
        
        return {
            'articles': articles,
            'total_count': self._data['sidenotes']['total_count']
        }
    
    def get_outlines(self):
        """Get all outlines with metadata."""
        if not self._data:
            return {'articles': [], 'total_count': 0}
        
        outlines_data = self._data['outlines']['articles']  # {file_path: [outlines]}
        
        # Create file metadata lookup from blog_posts (fast dictionary lookup)
        file_metadata = {}
        for post in self._data.get('blog_posts', []):
            # Convert URL back to file path for lookup
            file_path = 'data' + post['url'] + '.md'
            file_metadata[file_path] = post
        
        articles = []
        for file_path, outlines in outlines_data.items():
            if not outlines:
                continue
                
            # Use pre-computed metadata instead of re-processing files
            metadata = file_metadata.get(file_path)
            if metadata:
                # Process headings to extract IDs and create anchor URLs
                processed_headings = []
                for o in outlines:
                    # Always generate an ID from the text to ensure links work
                    import re
                    heading_id = re.sub(r'[^\w\s-]', '', o['text'].lower())
                    heading_id = re.sub(r'[-\s]+', '-', heading_id).strip('-')
                    
                    # Try to extract ID from HTML if present (preferred)
                    if 'html' in o and o['html']:
                        id_match = re.search(r'id="([^"]*)"', o['html'])
                        if id_match and id_match.group(1):
                            heading_id = id_match.group(1)
                    
                    processed_headings.append({
                        'level': int(o['level']),
                        'text': o['text'],
                        'id': heading_id,
                        'anchor_url': f"{metadata['url']}#{heading_id}"
                    })
                
                articles.append({
                    'title': metadata['title'],
                    'url': metadata['url'],
                    'date': metadata.get('pub_date'),
                    'category': metadata['category'].replace('-', ' ').title(),
                    'headings': processed_headings,
                    'unique_icon': metadata.get('unique_icon')
                })
        
        # Sort by date (most recent first)
        articles.sort(key=lambda x: x['date'] if x['date'] else datetime(1900, 1, 1), reverse=True)
        
        return {
            'articles': articles,
            'total_count': self._data['outlines']['total_count']
        }
    
    def get_quotes(self):
        """Get all quotes with metadata."""
        if not self._data:
            return {'articles': [], 'total_count': 0}
        
        quotes_data = self._data['quotes']['articles']
        
        # Create file metadata lookup from blog_posts (fast dictionary lookup)
        file_metadata = {}
        for post in self._data.get('blog_posts', []):
            # Convert URL back to file path for lookup
            file_path = 'data' + post['url'] + '.md'
            file_metadata[file_path] = post
        
        articles = []
        for file_path, quotes in quotes_data.items():
            if not quotes:
                continue
                
            # Use pre-computed metadata instead of re-processing files
            metadata = file_metadata.get(file_path)
            if metadata:
                articles.append({
                    'title': metadata['title'],
                    'url': metadata['url'],
                    'date': metadata.get('pub_date'),
                    'category': metadata['category'].replace('-', ' ').title(),
                    'quotes': [q['text'] for q in quotes],
                    'unique_icon': metadata.get('unique_icon')
                })
        
        articles.sort(key=lambda x: x['date'] if x['date'] else datetime(1900, 1, 1), reverse=True)
        
        return {
            'articles': articles,
            'total_count': self._data['quotes']['total_count']
        }
    
    def get_connections(self):
        """Get all connections with metadata in template-expected format."""
        if not self._data:
            return {'articles': [], 'total_count': 0, 'total_outgoing': 0, 'total_incoming': 0}
        
        connections_cache = self._data['connections']
        outgoing_refs = connections_cache.get('outgoing_refs', {})
        incoming_refs = connections_cache.get('incoming_refs', {})
        
        print(f"DEBUG: get_connections - outgoing_refs has {len(outgoing_refs)} files")
        print(f"DEBUG: get_connections - incoming_refs has {len(incoming_refs)} refs")
        
        # Create URL to metadata lookup from blog_posts (fast dictionary lookup)
        url_metadata = {}
        file_to_url = {}
        for post in self._data.get('blog_posts', []):
            url_metadata[post['url']] = post
            # Check for both possible file path keys
            file_path = post.get('file_path') or post.get('path')
            if file_path:
                file_to_url[file_path] = post['url']
        
        # Build articles with their connections
        articles = []
        
        print(f"DEBUG: file_to_url mapping has {len(file_to_url)} entries")
        
        # Process outgoing connections by file path
        for file_path, outgoing_list in outgoing_refs.items():
            article_url = file_to_url.get(file_path)
            if not article_url:
                print(f"DEBUG: No URL found for file_path: {file_path}")
                continue
                
            metadata = url_metadata.get(article_url)
            if not metadata:
                print(f"DEBUG: No metadata found for article_url: {article_url}")
                continue
            
            # Build outgoing connections with proper target_url and link_text
            processed_outgoing = []
            for conn in outgoing_list:
                processed_outgoing.append({
                    'target_url': conn['url'],
                    'link_text': conn['text']
                })
            
            # Get incoming connections for this article
            incoming_list = incoming_refs.get(article_url, [])
            processed_incoming = []
            for conn in incoming_list:
                # Find source metadata
                source_url = file_to_url.get(conn['source_file'])
                source_metadata = url_metadata.get(source_url) if source_url else None
                
                # If no URL mapping found, try to extract title from file
                source_title = 'Unknown'
                if source_metadata:
                    source_title = source_metadata['title']
                else:
                    # Try to extract title from the file itself
                    try:
                        file_path = conn['source_file']
                        if os.path.exists(file_path):
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                                # Look for markdown title (# Title)
                                for line in content.split('\n')[:10]:  # Check first 10 lines
                                    line = line.strip()
                                    if line.startswith('# '):
                                        source_title = line[2:].strip()
                                        break
                                    elif line.startswith('title:'):  # YAML frontmatter
                                        source_title = line[6:].strip().strip('"\'')
                                        break
                    except Exception:
                        pass  # Keep 'Unknown' if file reading fails
                
                processed_incoming.append({
                    'source_url': source_url or conn['source_file'],
                    'source_title': source_title,
                    'link_text': conn['text']
                })
            
            # Only include articles that have connections
            if processed_outgoing or processed_incoming:
                articles.append({
                    'title': metadata['title'],
                    'url': article_url,
                    'date': metadata.get('pub_date'),
                    'category': metadata['category'].replace('-', ' ').title(),
                    'connections': processed_outgoing,  # For backward compatibility
                    'outgoing_connections': processed_outgoing,
                    'incoming_connections': processed_incoming,
                    'unique_icon': metadata.get('unique_icon')
                })
        
        # Sort by date (most recent first)
        articles.sort(key=lambda x: x['date'] if x['date'] else datetime(1900, 1, 1), reverse=True)
        
        # Calculate totals
        total_outgoing = sum(len(article['outgoing_connections']) for article in articles)
        total_incoming = sum(len(article['incoming_connections']) for article in articles)
        
        return {
            'articles': articles,
            'total_count': total_outgoing + total_incoming,
            'total_outgoing': total_outgoing,
            'total_incoming': total_incoming
        }
    
    def get_terms(self):
        """Get all terms with metadata.""" 
        if not self._data:
            return {'terms': [], 'total_terms': 0, 'total_occurrences': 0}
        
        terms_data = self._data['terms']
        return {
            'terms': terms_data['terms'],
            'total_terms': len(terms_data['terms']),
            'total_occurrences': terms_data['total_occurrences']
        }
    
    def get_blog_posts(self):
        """Get all blog posts from unified cache."""
        if not self._data:
            return []
        
        return self._data.get('blog_posts', [])

# Global metadata cache instance
metadata_cache = MetadataCache()

def initialize_unified_cache():
    """Initialize unified cache at startup."""
    global _blog_posts_cache, _sidenotes_cache, _outlines_cache
    global _quotes_cache, _connections_cache, _terms_cache
    
    # Initialize the clean metadata cache
    metadata_cache.initialize()

def extract_intelligent_date(item_path, content_data=None):
    """Extract date intelligently, prioritizing filename patterns as requested."""
    pub_date = None

    # 1. PRIORITY: Try full YYYY-MM-DD format anywhere in filename first
    date_match = re.search(r'(\d{4}-\d{2}-\d{2})', item_path.name)
    if date_match:
        try:
            pub_date = datetime.strptime(date_match.group(1), '%Y-%m-%d')
            return pub_date
        except:
            pass

    # 2. Try YYYY-MM format at start of filename
    date_match = re.match(r'(\d{4}-\d{2})', item_path.stem)
    if date_match:
        try:
            # Extract day from content if present, otherwise use first of month
            day = 1
            try:
                with open(item_path, 'r', encoding='utf-8') as f:
                    content_preview = f.read(1000)
                day_match = re.search(r'(\d{4}-\d{2}-(\d{2}))', content_preview)
                if day_match:
                    day = int(day_match.group(2))
            except:
                pass

            pub_date = datetime.strptime(date_match.group(1) + f'-{day:02d}', '%Y-%m-%d')
            return pub_date
        except:
            pass

    # 3. Try just year at start of filename (YYYY)
    year_match = re.match(r'(\d{4})', item_path.stem)
    if year_match:
        try:
            # Try to get month from content, otherwise use January
            year = int(year_match.group(1))
            month = 1
            day = 1

            try:
                with open(item_path, 'r', encoding='utf-8') as f:
                    first_few_lines = ''.join(f.readlines()[:10])

                # Look for "*Month YYYY*" pattern in content
                month_match = re.search(r'\*([A-Za-z]+)\s+' + str(year) + r'\*', first_few_lines)
                if month_match:
                    month_name = month_match.group(1)
                    month = datetime.strptime(month_name, '%B').month
            except:
                pass

            pub_date = datetime(year, month, day)
            return pub_date
        except:
            pass

    # 4. Check YAML front matter for date (lower priority now)
    if content_data and content_data['metadata'].get('date'):
        try:
            if isinstance(content_data['metadata']['date'], list):
                pub_date = datetime.strptime(content_data['metadata']['date'][0], '%Y-%m-%d')
            else:
                pub_date = datetime.strptime(str(content_data['metadata']['date']), '%Y-%m-%d')
            return pub_date
        except:
            pass

    # 5. Check for date in content (look for *Month YYYY* pattern)
    try:
        with open(item_path, 'r', encoding='utf-8') as f:
            first_few_lines = ''.join(f.readlines()[:10])

        # Look for patterns like "*January 2025*" or "*Month YYYY*"
        month_year_match = re.search(r'\*([A-Za-z]+\s+\d{4})\*', first_few_lines)
        if month_year_match:
            try:
                pub_date = datetime.strptime(month_year_match.group(1), '%B %Y')
                # Set to first day of month for month-only dates
                pub_date = pub_date.replace(day=1)
                return pub_date
            except:
                pass
    except:
        pass

    # 6. Final fallback: if no date found anywhere, return None
    # (Removed file creation time fallback due to deployment issues)
    return None


def _collect_all_blog_posts_cached():
    """Internal cached function to collect all blog posts with TTL."""
    current_time = time.time()

    # Check if cache is valid
    if (_blog_posts_cache['data'] is not None and
        current_time - _blog_posts_cache['timestamp'] < CACHE_TTL):
        return _blog_posts_cache['data']

    # Cache miss or expired - rebuild
    posts = []

    # Define blog post directories
    blog_dirs = [
        DATA_DIR / 'essays',
        DATA_DIR / 'artificial-intelligence'  # This will pick up root AI posts and scan subdirs
    ]

    def scan_for_posts(path, category=""):
        if not path.exists() or not path.is_dir():
            return

        for item in sorted(path.iterdir(), reverse=True):  # Most recent first
            if item.name.startswith('.') or item.name.lower() == 'index.md':
                continue

            if item.is_file() and item.suffix == '.md':
                # Get post data
                try:
                    content_data = render_markdown_file(item)

                    # Extract publication date using intelligent extraction
                    pub_date = extract_intelligent_date(item, content_data)

                    # Skip posts without determinable dates (no filename date, no YAML date, no content date)
                    if pub_date is None:
                        continue

                    # Create clean URL
                    relative_path = str(item.relative_to(DATA_DIR))
                    clean_url = '/' + relative_path[:-3]  # Remove .md extension

                    # Extract description (first paragraph or first 200 chars)
                    # Strip HTML tags for description
                    content_text = re.sub(r'<[^>]+>', '', content_data['content'])
                    content_text = content_text.strip()

                    # Get first paragraph or first 200 chars
                    description = ""
                    if content_text:
                        first_para = content_text.split('\n\n')[0]
                        description = first_para[:300] + '...' if len(first_para) > 300 else first_para

                    posts.append({
                        'title': content_data['title'],
                        'url': clean_url,
                        'description': description,
                        'pub_date': pub_date,
                        'category': category or item.parent.name.replace('-', ' ').title(),
                        'content': content_data['content'][:1000] + '...' if len(content_data['content']) > 1000 else content_data['content']
                    })
                except Exception:
                    continue
            elif item.is_dir():
                # Recursively scan subdirectories
                scan_for_posts(item, category or item.name.replace('-', ' ').title())

    # Scan each blog directory
    for blog_dir in blog_dirs:
        if blog_dir.exists():
            category = blog_dir.name.replace('-', ' ').title()
            if 'artificial-intelligence' in str(blog_dir):
                category = 'AI & Consciousness'
            scan_for_posts(blog_dir, category)

    # Sort by publication date (most recent first)
    posts.sort(key=lambda x: x['pub_date'], reverse=True)

    # Update cache
    result = tuple(posts)
    _blog_posts_cache['data'] = result
    _blog_posts_cache['timestamp'] = time.time()

    return result


def collect_all_blog_posts():
    """Public function to collect all blog posts - converts cached tuple back to list."""
    return list(_collect_all_blog_posts_cached())


def preload_blog_posts():
    """Preload blog posts cache at startup for faster initial page loads."""
    print("Preloading blog posts cache...")
    start_time = time.time()
    posts = _collect_all_blog_posts_cached()
    load_time = time.time() - start_time
    print(f"Loaded {len(posts)} posts in {load_time:.2f}s")


def preload_sidenotes():
    """Preload sidenotes cache at startup for faster initial page loads."""
    print("Preloading sidenotes cache...")
    start_time = time.time()
    sidenotes_data = _extract_all_sidenotes_cached()
    load_time = time.time() - start_time
    print(f"Extracted {sidenotes_data['total_count']} sidenotes from {len(sidenotes_data['articles'])} articles in {load_time:.2f}s")


def preload_outlines():
    """Preload outlines cache at startup for faster initial page loads."""
    print("Preloading outlines cache...")
    start_time = time.time()
    outlines_data = _extract_all_outlines_cached()
    load_time = time.time() - start_time
    print(f"Extracted {outlines_data['total_count']} headings from {len(outlines_data['articles'])} articles in {load_time:.2f}s")


def preload_quotes():
    """Preload quotes cache at startup for faster initial page loads."""
    print("Preloading quotes cache...")
    start_time = time.time()
    quotes_data = _extract_all_quotes_cached()
    load_time = time.time() - start_time
    print(f"Extracted {quotes_data['total_count']} quotes from {len(quotes_data['articles'])} articles in {load_time:.2f}s")


def preload_connections():
    """Preload connections cache at startup for faster initial page loads."""
    print("Preloading connections cache...")
    start_time = time.time()
    connections_data = _extract_all_connections_cached()
    load_time = time.time() - start_time
    print(f"Extracted {connections_data['total_count']} cross-references in {load_time:.2f}s")


def _extract_all_external_links_cached():
    """Extract all external links from articles with 10-hour TTL cache."""
    current_time = time.time()
    
    # Check if cache is still valid (10 hour TTL)
    if (_external_links_cache['data'] is not None and 
        current_time - _external_links_cache['timestamp'] < CACHE_TTL and
        _external_links_cache['timestamp'] > _force_cache_clear):
        return _external_links_cache['data']
    
    posts = _collect_all_blog_posts_cached()
    articles_with_links = []
    total_count = 0
    domain_counts = defaultdict(int)
    
    # Pattern to match external links (http/https URLs that don't start with current domain)
    external_link_pattern = r'<a[^>]*href="(https?://[^"]*)"[^>]*>(.*?)</a>'
    
    for post in posts:
        external_links = []
        
        # Find all external links in content
        matches = re.findall(external_link_pattern, post['content'], re.IGNORECASE | re.DOTALL)
        
        for url, link_text in matches:
            # Skip internal links (adjust domain as needed)
            if 'kennethreitz.org' not in url:
                # Clean link text
                clean_text = re.sub(r'<[^>]+>', '', link_text).strip()
                if not clean_text:
                    clean_text = url
                
                # Extract domain for stats
                domain = re.match(r'https?://(?:www\.)?([^/]+)', url)
                if domain:
                    domain_counts[domain.group(1)] += 1
                
                external_links.append({
                    'url': url,
                    'link_text': clean_text[:100],  # Truncate very long link text
                    'domain': domain.group(1) if domain else 'unknown'
                })
        
        if external_links:
            articles_with_links.append({
                'title': post['title'],
                'url': post['url'],
                'date': post.get('date'),
                'category': post.get('category', 'Unknown'),
                'external_links': external_links
            })
            total_count += len(external_links)
    
    # Sort articles by publication date (most recent first)
    articles_with_links.sort(key=lambda x: x['date'] or datetime.min, reverse=True)
    
    # Sort domains by frequency
    top_domains = sorted(domain_counts.items(), key=lambda x: x[1], reverse=True)
    
    result = {
        'articles': articles_with_links,
        'total_count': total_count,
        'domain_stats': top_domains
    }
    
    # Cache the result
    _external_links_cache['data'] = result
    _external_links_cache['timestamp'] = current_time
    
    return result


def preload_external_links():
    """Preload external links cache at startup for faster initial page loads."""
    print("Preloading external links cache...")
    start_time = time.time()
    links_data = _extract_all_external_links_cached()
    load_time = time.time() - start_time
    print(f"Extracted {links_data['total_count']} external links from {len(links_data['articles'])} articles in {load_time:.2f}s")


def _extract_all_terms_cached():
    """Return pre-loaded terms cache data (pure RAM, no TTL)."""
    # Return pre-loaded cache data if available
    if _terms_cache['data'] is not None:
        return _terms_cache['data']
    
    posts = _collect_all_blog_posts_cached()
    term_occurrences = defaultdict(list)  # term -> [(article_title, article_url, count)]
    
    # Common stop words to filter out
    stop_words = {
        'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 
        'by', 'from', 'as', 'an', 'a', 'is', 'was', 'are', 'were', 'be', 'been',
        'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should',
        'may', 'might', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he',
        'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them', 'my', 'your',
        'his', 'its', 'our', 'their', 'not', 'all', 'some', 'any', 'each', 'every',
        'one', 'two', 'if', 'then', 'so', 'when', 'where', 'how', 'why', 'what',
        'about', 'into', 'through', 'during', 'before', 'after', 'above', 'below',
        'up', 'down', 'out', 'off', 'over', 'under', 'again', 'further', 'then',
        'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both',
        'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'only',
        'own', 'same', 'than', 'too', 'very', 'just', 'now', 'also', 'often', 'really',
        'much', 'many', 'way', 'well', 'even', 'still', 'get', 'go', 'come', 'make',
        'take', 'know', 'see', 'think', 'say', 'work', 'feel', 'look', 'seem', 'want',
        'use', 'find', 'give', 'tell', 'ask', 'try', 'help', 'need', 'become', 'turn',
        'start', 'show', 'hear', 'play', 'run', 'move', 'live', 'believe', 'hold',
        'bring', 'happen', 'write', 'provide', 'sit', 'stand', 'lose', 'pay', 'meet'
    }
    
    # Technical terms that should always be included
    important_terms = {
        'API', 'HTTP', 'Python', 'JavaScript', 'AI', 'ML', 'consciousness', 'algorithm',
        'Requests', 'Flask', 'Django', 'GitHub', 'software', 'programming', 'technology',
        'artificial intelligence', 'machine learning', 'open source', 'philosophy'
    }
    
    for post in posts:
        # Clean content - remove HTML tags and get plain text
        import re
        clean_content = re.sub(r'<[^>]+>', ' ', post['content'])
        clean_content = re.sub(r'\s+', ' ', clean_content)
        
        # Extract potential terms using multiple strategies
        terms_in_post = defaultdict(int)
        
        # Strategy 1: Capitalized words/phrases (likely proper nouns, concepts)
        capitalized_terms = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', clean_content)
        for term in capitalized_terms:
            if len(term) > 2 and term.lower() not in stop_words:
                terms_in_post[term] += 1
        
        # Strategy 2: Technical terms in quotes or emphasized
        quoted_terms = re.findall(r'["\']([^"\']{3,30})["\']', clean_content)
        for term in quoted_terms:
            if not term.lower() in stop_words and len(term.split()) <= 3:
                terms_in_post[term] += 1
        
        # Strategy 3: Acronyms and technical terms
        acronyms = re.findall(r'\b[A-Z]{2,8}\b', clean_content)
        for term in acronyms:
            if term not in ['THE', 'AND', 'FOR', 'BUT', 'NOT']:
                terms_in_post[term] += 2  # Weight acronyms higher
        
        # Strategy 4: Important technical words
        words = re.findall(r'\b\w{4,}\b', clean_content.lower())
        for word in words:
            if word in important_terms or word.lower() in important_terms:
                terms_in_post[word] += 1
        
        # Strategy 5: Multi-word technical phrases
        tech_phrases = [
            'artificial intelligence', 'machine learning', 'open source', 'user experience',
            'mental health', 'spiritual practice', 'human consciousness', 'digital mind',
            'for humans', 'API design', 'software development', 'programming language'
        ]
        for phrase in tech_phrases:
            if phrase.lower() in clean_content.lower():
                terms_in_post[phrase] += 2
        
        # Add significant terms to the global index
        for term, count in terms_in_post.items():
            if count >= 1:  # Must appear at least once
                term_occurrences[term].append({
                    'title': post['title'],
                    'url': post['url'],
                    'count': count
                })
    
    # Filter and organize terms
    final_terms = {}
    for term, occurrences in term_occurrences.items():
        # Only include terms that appear in multiple articles OR appear frequently in one
        total_occurrences = sum(occ['count'] for occ in occurrences)
        if len(occurrences) >= 2 or total_occurrences >= 3:
            # Sort articles by term frequency within each article
            occurrences.sort(key=lambda x: x['count'], reverse=True)
            final_terms[term] = {
                'articles': occurrences,
                'total_count': total_occurrences,
                'article_count': len(occurrences)
            }
    
    # Sort terms alphabetically
    sorted_terms = dict(sorted(final_terms.items(), key=lambda x: x[0].lower()))
    
    result = {
        'terms': sorted_terms,
        'total_terms': len(sorted_terms),
        'total_occurrences': sum(term_data['total_count'] for term_data in sorted_terms.values())
    }
    
    # Cache the result
    _terms_cache['data'] = result
    
    return result


def preload_terms():
    """Preload terms cache at startup for faster initial page loads."""
    print("Preloading terms cache...")
    start_time = time.time()
    terms_data = _extract_all_terms_cached()
    load_time = time.time() - start_time
    print(f"Extracted {terms_data['total_terms']} terms with {terms_data['total_occurrences']} total occurrences in {load_time:.2f}s")


def find_related_posts(current_post_path, limit=3):
    """Find related posts based on category and content similarity."""
    posts = collect_all_blog_posts()
    current_post_url = '/' + current_post_path[:-3] if current_post_path.endswith('.md') else '/' + current_post_path

    # Find current post
    current_post = None
    for post in posts:
        if post['url'] == current_post_url:
            current_post = post
            break

    if not current_post:
        return []

    # Score related posts
    related_posts = []
    for post in posts:
        if post['url'] == current_post_url:
            continue  # Skip current post

        score = 0

        # Category match gets high score
        if post['category'] == current_post['category']:
            score += 10

        # Check for common words in titles (simple text similarity)
        current_title_words = set(current_post['title'].lower().split())
        post_title_words = set(post['title'].lower().split())
        common_title_words = current_title_words.intersection(post_title_words)
        score += len(common_title_words) * 2

        # Check for common words in descriptions
        current_desc_words = set(current_post['description'].lower().split()) if current_post['description'] else set()
        post_desc_words = set(post['description'].lower().split()) if post['description'] else set()
        common_desc_words = current_desc_words.intersection(post_desc_words)
        score += len(common_desc_words) * 0.5

        # Prefer more recent posts (slight boost)
        days_diff = abs((current_post['pub_date'] - post['pub_date']).days)
        if days_diff < 365:  # Posts within a year get a small boost
            score += max(0, (365 - days_diff) / 365)

        if score > 0:
            related_posts.append((post, score))

    # Sort by score and return top N
    related_posts.sort(key=lambda x: x[1], reverse=True)
    return [post for post, score in related_posts[:limit]]


def find_adjacent_posts(current_post_path):
    """Find next and previous posts chronologically."""
    posts = collect_all_blog_posts()
    current_post_url = '/' + current_post_path[:-3] if current_post_path.endswith('.md') else '/' + current_post_path

    # Find current post index
    current_index = None
    for i, post in enumerate(posts):
        if post['url'] == current_post_url:
            current_index = i
            break

    if current_index is None:
        return None, None

    # Get previous (newer) and next (older) posts
    prev_post = posts[current_index - 1] if current_index > 0 else None
    next_post = posts[current_index + 1] if current_index < len(posts) - 1 else None

    return prev_post, next_post


def generate_sitemap_data():
    """Generate sitemap data by recursively scanning the data directory."""
    sitemap_items = []

    def scan_directory(path, url_path=""):
        if not path.exists() or not path.is_dir():
            return

        for item in sorted(path.iterdir()):
            if item.name.startswith('.'):
                continue

            item_url_path = f"{url_path}/{item.name}" if url_path else item.name

            if item.is_dir():
                # Add directory to sitemap
                sitemap_items.append({
                    'url': f"/{item_url_path}",
                    'title': item.name.replace('-', ' ').replace('_', ' ').title(),
                    'type': 'directory',
                    'modified': datetime.fromtimestamp(item.stat().st_mtime)
                })
                # Recursively scan subdirectories
                scan_directory(item, item_url_path)
            elif item.suffix == '.md':
                # Remove .md extension for clean URLs
                clean_url_path = item_url_path[:-3] if item_url_path.endswith('.md') else item_url_path

                # Get title from file content
                title = item.stem.replace('-', ' ').replace('_', ' ').title()
                try:
                    content_data = render_markdown_file(item)
                    title = content_data['title']
                except:
                    pass

                sitemap_items.append({
                    'url': f"/{clean_url_path}",
                    'title': title,
                    'type': 'article',
                    'modified': datetime.fromtimestamp(item.stat().st_mtime)
                })

    # Start scanning from data directory
    scan_directory(DATA_DIR)

    # Add static pages
    static_pages = [
        {'url': '/', 'title': 'Kenneth Reitz - Digital Mind Map', 'type': 'homepage'},
        {'url': '/directory', 'title': 'File Explorer', 'type': 'directory'},
        {'url': '/sitemap', 'title': 'Site Map', 'type': 'sitemap'}
    ]

    return static_pages + sitemap_items

@app.route('/sitemap')
def sitemap():
    """Show the site sitemap."""
    sitemap_data = generate_sitemap_data()

    # Group by type
    grouped_sitemap = {
        'homepage': [],
        'directory': [],
        'article': [],
        'sitemap': []
    }

    for item in sitemap_data:
        item_type = item.get('type', 'article')
        if item_type in grouped_sitemap:
            grouped_sitemap[item_type].append(item)

    return render_template('sitemap.html',
                         title='Site Map',
                         sitemap_data=grouped_sitemap,
                         total_items=len(sitemap_data),
                         breadcrumbs=[],
                         current_year=datetime.now().year,
                         current_page='Site Map')

@app.route('/sitemap.xml')
def sitemap_xml():
    """Generate XML sitemap for search engines."""
    sitemap_data = generate_sitemap_data()

    xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

    for item in sitemap_data:
        xml_content += '  <url>\n'
        xml_content += f'    <loc>https://kennethreitz.org{escape(item["url"])}</loc>\n'
        if 'modified' in item:
            xml_content += f'    <lastmod>{item["modified"].strftime("%Y-%m-%d")}</lastmod>\n'
        xml_content += '  </url>\n'

    xml_content += '</urlset>'

    return Response(xml_content, mimetype='application/xml')


@app.route('/feed.xml')
@app.route('/rss.xml')
def rss_feed():
    """Generate RSS feed with full article content."""
    posts = collect_all_blog_posts()  # Use all posts like the archive page

    # Generate RSS XML with full content
    rss_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    rss_content += '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:content="http://purl.org/rss/1.0/modules/content/">\n'
    rss_content += '  <channel>\n'
    rss_content += '    <title>Kenneth Reitz - Essays &amp; AI Writings</title>\n'
    rss_content += '    <description>Complete archive with full articles - Essays, AI consciousness research, and philosophical explorations</description>\n'
    rss_content += '    <link>https://kennethreitz.org</link>\n'
    rss_content += '    <atom:link href="https://kennethreitz.org/feed.xml" rel="self" type="application/rss+xml" />\n'
    rss_content += f'    <lastBuildDate>{datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT")}</lastBuildDate>\n'
    rss_content += '    <language>en-us</language>\n'
    rss_content += '    <managingEditor>me@kennethreitz.org (Kenneth Reitz)</managingEditor>\n'
    rss_content += '    <webMaster>me@kennethreitz.org (Kenneth Reitz)</webMaster>\n'

    for post in posts:
        # Get full content for this post by re-reading the file
        try:
            # Build the file path - post['url'] is like '/essays/2025-09-01-something'
            relative_path = post['url'][1:]  # Remove leading /
            file_path = DATA_DIR / (relative_path + '.md')
            
            if file_path.exists():
                full_content_data = render_markdown_file(file_path)
                full_content = full_content_data['content']
            else:
                # Fallback to stored content (truncated)
                full_content = post.get('content', post['description'])
        except Exception as e:
            # Debug: use description with error info
            full_content = f"{post['description']} <!-- Error loading full content: {str(e)} -->"
        
        rss_content += '    <item>\n'
        rss_content += f'      <title>{escape(post["title"])}</title>\n'
        rss_content += f'      <link>https://kennethreitz.org{post["url"]}</link>\n'
        rss_content += f'      <description>{escape(post["description"])}</description>\n'
        rss_content += f'      <content:encoded><![CDATA[{full_content}]]></content:encoded>\n'
        rss_content += f'      <category>{escape(post["category"])}</category>\n'
        rss_content += f'      <pubDate>{post["pub_date"].strftime("%a, %d %b %Y %H:%M:%S GMT")}</pubDate>\n'
        rss_content += f'      <guid>https://kennethreitz.org{post["url"]}</guid>\n'
        rss_content += '    </item>\n'

    rss_content += '  </channel>\n'
    rss_content += '</rss>'

    return Response(rss_content, mimetype='application/rss+xml')



# Preload caches concurrently for faster startup (works with both direct run and Gunicorn)
import concurrent.futures
import threading

def preload_all_caches():
    """Run all cache preloading functions sequentially to reduce memory usage."""
    print("Starting background cache preloading...")
    
    preload_functions = [
        ("blog posts", preload_blog_posts),
        ("sidenotes", preload_sidenotes), 
        ("outlines", preload_outlines),
        ("quotes", preload_quotes),
        ("connections", preload_connections),
        ("terms", preload_terms)
    ]
    
    for name, func in preload_functions:
        try:
            func()
        except Exception as e:
            print(f"Error preloading {name}: {e}")
            import traceback
            traceback.print_exc()
    
    print("Background cache preloading completed!")

def start_background_preload():
    """Start cache preloading in a background daemon thread."""
    cache_thread = threading.Thread(target=preload_all_caches, daemon=True)
    cache_thread.start()
    print("Cache preloading started in background. App ready to serve requests!")

# Only start background preloading once, not in every Gunicorn worker
# Use a lock file to ensure only one process does the preloading
import os
import fcntl
import atexit

cache_lock_file = None

def should_preload_caches():
    """Check if this process should handle cache preloading."""
    global cache_lock_file
    
    # Skip preloading since we already initialized unified cache
    print("Skipping runtime preload - unified cache already loaded!")
    return False
    
    # Default to preloading (better for reliability and single-container deployments)
    # Only skip if we explicitly can't get the lock
    try:
        # Create a lock file in app directory (more reliable than /tmp in Docker)
        lock_path = '.cache_preload.lock'
        cache_lock_file = open(lock_path, 'w')
        # Try to acquire exclusive lock (non-blocking)
        fcntl.lockf(cache_lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
        # If we got here, we got the lock - we should preload
        
        # Clean up lock on exit
        def cleanup_lock():
            if cache_lock_file:
                cache_lock_file.close()
                try:
                    os.unlink(lock_path)
                except:
                    pass
        atexit.register(cleanup_lock)
        return True
    except (IOError, OSError):
        # Lock is already held by another process - skip preloading
        if cache_lock_file:
            cache_lock_file.close()
        return False

# Initialize unified cache at startup (after all functions are defined)
initialize_unified_cache()

# Start background preloading only in one process (and only if needed)
if should_preload_caches():
    start_background_preload()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
