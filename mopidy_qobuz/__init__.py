from __future__ import unicode_literals

import os
from mopidy import config, ext


__version__ = '0.0.1'


class Extension(ext.Extension):

    dist_name = "Mopidy-Qobuz"
    ext_name = "qobuz"
    version = __version__

    def get_default_config(self):
        conf_file = os.path.join(os.path.dirname(__file__), "ext.conf")
        return config.read(conf_file)

    def get_config_schema(self):
        schema = super(Extension, self).get_config_schema()

        schema["username"] = config.String()
        schema["password"] = config.Secret()
        schema["app_id"] = config.String()
        schema["secrets"] = config.Secret()

        return schema

    def setup(self, registry):
        from mopidy_qobuz.backend import QobuzBackend

        registry.add("backend", QobuzBackend)
