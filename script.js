// Bug Bounty Bootcamp Manual - Interactive Script

class BugBountyManual {
    constructor() {
        this.currentChapter = 'chapter1';
        this.sidebar = document.querySelector('.sidebar');
        this.sidebarToggle = document.getElementById('sidebarToggle');
        this.navLinks = document.querySelectorAll('.nav-link');
        this.chapters = document.querySelectorAll('.chapter');
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.setupKeyboardNavigation();
        this.addScrollProgress();
        this.addSmoothAnimations();
    }

    setupEventListeners() {
        // Sidebar toggle for mobile
        if (this.sidebarToggle) {
            this.sidebarToggle.addEventListener('click', () => {
                this.toggleSidebar();
            });
        }

        // Navigation links
        this.navLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const chapterId = link.getAttribute('href').substring(1);
                this.showChapter(chapterId);
            });
        });

        // Close sidebar on mobile when clicking outside
        document.addEventListener('click', (e) => {
            if (window.innerWidth <= 1024 && 
                !this.sidebar.contains(e.target) && 
                !this.sidebarToggle.contains(e.target) &&
                this.sidebar.classList.contains('open')) {
                this.sidebar.classList.remove('open');
            }
        });

        // Handle window resize
        window.addEventListener('resize', () => {
            if (window.innerWidth > 1024) {
                this.sidebar.classList.remove('open');
            }
        });

        // Add click handlers for asset cards and platform cards
        this.addCardInteractions();
    }

    setupKeyboardNavigation() {
        document.addEventListener('keydown', (e) => {
            // Escape key to close sidebar on mobile
            if (e.key === 'Escape' && this.sidebar.classList.contains('open')) {
                this.sidebar.classList.remove('open');
            }

            // Arrow keys for chapter navigation
            if (e.key === 'ArrowLeft' || e.key === 'ArrowRight') {
                e.preventDefault();
                this.navigateChapter(e.key === 'ArrowRight' ? 'next' : 'prev');
            }
        });
    }

    toggleSidebar() {
        this.sidebar.classList.toggle('open');
    }

    showChapter(chapterId) {
        // Hide all chapters
        this.chapters.forEach(chapter => {
            chapter.classList.remove('active');
        });

        // Show selected chapter
        const targetChapter = document.getElementById(chapterId);
        if (targetChapter) {
            targetChapter.classList.add('active');
            this.currentChapter = chapterId;
        }

        // Update navigation
        this.updateNavigation(chapterId);

        // Close sidebar on mobile
        if (window.innerWidth <= 1024) {
            this.sidebar.classList.remove('open');
        }

        // Scroll to top
        window.scrollTo({ top: 0, behavior: 'smooth' });

        // Add page transition effect
        this.addPageTransition();
    }

    updateNavigation(activeChapterId) {
        // Remove active class from all nav items
        document.querySelectorAll('.nav-item').forEach(item => {
            item.classList.remove('active');
        });

        // Add active class to current nav item
        const activeLink = document.querySelector(`[href="#${activeChapterId}"]`);
        if (activeLink) {
            activeLink.closest('.nav-item').classList.add('active');
        }
    }

    navigateChapter(direction) {
        const chapterIds = Array.from(this.chapters).map(ch => ch.id);
        const currentIndex = chapterIds.indexOf(this.currentChapter);
        
        let nextIndex;
        if (direction === 'next' && currentIndex < chapterIds.length - 1) {
            nextIndex = currentIndex + 1;
        } else if (direction === 'prev' && currentIndex > 0) {
            nextIndex = currentIndex - 1;
        }

        if (nextIndex !== undefined) {
            this.showChapter(chapterIds[nextIndex]);
        }
    }

    addScrollProgress() {
        // Create progress bar
        const progressBar = document.createElement('div');
        progressBar.className = 'scroll-progress';
        progressBar.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 0%;
            height: 3px;
            background: linear-gradient(90deg, #3b82f6, #10b981);
            z-index: 9999;
            transition: width 0.3s ease;
        `;
        document.body.appendChild(progressBar);

        // Update progress on scroll
        window.addEventListener('scroll', () => {
            const scrollTop = window.pageYOffset;
            const docHeight = document.documentElement.scrollHeight - window.innerHeight;
            const scrollPercent = (scrollTop / docHeight) * 100;
            progressBar.style.width = scrollPercent + '%';
        });
    }

    addSmoothAnimations() {
        // Intersection Observer for fade-in animations
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }
            });
        }, observerOptions);

        // Observe all content sections
        document.querySelectorAll('.content-section').forEach(section => {
            section.style.opacity = '0';
            section.style.transform = 'translateY(20px)';
            section.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            observer.observe(section);
        });
    }

    addCardInteractions() {
        // Add click interactions to asset cards
        document.querySelectorAll('.asset-type-card').forEach(card => {
            card.addEventListener('click', () => {
                this.showAssetDetails(card);
            });

            // Add keyboard accessibility
            card.setAttribute('tabindex', '0');
            card.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    this.showAssetDetails(card);
                }
            });
        });

        // Add click interactions to platform cards
        document.querySelectorAll('.platform-card').forEach(card => {
            card.addEventListener('click', () => {
                this.showPlatformInfo(card);
            });

            card.setAttribute('tabindex', '0');
            card.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    this.showPlatformInfo(card);
                }
            });
        });

        // Add timeline item interactions
        document.querySelectorAll('.timeline-item').forEach(item => {
            item.addEventListener('click', () => {
                this.highlightTimelineItem(item);
            });
        });
    }

    showAssetDetails(card) {
        const title = card.querySelector('h4').textContent;
        const description = card.querySelector('p').textContent;
        const features = Array.from(card.querySelectorAll('.feature-tag')).map(tag => tag.textContent);

        this.showModal({
            title: title,
            content: `
                <div class="modal-asset-details">
                    <p>${description}</p>
                    <h4 style="margin: 1.5rem 0 0.75rem 0; color: var(--text-primary);">Key Features:</h4>
                    <ul style="list-style: none; padding: 0;">
                        ${features.map(feature => `<li style="padding: 0.25rem 0; color: var(--text-secondary);"><i class="fas fa-check" style="color: var(--secondary-color); margin-right: 0.5rem;"></i>${feature}</li>`).join('')}
                    </ul>
                    <div style="margin-top: 1.5rem; padding: 1rem; background: var(--dark-surface-light); border-radius: 0.5rem; border-left: 4px solid var(--primary-color);">
                        <strong style="color: var(--text-primary);">Pro Tip:</strong> 
                        <span style="color: var(--text-secondary);">Start with asset types that match your current skill level and gradually expand to more complex targets.</span>
                    </div>
                </div>
            `
        });
    }

    showPlatformInfo(card) {
        const platformName = card.querySelector('h5').textContent;
        const platformData = this.getPlatformData(platformName);

        this.showModal({
            title: platformName,
            content: `
                <div class="modal-platform-info">
                    <p>${platformData.description}</p>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin: 1.5rem 0;">
                        <div style="background: var(--dark-surface-light); padding: 1rem; border-radius: 0.5rem;">
                            <strong style="color: var(--primary-color);">Founded:</strong><br>
                            <span style="color: var(--text-secondary);">${platformData.founded}</span>
                        </div>
                        <div style="background: var(--dark-surface-light); padding: 1rem; border-radius: 0.5rem;">
                            <strong style="color: var(--primary-color);">Focus:</strong><br>
                            <span style="color: var(--text-secondary);">${platformData.focus}</span>
                        </div>
                    </div>
                    <h4 style="margin: 1.5rem 0 0.75rem 0; color: var(--text-primary);">Key Features:</h4>
                    <ul style="list-style: none; padding: 0;">
                        ${platformData.features.map(feature => `<li style="padding: 0.25rem 0; color: var(--text-secondary);"><i class="fas fa-star" style="color: var(--warning-color); margin-right: 0.5rem;"></i>${feature}</li>`).join('')}
                    </ul>
                </div>
            `
        });
    }

    getPlatformData(platformName) {
        const platformData = {
            'HackerOne': {
                description: 'The world\'s largest bug bounty platform connecting organizations with ethical hackers.',
                founded: '2012',
                focus: 'Enterprise & Government',
                features: ['Large community', 'Comprehensive reporting tools', 'Reputation system', 'CVE coordination']
            },
            'Bugcrowd': {
                description: 'Crowdsourced security platform offering bug bounty and vulnerability disclosure programs.',
                founded: '2012',
                focus: 'Diverse Program Types',
                features: ['Flexible program types', 'Research collaboration', 'Advanced analytics', 'Custom integrations']
            },
            'Synack': {
                description: 'Managed security testing platform with vetted researcher community.',
                founded: '2013',
                focus: 'Managed Service',
                features: ['Vetted researchers', 'Continuous testing', 'AI-powered platform', 'Real-time results']
            },
            'Intigriti': {
                description: 'European-based bug bounty platform focusing on quality and researcher experience.',
                founded: '2016',
                focus: 'European Market',
                features: ['Quality over quantity', 'Personal researcher support', 'European compliance', 'Educational resources']
            }
        };

        return platformData[platformName] || {
            description: 'A bug bounty platform connecting researchers with organizations.',
            founded: 'N/A',
            focus: 'Security Research',
            features: ['Bug bounty programs', 'Vulnerability disclosure', 'Researcher community']
        };
    }

    highlightTimelineItem(item) {
        // Remove previous highlights
        document.querySelectorAll('.timeline-item').forEach(ti => {
            ti.style.background = '';
            ti.style.borderRadius = '';
            ti.style.padding = '';
        });

        // Highlight selected item
        item.style.background = 'var(--dark-surface-light)';
        item.style.borderRadius = '0.5rem';
        item.style.padding = '1rem';
        item.style.transition = 'all 0.3s ease';

        // Remove highlight after 3 seconds
        setTimeout(() => {
            item.style.background = '';
            item.style.borderRadius = '';
            item.style.padding = '';
        }, 3000);
    }

    showModal({ title, content }) {
        // Create modal overlay
        const overlay = document.createElement('div');
        overlay.className = 'modal-overlay';
        overlay.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.8);
            z-index: 10000;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 2rem;
            animation: fadeIn 0.3s ease;
        `;

        // Create modal content
        const modal = document.createElement('div');
        modal.className = 'modal-content';
        modal.style.cssText = `
            background: var(--dark-surface);
            border-radius: 1rem;
            padding: 2rem;
            max-width: 600px;
            width: 100%;
            max-height: 80vh;
            overflow-y: auto;
            border: 1px solid var(--border-color);
            box-shadow: var(--shadow-lg);
            animation: slideInUp 0.3s ease;
        `;

        modal.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
                <h3 style="color: var(--text-primary); margin: 0; font-size: 1.5rem;">${title}</h3>
                <button class="modal-close" style="background: none; border: none; color: var(--text-secondary); font-size: 1.5rem; cursor: pointer; padding: 0.5rem; border-radius: 0.25rem; transition: all 0.2s ease;">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            <div style="color: var(--text-secondary); line-height: 1.6;">
                ${content}
            </div>
        `;

        overlay.appendChild(modal);
        document.body.appendChild(overlay);

        // Add animations
        const style = document.createElement('style');
        style.textContent = `
            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }
            @keyframes slideInUp {
                from { opacity: 0; transform: translateY(20px); }
                to { opacity: 1; transform: translateY(0); }
            }
        `;
        document.head.appendChild(style);

        // Close modal functionality
        const closeModal = () => {
            overlay.style.animation = 'fadeIn 0.3s ease reverse';
            setTimeout(() => {
                document.body.removeChild(overlay);
                document.head.removeChild(style);
            }, 300);
        };

        modal.querySelector('.modal-close').addEventListener('click', closeModal);
        overlay.addEventListener('click', (e) => {
            if (e.target === overlay) closeModal();
        });

        // Close on Escape key
        const escapeHandler = (e) => {
            if (e.key === 'Escape') {
                closeModal();
                document.removeEventListener('keydown', escapeHandler);
            }
        };
        document.addEventListener('keydown', escapeHandler);

        // Style close button hover
        const closeBtn = modal.querySelector('.modal-close');
        closeBtn.addEventListener('mouseenter', () => {
            closeBtn.style.background = 'var(--dark-surface-light)';
            closeBtn.style.color = 'var(--text-primary)';
        });
        closeBtn.addEventListener('mouseleave', () => {
            closeBtn.style.background = 'none';
            closeBtn.style.color = 'var(--text-secondary)';
        });
    }

    addPageTransition() {
        const activeChapter = document.querySelector('.chapter.active');
        if (activeChapter) {
            activeChapter.style.opacity = '0';
            activeChapter.style.transform = 'translateY(20px)';
            
            setTimeout(() => {
                activeChapter.style.opacity = '1';
                activeChapter.style.transform = 'translateY(0)';
            }, 100);
        }
    }
}

// Global function to show chapters (for button onclick)
function showChapter(chapterId) {
    if (window.manualApp) {
        window.manualApp.showChapter(chapterId);
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.manualApp = new BugBountyManual();
    
    // Add some developer easter eggs
    console.log(`
    🛡️ Bug Bounty Bootcamp - Interactive Manual
    ==========================================
    
    Keyboard Shortcuts:
    - Left/Right arrows: Navigate chapters
    - Escape: Close sidebar (mobile)
    
    Happy hacking! 🎯
    `);
});

// Add service worker for offline support (basic)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js')
            .then(registration => {
                console.log('SW registered: ', registration);
            })
            .catch(registrationError => {
                console.log('SW registration failed: ', registrationError);
            });
    });
} 