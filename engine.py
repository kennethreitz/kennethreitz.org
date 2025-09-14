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

DATA_DIR = Path('data')

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
            'static_path': f"/static/data/{item.relative_to(DATA_DIR)}" if not item.is_dir() else None
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

        return {
            'content': html_content,
            'title': title,
            'metadata': metadata,
            'reading_time': reading_time,
            'word_count': word_count,
            'tags': tags,
            'series_posts': series_posts,
            'series_name': metadata.get('series')
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


@app.route('/search')
def search_page():
    """Search page with interactive search functionality."""
    return render_template('search.html',
                         title='Search',
                         breadcrumbs=[],
                         current_year=datetime.now().year,
                         current_page='Search')


def _extract_all_sidenotes_cached():
    """Cached function to extract all sidenotes with TTL."""
    current_time = time.time()
    
    # Check if cache is valid
    if (_sidenotes_cache['data'] is not None and
        current_time - _sidenotes_cache['timestamp'] < CACHE_TTL):
        return _sidenotes_cache['data']
    
    # Cache miss or expired - rebuild
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
    _sidenotes_cache['timestamp'] = time.time()
    
    return result


@app.route('/sidenotes')
def sidenotes_index():
    """Extract and display all sidenotes from across the site as an index."""
    # Get cached sidenotes data
    sidenotes_data = _extract_all_sidenotes_cached()
    
    return render_template('sidenotes.html',
                         articles=sidenotes_data['articles'],
                         total_count=sidenotes_data['total_count'],
                         title='Sidenotes Index',
                         breadcrumbs=[],
                         current_year=datetime.now().year,
                         current_page='Sidenotes')


def _extract_all_outlines_cached():
    """Cached function to extract all essay outlines with TTL."""
    current_time = time.time()
    
    # Check if cache is valid
    if (_outlines_cache['data'] is not None and
        current_time - _outlines_cache['timestamp'] < CACHE_TTL):
        return _outlines_cache['data']
    
    # Cache miss or expired - rebuild
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
    _outlines_cache['timestamp'] = time.time()
    
    return result


@app.route('/outlines')
def outlines_index():
    """Extract and display all essay outlines from across the site as an index."""
    # Get cached outlines data
    outlines_data = _extract_all_outlines_cached()
    
    return render_template('outlines.html',
                         articles=outlines_data['articles'],
                         total_count=outlines_data['total_count'],
                         title='Outlines Index',
                         breadcrumbs=[],
                         current_year=datetime.now().year,
                         current_page='Outlines')


def _extract_all_quotes_cached():
    """Cached function to extract all blockquotes with TTL."""
    current_time = time.time()
    
    # Check if cache is valid
    if (_quotes_cache['data'] is not None and
        current_time - _quotes_cache['timestamp'] < CACHE_TTL):
        return _quotes_cache['data']
    
    # Cache miss or expired - rebuild
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
    _quotes_cache['timestamp'] = time.time()
    
    return result


@app.route('/quotes')
def quotes_index():
    """Extract and display all blockquotes from across the site as an index."""
    # Get cached quotes data
    quotes_data = _extract_all_quotes_cached()
    
    return render_template('quotes.html',
                         articles=quotes_data['articles'],
                         total_count=quotes_data['total_count'],
                         title='Quotes Index',
                         breadcrumbs=[],
                         current_year=datetime.now().year,
                         current_page='Quotes')


def _extract_all_connections_cached():
    """Cached function to extract all internal cross-references with TTL."""
    current_time = time.time()
    
    # Check if cache is valid
    if (_connections_cache['data'] is not None and
        current_time - _connections_cache['timestamp'] < CACHE_TTL):
        return _connections_cache['data']
    
    # Cache miss or expired - rebuild
    import glob
    from collections import defaultdict
    
    articles_with_connections = defaultdict(list)
    
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
            
            # Extract internal links from the HTML
            # Pattern matches <a href="/internal/path">link text</a>
            link_pattern = r'<a[^>]*href="(/[^"]*)"[^>]*>(.*?)</a>'
            links = re.findall(link_pattern, html_content, re.DOTALL)
            
            if links:
                # Create URL for this file
                relative_path = str(full_path.relative_to(DATA_DIR))
                source_url = '/' + relative_path[:-3]  # Remove .md extension
                
                # Extract date for sorting
                pub_date = extract_intelligent_date(full_path, content_data)
                
                # Collect connections for this article
                article_connections = []
                
                # Filter for internal links only (skip external URLs and fragments)
                for link_url, link_text in links:
                    if (link_url.startswith('/') and 
                        not link_url.startswith('//') and 
                        not link_url.startswith('/static') and
                        link_url != source_url):  # Don't include self-references
                        
                        # Clean up link text
                        link_text = re.sub(r'<[^>]*>', '', link_text)
                        link_text = re.sub(r'\s+', ' ', link_text).strip()
                        
                        article_connections.append({
                            'target_url': link_url,
                            'link_text': link_text
                        })
                
                if article_connections:
                    articles_with_connections[content_data['title']].append({
                        'connections': article_connections,
                        'url': source_url,
                        'date': pub_date,
                        'category': full_path.parent.name.replace('-', ' ').title()
                    })
        except Exception as e:
            # Skip files that can't be processed
            continue
    
    # Convert to list and sort by date (most recent first)
    articles_list = []
    for title, article_data in articles_with_connections.items():
        # Should only be one entry per article
        data = article_data[0]
        articles_list.append({
            'title': title,
            'url': data['url'],
            'date': data['date'],
            'category': data['category'],
            'connections': data['connections']
        })
    
    articles_list.sort(key=lambda x: x['date'] if x['date'] else datetime(1900, 1, 1), reverse=True)
    
    # Count total connections
    total_count = sum(len(article['connections']) for article in articles_list)
    
    # Update cache
    result = {
        'articles': articles_list,
        'total_count': total_count
    }
    _connections_cache['data'] = result
    _connections_cache['timestamp'] = time.time()
    
    return result


@app.route('/connections')
def connections_index():
    """Extract and display all cross-references between essays."""
    # Get cached connections data
    connections_data = _extract_all_connections_cached()
    
    return render_template('connections.html',
                         articles=connections_data['articles'],
                         total_count=connections_data['total_count'],
                         title='Connections Index',
                         breadcrumbs=[],
                         current_year=datetime.now().year,
                         current_page='Connections')


@app.route('/graph/data')
def graph_data():
    """API endpoint that returns graph data for network visualization."""
    connections_data = _extract_all_connections_cached()
    
    nodes = []
    edges = []
    node_ids = set()
    
    # Create nodes and edges from connections
    for article in connections_data['articles']:
        source_id = article['url']
        node_ids.add(source_id)
        
        for connection in article['connections']:
            target_id = connection['target_url']
            node_ids.add(target_id)
            
            edges.append({
                'source': source_id,
                'target': target_id,
                'link_text': connection['link_text']
            })
    
    # Create node objects with titles
    posts = _collect_all_blog_posts_cached()
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


@app.route('/external-links')
def external_links_index():
    """Extract and display all external links from essays."""
    # Get cached external links data
    links_data = _extract_all_external_links_cached()
    
    return render_template('external_links.html',
                         articles=links_data['articles'],
                         total_count=links_data['total_count'],
                         domain_stats=links_data['domain_stats'],
                         title='External Links Index',
                         breadcrumbs=[],
                         current_year=datetime.now().year,
                         current_page='External Links')


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
    posts = collect_all_blog_posts()

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
    posts = collect_all_blog_posts()

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
    posts = collect_all_blog_posts()

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
                             current_page='Themes')
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

        title = path_parts[-1].replace('-', ' ').replace('_', ' ').title()

        return render_template('directory.html',
                             items=items,
                             current_path=original_path,
                             title=title,
                             breadcrumbs=breadcrumbs,
                             index_content=index_content,
                             content_position=content_position,
                             is_image_gallery=is_image_gallery,
                             image_items=image_items,
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
                             series_name=content_data.get('series_name'))

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
                result = {
                    'name': item.name,
                    'type': 'directory' if item.is_dir() else ('article' if item.suffix == '.md' else 'file'),
                    'path': relative_path,
                    'display_path': item_display_path,
                    'relevance': 0,
                }

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
CACHE_TTL = 36000  # 10 hours cache

# Force cache invalidation for filename change
import time
_force_cache_clear = time.time()

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
    """Run all cache preloading functions concurrently."""
    print("Starting background cache preloading...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        futures = [
            executor.submit(preload_blog_posts),
            executor.submit(preload_sidenotes),
            executor.submit(preload_outlines),
            executor.submit(preload_quotes),
            executor.submit(preload_connections),
            executor.submit(preload_external_links)
        ]
        # Wait for all to complete
        concurrent.futures.wait(futures)
    print("Background cache preloading completed!")

def start_background_preload():
    """Start cache preloading in a background daemon thread."""
    cache_thread = threading.Thread(target=preload_all_caches, daemon=True)
    cache_thread.start()
    print("Cache preloading started in background. App ready to serve requests!")

# Start background preloading - app can serve requests immediately
start_background_preload()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
