import os
import mistune
from flask import Flask, render_template, abort, request, url_for, jsonify, redirect
from pathlib import Path
import re
from datetime import datetime
from urllib.parse import quote
import json
from functools import lru_cache

app = Flask(__name__, template_folder='templates')

# Add custom Jinja2 filters
@app.template_filter('strftime')
def strftime_filter(date, fmt='%Y-%m-%d'):
    """Format a datetime object using strftime."""
    if date is None:
        return ''
    if isinstance(date, str) and date.lower() == 'now':
        date = datetime.now()
    return date.strftime(fmt)

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
            'file_type': item.suffix.lower() if item.is_file() else 'directory',
            'static_path': f"/static/data/{item.relative_to(DATA_DIR)}" if not item.is_dir() else None
        }
        
        if item.is_dir():
            dirs.append(item_info)
        else:
            files.append(item_info)
    
    # Return directories first, then files
    return dirs + files



@lru_cache(maxsize=16)
def render_markdown_file(file_path):
    """Render a markdown file to HTML with caching for performance."""
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
        
        # Configure mistune renderer
        markdown = mistune.create_markdown(
            escape=False,
            plugins=['strikethrough', 'footnotes', 'table', 'task_lists', 'def_list']
        )
        
        # Process content to HTML
        html_content = markdown(content.strip())
        
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
        
        return {
            'content': html_content,
            'title': title,
            'metadata': metadata
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
        
        return render_template('post.html',
                             content=content_data['content'],
                             title=content_data['title'],
                             metadata=content_data['metadata'],
                             breadcrumbs=breadcrumbs,
                             current_path=path,
                             current_year=datetime.now().year,
                             current_page=content_data['title'])
    
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
        xml_content += f'    <loc>https://kennethreitz.org{item["url"]}</loc>\n'
        if 'modified' in item:
            xml_content += f'    <lastmod>{item["modified"].strftime("%Y-%m-%d")}</lastmod>\n'
        xml_content += '  </url>\n'
    
    xml_content += '</urlset>'
    
    from flask import Response
    return Response(xml_content, mimetype='application/xml')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)