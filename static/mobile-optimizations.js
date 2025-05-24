// Mobile-Optimized JavaScript for Kenneth Reitz Website

(function() {
    'use strict';
    
    // Mobile detection
    const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
    const isSmallScreen = window.innerWidth <= 768;
    const isTouchDevice = 'ontouchstart' in window || navigator.maxTouchPoints > 0;
    
    // Performance optimization flags
    let animationsEnabled = !isSmallScreen && window.matchMedia('(prefers-reduced-motion: no-preference)').matches;
    let complexGeometryEnabled = !isSmallScreen;
    
    // Throttle function for performance
    function throttle(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        }
    }
    
    // Debounce function for resize events
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
    
    // Mobile-optimized sacred geometry manager
    class MobileSacredGeometry {
        constructor() {
            this.isActive = complexGeometryEnabled;
            this.elements = [];
            this.animationFrameId = null;
            this.lastUpdateTime = 0;
            this.updateInterval = isSmallScreen ? 100 : 16; // Reduce update frequency on mobile
        }
        
        init() {
            this.elements = document.querySelectorAll('.sacred-geometry, .global-sacred-geometry, .floating-sacred');
            
            if (isSmallScreen) {
                this.simplifyGeometry();
            }
            
            if (animationsEnabled && this.isActive) {
                this.startAnimations();
            }
        }
        
        simplifyGeometry() {
            this.elements.forEach(element => {
                const svg = element.querySelector('svg');
                if (svg) {
                    // Reduce complexity by hiding some elements
                    const complexPaths = svg.querySelectorAll('g:nth-child(n+4)');
                    complexPaths.forEach(path => path.style.display = 'none');
                    
                    // Reduce stroke width for better mobile performance
                    const allPaths = svg.querySelectorAll('[stroke-width]');
                    allPaths.forEach(path => {
                        const currentWidth = parseFloat(path.getAttribute('stroke-width') || 1);
                        path.setAttribute('stroke-width', Math.max(0.5, currentWidth * 0.7));
                    });
                }
            });
        }
        
        startAnimations() {
            const animate = (currentTime) => {
                if (currentTime - this.lastUpdateTime > this.updateInterval) {
                    this.updateGeometry();
                    this.lastUpdateTime = currentTime;
                }
                this.animationFrameId = requestAnimationFrame(animate);
            };
            this.animationFrameId = requestAnimationFrame(animate);
        }
        
        updateGeometry() {
            if (!this.isActive) return;
            
            this.elements.forEach((element, index) => {
                const offset = index * 0.1;
                const time = Date.now() * 0.001 + offset;
                const scale = isSmallScreen ? 0.6 : 0.8 + Math.sin(time * 0.5) * 0.1;
                const opacity = isSmallScreen ? 0.02 : 0.05 + Math.sin(time * 0.3) * 0.02;
                
                element.style.transform = `scale(${scale})`;
                element.style.opacity = opacity;
            });
        }
        
        stop() {
            if (this.animationFrameId) {
                cancelAnimationFrame(this.animationFrameId);
                this.animationFrameId = null;
            }
        }
    }
    
    // Mobile-optimized counter animations
    class MobileCounterManager {
        constructor() {
            this.counters = {
                requests: document.getElementById('requests-counter'),
                cerifi: document.getElementById('cerifi-counter'),
                total: document.getElementById('total-counter')
            };
            this.isAnimating = false;
            this.animationSpeed = isSmallScreen ? 2000 : 1000; // Slower on mobile
        }
        
        init() {
            if (this.counters.requests && this.counters.cerifi && this.counters.total) {
                this.startCounters();
            }
        }
        
        startCounters() {
            if (this.isAnimating) return;
            this.isAnimating = true;
            
            const baseRequests = 8000000;
            const baseCerifi = 8000000;
            const startTime = Date.now();
            
            const animate = () => {
                const elapsed = Date.now() - startTime;
                const progress = Math.min(elapsed / this.animationSpeed, 1);
                
                const requestsCount = Math.floor(baseRequests + (Math.random() * 100000 * progress));
                const cerifiCount = Math.floor(baseCerifi + (Math.random() * 100000 * progress));
                const totalCount = requestsCount + cerifiCount;
                
                this.counters.requests.textContent = this.formatNumber(requestsCount);
                this.counters.cerifi.textContent = this.formatNumber(cerifiCount);
                this.counters.total.textContent = this.formatNumber(totalCount);
                
                if (progress < 1) {
                    requestAnimationFrame(animate);
                } else {
                    this.isAnimating = false;
                    // Continue with slower updates
                    setTimeout(() => this.slowUpdate(), 5000);
                }
            };
            
            animate();
        }
        
        slowUpdate() {
            // Periodic slow updates to show activity
            const updateInterval = isSmallScreen ? 10000 : 5000;
            
            const update = () => {
                if (this.counters.requests) {
                    const currentRequests = parseInt(this.counters.requests.textContent.replace(/,/g, ''));
                    const currentCerifi = parseInt(this.counters.cerifi.textContent.replace(/,/g, ''));
                    
                    const newRequests = currentRequests + Math.floor(Math.random() * 1000);
                    const newCerifi = currentCerifi + Math.floor(Math.random() * 1000);
                    
                    this.counters.requests.textContent = this.formatNumber(newRequests);
                    this.counters.cerifi.textContent = this.formatNumber(newCerifi);
                    this.counters.total.textContent = this.formatNumber(newRequests + newCerifi);
                }
                
                setTimeout(update, updateInterval);
            };
            
            update();
        }
        
        formatNumber(num) {
            return num.toLocaleString();
        }
    }
    
    // Touch gesture manager
    class TouchGestureManager {
        constructor() {
            this.startX = 0;
            this.startY = 0;
            this.currentX = 0;
            this.currentY = 0;
            this.isGesturing = false;
        }
        
        init() {
            if (!isTouchDevice) return;
            
            document.addEventListener('touchstart', this.handleTouchStart.bind(this), { passive: true });
            document.addEventListener('touchmove', this.handleTouchMove.bind(this), { passive: true });
            document.addEventListener('touchend', this.handleTouchEnd.bind(this), { passive: true });
        }
        
        handleTouchStart(e) {
            if (e.touches.length !== 1) return;
            
            this.startX = e.touches[0].clientX;
            this.startY = e.touches[0].clientY;
            this.isGesturing = true;
        }
        
        handleTouchMove(e) {
            if (!this.isGesturing || e.touches.length !== 1) return;
            
            this.currentX = e.touches[0].clientX;
            this.currentY = e.touches[0].clientY;
            
            // Add subtle visual feedback for touch interactions
            this.updateTouchFeedback();
        }
        
        handleTouchEnd(e) {
            if (!this.isGesturing) return;
            
            const deltaX = this.currentX - this.startX;
            const deltaY = this.currentY - this.startY;
            const distance = Math.sqrt(deltaX * deltaX + deltaY * deltaY);
            
            // Handle swipe gestures if needed
            if (distance > 50) {
                this.handleSwipe(deltaX, deltaY);
            }
            
            this.isGesturing = false;
            this.removeTouchFeedback();
        }
        
        updateTouchFeedback() {
            // Subtle visual feedback during touch
            document.body.style.background = 'linear-gradient(135deg, #1f2937 0%, #374151 100%)';
        }
        
        removeTouchFeedback() {
            // Remove touch feedback
            document.body.style.background = '';
        }
        
        handleSwipe(deltaX, deltaY) {
            // Handle swipe gestures - can be extended for navigation
            if (Math.abs(deltaX) > Math.abs(deltaY)) {
                if (deltaX > 0) {
                    // Swipe right
                    this.triggerHapticFeedback();
                } else {
                    // Swipe left
                    this.triggerHapticFeedback();
                }
            }
        }
        
        triggerHapticFeedback() {
            if (navigator.vibrate) {
                navigator.vibrate(50);
            }
        }
    }
    
    // Mobile viewport manager
    class MobileViewportManager {
        constructor() {
            this.vh = window.innerHeight * 0.01;
        }
        
        init() {
            this.setVhProperty();
            window.addEventListener('resize', debounce(this.handleResize.bind(this), 250));
            window.addEventListener('orientationchange', debounce(this.handleOrientationChange.bind(this), 300));
        }
        
        setVhProperty() {
            this.vh = window.innerHeight * 0.01;
            document.documentElement.style.setProperty('--vh', `${this.vh}px`);
        }
        
        handleResize() {
            this.setVhProperty();
            this.updateLayoutForScreenSize();
        }
        
        handleOrientationChange() {
            setTimeout(() => {
                this.setVhProperty();
                this.updateLayoutForScreenSize();
            }, 300);
        }
        
        updateLayoutForScreenSize() {
            const newIsSmallScreen = window.innerWidth <= 768;
            
            if (newIsSmallScreen !== isSmallScreen) {
                // Screen size category changed, reinitialize components
                location.reload(); // Simple approach for major layout changes
            }
        }
    }
    
    // Performance monitor
    class PerformanceMonitor {
        constructor() {
            this.frameCount = 0;
            this.lastTime = performance.now();
            this.fps = 60;
        }
        
        init() {
            if (isSmallScreen) {
                this.startMonitoring();
            }
        }
        
        startMonitoring() {
            const monitor = () => {
                this.frameCount++;
                const currentTime = performance.now();
                
                if (currentTime - this.lastTime >= 1000) {
                    this.fps = this.frameCount;
                    this.frameCount = 0;
                    this.lastTime = currentTime;
                    
                    this.optimizeBasedOnPerformance();
                }
                
                requestAnimationFrame(monitor);
            };
            
            requestAnimationFrame(monitor);
        }
        
        optimizeBasedOnPerformance() {
            if (this.fps < 30 && animationsEnabled) {
                // Performance is poor, disable some animations
                animationsEnabled = false;
                complexGeometryEnabled = false;
                
                // Disable complex sacred geometry
                const geometryElements = document.querySelectorAll('.sacred-geometry, .floating-sacred');
                geometryElements.forEach(el => {
                    el.style.display = 'none';
                });
                
                console.log('Performance optimization: Disabled complex animations');
            }
        }
    }
    
    // Lazy loading for images and content
    class LazyLoader {
        constructor() {
            this.observer = null;
        }
        
        init() {
            if ('IntersectionObserver' in window) {
                this.observer = new IntersectionObserver(
                    this.handleIntersection.bind(this),
                    {
                        rootMargin: '50px 0px',
                        threshold: 0.1
                    }
                );
                
                const lazyElements = document.querySelectorAll('[data-lazy]');
                lazyElements.forEach(el => this.observer.observe(el));
            }
        }
        
        handleIntersection(entries) {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const element = entry.target;
                    const src = element.dataset.lazy;
                    
                    if (element.tagName === 'IMG') {
                        element.src = src;
                    } else {
                        element.style.backgroundImage = `url(${src})`;
                    }
                    
                    element.removeAttribute('data-lazy');
                    this.observer.unobserve(element);
                }
            });
        }
    }
    
    // Initialize all mobile optimizations
    function initMobileOptimizations() {
        const sacredGeometry = new MobileSacredGeometry();
        const counterManager = new MobileCounterManager();
        const touchGestureManager = new TouchGestureManager();
        const viewportManager = new MobileViewportManager();
        const performanceMonitor = new PerformanceMonitor();
        const lazyLoader = new LazyLoader();
        
        // Initialize components
        sacredGeometry.init();
        counterManager.init();
        touchGestureManager.init();
        viewportManager.init();
        performanceMonitor.init();
        lazyLoader.init();
        
        // Add mobile-specific CSS class
        document.documentElement.classList.add(isMobile ? 'mobile' : 'desktop');
        document.documentElement.classList.add(isSmallScreen ? 'small-screen' : 'large-screen');
        document.documentElement.classList.add(isTouchDevice ? 'touch' : 'no-touch');
        
        // Preload critical resources on mobile
        if (isMobile) {
            preloadCriticalResources();
        }
        
        // Handle visibility change for performance
        document.addEventListener('visibilitychange', () => {
            if (document.hidden) {
                sacredGeometry.stop();
            } else if (animationsEnabled) {
                sacredGeometry.init();
            }
        });
    }
    
    // Preload critical resources
    function preloadCriticalResources() {
        const criticalCSS = [
            '/static/mobile-enhancements.css',
            '/static/custom-tufte.css'
        ];
        
        criticalCSS.forEach(href => {
            const link = document.createElement('link');
            link.rel = 'preload';
            link.as = 'style';
            link.href = href;
            document.head.appendChild(link);
        });
    }
    
    // Wait for DOM to be ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initMobileOptimizations);
    } else {
        initMobileOptimizations();
    }
    
    // Export for debugging
    window.MobileOptimizations = {
        isMobile,
        isSmallScreen,
        isTouchDevice,
        animationsEnabled,
        complexGeometryEnabled
    };
    
})();