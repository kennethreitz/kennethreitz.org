import os
import markdown
from flask import Flask, render_template, abort, request, url_for, jsonify
from pathlib import Path
import re
from datetime import datetime
from urllib.parse import quote
import json

app = Flask(__name__, template_folder='templates')

DATA_DIR = Path('data')

def get_directory_structure(path):
    """Get the directory structure for a given path."""
    items = []
    if not path.exists() or not path.is_dir():
        return items
    
    # Separate directories and files for better organization
    dirs = []
    files = []
    
    for item in sorted(path.iterdir()):
        if item.name.startswith('.') or item.name.lower() == 'index.md':
            continue
            
        # Create display name without extension for files
        display_name = item.stem if item.is_file() and item.suffix else item.name
        display_name = display_name.replace('-', ' ').replace('_', ' ').title()
        
        # Create URL path with trailing slash for directories
        url_path = '/' + str(item.relative_to(DATA_DIR))
        if item.is_dir():
            url_path += '/'
        
        item_info = {
            'name': item.name,
            'display_name': display_name,
            'path': str(item.relative_to(DATA_DIR)),
            'url_path': url_path,
            'is_dir': item.is_dir(),
            'is_markdown': item.suffix == '.md',
            'is_image': item.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.webp'],
            'size': item.stat().st_size if item.is_file() else None,
            'modified': datetime.fromtimestamp(item.stat().st_mtime),
            'file_type': item.suffix.lower() if item.is_file() else 'directory'
        }
        
        if item.is_dir():
            dirs.append(item_info)
        else:
            files.append(item_info)
    
    # Return directories first, then files
    return dirs + files

def build_mindmap_data():
    """Build a hierarchical data structure for the mindmap."""
    def process_directory(path, relative_path=""):
        node = {
            'name': path.name if path.name else 'Kenneth Reitz',
            'type': 'directory',
            'path': relative_path,
            'children': []
        }
        
        if not path.exists() or not path.is_dir():
            return node
            
        for item in sorted(path.iterdir()):
            if item.name.startswith('.'):
                continue
                
            item_relative_path = str(item.relative_to(DATA_DIR)) if item != DATA_DIR else ""
            
            if item.is_dir():
                child_node = process_directory(item, item_relative_path)
                node['children'].append(child_node)
            elif item.suffix == '.md':
                # Create display name without extension
                display_name = item.stem.replace('-', ' ').replace('_', ' ').title()
                child_node = {
                    'name': display_name,
                    'type': 'markdown',
                    'path': item_relative_path,
                    'size': item.stat().st_size,
                    'modified': item.stat().st_mtime
                }
                node['children'].append(child_node)
        
        return node
    
    return process_directory(DATA_DIR)

def render_markdown_file(file_path):
    """Render a markdown file to HTML."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Extract first h1 header if it exists
        first_h1 = None
        import re
        # Look for the first H1 at the start of the file or after metadata
        h1_match = re.search(r'(?:^|\n\n)# (.+?)(?:\n|$)', content)
        if h1_match:
            first_h1 = h1_match.group(1).strip()
            # Remove the first h1 from content to avoid duplication
            content = content.replace(h1_match.group(0), '', 1)
        
        # Configure markdown with extensions
        md = markdown.Markdown(extensions=[
            'meta',
            'toc',
            'codehilite',
            'fenced_code',
            'tables',
            'footnotes',
            'smarty',
            'nl2br',
            'sane_lists'
        ])
        
        # Process content to add classes to headers for styling
        html_content = md.convert(content.strip())
        
        # Add classes to headers to prevent conflicts with page headers
        html_content = html_content.replace('<h1>', '<h1 class="content-header">')
        html_content = html_content.replace('<h2>', '<h2 class="content-header">')
        html_content = html_content.replace('<h3>', '<h3 class="content-header">')
        html_content = html_content.replace('<h4>', '<h4 class="content-header">')
        html_content = html_content.replace('<h5>', '<h5 class="content-header">')
        html_content = html_content.replace('<h6>', '<h6 class="content-header">')
        
        # Get metadata
        metadata = getattr(md, 'Meta', {})
        
        # Use the first h1 as title if available, otherwise fallback to metadata or filename
        if first_h1:
            title = first_h1
        else:
            title = metadata.get('title', [file_path.stem.replace('-', ' ').replace('_', ' ').title()])[0]
        
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
    """Homepage showing the root data directory."""
    items = get_directory_structure(DATA_DIR)
    
    # Check for index.md in the root data directory
    index_file = DATA_DIR / 'index.md'
    index_content = None
    if index_file.exists():
        index_content = render_markdown_file(index_file)
    
    return render_template('directory.html', 
                         items=items, 
                         current_path='', 
                         title='Kenneth Reitz',
                         breadcrumbs=[],
                         index_content=index_content,
                         current_year=datetime.now().year)

@app.route('/<path:path>')
def serve_path(path):
    """Serve files and directories from the data folder."""
    full_path = DATA_DIR / path
    
    if not full_path.exists():
        abort(404)
    
    # Generate breadcrumbs
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
        
        # Check for index.md in the directory
        index_file = full_path / 'index.md'
        index_content = None
        if index_file.exists():
            index_content = render_markdown_file(index_file)
        
        title = path_parts[-1].replace('-', ' ').replace('_', ' ').title()
        
        return render_template('directory.html', 
                             items=items, 
                             current_path=path,
                             title=title,
                             breadcrumbs=breadcrumbs,
                             index_content=index_content,
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

@app.route('/api/mindmap')
def api_mindmap():
    """API endpoint to get mindmap data."""
    mindmap_data = build_mindmap_data()
    return jsonify(mindmap_data)

@app.route('/mindmap')
def mindmap():
    """Show the mindmap visualization."""
    return render_template('mindmap.html',
                         title='Mind Map',
                         breadcrumbs=[],
                         current_year=datetime.now().year,
                         current_page='Mind Map')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)