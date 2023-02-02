import tomli, re, loguru
from os import getenv
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

class Consts:
    HOME = Path(__file__).parent.absolute()
    CONSTS = tomli.loads((HOME/"consts.toml").read_text())
    DISSES = CONSTS["disses"]
    NAMES = CONSTS["names"]
    TOKEN = getenv("TOKEN")
    GUILD = "Daddy Noel's Extended Family"
    OTHER_MSG = "joined left lost disconnected".split()