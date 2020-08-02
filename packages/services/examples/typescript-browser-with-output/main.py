"""
Copyright (c) Jupyter Development Team.
Distributed under the terms of the Modified BSD License.
"""
import os
import json
import os.path as osp
from jupyter_server.base.handlers import JupyterHandler, FileFindHandler
from jupyter_server.extension.handler import ExtensionHandlerMixin, ExtensionHandlerJinjaMixin
from jupyterlab_server import LabServerApp, LabConfig
from jupyter_server.utils import url_path_join as ujoin
from traitlets import Unicode


HERE = osp.dirname(__file__)

with open(os.path.join(HERE, 'package.json')) as fid:
    version = json.load(fid)['version']

def _jupyter_server_extension_paths():
    return [
        {
            'module': __name__,
            'app': ExampleApp
        }
    ]

class ExampleHandler(
    ExtensionHandlerJinjaMixin,
    ExtensionHandlerMixin,
    JupyterHandler
    ):
    """Handle requests between the main app page and notebook server."""

    def get(self):
        """Get the main page for the application's interface."""
        config_data = {
            # Use camelCase here, since that's what the lab components expect
            "appVersion": version,
            'baseUrl': self.base_url,
            'token': self.settings['token'],
            'fullStaticUrl': ujoin(self.base_url, 'static', self.name),
            'frontendUrl': ujoin(self.base_url, 'main/'),
        }
        return self.write(
            self.render_template(
                'index.html',
                static=self.static_url,
                base_url=self.base_url,
                token=self.settings['token'],
                page_config=config_data
                )
            )

class ExampleApp(LabServerApp):

    extension_url = '/example'
    name = 'main'
    app_name = 'JupyterLab Example Service'
    app_url = '/example_app'
    static_dir = os.path.join(HERE, 'build')
    templates_dir = os.path.join(HERE, 'templates')
    app_version = version
    app_settings_dir = os.path.join(HERE, 'build', 'application_settings')
    schemas_dir = os.path.join(HERE, 'build', 'schemas')
    themes_dir = os.path.join(HERE, 'build', 'themes')
    user_settings_dir = os.path.join(HERE, 'build', 'user_settings')
    workspaces_dir = os.path.join(HERE, 'build', 'workspaces')

    def initialize_handlers(self):
        """Add example handler to Lab Server's handler list.
        """
        self.handlers.append(
            ('/example', ExampleHandler)
        )


if __name__ == '__main__':
    ExampleApp.launch_instance()
