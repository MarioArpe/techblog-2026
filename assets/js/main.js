// ===== NAVIGATION TOGGLE =====
document.addEventListener('DOMContentLoaded', function() {
    const navToggle = document.querySelector('.nav-toggle');
    const navMenu = document.querySelector('.nav-menu');
    
    navToggle.addEventListener('click', function() {
        navToggle.classList.toggle('active');
        navMenu.classList.toggle('active');
    });
    
    // Close menu when clicking on a link
    document.querySelectorAll('.nav-menu a').forEach(link => {
        link.addEventListener('click', function() {
            navToggle.classList.remove('active');
            navMenu.classList.remove('active');
        });
    });
    
    // Header scroll effect
    const header = document.querySelector('.header-fixed');
    let lastScroll = 0;
    
    window.addEventListener('scroll', function() {
        const currentScroll = window.pageYOffset;
        
        if (currentScroll > 100) {
            header.style.background = 'rgba(255, 255, 255, 0.95)';
            header.style.backdropFilter = 'blur(10px)';
        } else {
            header.style.background = 'var(--white)';
            header.style.backdropFilter = 'none';
        }
        
        lastScroll = currentScroll;
    });
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Newsletter form submission
    const newsletterForm = document.querySelector('.newsletter-form');
    const footerForm = document.querySelector('.footer-form');
    
    function handleNewsletterSubmit(e, form) {
        e.preventDefault();
        const email = form.querySelector('input[type="email"]').value;
        
        if (email) {
            // Simulate newsletter subscription
            showNotification('¡Gracias por suscribirte! Revisa tu email para confirmar.', 'success');
            form.reset();
        }
    }
    
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', (e) => handleNewsletterSubmit(e, newsletterForm));
    }
    
    if (footerForm) {
        footerForm.addEventListener('submit', (e) => handleNewsletterSubmit(e, footerForm));
    }
    
    // Animate elements on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    // Observe elements for animation
    document.querySelectorAll('.post-card, .category-card').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'all 0.6s ease';
        observer.observe(el);
    });
    
    // Counter animation for stats
    function animateCounter(element, target, duration = 2000) {
        let start = 0;
        const increment = target / (duration / 16);
        
        function updateCounter() {
            start += increment;
            if (start < target) {
                element.textContent = Math.floor(start) + (element.textContent.includes('+') ? '+' : '');
                requestAnimationFrame(updateCounter);
            } else {
                element.textContent = target + (element.textContent.includes('+') ? '+' : '');
            }
        }
        
        updateCounter();
    }
    
    // Trigger counter animation when stats are visible
    const stats = document.querySelectorAll('.stat-number');
    const statsObserver = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting && !entry.target.animated) {
                const text = entry.target.textContent;
                const number = parseInt(text.replace(/\D/g, ''));
                animateCounter(entry.target, number);
                entry.target.animated = true;
            }
        });
    }, { threshold: 0.5 });
    
    stats.forEach(stat => statsObserver.observe(stat));
    
    // Lazy loading for images
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
    
    // Search functionality (if implemented)
    function initSearch() {
        const searchInput = document.querySelector('.search-input');
        const searchResults = document.querySelector('.search-results');
        
        if (searchInput) {
            searchInput.addEventListener('input', debounce(function(e) {
                const query = e.target.value.toLowerCase();
                if (query.length > 2) {
                    // Implement search logic here
                    console.log('Searching for:', query);
                } else {
                    if (searchResults) {
                        searchResults.innerHTML = '';
                        searchResults.style.display = 'none';
                    }
                }
            }, 300));
        }
    }
    
    // Initialize search
    initSearch();
    
    // Theme toggle (optional)
    function initThemeToggle() {
        const themeToggle = document.querySelector('.theme-toggle');
        const body = document.body;
        
        if (themeToggle) {
            themeToggle.addEventListener('click', function() {
                body.classList.toggle('dark-theme');
                const isDark = body.classList.contains('dark-theme');
                localStorage.setItem('theme', isDark ? 'dark' : 'light');
                updateThemeIcon(isDark);
            });
            
            // Load saved theme
            const savedTheme = localStorage.getItem('theme');
            if (savedTheme === 'dark') {
                body.classList.add('dark-theme');
                updateThemeIcon(true);
            }
        }
    }
    
    function updateThemeIcon(isDark) {
        const themeToggle = document.querySelector('.theme-toggle i');
        if (themeToggle) {
            themeToggle.className = isDark ? 'fas fa-sun' : 'fas fa-moon';
        }
    }
    
    // Initialize theme toggle
    initThemeToggle();

    // Share buttons handlers
    function openShareWindow(url, width = 600, height = 400) {
        const left = (screen.width / 2) - (width / 2);
        const top = (screen.height / 2) - (height / 2);
        window.open(url, 'shareWindow', `toolbar=0,status=0,resizable=1,width=${width},height=${height},top=${top},left=${left}`);
    }

    function handleShare(action) {
        const title = document.title || '';
        const url = window.location.href;

        if (action === 'share' && navigator.share) {
            navigator.share({ title, url }).catch(() => {});
            return;
        }

        if (action === 'twitter') {
            const shareUrl = `https://twitter.com/intent/tweet?text=${encodeURIComponent(title)}&url=${encodeURIComponent(url)}`;
            openShareWindow(shareUrl);
        } else if (action === 'facebook') {
            const shareUrl = `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(url)}`;
            openShareWindow(shareUrl);
        } else if (action === 'whatsapp') {
            const shareUrl = `https://api.whatsapp.com/send?text=${encodeURIComponent(title + ' ' + url)}`;
            openShareWindow(shareUrl, 400, 700);
        } else if (action === 'copy') {
            navigator.clipboard.writeText(url).then(() => showNotification('Enlace copiado al portapapeles', 'success'))
            .catch(() => showNotification('No se pudo copiar', 'error'));
        }
    }

    document.querySelectorAll('.share-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const action = this.getAttribute('data-action');
            handleShare(action);
        });
    });
    
    // Performance monitoring
    function trackPerformance() {
        // Track page load time
        window.addEventListener('load', function() {
            const loadTime = performance.timing.loadEventEnd - performance.timing.navigationStart;
            console.log('Page load time:', loadTime + 'ms');
        });
        
        // Track scroll depth
        let maxScroll = 0;
        window.addEventListener('scroll', function() {
            const scrollPercent = Math.round((window.scrollY / (document.documentElement.scrollHeight - window.innerHeight)) * 100);
            maxScroll = Math.max(maxScroll, scrollPercent);
            
            // Send scroll depth analytics (if implemented)
            if (scrollPercent === 25 || scrollPercent === 50 || scrollPercent === 75 || scrollPercent === 90) {
                console.log('Scroll depth reached:', scrollPercent + '%');
            }
        });
    }
    
    // Initialize performance tracking
    trackPerformance();
    
    // Error handling
    window.addEventListener('error', function(e) {
        console.error('JavaScript error:', e.error);
        // Send error to analytics (if implemented)
    });
    
    // Service Worker registration (for PWA)
    if ('serviceWorker' in navigator) {
        window.addEventListener('load', function() {
            navigator.serviceWorker.register('/sw.js')
                .then(function(registration) {
                    console.log('SW registered: ', registration);
                })
                .catch(function(registrationError) {
                    console.log('SW registration failed: ', registrationError);
                });
        });
    }
});

// ===== UTILITY FUNCTIONS =====
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

function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    // Add styles
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'success' ? '#00C853' : type === 'error' ? '#FF4444' : '#FF6B00'};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        z-index: 10000;
        transform: translateX(100%);
        transition: transform 0.3s ease;
        max-width: 300px;
    `;
    
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

// ===== FORM VALIDATION =====
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function validateForm(form) {
    const inputs = form.querySelectorAll('input[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            isValid = false;
            input.classList.add('error');
        } else {
            input.classList.remove('error');
        }
        
        if (input.type === 'email' && !validateEmail(input.value)) {
            isValid = false;
            input.classList.add('error');
        }
    });
    
    return isValid;
}

// ===== LOCAL STORAGE HELPERS =====
function setLocalStorage(key, value) {
    try {
        localStorage.setItem(key, JSON.stringify(value));
    } catch (e) {
        console.error('LocalStorage error:', e);
    }
}

function getLocalStorage(key) {
    try {
        const item = localStorage.getItem(key);
        return item ? JSON.parse(item) : null;
    } catch (e) {
        console.error('LocalStorage error:', e);
        return null;
    }
}

// ===== DATE HELPERS =====
function formatDate(date, options = {}) {
    const defaults = {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    };
    
    return new Date(date).toLocaleDateString('es-ES', { ...defaults, ...options });
}

function timeAgo(date) {
    const seconds = Math.floor((new Date() - new Date(date)) / 1000);
    
    let interval = Math.floor(seconds / 31536000);
    if (interval > 1) return interval + " años";
    
    interval = Math.floor(seconds / 2592000);
    if (interval > 1) return interval + " meses";
    
    interval = Math.floor(seconds / 86400);
    if (interval > 1) return interval + " días";
    
    interval = Math.floor(seconds / 3600);
    if (interval > 1) return interval + " horas";
    
    interval = Math.floor(seconds / 60);
    if (interval > 1) return interval + " minutos";
    
    return "ahora mismo";
}

// ===== EXPORT FUNCTIONS =====
window.TechBlogUtils = {
    showNotification,
    validateEmail,
    validateForm,
    setLocalStorage,
    getLocalStorage,
    formatDate,
    timeAgo,
    debounce
};
