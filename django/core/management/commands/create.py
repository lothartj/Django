from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
import os
import re


class Command(BaseCommand):
    help = "Creates a Django project and app in one command."
    missing_args_message = "You must provide both project name and app name."

    def add_arguments(self, parser):
        parser.add_argument('project_name', help='Name of the Django project')
        parser.add_argument('app_name', help='Name of the Django app')
        parser.add_argument(
            '--directory',
            help='Optional destination directory',
            default=None
        )
    def add_app_to_settings(self, project_dir, app_name):
        settings_path = os.path.join(project_dir, project_dir, 'settings.py')
        if not os.path.exists(settings_path):
            raise CommandError(f"Could not find settings.py at {settings_path}")
        with open(settings_path, 'r') as f:
            content = f.read()
        installed_apps_match = re.search(r'INSTALLED_APPS\s*=\s*\[(.*?)\]', content, re.DOTALL)
        if not installed_apps_match:
            raise CommandError("Could not find INSTALLED_APPS in settings.py")
        apps_str = installed_apps_match.group(1)
        last_app = re.findall(r'[\'"].*?[\'"]', apps_str)[-1]
        quote_char = last_app[0]
        indent = re.search(r'(\s*)[\'"]', apps_str).group(1)
        new_app_entry = f"{indent}{quote_char}{app_name}{quote_char},\n"
        closing_bracket_pos = content.find(']', installed_apps_match.start())
        new_content = content[:closing_bracket_pos] + new_app_entry + content[closing_bracket_pos:]
        with open(settings_path, 'w') as f:
            f.write(new_content)

    def handle(self, *args, **options):
        project_name = options['project_name']
        app_name = options['app_name']
        target_dir = options['directory']
        try:
            self.stdout.write(f"Creating project '{project_name}'...")
            call_command('startproject', project_name, target_dir)
        except Exception as e:
            raise CommandError(f"Failed to create project: {e}")
        project_dir = os.path.join(target_dir if target_dir else os.getcwd(), project_name)
        original_cwd = os.getcwd()
        os.chdir(project_dir)
        try:
            self.stdout.write(f"Creating app '{app_name}'...")
            call_command('startapp', app_name)
        except Exception as e:
            os.chdir(original_cwd)
            raise CommandError(f"Failed to create app: {e}")
        try:
            self.stdout.write(f"Adding '{app_name}' to INSTALLED_APPS...")
            self.add_app_to_settings(project_name, app_name)
        except Exception as e:
            self.stderr.write(f"Warning: Failed to add app to INSTALLED_APPS: {e}")
        finally:
            os.chdir(original_cwd)

        self.stdout.write(self.style.SUCCESS(
            f"Successfully created project '{project_name}' and app '{app_name}' and added it to INSTALLED_APPS"
        ))