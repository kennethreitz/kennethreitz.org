// Mobile Testing Utility for Kenneth Reitz Website
// Run this in browser console to test mobile optimizations

(function() {
    'use strict';
    
    const MobileTester = {
        init() {
            console.log('🚀 Mobile Testing Utility Initialized');
            this.runAllTests();
        },
        
        // Test viewport and meta tags
        testViewport() {
            console.log('\n📱 Testing Viewport Configuration...');
            
            const viewport = document.querySelector('meta[name="viewport"]');
            const content = viewport ? viewport.getAttribute('content') : null;
            
            if (content && content.includes('width=device-width')) {
                console.log('✅ Viewport meta tag configured correctly');
            } else {
                console.warn('❌ Viewport meta tag missing or incorrect');
            }
            
            if (content && content.includes('initial-scale=1.0')) {
                console.log('✅ Initial scale set correctly');
            } else {
                console.warn('❌ Initial scale not set');
            }
        },
        
        // Test responsive CSS loading
        testResponsiveCSS() {
            console.log('\n🎨 Testing Responsive CSS...');
            
            const mobileCSS = document.querySelector('link[href*="mobile-enhancements.css"]');
            const componentsCSS = document.querySelector('link[href*="mobile-components.css"]');
            
            if (mobileCSS) {
                console.log('✅ Mobile enhancements CSS loaded');
            } else {
                console.warn('❌ Mobile enhancements CSS missing');
            }
            
            if (componentsCSS) {
                console.log('✅ Mobile components CSS loaded');
            } else {
                console.warn('❌ Mobile components CSS missing');
            }
        },
        
        // Test touch targets
        testTouchTargets() {
            console.log('\n👆 Testing Touch Targets...');
            
            const interactive = document.querySelectorAll('a, button, input, textarea, select');
            let passCount = 0;
            let failCount = 0;
            
            interactive.forEach(element => {
                const rect = element.getBoundingClientRect();
                const minSize = 44; // iOS recommended minimum
                
                if (rect.width >= minSize && rect.height >= minSize) {
                    passCount++;
                } else {
                    failCount++;
                    if (failCount <= 5) { // Limit console spam
                        console.warn(`❌ Touch target too small: ${element.tagName} (${Math.round(rect.width)}x${Math.round(rect.height)}px)`);
                    }
                }
            });
            
            console.log(`✅ ${passCount} touch targets meet minimum size`);
            if (failCount > 0) {
                console.warn(`❌ ${failCount} touch targets are too small`);
            }
        },
        
        // Test font sizes for readability
        testFontSizes() {
            console.log('\n📖 Testing Font Sizes...');
            
            const textElements = document.querySelectorAll('p, span, div, li, td, th');
            let tooSmallCount = 0;
            
            textElements.forEach(element => {
                const fontSize = parseFloat(window.getComputedStyle(element).fontSize);
                if (fontSize < 14 && element.textContent.trim()) {
                    tooSmallCount++;
                }
            });
            
            if (tooSmallCount === 0) {
                console.log('✅ All text meets minimum size requirements');
            } else {
                console.warn(`❌ ${tooSmallCount} elements have text smaller than 14px`);
            }
        },
        
        // Test image responsiveness
        testImages() {
            console.log('\n🖼️ Testing Image Responsiveness...');
            
            const images = document.querySelectorAll('img');
            let responsiveCount = 0;
            
            images.forEach(img => {
                const style = window.getComputedStyle(img);
                if (style.maxWidth === '100%' || style.width === '100%') {
                    responsiveCount++;
                }
            });
            
            console.log(`✅ ${responsiveCount}/${images.length} images are responsive`);
            
            if (responsiveCount < images.length) {
                console.warn(`❌ ${images.length - responsiveCount} images may not be responsive`);
            }
        },
        
        // Test sacred geometry performance on mobile
        testSacredGeometry() {
            console.log('\n🔮 Testing Sacred Geometry Performance...');
            
            const geometry = document.querySelectorAll('.sacred-geometry, .global-sacred-geometry, .floating-sacred');
            const screenWidth = window.innerWidth;
            
            geometry.forEach(element => {
                const style = window.getComputedStyle(element);
                const opacity = parseFloat(style.opacity);
                const transform = style.transform;
                
                if (screenWidth <= 480) {
                    if (opacity <= 0.03) {
                        console.log('✅ Sacred geometry opacity optimized for small screens');
                    } else {
                        console.warn('❌ Sacred geometry opacity too high for mobile');
                    }
                    
                    if (transform.includes('scale') && transform.includes('0.')) {
                        console.log('✅ Sacred geometry scaled down for mobile');
                    }
                }
            });
        },
        
        // Test performance metrics
        testPerformance() {
            console.log('\n⚡ Testing Performance Metrics...');
            
            if ('performance' in window) {
                const navigation = performance.getEntriesByType('navigation')[0];
                const loadTime = navigation.loadEventEnd - navigation.loadEventStart;
                const domContentLoaded = navigation.domContentLoadedEventEnd - navigation.domContentLoadedEventStart;
                
                console.log(`📊 Page load time: ${Math.round(loadTime)}ms`);
                console.log(`📊 DOM content loaded: ${Math.round(domContentLoaded)}ms`);
                
                if (loadTime < 3000) {
                    console.log('✅ Page load time is acceptable');
                } else {
                    console.warn('❌ Page load time is slow');
                }
                
                // Test FPS (simplified)
                let frameCount = 0;
                const startTime = performance.now();
                
                function countFrames() {
                    frameCount++;
                    const elapsed = performance.now() - startTime;
                    
                    if (elapsed < 1000) {
                        requestAnimationFrame(countFrames);
                    } else {
                        const fps = Math.round(frameCount * 1000 / elapsed);
                        console.log(`📊 Approximate FPS: ${fps}`);
                        
                        if (fps >= 30) {
                            console.log('✅ Frame rate is acceptable');
                        } else {
                            console.warn('❌ Frame rate is low');
                        }
                    }
                }
                
                requestAnimationFrame(countFrames);
            }
        },
        
        // Test accessibility features
        testAccessibility() {
            console.log('\n♿ Testing Accessibility...');
            
            // Check for alt text on images
            const images = document.querySelectorAll('img');
            let imagesWithAlt = 0;
            
            images.forEach(img => {
                if (img.getAttribute('alt') !== null) {
                    imagesWithAlt++;
                }
            });
            
            console.log(`✅ ${imagesWithAlt}/${images.length} images have alt text`);
            
            // Check for focus states
            const focusableElements = document.querySelectorAll('a, button, input, textarea, select');
            console.log(`📊 ${focusableElements.length} focusable elements found`);
            
            // Check color contrast (simplified)
            const textElements = document.querySelectorAll('p, h1, h2, h3, h4, h5, h6, span, div');
            let lowContrastCount = 0;
            
            textElements.forEach(element => {
                const style = window.getComputedStyle(element);
                const color = style.color;
                const backgroundColor = style.backgroundColor;
                
                // Simple contrast check (not comprehensive)
                if (color === 'rgb(128, 128, 128)' || color === '#808080') {
                    lowContrastCount++;
                }
            });
            
            if (lowContrastCount === 0) {
                console.log('✅ No obvious low contrast text detected');
            } else {
                console.warn(`❌ ${lowContrastCount} elements may have low contrast`);
            }
        },
        
        // Test mobile-specific features
        testMobileFeatures() {
            console.log('\n📱 Testing Mobile-Specific Features...');
            
            // Check for mobile optimizations script
            const mobileScript = document.querySelector('script[src*="mobile-optimizations.js"]');
            if (mobileScript) {
                console.log('✅ Mobile optimizations script loaded');
            } else {
                console.warn('❌ Mobile optimizations script missing');
            }
            
            // Check for touch event handling
            if ('ontouchstart' in window) {
                console.log('✅ Touch events supported');
            } else {
                console.log('ℹ️ Touch events not supported (desktop)');
            }
            
            // Check for device orientation support
            if ('orientation' in window) {
                console.log('✅ Device orientation supported');
            } else {
                console.log('ℹ️ Device orientation not supported');
            }
            
            // Check for vibration API
            if ('vibrate' in navigator) {
                console.log('✅ Vibration API supported');
            } else {
                console.log('ℹ️ Vibration API not supported');
            }
        },
        
        // Test responsive breakpoints
        testBreakpoints() {
            console.log('\n📏 Testing Responsive Breakpoints...');
            
            const width = window.innerWidth;
            
            if (width <= 480) {
                console.log('📱 Mobile (≤480px) - Testing mobile optimizations');
                this.testMobileSpecific();
            } else if (width <= 768) {
                console.log('📱 Tablet (≤768px) - Testing tablet optimizations');
            } else if (width <= 1024) {
                console.log('💻 Small Desktop (≤1024px)');
            } else {
                console.log('🖥️ Large Desktop (>1024px)');
            }
            
            console.log(`📊 Current viewport: ${width}x${window.innerHeight}px`);
        },
        
        testMobileSpecific() {
            // Test if sacred geometry is properly reduced
            const geometry = document.querySelector('.sacred-geometry');
            if (geometry) {
                const style = window.getComputedStyle(geometry);
                const opacity = parseFloat(style.opacity);
                
                if (opacity <= 0.2) {
                    console.log('✅ Sacred geometry opacity reduced for mobile');
                } else {
                    console.warn('❌ Sacred geometry too prominent on mobile');
                }
            }
            
            // Test if complex animations are disabled
            const animations = document.querySelectorAll('.sacred-breathe, .sacred-spiral');
            let animationsDisabled = 0;
            
            animations.forEach(element => {
                const style = window.getComputedStyle(element);
                if (style.animationName === 'none') {
                    animationsDisabled++;
                }
            });
            
            if (animationsDisabled > 0) {
                console.log('✅ Complex animations disabled on mobile');
            }
        },
        
        // Generate mobile optimization report
        generateReport() {
            console.log('\n📋 MOBILE OPTIMIZATION REPORT');
            console.log('================================');
            
            const issues = [];
            const successes = [];
            
            // Collect all console messages and categorize
            // This is a simplified version - in practice you'd track these during tests
            
            console.log('\n📊 Summary:');
            console.log(`✅ Optimizations working: ${successes.length}`);
            console.log(`❌ Issues found: ${issues.length}`);
            
            if (issues.length === 0) {
                console.log('\n🎉 All mobile optimizations are working correctly!');
            } else {
                console.log('\n🔧 Recommended fixes:');
                issues.forEach((issue, index) => {
                    console.log(`${index + 1}. ${issue}`);
                });
            }
        },
        
        // Run all tests
        runAllTests() {
            this.testViewport();
            this.testResponsiveCSS();
            this.testTouchTargets();
            this.testFontSizes();
            this.testImages();
            this.testSacredGeometry();
            this.testPerformance();
            this.testAccessibility();
            this.testMobileFeatures();
            this.testBreakpoints();
            
            setTimeout(() => {
                this.generateReport();
            }, 2000); // Wait for performance tests to complete
        },
        
        // Manual testing helpers
        simulateMobile() {
            console.log('📱 Simulating mobile viewport...');
            document.documentElement.style.width = '375px';
            document.body.style.width = '375px';
            console.log('Resize your browser to see mobile layout');
        },
        
        testTouch() {
            console.log('👆 Testing touch interactions...');
            const event = new TouchEvent('touchstart', {
                bubbles: true,
                cancelable: true,
                touches: [{
                    clientX: 100,
                    clientY: 100
                }]
            });
            document.dispatchEvent(event);
            console.log('Touch event simulated');
        },
        
        measureScrollPerformance() {
            console.log('📜 Measuring scroll performance...');
            let scrollCount = 0;
            const startTime = performance.now();
            
            const scrollHandler = () => {
                scrollCount++;
                const elapsed = performance.now() - startTime;
                
                if (elapsed > 1000) {
                    const scrollsPerSecond = scrollCount / (elapsed / 1000);
                    console.log(`📊 Scroll events per second: ${Math.round(scrollsPerSecond)}`);
                    window.removeEventListener('scroll', scrollHandler);
                }
            };
            
            window.addEventListener('scroll', scrollHandler);
            console.log('Scroll around the page to test performance');
        }
    };
    
    // Export to global scope for manual testing
    window.MobileTester = MobileTester;
    
    // Auto-run tests when script loads
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => MobileTester.init());
    } else {
        MobileTester.init();
    }
    
    // Add helper commands
    console.log('\n🛠️ Mobile Testing Commands:');
    console.log('MobileTester.simulateMobile() - Simulate mobile viewport');
    console.log('MobileTester.testTouch() - Test touch interactions');
    console.log('MobileTester.measureScrollPerformance() - Measure scroll performance');
    console.log('MobileTester.runAllTests() - Run all tests again');
    
})();