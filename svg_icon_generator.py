import hashlib
import math
import base64
import random
from functools import lru_cache

@lru_cache(maxsize=1000)
def generate_unique_svg_icon(title, size=24):
    """Generate a unique procedural SVG icon based on the title string."""
    # Create hash from title for deterministic randomness
    hash_obj = hashlib.md5(title.encode())
    hash_bytes = hash_obj.digest()
    
    # Use hash to seed random generator for deterministic but varied results
    seed = int.from_bytes(hash_bytes[:4], 'big')
    rng = random.Random(seed)
    
    # Extract color palette from hash - prettier, more vibrant colors
    hue_base = (hash_bytes[0] * 360) // 256
    hue_range = 60 + (hash_bytes[1] % 60)  # 60-120 degree hue range for harmony
    saturation_base = 55 + (hash_bytes[2] % 25)  # 55-80% saturation for vibrancy
    lightness_base = 45 + (hash_bytes[3] % 20)  # 45-65% lightness for good contrast
    
    # Generate 2-3 harmonious colors
    num_colors = 2 + (hash_bytes[4] % 2)
    colors = []
    for i in range(num_colors):
        hue = (hue_base + (i * hue_range // num_colors)) % 360
        sat = saturation_base + rng.randint(-5, 10)
        light = lightness_base + rng.randint(-5, 15)
        colors.append(f"hsl({hue}, {sat}%, {light}%)")
    
    # Generate gradient IDs
    gradient_id = f"grad_{abs(hash(title)) % 10000}"
    gradient_id2 = f"grad2_{abs(hash(title)) % 10000}"
    
    shapes = []
    defs = []
    
    # Create smoother gradient definitions
    gradient_type = rng.choice(['linear', 'radial'])
    if gradient_type == 'linear':
        angle = rng.randint(0, 360)
        x1 = 50 + 50 * math.cos(angle * math.pi / 180)
        y1 = 50 + 50 * math.sin(angle * math.pi / 180)
        x2 = 50 - 50 * math.cos(angle * math.pi / 180)
        y2 = 50 - 50 * math.sin(angle * math.pi / 180)
        gradient_def = f'<linearGradient id="{gradient_id}" x1="{x1:.0f}%" y1="{y1:.0f}%" x2="{x2:.0f}%" y2="{y2:.0f}%">'
    else:
        cx, cy = rng.randint(30, 70), rng.randint(30, 70)
        gradient_def = f'<radialGradient id="{gradient_id}" cx="{cx}%" cy="{cy}%">'
    
    # Smoother color transitions
    for i, color in enumerate(colors):
        offset = (i * 100) // (len(colors) - 1) if len(colors) > 1 else 50
        gradient_def += f'<stop offset="{offset}%" stop-color="{color}"/>'
    
    gradient_def += '</linearGradient>' if gradient_type == 'linear' else '</radialGradient>'
    defs.append(gradient_def)
    
    # Create a secondary gradient for variety
    if rng.random() > 0.5:
        gradient_def2 = f'<linearGradient id="{gradient_id2}" x1="0%" y1="0%" x2="100%" y2="100%">'
        for i, color in enumerate(reversed(colors)):
            offset = (i * 100) // (len(colors) - 1) if len(colors) > 1 else 50
            gradient_def2 += f'<stop offset="{offset}%" stop-color="{color}" stop-opacity="0.8"/>'
        gradient_def2 += '</linearGradient>'
        defs.append(gradient_def2)
    
    # Choose a composition style for better aesthetics
    composition_style = rng.choice(['centered', 'spiral', 'grid', 'organic', 'geometric'])
    
    if composition_style == 'centered':
        # Centered composition with decreasing sizes
        num_shapes = 3 + rng.randint(0, 2)
        for i in range(num_shapes):
            scale = 1 - (i * 0.25)
            opacity = 0.9 - (i * 0.2)
            
            shape_type = rng.choice(['circle', 'rounded_square', 'star'])
            
            if shape_type == 'circle':
                r = (size * 0.4 * scale)
                shapes.append(f'<circle cx="{size//2}" cy="{size//2}" r="{r:.1f}" fill="url(#{gradient_id})" opacity="{opacity:.2f}"/>')
            
            elif shape_type == 'rounded_square':
                s = size * 0.7 * scale
                x = (size - s) / 2
                shapes.append(f'<rect x="{x:.1f}" y="{x:.1f}" width="{s:.1f}" height="{s:.1f}" rx="{s*0.2:.1f}" fill="url(#{gradient_id})" opacity="{opacity:.2f}" transform="rotate({i*15} {size//2} {size//2})"/>')
            
            elif shape_type == 'star':
                points = create_star_points(size//2, size//2, size*0.4*scale, size*0.2*scale, 5 + i)
                shapes.append(f'<polygon points="{points}" fill="url(#{gradient_id})" opacity="{opacity:.2f}"/>')
    
    elif composition_style == 'spiral':
        # Spiral arrangement
        num_elements = 5 + rng.randint(0, 3)
        for i in range(num_elements):
            angle = (i * 360 / num_elements) + (i * 30)
            distance = (size * 0.2) + (i * size * 0.05)
            x = size//2 + distance * math.cos(angle * math.pi / 180)
            y = size//2 + distance * math.sin(angle * math.pi / 180)
            r = size * 0.15 - (i * size * 0.01)
            opacity = 0.8 - (i * 0.08)
            
            fill = f"url(#{gradient_id})" if i % 2 == 0 else colors[i % len(colors)]
            shapes.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{fill}" opacity="{opacity:.2f}"/>')
    
    elif composition_style == 'grid':
        # Clean grid arrangement
        grid_size = 3
        cell_size = size / grid_size
        for i in range(grid_size):
            for j in range(grid_size):
                if rng.random() > 0.3:  # 70% chance to place element
                    x = (i + 0.5) * cell_size
                    y = (j + 0.5) * cell_size
                    
                    shape_type = rng.choice(['circle', 'square'])
                    s = cell_size * 0.6
                    opacity = 0.5 + rng.uniform(0, 0.4)
                    
                    fill = f"url(#{gradient_id})" if (i + j) % 2 == 0 else colors[(i+j) % len(colors)]
                    
                    if shape_type == 'circle':
                        shapes.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{s/2:.1f}" fill="{fill}" opacity="{opacity:.2f}"/>')
                    else:
                        shapes.append(f'<rect x="{x-s/2:.1f}" y="{y-s/2:.1f}" width="{s:.1f}" height="{s:.1f}" rx="{s*0.2:.1f}" fill="{fill}" opacity="{opacity:.2f}"/>')
    
    elif composition_style == 'organic':
        # Organic blob-like shapes
        num_blobs = 3 + rng.randint(0, 2)
        for i in range(num_blobs):
            # Create smooth blob using bezier curves
            cx = size//2 + rng.uniform(-size*0.2, size*0.2)
            cy = size//2 + rng.uniform(-size*0.2, size*0.2)
            
            path_data = create_blob_path(cx, cy, size*0.3, rng)
            opacity = 0.7 - (i * 0.15)
            fill = f"url(#{gradient_id})" if i == 0 else colors[i % len(colors)]
            
            shapes.append(f'<path d="{path_data}" fill="{fill}" opacity="{opacity:.2f}"/>')
    
    else:  # geometric
        # Geometric pattern with triangles or hexagons
        if rng.random() > 0.5:
            # Triangular composition
            for i in range(3):
                rotation = i * 120
                cx, cy = size//2, size//2
                
                # Create equilateral triangle
                height = size * 0.6
                width = height * 0.866
                
                x1 = cx
                y1 = cy - height/2
                x2 = cx - width/2
                y2 = cy + height/4
                x3 = cx + width/2
                y3 = cy + height/4
                
                opacity = 0.7 - (i * 0.2)
                fill = f"url(#{gradient_id})" if i == 0 else colors[i % len(colors)]
                
                shapes.append(f'<polygon points="{x1:.1f},{y1:.1f} {x2:.1f},{y2:.1f} {x3:.1f},{y3:.1f}" fill="{fill}" opacity="{opacity:.2f}" transform="rotate({rotation} {cx} {cy})"/>')
        else:
            # Diamond/rhombus pattern
            for i in range(4):
                angle = i * 90 + 45
                distance = size * 0.25
                x = size//2 + distance * math.cos(angle * math.pi / 180)
                y = size//2 + distance * math.sin(angle * math.pi / 180)
                
                # Create diamond
                d_size = size * 0.3
                diamond = f"{x:.1f},{y-d_size/2:.1f} {x+d_size/2:.1f},{y:.1f} {x:.1f},{y+d_size/2:.1f} {x-d_size/2:.1f},{y:.1f}"
                
                opacity = 0.6 + (i % 2) * 0.2
                fill = f"url(#{gradient_id})" if i % 2 == 0 else colors[i % len(colors)]
                
                shapes.append(f'<polygon points="{diamond}" fill="{fill}" opacity="{opacity:.2f}"/>')
    
    # Add subtle accent dots for visual interest
    if rng.random() > 0.6:
        num_accents = rng.randint(3, 5)
        for _ in range(num_accents):
            x = rng.uniform(size * 0.15, size * 0.85)
            y = rng.uniform(size * 0.15, size * 0.85)
            r = rng.uniform(0.8, 1.5)
            opacity = rng.uniform(0.3, 0.6)
            
            shapes.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{colors[-1]}" opacity="{opacity:.2f}"/>')
    
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

def create_star_points(cx, cy, outer_r, inner_r, num_points):
    """Create points for a star shape."""
    points = []
    for i in range(num_points * 2):
        angle = (i * math.pi) / num_points - math.pi / 2
        r = outer_r if i % 2 == 0 else inner_r
        x = cx + r * math.cos(angle)
        y = cy + r * math.sin(angle)
        points.append(f"{x:.1f},{y:.1f}")
    return " ".join(points)

def create_blob_path(cx, cy, radius, rng):
    """Create a smooth blob shape using bezier curves."""
    num_points = 6
    points = []
    
    # Generate control points around a circle with some randomness
    for i in range(num_points):
        angle = (i * 2 * math.pi) / num_points
        r = radius * rng.uniform(0.7, 1.3)
        x = cx + r * math.cos(angle)
        y = cy + r * math.sin(angle)
        points.append((x, y))
    
    # Create smooth bezier path
    path_data = f"M {points[0][0]:.1f},{points[0][1]:.1f}"
    
    for i in range(num_points):
        next_i = (i + 1) % num_points
        
        # Calculate control points for smooth curves
        cp1x = points[i][0] + (points[next_i][0] - points[i][0]) * 0.5
        cp1y = points[i][1] + (points[next_i][1] - points[i][1]) * 0.2
        
        path_data += f" Q {cp1x:.1f},{cp1y:.1f} {points[next_i][0]:.1f},{points[next_i][1]:.1f}"
    
    path_data += " Z"
    return path_data