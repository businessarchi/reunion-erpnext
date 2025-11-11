/**
 * Fix pour l'erreur "Aucun événement is not valid JSON"
 * Ce fichier intercepte les réponses texte et les convertit en JSON valide
 */

frappe.provide("frappe.integrations");

// Wrapper sécurisé pour frappe.msgprint
(function() {
    const original_msgprint = frappe.msgprint;

    frappe.msgprint = function(msg, title) {
        // Si le message est "Aucun événement" ou similaire, on le gère proprement
        if (typeof msg === 'string' &&
            (msg.includes('Aucun événement') || msg.includes('Aucun évén'))) {

            return original_msgprint({
                title: title || __('Google Calendar'),
                indicator: 'blue',
                message: __('Aucun événement trouvé dans la période sélectionnée')
            });
        }

        // Comportement normal pour les autres cas
        return original_msgprint(msg, title);
    };

    console.log('Google Calendar fix loaded: frappe.msgprint patched');
})();

// Wrapper pour les appels frappe.call avec Google Calendar
frappe.call_with_json_fallback = function(opts) {
    const original_callback = opts.callback;

    opts.callback = function(r) {
        // Si la réponse est une string au lieu d'un objet
        if (r.message && typeof r.message === 'string') {
            try {
                // Essayer de parser comme JSON
                r.message = JSON.parse(r.message);
            } catch (e) {
                // Si ce n'est pas du JSON, créer un objet standard
                console.warn('Response is not valid JSON, wrapping in object:', r.message);

                // Si c'est "Aucun événement" ou similaire
                if (r.message.includes('Aucun') || r.message.includes('événement')) {
                    r.message = {
                        success: true,
                        message: r.message,
                        events: []
                    };
                } else {
                    r.message = {
                        success: false,
                        message: r.message,
                        events: []
                    };
                }
            }
        }

        if (original_callback) {
            original_callback(r);
        }
    };

    return frappe.call(opts);
};

console.log('Google Calendar JSON fallback loaded');
