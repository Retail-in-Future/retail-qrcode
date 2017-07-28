import yaml


def read_yaml_config(cfg_file):
    config = None
    try:
        with open(cfg_file, "r") as stream:
            config = yaml.load(stream)
    except yaml.YAMLError as exc:
        print("Invalid cfg_file %s:%s" % (cfg_file, exc))

    return config


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
