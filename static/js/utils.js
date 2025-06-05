// Utility functions for enhanced client-side functionality

// Theme management
const ThemeManager = {
    themes: {
        blue: {
            primary: '#667eea',
            secondary: '#764ba2',
            accent: '#4facfe'
        },
        green: {
            primary: '#10b981',
            secondary: '#047857',
            accent: '#6ee7b7'
        },
        purple: {
            primary: '#8b5cf6',
            secondary: '#7c3aed',
            accent: '#c4b5fd'
        },
        orange: {
            primary: '#f59e0b',
            secondary: '#d97706',
            accent: '#fbbf24'
        }
    },
    
    applyTheme(themeName) {
        const theme = this.themes[themeName];
        if (theme) {
            document.documentElement.style.setProperty('--primary-color', theme.primary);
            document.documentElement.style.setProperty('--secondary-color', theme.secondary);
            document.documentElement.style.setProperty('--accent-color', theme.accent);
        }
    }
};

// Animation utilities
const AnimationUtils = {
    fadeIn(element, duration = 300) {
        element.style.opacity = '0';
        element.style.transition = `opacity ${duration}ms ease`;
        
        setTimeout(() => {
            element.style.opacity = '1';
        }, 10);
    },
    
    slideIn(element, direction = 'up', duration = 300) {
        const transforms = {
            up: 'translateY(20px)',
            down: 'translateY(-20px)',
            left: 'translateX(20px)',
            right: 'translateX(-20px)'
        };
        
        element.style.transform = transforms[direction];
        element.style.opacity = '0';
        element.style.transition = `all ${duration}ms ease`;
        
        setTimeout(() => {
            element.style.transform = 'translate(0)';
            element.style.opacity = '1';
        }, 10);
    },
    
    pulse(element, duration = 1000) {
        element.style.animation = `pulse ${duration}ms ease-in-out`;
        
        setTimeout(() => {
            element.style.animation = '';
        }, duration);
    }
};

// Form validation utilities
const FormValidator = {
    validateEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    },
    
    validatePassword(password) {
        return password && password.length >= 6;
    },
    
    validateRequired(value) {
        return value && value.trim().length > 0;
    },
    
    showError(element, message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.textContent = message;
        
        // Remove existing error
        const existingError = element.parentNode.querySelector('.error-message');
        if (existingError) {
            existingError.remove();
        }
        
        element.parentNode.appendChild(errorDiv);
        AnimationUtils.fadeIn(errorDiv);
    },
    
    clearError(element) {
        const errorDiv = element.parentNode.querySelector('.error-message');
        if (errorDiv) {
            errorDiv.remove();
        }
    }
};

// Local storage utilities
const StorageUtils = {
    set(key, value) {
        try {
            localStorage.setItem(key, JSON.stringify(value));
            return true;
        } catch (e) {
            console.error('Failed to save to localStorage:', e);
            return false;
        }
    },
    
    get(key, defaultValue = null) {
        try {
            const item = localStorage.getItem(key);
            return item ? JSON.parse(item) : defaultValue;
        } catch (e) {
            console.error('Failed to read from localStorage:', e);
            return defaultValue;
        }
    },
    
    remove(key) {
        try {
            localStorage.removeItem(key);
            return true;
        } catch (e) {
            console.error('Failed to remove from localStorage:', e);
            return false;
        }
    }
};

// Performance monitoring
const PerformanceMonitor = {
    marks: {},
    
    start(name) {
        this.marks[name] = performance.now();
    },
    
    end(name) {
        if (this.marks[name]) {
            const duration = performance.now() - this.marks[name];
            console.log(`${name}: ${duration.toFixed(2)}ms`);
            delete this.marks[name];
            return duration;
        }
        return null;
    },
    
    measure(name, fn) {
        this.start(name);
        const result = fn();
        this.end(name);
        return result;
    }
};

// Error handling utilities
const ErrorHandler = {
    log(error, context = '') {
        console.error(`Error ${context}:`, error);
        
        // In a real application, you might want to send this to a logging service
        // this.sendToLoggingService(error, context);
    },
    
    showUserFriendlyError(message) {
        // Create a user-friendly error notification
        const notification = document.createElement('div');
        notification.className = 'notification-error';
        notification.textContent = message;
        
        document.body.appendChild(notification);
        AnimationUtils.slideIn(notification, 'down');
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            notification.remove();
        }, 5000);
    },
    
    handleApiError(response) {
        if (!response.ok) {
            throw new Error(`API Error: ${response.status} ${response.statusText}`);
        }
        return response;
    }
};

// Debounce utility for performance
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

// Throttle utility for performance
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
    };
}

// Export utilities for use in other scripts
window.AppUtils = {
    ThemeManager,
    AnimationUtils,
    FormValidator,
    StorageUtils,
    PerformanceMonitor,
    ErrorHandler,
    debounce,
    throttle
};