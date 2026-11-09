from fire import Fire

from eclyon.webui import run_webui


def main():
    Fire({"webui": run_webui})
