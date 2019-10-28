import argparse
import sys
import os
import json

from torinaku.app.config.options import OPTIONS
from torinaku.app.config.exceptions import InvalidOptionValue


class CombinedArgumentParser:
    """
    Parses arguments from a multitude of sources.

    In order of precedence:
    *   Command line args
    *   Environment variables
    *   Configuration file (JSON)

    Parameter names are converted as (consider `parameter_name`):
    *   Command line arg: `--parameter-name` (notice how `_` changed to `-`)
    *   Environment variable: `TORINAKU_PARAMETER_NAME`
    *   Configuration file: `{"parameter_name": "value"}`
    """

    def __init__(self):
        self.cmdline_parser = argparse.ArgumentParser()
        self._add_cmdline_args()

        self.validator_map = {
            validator.__name__: validator for validator in OPTIONS
        }

    def _unpack_option(self, option):
        return (
            option.__name__,
            list(option.__annotations__.values())[0],
            option.__doc__
        )

    def _add_cmdline_args(self):
        self.cmdline_parser.add_argument("--config", "-c", help="Config file path",
                                         required=False)
        for validator in OPTIONS:
            name, type_, desc = self._unpack_option(validator)
            name = name.replace("_", "-")
            if type_ != bool:
                self.cmdline_parser.add_argument(f"--{name}", help=desc, required=False)
            else:
                self.cmdline_parser.add_argument(f"--{name}", help=desc, required=False,
                                                 action="store_true")

    def _set_config_value(self, config, key, value):
        try:
            config[key] = self.validator_map[key](value)
        except Exception as e:
            raise InvalidOptionValue(key, str(e))

    def _validate(self, config):
        validated_config = {}
        for key, value in config.items():
            self._set_config_value(validated_config, key, value)
        return validated_config

    def parse_args(self):
        config = {}

        args = vars(self.cmdline_parser.parse_args(sys.argv[1:]))
        config_path = args.pop("config", None)
        if config_path:
            with open(config_path, "r") as f:
                data = json.load(f)
            for key, value in data.items():
                config[key] = value

        for key, value in os.environ.items():
            if key.startswith("TORINAKU_"):
                name = key[len("TORINAKU_"):].lower()
                config[name] = value

        for key, value in args.items():
            if value or not config.get(key):  # override only if not None
                config[key] = value

        return self._validate(config)
