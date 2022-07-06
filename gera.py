from cardig.generator import Generator
import toml

config = toml.load('config.toml')
Generator.from_configs(config)
