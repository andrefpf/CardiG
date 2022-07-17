from cardig.generator import Generator
import toml

config = toml.load('examples/config.toml')
Generator.from_configs(config)
