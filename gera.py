from cardig.generator import Generator
import toml

config = toml.load('examples/config_1.toml')
Generator.from_configs(config)
