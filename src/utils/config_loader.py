import yaml

class ConfigLoader:
    def __init__(self, config_file='../config.yaml'):
        """
        Initializes the ConfigLoader with a YAML config file.

        :param config_file: Path to the YAML configuration file.
        """
        self.config_file = config_file
        self.config = None
        self.load_config()

    def load_config(self):
        """Loads the configuration from the YAML file."""
        try:
            with open(self.config_file, 'r') as file:
                self.config = yaml.safe_load(file)
            print('Config Loaded', self.config)
        except FileNotFoundError:
            raise Exception(f"Config file {self.config_file} not found.")
        except yaml.YAMLError as exc:
            raise Exception(f"Error parsing YAML: {exc}")

    def get(self, key, default=None):
        """
        Retrieve a configuration value by key.

        :param key: The key of the configuration value to retrieve.
        :param default: The default value to return if the key is not found.
        :return: The value from the config, or the default if not found.
        """
        if self.config:
            return self.config.get(key, default)
        else:
            raise Exception("Configuration has not been loaded.")

    def reload_config(self):
        """Reloads the configuration from the YAML file."""
        self.load_config()