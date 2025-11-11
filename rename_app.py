#!/usr/bin/env python3
"""
Script pour renommer automatiquement l'application template

Usage:
    python rename_app.py mon_app "Mon App" "Ma Société" "contact@masociete.com"

Arguments:
    app_name: Nom technique de l'app (snake_case)
    app_title: Titre affiché de l'app
    publisher: Nom de la société/développeur
    email: Email de contact
"""

import os
import sys
import shutil
import re


def rename_app(app_name, app_title, publisher, email):
    """
    Renomme l'application template avec les nouveaux paramètres
    """
    print("🚀 Renommage de l'application Frappe...")
    print(f"   Nom: {app_name}")
    print(f"   Titre: {app_title}")
    print(f"   Éditeur: {publisher}")
    print(f"   Email: {email}")
    print()

    # 1. Renommer le dossier principal
    if os.path.exists("frappe_app"):
        print("📁 Renommage du dossier frappe_app -> " + app_name)
        shutil.move("frappe_app", app_name)

    # 2. Mettre à jour pyproject.toml
    print("📝 Mise à jour de pyproject.toml...")
    update_file("pyproject.toml", [
        ('name = "frappe_app"', f'name = "{app_name}"'),
        ('name = "Mélodie"', f'name = "{publisher}"'),
        ('email = "logiciel@businessarchitecte.com"', f'email = "{email}"'),
    ])

    # 3. Mettre à jour setup.py
    print("📝 Mise à jour de setup.py...")
    update_file("setup.py", [
        ('from frappe_app import', f'from {app_name} import'),
        ('name="frappe_app"', f'name="{app_name}"'),
        ('author="Mélodie"', f'author="{publisher}"'),
        ('author_email="logiciel@businessarchitecte.com"', f'author_email="{email}"'),
    ])

    # 4. Mettre à jour hooks.py
    print("📝 Mise à jour de hooks.py...")
    hooks_path = os.path.join(app_name, "hooks.py")
    update_file(hooks_path, [
        ('app_name = "frappe_app"', f'app_name = "{app_name}"'),
        ('app_title = "Frappe App Template"', f'app_title = "{app_title}"'),
        ('app_publisher = "Your Company"', f'app_publisher = "{publisher}"'),
        ('app_email = "hello@yourcompany.com"', f'app_email = "{email}"'),
    ])

    # 5. Mettre à jour utils.py
    print("📝 Mise à jour de utils.py...")
    utils_path = os.path.join(app_name, "utils.py")
    update_file(utils_path, [
        ('from frappe_app import', f'from {app_name} import'),
    ])

    # 6. Mettre à jour test_utils.py
    print("📝 Mise à jour de test_utils.py...")
    test_utils_path = os.path.join(app_name, "tests", "test_utils.py")
    update_file(test_utils_path, [
        ('from frappe_app.utils', f'from {app_name}.utils'),
    ])

    # 7. Mettre à jour permissions.py
    print("📝 Mise à jour de permissions.py...")
    permissions_path = os.path.join(app_name, "permissions.py")
    update_file(permissions_path, [
        ('"frappe_app.permissions.', f'"{app_name}.permissions.'),
        ('frappe_app.permissions.', f'{app_name}.permissions.'),
    ])

    # 8. Mettre à jour patches.txt
    print("📝 Mise à jour de patches.txt...")
    patches_path = os.path.join(app_name, "patches.txt")
    update_file(patches_path, [
        ('frappe_app.patches.', f'{app_name}.patches.'),
    ])

    # 9. Mettre à jour example_patch.py
    print("📝 Mise à jour de example_patch.py...")
    patch_path = os.path.join(app_name, "patches", "v0_1", "example_patch.py")
    update_file(patch_path, [
        ('frappe_app.patches.', f'{app_name}.patches.'),
    ])

    # 10. Renommer le module interne
    internal_module = os.path.join(app_name, "frappe_app")
    if os.path.exists(internal_module):
        new_internal = os.path.join(app_name, app_name)
        print(f"📁 Renommage du module interne -> {app_name}/{app_name}")
        shutil.move(internal_module, new_internal)

    # 11. Mettre à jour modules.txt
    print("📝 Mise à jour de modules.txt...")
    modules_path = os.path.join(app_name, "modules.txt")
    update_file(modules_path, [
        ('Frappe App', app_title),
    ])

    # 12. Mettre à jour desktop.py
    print("📝 Mise à jour de desktop.py...")
    desktop_path = os.path.join(app_name, "config", "desktop.py")
    update_file(desktop_path, [
        ('"module_name": "Frappe App"', f'"module_name": "{app_title}"'),
        ('"label": _("Frappe App")', f'"label": _("{app_title}")'),
    ])

    # 13. Mettre à jour sample_doctype.json
    print("📝 Mise à jour de sample_doctype.json...")
    doctype_json = os.path.join(app_name, app_name, "doctype", "sample_doctype", "sample_doctype.json")
    update_file(doctype_json, [
        ('"module": "Frappe App"', f'"module": "{app_title}"'),
    ])

    print()
    print("✅ Renommage terminé avec succès !")
    print()
    print("📋 Prochaines étapes :")
    print(f"   1. Vérifier les fichiers modifiés")
    print(f"   2. Installer l'app : bench get-app /path/to/{app_name}")
    print(f"   3. Installer sur un site : bench --site monsite.local install-app {app_name}")
    print(f"   4. Démarrer : bench start")


def update_file(filepath, replacements):
    """
    Met à jour un fichier avec les remplacements donnés

    Args:
        filepath: Chemin du fichier
        replacements: Liste de tuples (old_text, new_text)
    """
    if not os.path.exists(filepath):
        print(f"   ⚠️  Fichier non trouvé : {filepath}")
        return

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    for old, new in replacements:
        content = content.replace(old, new)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)


def validate_app_name(app_name):
    """
    Valide le nom de l'app (snake_case, lettres minuscules et underscore)
    """
    pattern = r'^[a-z][a-z0-9_]*$'
    if not re.match(pattern, app_name):
        print("❌ Erreur : Le nom de l'app doit être en snake_case (lettres minuscules et underscore)")
        print(f"   Exemple : mon_app, my_application, custom_erp")
        return False
    return True


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python rename_app.py <app_name> <app_title> <publisher> <email>")
        print()
        print("Exemple:")
        print('  python rename_app.py mon_app "Mon App" "Ma Société" "contact@masociete.com"')
        print()
        print("Arguments:")
        print("  app_name  : Nom technique en snake_case (ex: mon_app)")
        print("  app_title : Titre affiché (ex: 'Mon App')")
        print("  publisher : Nom de la société/développeur")
        print("  email     : Email de contact")
        sys.exit(1)

    app_name = sys.argv[1]
    app_title = sys.argv[2]
    publisher = sys.argv[3]
    email = sys.argv[4]

    # Validation
    if not validate_app_name(app_name):
        sys.exit(1)

    # Confirmation
    print()
    response = input(f"⚠️  Cette opération va renommer l'app en '{app_name}'. Continuer ? (o/N) : ")
    if response.lower() not in ['o', 'oui', 'y', 'yes']:
        print("❌ Opération annulée")
        sys.exit(0)

    print()
    rename_app(app_name, app_title, publisher, email)
