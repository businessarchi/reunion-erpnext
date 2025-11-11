# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Cette application Frappe a pour objectif d'automatiser et standardiser la création de tâches dans ERPNext en s'appuyant sur des procédures prédéfinies, tout en permettant une personnalisation par client et par sujet.

- **Framework**: Frappe Framework (Python-based full-stack web application framework)
- **Python Version**: >=3.10
- **Main Dependency**: frappe
- **License**: MIT
- **Objectif Principal**: Gestion automatisée de procédures et création de tâches standardisées dans ERPNext

## Development Commands

### Installation
```bash
# Install the app on a Frappe site
bench get-app procedure
bench --site yoursite.local install-app procedure
```

### Common Bench Commands
```bash
# Start development server
bench start

# Run Python console
bench console

# Create new DocType
bench new-doc-type

# Run migrations
bench migrate

# Clear cache
bench clear-cache

# Build JS/CSS assets
bench build
```

## Architecture

The application follows standard Frappe app structure:

- `procedure/` - Main application module
  - `hooks.py` - Central configuration file for Frappe hooks (events, scheduled tasks, overrides)
  - `modules.txt` - Lists app modules
  - `patches.txt` - Database migration patches
  - `config/` - App-specific configurations
  - `fixtures/` - Data fixtures for initialization
  - `public/` - Static assets (JS, CSS, images)
  - `templates/` - Jinja2 templates
  - `www/` - Web pages

## Key Configuration

### hooks.py
This file controls how the app integrates with Frappe:
- Document events (before_save, after_insert, etc.)
- Scheduled tasks (hourly, daily, weekly)
- Permission handlers
- Web asset inclusions
- DocType class overrides

Currently, all hooks are commented out as examples.

## Development Guidelines

1. **Creating DocTypes**: Use `bench new-doc-type` to create new DocTypes, which will generate the necessary Python and JSON files

2. **Adding Business Logic**: Implement document controllers in `procedure/[module_name]/doctype/[doctype_name]/[doctype_name].py`

3. **Client-Side Code**: Place JavaScript in `procedure/public/js/` and reference in hooks.py

4. **API Endpoints**: Create whitelisted methods in Python files and expose them via `@frappe.whitelist()`

5. **Database Migrations**: Add patches to `procedure/patches/` and list them in `patches.txt`

## Testing

No test framework is currently set up. Frappe typically uses:
```bash
# Run all tests
bench run-tests

# Run specific app tests
bench run-tests --app procedure
```
