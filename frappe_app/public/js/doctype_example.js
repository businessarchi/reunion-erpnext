/**
 * Example Client Script for a DocType
 *
 * To use this, add to hooks.py:
 * doctype_js = {"Your DocType": "public/js/doctype_example.js"}
 */

frappe.ui.form.on('Sample Doctype', {
	// Triggered when form is loaded
	refresh: function(frm) {
		console.log('Form refreshed');

		// Add a custom button
		if (!frm.is_new()) {
			frm.add_custom_button(__('Custom Action'), function() {
				frappe.msgprint(__('Custom button clicked'));
			});
		}

		// Set field properties
		if (frm.doc.status === 'Active') {
			frm.set_df_property('description', 'read_only', 1);
		}
	},

	// Triggered when form is saved
	onload: function(frm) {
		console.log('Form loaded');
	},

	// Triggered before form is saved
	validate: function(frm) {
		// Validation logic
		if (!frm.doc.title) {
			frappe.msgprint(__('Title is required'));
			frappe.validated = false;
		}
	},

	// Triggered when a field value changes
	title: function(frm) {
		console.log('Title changed to:', frm.doc.title);
	},

	// Example of an async operation
	status: function(frm) {
		if (frm.doc.status === 'Active') {
			frappe.call({
				method: 'frappe_app.utils.ping',
				callback: function(r) {
					console.log('API Response:', r.message);
				}
			});
		}
	}
});
