/**
 * Example List View Script
 *
 * To use this, add to hooks.py:
 * doctype_list_js = {"Your DocType": "public/js/list_view_example.js"}
 */

frappe.listview_settings['Sample Doctype'] = {
	// Add custom button in list view
	add_fields: ['status', 'title'],

	// Custom formatting for list items
	get_indicator: function(doc) {
		if (doc.status === 'Active') {
			return [__('Active'), 'green', 'status,=,Active'];
		} else if (doc.status === 'Inactive') {
			return [__('Inactive'), 'red', 'status,=,Inactive'];
		} else {
			return [__('Draft'), 'gray', 'status,=,Draft'];
		}
	},

	// Custom button in list view
	button: {
		show: function(doc) {
			return doc.status !== 'Active';
		},
		get_label: function() {
			return __('Activate');
		},
		get_description: function(doc) {
			return __('Activate {0}', [doc.name]);
		},
		action: function(doc) {
			frappe.call({
				method: 'frappe.client.set_value',
				args: {
					doctype: 'Sample Doctype',
					name: doc.name,
					fieldname: 'status',
					value: 'Active'
				},
				callback: function() {
					frappe.show_alert({
						message: __('Activated successfully'),
						indicator: 'green'
					});
					cur_list.refresh();
				}
			});
		}
	},

	// Custom filters
	onload: function(listview) {
		// Add custom filter button
		listview.page.add_menu_item(__('Show Active Only'), function() {
			listview.filter_area.clear();
			listview.filter_area.add([[listview.doctype, 'status', '=', 'Active']]);
		});
	}
};
