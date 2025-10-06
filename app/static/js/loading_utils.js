/**
 * 🔧 Loading Overlay Utilities
 * Gestisce il loading overlay per operazioni asincrone bloccanti
 */

const LoadingOverlay = {
    /**
     * Mostra il loading overlay
     * @param {string} title - Titolo del loading
     * @param {string} message - Messaggio descrittivo
     */
    show(title = 'Elaborazione in corso...', message = 'Attendere prego') {
        const overlay = document.getElementById('loadingOverlay');
        const titleEl = document.getElementById('loadingTitle');
        const messageEl = document.getElementById('loadingMessage');
        
        if (titleEl) titleEl.textContent = title;
        if (messageEl) messageEl.textContent = message;
        
        if (overlay) {
            overlay.style.display = 'flex';
            // Blocca lo scroll del body
            document.body.style.overflow = 'hidden';
        }
    },

    /**
     * Nasconde il loading overlay
     */
    hide() {
        const overlay = document.getElementById('loadingOverlay');
        if (overlay) {
            overlay.style.display = 'none';
            // Ripristina lo scroll del body
            document.body.style.overflow = '';
        }
    },

    /**
     * Gestisce automaticamente una chiamata fetch con loading
     * @param {Promise} promise - Promise da gestire
     * @param {string} title - Titolo del loading
     * @param {string} message - Messaggio descrittivo
     * @returns {Promise} - La promise originale
     */
    async withLoading(promise, title, message) {
        try {
            this.show(title, message);
            const result = await promise;
            return result;
        } finally {
            this.hide();
        }
    }
};

// Esporta globalmente per uso nei template
window.LoadingOverlay = LoadingOverlay;
