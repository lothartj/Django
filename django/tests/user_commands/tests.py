import os
import shutil
import tempfile
from io import StringIO
from unittest import mock

from django.core.management import call_command
from django.test import TestCase


class CreateCommandTests(TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.test_dir)
        self.stdout = StringIO()
        self.stderr = StringIO()

    def test_create_command_basic(self):
        """Test basic project and app creation"""
        call_command(
            'create',
            'testproject',
            'testapp',
            '--directory', self.test_dir,
            stdout=self.stdout,
            stderr=self.stderr
        )

        # Check if project directory was created
        project_dir = os.path.join(self.test_dir, 'testproject')
        self.assertTrue(os.path.exists(project_dir))

        # Check if app directory was created
        app_dir = os.path.join(project_dir, 'testapp')
        self.assertTrue(os.path.exists(app_dir))

        # Check if settings.py exists and contains our app
        settings_path = os.path.join(project_dir, 'testproject', 'settings.py')
        self.assertTrue(os.path.exists(settings_path))
        
        with open(settings_path) as f:
            settings_content = f.read()
            self.assertIn('testapp', settings_content)

    def test_create_command_existing_directory(self):
        """Test command fails when project directory already exists"""
        # Create the project directory first
        os.makedirs(os.path.join(self.test_dir, 'testproject'))

        with self.assertRaises(Exception):
            call_command(
                'create',
                'testproject',
                'testapp',
                '--directory', self.test_dir,
                stdout=self.stdout,
                stderr=self.stderr
            )

    def test_create_command_output(self):
        """Test command output messages"""
        call_command(
            'create',
            'testproject',
            'testapp',
            '--directory', self.test_dir,
            stdout=self.stdout,
            stderr=self.stderr
        )

        output = self.stdout.getvalue()
        self.assertIn("Creating project 'testproject'", output)
        self.assertIn("Creating app 'testapp'", output)
        self.assertIn("Successfully created project 'testproject' and app 'testapp'", output)

    def test_create_command_no_directory(self):
        """Test command works without specifying directory"""
        current_dir = os.getcwd()
        try:
            os.chdir(self.test_dir)
            call_command(
                'create',
                'testproject',
                'testapp',
                stdout=self.stdout,
                stderr=self.stderr
            )

            # Check if project was created in current directory
            self.assertTrue(os.path.exists('testproject'))
            self.assertTrue(os.path.exists(os.path.join('testproject', 'testapp')))
        finally:
            os.chdir(current_dir)

    def test_installed_apps_formatting(self):
        """Test that app is added to INSTALLED_APPS with correct formatting"""
        call_command(
            'create',
            'testproject',
            'testapp',
            '--directory', self.test_dir,
            stdout=self.stdout,
            stderr=self.stderr
        )

        settings_path = os.path.join(self.test_dir, 'testproject', 'testproject', 'settings.py')
        with open(settings_path) as f:
            content = f.read()
            
        # Check that our app is properly formatted in INSTALLED_APPS
        self.assertRegex(
            content,
            r'INSTALLED_APPS\s*=\s*\[.*?\s+[\'"]testapp[\'"],?\n.*?\]',
            "App not properly formatted in INSTALLED_APPS"
        ) 