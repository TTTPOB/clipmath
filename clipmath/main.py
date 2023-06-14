import base64
from io import BytesIO
from pathlib import Path

import click
import httpx
import pyperclip
import yaml
from PIL import Image, ImageGrab


class Config:
    app_key: str
    app_secret: str

    def __init__(self, app_key, app_secret) -> None:
        self.app_key = app_key
        self.app_secret = app_secret

    @classmethod
    def from_yaml(cls, path: Path):
        with open(path, "r") as f:
            config = yaml.safe_load(f)
        return cls(**config)

    @classmethod
    def default(cls):
        path = Path(click.get_app_dir("clipmath")) / "config.yaml"
        if not path.exists():
            raise Exception("Config file not found.")
        return cls.from_yaml(path)

    def to_yaml(self, path: Path):
        value_dict = {
            "app_key": self.app_key,
            "app_secret": self.app_secret,
        }
        with open(path, "w") as f:
            yaml.safe_dump(value_dict, f)


class Ocr:
    config: Config
    __baseurl = "https://open.ocrmath.com/v3/printed/ocr"

    def __init__(self, config: Config):
        self.config = config

    def ocr(self, image: Image):
        # base64, jpeg
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        image_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

        header = {
            "app_key": self.config.app_key,
            "app_secret": self.config.app_secret,
            "User-Agent": "clipmath",
        }

        data = {"base64": image_base64}
        # do the request
        resp = httpx.post(self.__baseurl, headers=header, data=data)
        if resp.status_code != 200:
            raise Exception("Request failed.")
        return resp.json()["data"]["latex"]


@click.group
def cli():
    pass


@cli.command()
def gen_config():
    config_dir = Path(click.get_app_dir("clipmath"))
    config_file = config_dir / "config.yaml"
    config_dir.mkdir(parents=True, exist_ok=True)
    if config_file.exists():
        click.echo("Config file already exists.")
        return
    app_key = click.prompt("App Key")
    app_secret = click.prompt("App Secret")
    config = Config(app_key, app_secret)
    config.to_yaml(config_file)
    click.echo("Config file generated.")


@cli.command()
def ocr():
    # get image from clipboard
    image = ImageGrab.grabclipboard()
    if image is None:
        click.echo("No image in clipboard.")
        return
    # init the client
    config = Config.default()
    ocr = Ocr(config)
    # do the ocr
    text = ocr.ocr(image)
    # set the result to clipboard
    pyperclip.copy(text)
