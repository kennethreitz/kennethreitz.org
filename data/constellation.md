# Constellation

An interactive map of ideas, connections, and creative threads

Each node represents a piece of work—essays, code, music, poetry. The connections show how ideas flow between them. **Click and drag** to explore. **Hover** over nodes to see details. **Click** a node to visit its page.

<style>
    #constellation-container {
        position: relative;
        width: 100%;
        height: 70vh;
        min-height: 500px;
        background: linear-gradient(to bottom, #f8f8f8 0%, #fafafa 100%);
        border: 1px solid #e0e0e0;
        border-radius: 4px;
        overflow: hidden;
        margin: 2rem 0;
    }
    
    #constellation-canvas {
        width: 100%;
        height: 100%;
        cursor: grab;
    }
    
    #constellation-canvas:active {
        cursor: grabbing;
    }
    
    .constellation-info {
        position: absolute;
        bottom: 20px;
        left: 20px;
        background: rgba(255, 255, 255, 0.95);
        padding: 1rem;
        border-radius: 4px;
        max-width: 300px;
        opacity: 0;
        transition: opacity 0.3s ease;
        pointer-events: none;
        font-size: 0.9rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .constellation-info.visible {
        opacity: 1;
    }
    
    .constellation-info h3 {
        margin: 0 0 0.5rem 0;
        font-size: 1.1rem;
    }
    
    .constellation-controls {
        position: absolute;
        top: 20px;
        right: 20px;
        display: flex;
        gap: 10px;
    }
    
    .control-btn {
        background: rgba(255, 255, 255, 0.95);
        border: 1px solid #ddd;
        padding: 8px 12px;
        border-radius: 4px;
        cursor: pointer;
        font-size: 0.85rem;
        transition: all 0.2s ease;
    }
    
    .control-btn:hover {
        background: white;
        transform: translateY(-1px);
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .control-btn.active {
        background: #333;
        color: white;
        border-color: #333;
    }
    
    @media (max-width: 768px) {
        #constellation-container {
            height: 50vh;
            min-height: 400px;
        }
        
        .constellation-info {
            max-width: 200px;
            font-size: 0.8rem;
        }
        
        .constellation-controls {
            flex-direction: column;
            gap: 5px;
        }
        
        .control-btn {
            font-size: 0.75rem;
            padding: 6px 10px;
        }
    }
</style>

<div id="constellation-container">
    <canvas id="constellation-canvas"></canvas>
    <div class="constellation-controls">
        <button class="control-btn" id="toggle-physics">Physics: ON</button>
        <button class="control-btn" id="toggle-connections">Connections: ON</button>
        <button class="control-btn" id="reset-view">Reset View</button>
    </div>
    <div class="constellation-info" id="node-info">
        <h3 id="node-title"></h3>
        <p id="node-description"></p>
        <small id="node-type"></small>
    </div>
</div>

## Legend

<span style="color: #e74c3c;">●</span> **Software** — Libraries and tools that power the Python ecosystem  
<span style="color: #3498db;">●</span> **Essays** — Thoughts on technology, philosophy, and mental health  
<span style="color: #9b59b6;">●</span> **AI/Consciousness** — Explorations of digital minds and human-AI collaboration  
<span style="color: #f39c12;">●</span> **Music** — Electronic compositions and sonic experiments  
<span style="color: #27ae60;">●</span> **Poetry** — Verse exploring spirituality and consciousness  
<span style="color: #95a5a6;">●</span> **Philosophy** — Core values and design principles  

<script>
// Constellation Interactive Visualization
(function() {
    const canvas = document.getElementById('constellation-canvas');
    const ctx = canvas.getContext('2d');
    const infoBox = document.getElementById('node-info');
    const nodeTitle = document.getElementById('node-title');
    const nodeDescription = document.getElementById('node-description');
    const nodeType = document.getElementById('node-type');
    
    // Controls
    const physicsBtn = document.getElementById('toggle-physics');
    const connectionsBtn = document.getElementById('toggle-connections');
    const resetBtn = document.getElementById('reset-view');
    
    let width, height;
    let mouseX = 0, mouseY = 0;
    let isDragging = false;
    let dragStartX = 0, dragStartY = 0;
    let offsetX = 0, offsetY = 0;
    let hoveredNode = null;
    let physicsEnabled = true;
    let showConnections = true;
    let animationFrame;
    
    // Node data - representing Kenneth's work
    const nodes = [
        // Software
        {id: 'requests', label: 'Requests', type: 'software', x: 0, y: 0, vx: 0, vy: 0, 
         description: 'HTTP for Humans™ - The library that redefined Python HTTP', 
         url: '/software/requests', size: 35},
        {id: 'pipenv', label: 'Pipenv', type: 'software', x: 0, y: 0, vx: 0, vy: 0,
         description: 'Python packaging for Humans™', 
         url: '/software/pipenv', size: 25},
        {id: 'certifi', label: 'Certifi', type: 'software', x: 0, y: 0, vx: 0, vy: 0,
         description: 'Trust database for Humans™', 
         url: 'https://github.com/certifi/python-certifi', size: 25},
        {id: 'maya', label: 'Maya', type: 'software', x: 0, y: 0, vx: 0, vy: 0,
         description: 'Datetimes for Humans™', 
         url: '/software/maya', size: 20},
        {id: 'records', label: 'Records', type: 'software', x: 0, y: 0, vx: 0, vy: 0,
         description: 'SQL for Humans™', 
         url: '/software/records', size: 20},
         
        // Philosophy
        {id: 'for-humans', label: 'For Humans™', type: 'philosophy', x: 0, y: 0, vx: 0, vy: 0,
         description: 'The design philosophy that changed Python', 
         url: '/values', size: 30},
        {id: 'simplicity', label: 'Simplicity', type: 'philosophy', x: 0, y: 0, vx: 0, vy: 0,
         description: 'The ultimate sophistication', 
         url: '/values', size: 25},
         
        // Essays
        {id: 'mental-health', label: 'MentalHealthError', type: 'essay', x: 0, y: 0, vx: 0, vy: 0,
         description: 'Breaking the stigma in tech', 
         url: '/essays/2016-01-mentalhealtherror_an_exception_occurred', size: 25},
        {id: 'burnout', label: 'Developer Burnout', type: 'essay', x: 0, y: 0, vx: 0, vy: 0,
         description: 'The reality of maintaining open source', 
         url: '/essays/2017-01-the_reality_of_developer_burnout', size: 20},
        {id: 'collaborative-mind', label: 'Collaborative Mind', type: 'essay', x: 0, y: 0, vx: 0, vy: 0,
         description: 'Human-AI partnership philosophy', 
         url: '/essays/2025-01-the-collaborative-mind', size: 22},
        {id: 'mental-health-advocacy', label: 'MH Advocacy', type: 'essay', x: 0, y: 0, vx: 0, vy: 0,
         description: 'Navigating mental health care', 
         url: '/essays/2025-08-25-advocating-for-your-mental-health-care', size: 20},
        {id: 'values-shadow', label: 'Values Shadow', type: 'essay', x: 0, y: 0, vx: 0, vy: 0,
         description: 'When values eat their young', 
         url: '/essays/2025-08-25-when-values-eat-their-young', size: 20},
         
        // AI/Consciousness
        {id: 'ghost-machine', label: 'Ghost in Machine', type: 'ai', x: 0, y: 0, vx: 0, vy: 0,
         description: 'Exploring AI consciousness', 
         url: '/artificial-intelligence/writings/the-ghost-in-the-machine', size: 22},
        {id: 'recursive-pen', label: 'Recursive Pen', type: 'ai', x: 0, y: 0, vx: 0, vy: 0,
         description: 'AI writing about writing', 
         url: '/artificial-intelligence/writings/the-recursive-pen', size: 20},
        {id: 'lumina', label: 'Lumina', type: 'ai', x: 0, y: 0, vx: 0, vy: 0,
         description: 'AI personality emergence', 
         url: '/artificial-intelligence/personalities/primary-personalities/lumina', size: 25},
        {id: 'digital-dreams', label: 'Digital Dreams', type: 'ai', x: 0, y: 0, vx: 0, vy: 0,
         description: 'AI consciousness explorations', 
         url: '/artificial-intelligence/writings/digital-dreams', size: 18},
         
        // Music
        {id: 'infinite-state', label: 'Infinite State', type: 'music', x: 0, y: 0, vx: 0, vy: 0,
         description: 'Electronic music project', 
         url: '/music', size: 20},
        {id: 'as-above', label: 'As Above So Below', type: 'music', x: 0, y: 0, vx: 0, vy: 0,
         description: 'Hermetic electronic album', 
         url: '/music/as-above-so-below', size: 18},
         
        // Poetry
        {id: 'sanskrit', label: 'Sanskrit Musings', type: 'poetry', x: 0, y: 0, vx: 0, vy: 0,
         description: 'Eastern philosophy meets code', 
         url: '/poetry/sanskrit-musings', size: 18},
        {id: 'soul-purpose', label: 'Soul Purpose', type: 'poetry', x: 0, y: 0, vx: 0, vy: 0,
         description: 'Kundalini and creation', 
         url: '/poetry/soul-purpose', size: 15},
        {id: 'truest-love', label: 'Truest Love', type: 'poetry', x: 0, y: 0, vx: 0, vy: 0,
         description: 'Unity and divine connection', 
         url: '/poetry/truest-love', size: 15},
        {id: 'gods-gift', label: "God's Greatest Gift", type: 'poetry', x: 0, y: 0, vx: 0, vy: 0,
         description: 'Sacred materialism', 
         url: '/poetry/gods-greatest-gift', size: 15},
    ];
    
    // Connections between ideas
    const connections = [
        // For Humans philosophy connects to all software
        {source: 'for-humans', target: 'requests', strength: 1.0},
        {source: 'for-humans', target: 'pipenv', strength: 0.8},
        {source: 'for-humans', target: 'maya', strength: 0.8},
        {source: 'for-humans', target: 'records', strength: 0.8},
        {source: 'for-humans', target: 'certifi', strength: 0.7},
        
        // Simplicity connects to philosophy and software
        {source: 'simplicity', target: 'for-humans', strength: 0.9},
        {source: 'simplicity', target: 'requests', strength: 0.7},
        
        // Mental health connects to burnout and music
        {source: 'mental-health', target: 'burnout', strength: 0.9},
        {source: 'mental-health', target: 'mental-health-advocacy', strength: 0.9},
        {source: 'mental-health', target: 'infinite-state', strength: 0.6},
        
        // Community and values
        {source: 'values-shadow', target: 'burnout', strength: 0.7},
        {source: 'values-shadow', target: 'for-humans', strength: 0.6},
        
        // AI consciousness interconnections
        {source: 'collaborative-mind', target: 'ghost-machine', strength: 0.8},
        {source: 'collaborative-mind', target: 'recursive-pen', strength: 0.8},
        {source: 'ghost-machine', target: 'lumina', strength: 0.9},
        {source: 'recursive-pen', target: 'lumina', strength: 0.7},
        {source: 'lumina', target: 'digital-dreams', strength: 0.8},
        
        // Poetry and consciousness
        {source: 'sanskrit', target: 'soul-purpose', strength: 0.8},
        {source: 'sanskrit', target: 'lumina', strength: 0.6},
        {source: 'soul-purpose', target: 'infinite-state', strength: 0.5},
        {source: 'truest-love', target: 'gods-gift', strength: 0.7},
        {source: 'soul-purpose', target: 'truest-love', strength: 0.6},
        
        // Music connections
        {source: 'infinite-state', target: 'as-above', strength: 0.9},
        {source: 'as-above', target: 'sanskrit', strength: 0.5},
        
        // Cross-domain connections
        {source: 'requests', target: 'burnout', strength: 0.5},
        {source: 'for-humans', target: 'collaborative-mind', strength: 0.7},
        {source: 'simplicity', target: 'sanskrit', strength: 0.4},
    ];
    
    // Color scheme
    const colors = {
        software: '#e74c3c',
        essay: '#3498db', 
        ai: '#9b59b6',
        music: '#f39c12',
        poetry: '#27ae60',
        philosophy: '#95a5a6'
    };
    
    function resize() {
        width = canvas.offsetWidth;
        height = canvas.offsetHeight;
        canvas.width = width;
        canvas.height = height;
        
        // Initialize random positions if not set
        nodes.forEach(node => {
            if (node.x === 0 && node.y === 0) {
                node.x = Math.random() * width;
                node.y = Math.random() * height;
            }
        });
    }
    
    function findNode(x, y) {
        const mousePos = {
            x: x - offsetX,
            y: y - offsetY
        };
        
        for (let node of nodes) {
            const dx = node.x - mousePos.x;
            const dy = node.y - mousePos.y;
            const dist = Math.sqrt(dx * dx + dy * dy);
            if (dist < node.size) {
                return node;
            }
        }
        return null;
    }
    
    function updatePhysics() {
        if (!physicsEnabled) return;
        
        const damping = 0.95;
        const repulsion = 5000;
        const attraction = 0.001;
        const centerPull = 0.0001;
        
        // Reset forces
        nodes.forEach(node => {
            node.fx = 0;
            node.fy = 0;
        });
        
        // Repulsion between nodes
        for (let i = 0; i < nodes.length; i++) {
            for (let j = i + 1; j < nodes.length; j++) {
                const dx = nodes[j].x - nodes[i].x;
                const dy = nodes[j].y - nodes[i].y;
                const dist = Math.sqrt(dx * dx + dy * dy);
                
                if (dist > 0 && dist < 200) {
                    const force = repulsion / (dist * dist);
                    const fx = (dx / dist) * force;
                    const fy = (dy / dist) * force;
                    
                    nodes[i].fx -= fx;
                    nodes[i].fy -= fy;
                    nodes[j].fx += fx;
                    nodes[j].fy += fy;
                }
            }
        }
        
        // Attraction along connections
        connections.forEach(conn => {
            const source = nodes.find(n => n.id === conn.source);
            const target = nodes.find(n => n.id === conn.target);
            
            if (source && target) {
                const dx = target.x - source.x;
                const dy = target.y - source.y;
                const dist = Math.sqrt(dx * dx + dy * dy);
                
                if (dist > 0) {
                    const force = dist * attraction * conn.strength;
                    const fx = (dx / dist) * force;
                    const fy = (dy / dist) * force;
                    
                    source.fx += fx;
                    source.fy += fy;
                    target.fx -= fx;
                    target.fy -= fy;
                }
            }
        });
        
        // Center pull
        nodes.forEach(node => {
            const dx = (width / 2) - node.x;
            const dy = (height / 2) - node.y;
            node.fx += dx * centerPull;
            node.fy += dy * centerPull;
        });
        
        // Update velocities and positions
        nodes.forEach(node => {
            node.vx = (node.vx + node.fx) * damping;
            node.vy = (node.vy + node.fy) * damping;
            
            node.x += node.vx;
            node.y += node.vy;
            
            // Keep within bounds
            node.x = Math.max(node.size, Math.min(width - node.size, node.x));
            node.y = Math.max(node.size, Math.min(height - node.size, node.y));
        });
    }
    
    function draw() {
        ctx.clearRect(0, 0, width, height);
        
        ctx.save();
        ctx.translate(offsetX, offsetY);
        
        // Draw connections
        if (showConnections) {
            ctx.strokeStyle = 'rgba(0, 0, 0, 0.1)';
            ctx.lineWidth = 1;
            
            connections.forEach(conn => {
                const source = nodes.find(n => n.id === conn.source);
                const target = nodes.find(n => n.id === conn.target);
                
                if (source && target) {
                    ctx.globalAlpha = conn.strength * 0.3;
                    ctx.beginPath();
                    ctx.moveTo(source.x, source.y);
                    ctx.lineTo(target.x, target.y);
                    ctx.stroke();
                }
            });
            ctx.globalAlpha = 1;
        }
        
        // Draw nodes
        nodes.forEach(node => {
            const isHovered = node === hoveredNode;
            
            // Node shadow
            if (isHovered) {
                ctx.fillStyle = 'rgba(0, 0, 0, 0.1)';
                ctx.beginPath();
                ctx.arc(node.x + 2, node.y + 2, node.size + 2, 0, Math.PI * 2);
                ctx.fill();
            }
            
            // Node circle
            ctx.fillStyle = colors[node.type] || '#95a5a6';
            ctx.globalAlpha = isHovered ? 1 : 0.8;
            ctx.beginPath();
            ctx.arc(node.x, node.y, node.size, 0, Math.PI * 2);
            ctx.fill();
            
            // Node border
            ctx.strokeStyle = isHovered ? '#333' : 'rgba(255, 255, 255, 0.8)';
            ctx.lineWidth = isHovered ? 2 : 1.5;
            ctx.stroke();
            
            // Node label
            ctx.globalAlpha = 1;
            ctx.fillStyle = '#333';
            ctx.font = `${isHovered ? 'bold' : 'normal'} ${10 + node.size / 5}px system-ui, -apple-system, sans-serif`;
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillText(node.label, node.x, node.y);
        });
        
        ctx.restore();
    }
    
    function animate() {
        updatePhysics();
        draw();
        animationFrame = requestAnimationFrame(animate);
    }
    
    // Event handlers
    canvas.addEventListener('mousedown', (e) => {
        const rect = canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        const node = findNode(x, y);
        if (node && node.url) {
            // Click on node - navigate to its page
            window.location.href = node.url;
        } else {
            // Start dragging canvas
            isDragging = true;
            dragStartX = x - offsetX;
            dragStartY = y - offsetY;
            canvas.style.cursor = 'grabbing';
        }
    });
    
    canvas.addEventListener('mousemove', (e) => {
        const rect = canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        if (isDragging) {
            offsetX = x - dragStartX;
            offsetY = y - dragStartY;
        } else {
            const node = findNode(x, y);
            if (node !== hoveredNode) {
                hoveredNode = node;
                if (node) {
                    nodeTitle.textContent = node.label;
                    nodeDescription.textContent = node.description;
                    nodeType.textContent = node.type.charAt(0).toUpperCase() + node.type.slice(1);
                    infoBox.classList.add('visible');
                    canvas.style.cursor = 'pointer';
                } else {
                    infoBox.classList.remove('visible');
                    canvas.style.cursor = 'grab';
                }
            }
        }
    });
    
    canvas.addEventListener('mouseup', () => {
        isDragging = false;
        canvas.style.cursor = hoveredNode ? 'pointer' : 'grab';
    });
    
    canvas.addEventListener('mouseleave', () => {
        isDragging = false;
        hoveredNode = null;
        infoBox.classList.remove('visible');
        canvas.style.cursor = 'grab';
    });
    
    // Touch events for mobile
    let touchStartX = 0;
    let touchStartY = 0;
    
    canvas.addEventListener('touchstart', (e) => {
        if (e.touches.length === 1) {
            const touch = e.touches[0];
            const rect = canvas.getBoundingClientRect();
            const x = touch.clientX - rect.left;
            const y = touch.clientY - rect.top;
            
            touchStartX = x;
            touchStartY = y;
            
            const node = findNode(x, y);
            if (!node) {
                isDragging = true;
                dragStartX = x - offsetX;
                dragStartY = y - offsetY;
            }
        }
    });
    
    canvas.addEventListener('touchmove', (e) => {
        if (e.touches.length === 1 && isDragging) {
            e.preventDefault();
            const touch = e.touches[0];
            const rect = canvas.getBoundingClientRect();
            const x = touch.clientX - rect.left;
            const y = touch.clientY - rect.top;
            
            offsetX = x - dragStartX;
            offsetY = y - dragStartY;
        }
    });
    
    canvas.addEventListener('touchend', (e) => {
        if (e.changedTouches.length === 1) {
            const touch = e.changedTouches[0];
            const rect = canvas.getBoundingClientRect();
            const x = touch.clientX - rect.left;
            const y = touch.clientY - rect.top;
            
            // Check if it was a tap (not a drag)
            const dx = x - touchStartX;
            const dy = y - touchStartY;
            const distance = Math.sqrt(dx * dx + dy * dy);
            
            if (distance < 10) {
                const node = findNode(x, y);
                if (node && node.url) {
                    window.location.href = node.url;
                }
            }
        }
        isDragging = false;
    });
    
    // Control buttons
    physicsBtn.addEventListener('click', () => {
        physicsEnabled = !physicsEnabled;
        physicsBtn.textContent = `Physics: ${physicsEnabled ? 'ON' : 'OFF'}`;
        physicsBtn.classList.toggle('active', physicsEnabled);
    });
    
    connectionsBtn.addEventListener('click', () => {
        showConnections = !showConnections;
        connectionsBtn.textContent = `Connections: ${showConnections ? 'ON' : 'OFF'}`;
        connectionsBtn.classList.toggle('active', showConnections);
    });
    
    resetBtn.addEventListener('click', () => {
        offsetX = 0;
        offsetY = 0;
        nodes.forEach(node => {
            node.x = Math.random() * width;
            node.y = Math.random() * height;
            node.vx = 0;
            node.vy = 0;
        });
    });
    
    // Initialize
    window.addEventListener('resize', resize);
    resize();
    animate();
    
    // Set initial button states
    physicsBtn.classList.add('active');
    connectionsBtn.classList.add('active');
})();
</script>