import yaml
from argparse import ArgumentParser
from functools import lru_cache
import pathlib
import os


def load_config(config_file):
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)
    return config


def get_args():


    parser = ArgumentParser(description='Program RPA template')
    parser.add_argument("--robot_dir", dest="robot_dir",
                    help="write conda directory")

    parser.add_argument("-d", "--output_dir", dest="output_dir",
                    help="write output directory")

    parser.add_argument("--variable", action='append', nargs=1, metavar='KEY:VALUE',
                    dest="variables", help="write params variables")

    parser.add_argument("-f", "--filepath", dest="filepath",
                    help="write robot filepath")

    return parser.parse_args()


class BaseConfig:
    args = get_args()
    robot_dir: pathlib.Path = pathlib.Path(os.getcwd())
    if args.robot_dir is not None:
        robot_dir = pathlib.Path(args.robot_dir)
    output_dir: pathlib.Path = robot_dir / 'results'
    if args.output_dir is not None:
        output_dir = pathlib.Path(args.output_dir)
    filepath: pathlib.Path | None = None
    if args.filepath is not None:
        filepath = pathlib.Path(args.filepath)

    config_file: pathlib.Path = pathlib.Path(robot_dir) / "YamlVariables.yml"
    variables = load_config(config_file)
@lru_cache
def get_settings():
    return BaseConfig()

settings: BaseConfig = get_settings()

if not settings.output_dir.is_dir():
    settings.output_dir.mkdir()
