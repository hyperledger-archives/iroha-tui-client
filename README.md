# Iroha TUI

A TUI client for [Hyperledger Iroha](https://github.com/hyperledger/iroha).
Works only with python3.6+.

### How to run

From the source directory:
```
$ python3 -m iroha_tui
```

### Options

```
$ python3 -m iroha_tui --help
usage: __main__.py [-h] [--config CONFIG]
                   [--persistence-file-path PERSISTENCE_FILE_PATH]

optional arguments:
  -h, --help            show this help message and exit
  --config CONFIG, -c CONFIG
                        Config file path
  --persistence-file-path PERSISTENCE_FILE_PATH
                        File path to persist transactions and queries to.
                        Needs to be both readable and writable.
```

## Configuration

There are several ways to set and option (in order of precedence):
*   Command-line argument.
*   Environment variable.
*   Configuration file.

Parameter names are converted as follows (consider `parameter_name`):
*   Command-line argument: `--parameter-name` (notice how `_` changed to `-`).
*   Environment variable: `IROHA_TUI_PARAMETER_NAME`.
*   Configuration file: `{"parameter_name": "value"}`.

### Configuration file

Configuration file is simple JSON. For example, consider this one:

```json
{
    "persistence_file_path": "/home/user/.config/iroha_tui/config.json"
}
```

This will set a parameter named `persistence_file_path` to that path.
You can also override any parameter first from environment, e.g.:

```
$ IROHA_TUI_PERSISTENCE_FILE_PATH=/home/user/.config/iroha_tui.json python3 -m iroha_tui
```

And also this can finally be overriden from command line arguments:

```
$ python3 -m iroha_tui --persistence-file-path /home/user/.config/iroha_tui.json
```

### Configuration options

*   `persistence_file_path` - path to a writable file to persist transactions and
    queries to.

    This file will automatically be created and managed. It is opened only on startup
    and on exit.

### Example setup for convenience

You can specify the config file using an environment variable, and configure persistence
for convenient launch using only `iroha_tui` without any parameters.

To do this, execute the following:
```
$ cat <<EOF > ~/.bash_profile
alias iroha_tui="iroha_tui -c ~/.config/iroha_tui/config.json"
EOF
$ mkdir -p ~/.config/iroha_tui
$ cat <<EOF > ~/.config/iroha_tui/config.json
{
    "persistence_file_path": "~/.config/iroha_tui/persistence.json"
}
```

