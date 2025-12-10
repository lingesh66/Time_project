/**
 * APPLE-STYLE 3D MOTION EFFECTS
 * Motion-based parallax, tilt, and physics-based interactions
 */

// ============================================
// MOTION-BASED TILT EFFECT (Apple-style)
// ============================================
class AppleMotion {
    constructor() {
        this.cards = document.querySelectorAll('.glass-card');
        this.header = document.querySelector('header');
        this.isReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

        if (!this.isReducedMotion) {
            this.init();
        }
    }

    init() {
        // Add tilt effect to cards
        this.cards.forEach(card => {
            card.addEventListener('mousemove', (e) => this.handleTilt(e, card));
            card.addEventListener('mouseleave', () => this.resetTilt(card));
        });

        // Add parallax to header
        if (this.header) {
            window.addEventListener('scroll', () => this.handleParallax());
            window.addEventListener('mousemove', (e) => this.handleHeaderTilt(e));
        }

        // Add smooth scroll reveal
        this.observeElements();
    }

    handleTilt(e, card) {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        const centerX = rect.width / 2;
        const centerY = rect.height / 2;

        const rotateX = (y - centerY) / 20;
        const rotateY = (centerX - x) / 20;

        card.style.transform = `
            perspective(1200px)
            rotateX(${rotateX}deg)
            rotateY(${rotateY}deg)
            translateZ(10px)
            scale3d(1.02, 1.02, 1.02)
        `;

        card.style.transition = 'transform 0.1s ease-out';
    }

    resetTilt(card) {
        card.style.transform = '';
        card.style.transition = 'transform 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
    }

    handleParallax() {
        if (!this.header) return;

        const scrolled = window.pageYOffset;
        const parallaxSpeed = 0.5;

        this.header.style.transform = `translateY(${scrolled * parallaxSpeed}px)`;
        this.header.style.opacity = Math.max(1 - scrolled / 500, 0);
    }

    handleHeaderTilt(e) {
        if (!this.header) return;

        const x = (e.clientX / window.innerWidth - 0.5) * 10;
        const y = (e.clientY / window.innerHeight - 0.5) * 10;

        this.header.style.transform = `
            translate(${x}px, ${y}px)
            perspective(1000px)
        `;
    }

    observeElements() {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        });

        document.querySelectorAll('.result-card, .glass-card').forEach(el => {
            observer.observe(el);
        });
    }
}

// ============================================
// SMOOTH BUTTON RIPPLE EFFECT
// ============================================
function addRippleEffect() {
    const buttons = document.querySelectorAll('button');

    buttons.forEach(button => {
        button.addEventListener('click', function (e) {
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;

            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.style.position = 'absolute';
            ripple.style.borderRadius = '50%';
            ripple.style.background = 'rgba(255, 255, 255, 0.5)';
            ripple.style.pointerEvents = 'none';
            ripple.style.animation = 'ripple 0.6s ease-out';

            this.appendChild(ripple);

            setTimeout(() => ripple.remove(), 600);
        });
    });
}

// ============================================
// PERFORMANCE-OPTIMIZED SCROLL EFFECTS
// ============================================
let ticking = false;

function onScroll() {
    if (!ticking) {
        window.requestAnimationFrame(() => {
            updateParallax();
            ticking = false;
        });
        ticking = true;
    }
}

function updateParallax() {
    const scrolled = window.pageYOffset;
    const blobs = document.querySelectorAll('.animate-blob');

    blobs.forEach((blob, index) => {
        const speed = 0.3 + (index * 0.1);
        blob.style.transform = `translateY(${scrolled * speed}px)`;
    });
}

// ============================================
// INITIALIZE ON DOM READY
// ============================================
document.addEventListener('DOMContentLoaded', () => {
    // Initialize Apple-style motion
    new AppleMotion();

    // Add ripple effects
    addRippleEffect();

    // Add scroll parallax
    window.addEventListener('scroll', onScroll, { passive: true });

    // Add smooth focus transitions
    document.querySelectorAll('input, textarea, button').forEach(el => {
        el.addEventListener('focus', function () {
            this.style.transition = 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)';
        });
    });
});

// ============================================
// EXPORT FOR MODULE USAGE (if needed)
// ============================================
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { AppleMotion };
}
