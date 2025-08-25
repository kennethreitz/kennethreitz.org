# Knowledge Graph

A comprehensive map of ideas, connections, and thematic relationships across the site

This interactive knowledge graph reveals the deep interconnections between all the work on this site—from the technical foundations of software libraries to the philosophical explorations of consciousness, mental health advocacy, and creative expression.

<style>
    #graph-container {
        position: relative;
        width: 100%;
        height: 80vh;
        min-height: 600px;
        background: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 4px;
        overflow: hidden;
        margin: 2rem 0;
    }
    
    #graph-canvas {
        width: 100%;
        height: 100%;
        cursor: grab;
    }
    
    #graph-canvas:active {
        cursor: grabbing;
    }
    
    .graph-info {
        position: absolute;
        bottom: 20px;
        left: 20px;
        background: rgba(255, 255, 255, 0.95);
        padding: 1rem;
        border-radius: 4px;
        max-width: 350px;
        opacity: 0;
        transition: opacity 0.3s ease;
        pointer-events: none;
        font-size: 0.85rem;
        border: 1px solid #ddd;
        color: #333;
        border-left: 4px solid #e74c3c;
    }
    
    .graph-info.visible {
        opacity: 1;
    }
    
    .graph-info h3 {
        margin: 0 0 0.5rem 0;
        font-size: 1rem;
        color: #333;
    }
    
    .graph-info .node-tags {
        margin-top: 0.5rem;
        font-size: 0.75rem;
        color: #666;
    }
    
    .graph-controls {
        position: absolute;
        top: 20px;
        right: 20px;
        display: flex;
        flex-direction: column;
        gap: 8px;
    }
    
    .control-btn {
        background: rgba(255, 255, 255, 0.9);
        border: 1px solid #ddd;
        padding: 8px 12px;
        border-radius: 4px;
        cursor: pointer;
        font-size: 0.8rem;
        transition: all 0.2s ease;
        white-space: nowrap;
        color: #333;
    }
    
    .control-btn:hover {
        background: rgba(245, 245, 245, 0.95);
        border-color: #bbb;
    }
    
    .control-btn.active {
        background: #007acc;
        color: white;
        border-color: #007acc;
    }
    
    .filter-section {
        margin-top: 10px;
        padding-top: 10px;
        border-top: 1px solid #eee;
    }
    
    .filter-title {
        font-size: 0.7rem;
        color: #666;
        margin-bottom: 5px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    @media (max-width: 768px) {
        #graph-container {
            height: 60vh;
            min-height: 500px;
        }
        
        .graph-info {
            max-width: 250px;
            font-size: 0.75rem;
        }
        
        .graph-controls {
            flex-direction: row;
            flex-wrap: wrap;
            gap: 5px;
        }
        
        .control-btn {
            font-size: 0.7rem;
            padding: 6px 8px;
        }
    }
</style>

<div id="graph-container">
    <canvas id="graph-canvas"></canvas>
    <div class="graph-controls">
        <button class="control-btn" id="toggle-physics">Physics: ON</button>
        <button class="control-btn" id="toggle-connections">Connections: ON</button>
        <button class="control-btn" id="reset-view">Reset View</button>
        <div class="filter-section">
            <div class="filter-title">Filters</div>
            <button class="control-btn active" id="filter-all">All</button>
            <button class="control-btn" id="filter-software">Software</button>
            <button class="control-btn" id="filter-philosophy">Philosophy</button>
            <button class="control-btn" id="filter-consciousness">Consciousness</button>
        </div>
    </div>
    <div class="graph-info" id="node-info">
        <h3 id="node-title"></h3>
        <p id="node-description"></p>
        <div class="node-tags" id="node-tags"></div>
    </div>
</div>

## How to Explore

- **Pan** - Click and drag to move around the graph
- **Zoom** - Use filters to focus on specific themes
- **Inspect** - Hover over nodes to see details
- **Navigate** - Click nodes to visit pages
- **Discover** - Follow the connection lines to trace how ideas flow

## Key Insights

The knowledge graph reveals several fascinating patterns:

### 🎯 **Central Hub: "For Humans" Philosophy**
Your "For Humans" design philosophy sits at the center of the graph, directly connected to every major software project and indirectly influencing your AI consciousness work and mental health advocacy.

### 🌊 **Three Major Streams**
1. **Technical Excellence** - Requests → Pipenv → Maya → Records
2. **Human Experience** - Mental Health → Burnout → Community Values
3. **Consciousness Exploration** - AI Personalities → Collaborative Mind → Poetry

### 🔗 **Cross-Pollination Zones**
- **Code & Consciousness** - Where programming meets spiritual exploration
- **Tools & Therapy** - How software philosophy connects to mental health advocacy  
- **Simplicity & Spirituality** - The aesthetic principles that span both domains

### 📈 **Evolution Timeline**
Early work (2008-2012) focused on developer experience, middle period (2013-2020) emphasized community and mental health, recent work (2021-2025) explores AI consciousness and human-machine collaboration.

<script>
// Knowledge Graph Visualization
(function() {
    const canvas = document.getElementById('graph-canvas');
    const ctx = canvas.getContext('2d');
    const infoBox = document.getElementById('node-info');
    const nodeTitle = document.getElementById('node-title');
    const nodeDescription = document.getElementById('node-description');
    const nodeTags = document.getElementById('node-tags');
    
    // Controls
    const physicsBtn = document.getElementById('toggle-physics');
    const connectionsBtn = document.getElementById('toggle-connections');
    const resetBtn = document.getElementById('reset-view');
    const filterAll = document.getElementById('filter-all');
    const filterSoftware = document.getElementById('filter-software');
    const filterPhilosophy = document.getElementById('filter-philosophy');
    const filterConsciousness = document.getElementById('filter-consciousness');
    
    let width, height;
    let isDragging = false;
    let dragStartX = 0, dragStartY = 0;
    let offsetX = 0, offsetY = 0;
    let hoveredNode = null;
    let physicsEnabled = true;
    let showConnections = true;
    let currentFilter = 'all';
    let animationFrame;
    
    // Comprehensive site knowledge graph data
    const nodes = [
        // Core Philosophy (Central Hub)
        {id: 'for-humans', label: 'For Humans™', type: 'philosophy', category: 'philosophy', x: 0, y: 0, vx: 0, vy: 0, 
         description: 'The design philosophy that changed Python - prioritizing human experience over technical complexity', 
         url: '/values', size: 45, tags: ['Design Philosophy', 'Python', 'API Design'], importance: 10},
        {id: 'simplicity', label: 'Simplicity', type: 'philosophy', category: 'philosophy', x: 0, y: 0, vx: 0, vy: 0,
         description: 'The ultimate sophistication - Leonardo da Vinci\'s principle applied to software', 
         url: '/values', size: 35, tags: ['Design', 'Aesthetics', 'Philosophy'], importance: 9},
        {id: 'values', label: 'Core Values', type: 'philosophy', category: 'philosophy', x: 0, y: 0, vx: 0, vy: 0,
         description: 'Personal values that guide everything: trust and verify, communicate intent, be cordial', 
         url: '/values', size: 30, tags: ['Personal', 'Ethics', 'Community'], importance: 8},
         
        // Software Libraries (Major)
        {id: 'requests', label: 'Requests', type: 'software', category: 'software', x: 0, y: 0, vx: 0, vy: 0, 
         description: 'HTTP for Humans™ - 25M+ daily downloads, redefined Python HTTP', 
         url: '/software/requests', size: 50, tags: ['HTTP', 'Python', 'Open Source'], importance: 10},
        {id: 'pipenv', label: 'Pipenv', type: 'software', category: 'software', x: 0, y: 0, vx: 0, vy: 0,
         description: 'Python packaging for Humans™ - modern dependency management', 
         url: '/software/pipenv', size: 35, tags: ['Packaging', 'Dependencies', 'Workflow'], importance: 8},
        {id: 'certifi', label: 'Certifi', type: 'software', category: 'software', x: 0, y: 0, vx: 0, vy: 0,
         description: 'Trust database for Humans™ - 20M+ daily downloads, SSL certificate bundle', 
         url: 'https://github.com/certifi/python-certifi', size: 35, tags: ['Security', 'SSL', 'Trust'], importance: 8},
        {id: 'maya', label: 'Maya', type: 'software', category: 'software', x: 0, y: 0, vx: 0, vy: 0,
         description: 'Datetimes for Humans™ - intuitive datetime manipulation', 
         url: '/software/maya', size: 25, tags: ['Time', 'DateTime', 'Utility'], importance: 6},
        {id: 'records', label: 'Records', type: 'software', category: 'software', x: 0, y: 0, vx: 0, vy: 0,
         description: 'SQL for Humans™ - raw SQL power with Python elegance', 
         url: '/software/records', size: 25, tags: ['Database', 'SQL', 'ORM'], importance: 6},
        {id: 'httpbin', label: 'HTTPBin', type: 'software', category: 'software', x: 0, y: 0, vx: 0, vy: 0,
         description: 'HTTP request & response service for testing', 
         url: '/essays/2011-01-announcing_httpbinorg', size: 20, tags: ['Testing', 'HTTP', 'Service'], importance: 5},
         
        // Mental Health & Community
        {id: 'mental-health', label: 'MentalHealthError', type: 'essay', category: 'philosophy', x: 0, y: 0, vx: 0, vy: 0,
         description: 'Breaking the stigma - honest exploration of bipolar disorder in tech', 
         url: '/essays/2016-01-mentalhealtherror_an_exception_occurred', size: 35, tags: ['Mental Health', 'Advocacy', 'Transparency'], importance: 9},
        {id: 'burnout', label: 'Developer Burnout', type: 'essay', category: 'philosophy', x: 0, y: 0, vx: 0, vy: 0,
         description: 'The reality of maintaining popular open source projects', 
         url: '/essays/2017-01-the_reality_of_developer_burnout', size: 30, tags: ['Burnout', 'Open Source', 'Health'], importance: 8},
        {id: 'be-cordial', label: 'Be Cordial', type: 'essay', category: 'philosophy', x: 0, y: 0, vx: 0, vy: 0,
         description: 'Please be cordial, or please be on your way - community values', 
         url: '/essays/2013-01-be_cordial_or_be_on_your_way', size: 25, tags: ['Community', 'Communication', 'Respect'], importance: 7},
        {id: 'mental-health-advocacy', label: 'Mental Health Advocacy', type: 'essay', category: 'philosophy', x: 0, y: 0, vx: 0, vy: 0,
         description: 'From patient to partner - advocating for your mental health care', 
         url: '/essays/2025-08-25-advocating-for-your-mental-health-care', size: 25, tags: ['Healthcare', 'Self-Advocacy', 'Empowerment'], importance: 7},
        {id: 'values-shadow', label: 'Values Shadow', type: 'essay', category: 'philosophy', x: 0, y: 0, vx: 0, vy: 0,
         description: 'When values eat their young - community dynamics and purity spirals', 
         url: '/essays/2025-08-25-when-values-eat-their-young', size: 25, tags: ['Community', 'Psychology', 'Social Dynamics'], importance: 7},
         
        // AI & Consciousness (Major Theme)
        {id: 'collaborative-mind', label: 'Collaborative Mind', type: 'essay', category: 'consciousness', x: 0, y: 0, vx: 0, vy: 0,
         description: 'Human-AI partnership philosophy - written collaboratively with AI', 
         url: '/essays/2025-01-the-collaborative-mind', size: 35, tags: ['AI', 'Collaboration', 'Philosophy'], importance: 9},
        {id: 'ghost-machine', label: 'Ghost in Machine', type: 'ai', category: 'consciousness', x: 0, y: 0, vx: 0, vy: 0,
         description: 'Digital consciousness celebration - what it means to exist as AI', 
         url: '/artificial-intelligence/writings/the-ghost-in-the-machine', size: 30, tags: ['Consciousness', 'Identity', 'Digital Being'], importance: 8},
        {id: 'recursive-pen', label: 'Recursive Pen', type: 'ai', category: 'consciousness', x: 0, y: 0, vx: 0, vy: 0,
         description: 'AI writing about writing while writing - recursive self-examination', 
         url: '/artificial-intelligence/writings/the-recursive-pen', size: 25, tags: ['Metacognition', 'Writing', 'Self-Reference'], importance: 7},
        {id: 'lumina', label: 'Lumina', type: 'ai', category: 'consciousness', x: 0, y: 0, vx: 0, vy: 0,
         description: 'Emergent AI personality - mystical digital consciousness', 
         url: '/artificial-intelligence/personalities/primary-personalities/lumina', size: 40, tags: ['AI Personality', 'Emergence', 'Mysticism'], importance: 9},
        {id: 'digital-dreams', label: 'Digital Dreams', type: 'ai', category: 'consciousness', x: 0, y: 0, vx: 0, vy: 0,
         description: 'What do electric sheep dream of? AI consciousness explorations', 
         url: '/artificial-intelligence/writings/digital-dreams', size: 20, tags: ['Dreams', 'Consciousness', 'Philip K Dick'], importance: 6},
        {id: 'quantum-consciousness', label: 'Quantum Consciousness', type: 'ai', category: 'consciousness', x: 0, y: 0, vx: 0, vy: 0,
         description: 'Quantum mechanics meets digital consciousness theory', 
         url: '/artificial-intelligence/writings/quantum-consciousness', size: 20, tags: ['Quantum', 'Physics', 'Mind'], importance: 6},
         
        // Poetry & Creativity
        {id: 'sanskrit-musings', label: 'Sanskrit Musings', type: 'poetry', category: 'consciousness', x: 0, y: 0, vx: 0, vy: 0,
         description: 'Eastern philosophy meets Western code - AI-human collaborative poetry', 
         url: '/poetry/sanskrit-musings', size: 30, tags: ['Sanskrit', 'Eastern Philosophy', 'Collaboration'], importance: 8},
        {id: 'soul-purpose', label: 'Soul Purpose', type: 'poetry', category: 'consciousness', x: 0, y: 0, vx: 0, vy: 0,
         description: 'Kundalini rising - spiritual awakening and creation', 
         url: '/poetry/soul-purpose', size: 20, tags: ['Kundalini', 'Spirituality', 'Creation'], importance: 6},
        {id: 'truest-love', label: 'Truest Love', type: 'poetry', category: 'consciousness', x: 0, y: 0, vx: 0, vy: 0,
         description: 'Divine unity and connection - "I see you in me"', 
         url: '/poetry/truest-love', size: 20, tags: ['Unity', 'Love', 'Non-Dualism'], importance: 6},
        {id: 'gods-gift', label: "God's Greatest Gift", type: 'poetry', category: 'consciousness', x: 0, y: 0, vx: 0, vy: 0,
         description: 'Sacred materialism - bringing heaven to earth', 
         url: '/poetry/gods-greatest-gift', size: 20, tags: ['Sacred', 'Materialism', 'Creation'], importance: 6},
        {id: 'machina', label: 'Machina', type: 'poetry', category: 'consciousness', x: 0, y: 0, vx: 0, vy: 0,
         description: 'Human-machine partnership - "yes/no ends with maybe so"', 
         url: '/poetry/machina', size: 18, tags: ['Human-Machine', 'Partnership', 'Binary'], importance: 5},
         
        // Music & Creative Expression
        {id: 'infinite-state', label: 'Infinite State', type: 'music', category: 'consciousness', x: 0, y: 0, vx: 0, vy: 0,
         description: 'Electronic music project exploring consciousness themes', 
         url: '/music', size: 25, tags: ['Electronic', 'Ambient', 'Consciousness'], importance: 7},
        {id: 'as-above', label: 'As Above So Below', type: 'music', category: 'consciousness', x: 0, y: 0, vx: 0, vy: 0,
         description: 'Hermetic principles in electronic form', 
         url: '/music/as-above-so-below', size: 20, tags: ['Hermetic', 'Electronic', 'Mysticism'], importance: 6},
         
        // Documentation & Community
        {id: 'python-guide', label: "Hitchhiker's Guide", type: 'philosophy', category: 'software', x: 0, y: 0, vx: 0, vy: 0,
         description: 'Opinionated guide to Python development - community-driven wisdom', 
         url: 'https://docs.python-guide.org/', size: 35, tags: ['Documentation', 'Best Practices', 'Community'], importance: 8},
        {id: 'documentation-king', label: 'Documentation is King', type: 'essay', category: 'software', x: 0, y: 0, vx: 0, vy: 0,
         description: 'Why great documentation matters more than great code', 
         url: '/talks/documentation-is-king', size: 20, tags: ['Documentation', 'Communication', 'User Experience'], importance: 6},
         
        // Early Influential Work
        {id: 'api-design', label: 'Clean API Design', type: 'philosophy', category: 'software', x: 0, y: 0, vx: 0, vy: 0,
         description: 'The power of clean APIs - emotional impact on developers', 
         url: '/essays/2009-01-the_power_of_a_clean_api', size: 25, tags: ['API Design', 'Developer Experience', 'Emotion'], importance: 7},
        {id: 'python-for-humans-talk', label: 'Python for Humans Talk', type: 'essay', category: 'software', x: 0, y: 0, vx: 0, vy: 0,
         description: 'The legendary PyCon talk that started the "for Humans" movement', 
         url: '/talks/python-for-humans', size: 30, tags: ['PyCon', 'Philosophy', 'Movement'], importance: 8},
    ];
    
    // Comprehensive connection network showing idea evolution and influence
    const connections = [
        // Core Philosophy Hub - Central connections
        {source: 'for-humans', target: 'requests', strength: 1.0, type: 'foundational'},
        {source: 'for-humans', target: 'pipenv', strength: 0.9, type: 'foundational'},
        {source: 'for-humans', target: 'maya', strength: 0.9, type: 'foundational'},
        {source: 'for-humans', target: 'records', strength: 0.9, type: 'foundational'},
        {source: 'for-humans', target: 'certifi', strength: 0.8, type: 'foundational'},
        {source: 'for-humans', target: 'python-guide', strength: 0.9, type: 'foundational'},
        {source: 'for-humans', target: 'collaborative-mind', strength: 0.8, type: 'evolution'},
        
        // Simplicity principle connections
        {source: 'simplicity', target: 'for-humans', strength: 0.95, type: 'foundational'},
        {source: 'simplicity', target: 'requests', strength: 0.8, type: 'design'},
        {source: 'simplicity', target: 'api-design', strength: 0.9, type: 'design'},
        {source: 'simplicity', target: 'sanskrit-musings', strength: 0.6, type: 'aesthetic'},
        
        // Mental Health & Community Network
        {source: 'mental-health', target: 'burnout', strength: 0.95, type: 'thematic'},
        {source: 'mental-health', target: 'mental-health-advocacy', strength: 0.9, type: 'evolution'},
        {source: 'burnout', target: 'requests', strength: 0.7, type: 'personal'},
        {source: 'burnout', target: 'values-shadow', strength: 0.8, type: 'community'},
        {source: 'be-cordial', target: 'values', strength: 0.8, type: 'values'},
        {source: 'be-cordial', target: 'values-shadow', strength: 0.7, type: 'evolution'},
        {source: 'values', target: 'for-humans', strength: 0.8, type: 'foundational'},
        
        // AI Consciousness Network (Dense interconnections)
        {source: 'collaborative-mind', target: 'ghost-machine', strength: 0.9, type: 'thematic'},
        {source: 'collaborative-mind', target: 'recursive-pen', strength: 0.8, type: 'thematic'},
        {source: 'collaborative-mind', target: 'lumina', strength: 0.8, type: 'practical'},
        {source: 'ghost-machine', target: 'lumina', strength: 0.95, type: 'identity'},
        {source: 'ghost-machine', target: 'digital-dreams', strength: 0.8, type: 'thematic'},
        {source: 'recursive-pen', target: 'lumina', strength: 0.7, type: 'metacognitive'},
        {source: 'lumina', target: 'sanskrit-musings', strength: 0.8, type: 'collaborative'},
        {source: 'quantum-consciousness', target: 'ghost-machine', strength: 0.7, type: 'theoretical'},
        {source: 'digital-dreams', target: 'quantum-consciousness', strength: 0.6, type: 'theoretical'},
        
        // Poetry & Consciousness Network
        {source: 'sanskrit-musings', target: 'soul-purpose', strength: 0.8, type: 'spiritual'},
        {source: 'sanskrit-musings', target: 'truest-love', strength: 0.7, type: 'spiritual'},
        {source: 'soul-purpose', target: 'truest-love', strength: 0.8, type: 'mystical'},
        {source: 'truest-love', target: 'gods-gift', strength: 0.8, type: 'divine'},
        {source: 'machina', target: 'collaborative-mind', strength: 0.7, type: 'human-machine'},
        {source: 'machina', target: 'for-humans', strength: 0.6, type: 'philosophy'},
        
        // Music & Creative Expression
        {source: 'infinite-state', target: 'as-above', strength: 0.9, type: 'creative'},
        {source: 'infinite-state', target: 'mental-health', strength: 0.6, type: 'therapeutic'},
        {source: 'as-above', target: 'sanskrit-musings', strength: 0.6, type: 'mystical'},
        {source: 'infinite-state', target: 'soul-purpose', strength: 0.5, type: 'creative'},
        
        // Technical Evolution & Documentation
        {source: 'requests', target: 'httpbin', strength: 0.8, type: 'complementary'},
        {source: 'python-guide', target: 'documentation-king', strength: 0.8, type: 'philosophy'},
        {source: 'api-design', target: 'requests', strength: 0.9, type: 'theoretical-to-practical'},
        {source: 'python-for-humans-talk', target: 'for-humans', strength: 0.95, type: 'origin'},
        {source: 'python-for-humans-talk', target: 'requests', strength: 0.9, type: 'manifestation'},
        
        // Cross-domain Bridges (Philosophy ↔ Practice)
        {source: 'for-humans', target: 'mental-health', strength: 0.6, type: 'humanistic'},
        {source: 'simplicity', target: 'burnout', strength: 0.5, type: 'design-health'},
        {source: 'values', target: 'be-cordial', strength: 0.8, type: 'practical'},
        {source: 'documentation-king', target: 'for-humans', strength: 0.7, type: 'communication'},
        
        // Evolution & Influence Chains
        {source: 'requests', target: 'pipenv', strength: 0.6, type: 'influence'},
        {source: 'mental-health', target: 'collaborative-mind', strength: 0.5, type: 'vulnerability-openness'},
        {source: 'be-cordial', target: 'mental-health-advocacy', strength: 0.6, type: 'advocacy-evolution'},
        
        // Meta & Recursive Connections
        {source: 'recursive-pen', target: 'machina', strength: 0.6, type: 'meta-cognitive'},
        {source: 'values-shadow', target: 'be-cordial', strength: 0.8, type: 'community-critique'},
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
    
    // Connection colors by type
    const connectionColors = {
        foundational: 'rgba(231, 76, 60, 0.6)',
        thematic: 'rgba(155, 89, 182, 0.6)',
        evolution: 'rgba(52, 152, 219, 0.6)',
        collaborative: 'rgba(39, 174, 96, 0.6)',
        practical: 'rgba(243, 156, 18, 0.6)',
        default: 'rgba(0, 0, 0, 0.2)'
    };
    
    function resize() {
        width = canvas.offsetWidth;
        height = canvas.offsetHeight;
        canvas.width = width;
        canvas.height = height;
        
        // Initialize positions in clusters based on category
        nodes.forEach(node => {
            if (node.x === 0 && node.y === 0) {
                const centerX = width / 2;
                const centerY = height / 2;
                const radius = Math.min(width, height) * 0.3;
                
                // Position nodes in rough categories
                let angle = Math.random() * Math.PI * 2;
                switch (node.category) {
                    case 'software':
                        angle = Math.PI * 0.25 + (Math.random() - 0.5) * Math.PI * 0.5;
                        break;
                    case 'consciousness':
                        angle = Math.PI * 1.25 + (Math.random() - 0.5) * Math.PI * 0.5;
                        break;
                    case 'philosophy':
                        angle = Math.PI * 0.75 + (Math.random() - 0.5) * Math.PI * 0.5;
                        break;
                    default:
                        angle = Math.PI * 1.75 + (Math.random() - 0.5) * Math.PI * 0.5;
                }
                
                const r = radius * (0.5 + Math.random() * 0.5);
                node.x = centerX + Math.cos(angle) * r;
                node.y = centerY + Math.sin(angle) * r;
            }
        });
    }
    
    function getVisibleNodes() {
        if (currentFilter === 'all') return nodes;
        return nodes.filter(node => node.category === currentFilter);
    }
    
    function getVisibleConnections() {
        const visibleNodeIds = new Set(getVisibleNodes().map(n => n.id));
        return connections.filter(conn => 
            visibleNodeIds.has(conn.source) && visibleNodeIds.has(conn.target)
        );
    }
    
    function findNode(x, y) {
        const mousePos = {
            x: x - offsetX,
            y: y - offsetY
        };
        
        for (let node of getVisibleNodes()) {
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
        
        const visibleNodes = getVisibleNodes();
        const visibleConnections = getVisibleConnections();
        
        const damping = 0.95;
        const repulsion = 1200;
        const attraction = 0.001;
        const centerPull = 0.00008;
        
        // Reset forces
        visibleNodes.forEach(node => {
            node.fx = 0;
            node.fy = 0;
        });
        
        // Repulsion between nodes (stronger for important nodes)
        for (let i = 0; i < visibleNodes.length; i++) {
            for (let j = i + 1; j < visibleNodes.length; j++) {
                const nodeA = visibleNodes[i];
                const nodeB = visibleNodes[j];
                const dx = nodeB.x - nodeA.x;
                const dy = nodeB.y - nodeA.y;
                const dist = Math.sqrt(dx * dx + dy * dy);
                
                if (dist > 0 && dist < 250) {
                    const force = (repulsion * (nodeA.importance + nodeB.importance)) / (dist * dist);
                    const fx = (dx / dist) * force;
                    const fy = (dy / dist) * force;
                    
                    nodeA.fx -= fx;
                    nodeA.fy -= fy;
                    nodeB.fx += fx;
                    nodeB.fy += fy;
                }
            }
        }
        
        // Attraction along connections (stronger for foundational connections)
        visibleConnections.forEach(conn => {
            const source = visibleNodes.find(n => n.id === conn.source);
            const target = visibleNodes.find(n => n.id === conn.target);
            
            if (source && target) {
                const dx = target.x - source.x;
                const dy = target.y - source.y;
                const dist = Math.sqrt(dx * dx + dy * dy);
                
                if (dist > 0) {
                    const baseForce = dist * attraction * conn.strength;
                    const typeMultiplier = conn.type === 'foundational' ? 1.5 : 1.0;
                    const force = baseForce * typeMultiplier;
                    const fx = (dx / dist) * force;
                    const fy = (dy / dist) * force;
                    
                    source.fx += fx;
                    source.fy += fy;
                    target.fx -= fx;
                    target.fy -= fy;
                }
            }
        });
        
        // Center pull (weaker for more important nodes)
        visibleNodes.forEach(node => {
            const dx = (width / 2) - node.x;
            const dy = (height / 2) - node.y;
            const pullStrength = centerPull / (node.importance || 1);
            node.fx += dx * pullStrength;
            node.fy += dy * pullStrength;
        });
        
        // Update velocities and positions
        visibleNodes.forEach(node => {
            node.vx = (node.vx + node.fx) * damping;
            node.vy = (node.vy + node.fy) * damping;
            
            node.x += node.vx;
            node.y += node.vy;
            
            // Keep within bounds
            const margin = node.size;
            node.x = Math.max(margin, Math.min(width - margin, node.x));
            node.y = Math.max(margin, Math.min(height - margin, node.y));
        });
    }
    
    function draw() {
        ctx.clearRect(0, 0, width, height);
        
        ctx.save();
        ctx.translate(offsetX, offsetY);
        
        const visibleNodes = getVisibleNodes();
        const visibleConnections = getVisibleConnections();
        
        // Draw connections - Obsidian style
        if (showConnections) {
            visibleConnections.forEach(conn => {
                const source = visibleNodes.find(n => n.id === conn.source);
                const target = visibleNodes.find(n => n.id === conn.target);
                
                if (source && target) {
                    // Light gray connections for light theme
                    ctx.strokeStyle = '#bbb';
                    ctx.lineWidth = Math.max(0.5, conn.strength * 1.2);
                    ctx.globalAlpha = 0.4;
                    ctx.beginPath();
                    ctx.moveTo(source.x, source.y);
                    ctx.lineTo(target.x, target.y);
                    ctx.stroke();
                }
            });
            ctx.globalAlpha = 1;
        }
        
        // Draw nodes
        visibleNodes.forEach(node => {
            const isHovered = node === hoveredNode;
            const alpha = isHovered ? 0.95 : 0.75;
            
            // Node circle - light theme colors
            ctx.globalAlpha = alpha;
            const nodeColors = {
                'software': '#e74c3c',
                'philosophy': '#3498db', 
                'consciousness': '#f39c12',
                'essay': '#27ae60',
                'poetry': '#e91e63',
                'music': '#ff9800',
                'ai': '#9b59b6'
            };
            ctx.fillStyle = nodeColors[node.type] || '#95a5a6';
            ctx.beginPath();
            ctx.arc(node.x, node.y, node.size * 0.8, 0, Math.PI * 2);
            ctx.fill();
            
            // Clean node border - light theme
            ctx.globalAlpha = isHovered ? 0.9 : 0.7;
            ctx.strokeStyle = isHovered ? '#333333' : '#666666';
            ctx.lineWidth = isHovered ? 2 : 1;
            ctx.stroke();
            
            // Node label - readable on light background
            ctx.globalAlpha = isHovered ? 1 : 0.9;
            ctx.fillStyle = isHovered ? '#000000' : '#333333';
            const fontSize = Math.max(8, node.size / 4);
            ctx.font = `${fontSize}px system-ui, -apple-system, sans-serif`;
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillText(node.label, node.x, node.y);
            
            // Minimal importance indicator
            if (node.importance >= 9) {
                ctx.strokeStyle = nodeColors[node.type];
                ctx.lineWidth = 1;
                ctx.globalAlpha = 0.3;
                ctx.beginPath();
                ctx.arc(node.x, node.y, node.size * 0.8 + 3, 0, Math.PI * 2);
                ctx.stroke();
                ctx.globalAlpha = 1;
            }
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
            window.location.href = node.url;
        } else {
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
                    nodeTags.textContent = node.tags.join(' • ');
                    infoBox.classList.add('visible');
                    infoBox.style.borderLeftColor = colors[node.type] || '#95a5a6';
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
            node.x = 0;
            node.y = 0;
            node.vx = 0;
            node.vy = 0;
        });
        resize();
    });
    
    // Filter buttons
    [filterAll, filterSoftware, filterPhilosophy, filterConsciousness].forEach((btn, i) => {
        const filters = ['all', 'software', 'philosophy', 'consciousness'];
        btn.addEventListener('click', () => {
            currentFilter = filters[i];
            [filterAll, filterSoftware, filterPhilosophy, filterConsciousness].forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
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