"""
Configuration related module

"""
import yaml
import logging as log



class Config:
    '''
    Creates a configuration using data from YAML file.
    Has ability to provide default values (including dynamic ones)
    Except for loading data, this class is read-only and therefore may be used from multiple threads.
    '''
    def __init__(self, cfg=None):
        if not cfg:
            cfg = {}
        self._cfg = cfg

    def __len__(self):
        return len(self._cfg)

    def __getitem__(self, key):
        ''' Works like "get()" '''
        return self.get(key)

    def get(self, key):
        try:
            return self._get(key)
        except KeyError:
            log.warning("%s not found in configuration file", key)
            raise KeyError(key)

    def _get(self, key):
        '''
        Gets data from multilevel dictionary using keys with dots.
        i.e. key="logging.file"
        Raises KeyError if there is no configured value and no default value for the given key.
        '''

        keys = key.split('.')

        curr = self._cfg
        for k in keys:
            if isinstance(curr, dict):
                curr = curr[k]
            elif isinstance(curr, list):
                curr = curr[int(k)]
            else:
                raise KeyError(k)

        if isinstance(curr, dict) or isinstance(curr, list):
            return Config(curr)
        else:
            return curr

    @property
    def cfg(self):
        '''
        Return list or dict configuration
        '''
        return self._cfg

    def load(self, file_name, defaults=None):
        '''
        Loads configuration from provided file name.

        Args:
            file_name(str) - YAML file name with configuration
            defaults(dict) - default values in a form of multilevel dictionary with optional callable objects
        '''
        if not defaults:
            defaults = {}
        defaults = self._simplify_defaults(defaults)

        with open(file_name, 'r') as stream:
            cfg = yaml.load(stream.read())
            self._cfg = self._recursive_merge(cfg, defaults)

        self._cfg['config_filename'] = file_name

    def _recursive_merge(self, data, defaults):
        #recursively replace defaults with configured data
        if isinstance(defaults, dict) and isinstance(data, dict):
            output = defaults.copy()
            for key, val in data.items():
                if key in output:
                    output[key] = self._recursive_merge(data[key], output[key])
                else:
                    output[key] = val
            return output
        elif isinstance(data, list) and isinstance(defaults, list):
            common = min(len(data), len(defaults))
            output = [self._recursive_merge(data[i], defaults[i]) for i in range(common)]
            output.extend(data[common:])
            output.extend(defaults[common:])
            return output
        else:
            return data

    def _simplify_defaults(self, defaults):
        if callable(defaults):
            return defaults()
        if isinstance(defaults, dict):
            return {key: self._simplify_defaults(val) for key, val in defaults.items()}
        if isinstance(defaults, list):
            return [self._simplify_defaults(val) for val in defaults]
        return defaults
