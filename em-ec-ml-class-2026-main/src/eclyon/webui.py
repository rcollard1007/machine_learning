import os
from pathlib import Path

import dill
import gradio as gr
import numpy as np
import pandas as pd
import yaml
from PIL import Image

from eclyon.transforms import process_df

# validation set given in notebook
N_VALID = 12000


def load_resources(data_path: str, model_path: str, images_path: str) -> dict:
    """
    Load data, regression model and bulldozer images.
    """
    # import raw data
    df_raw = pd.read_feather(data_path)

    # preprocess data
    x, y, nas = process_df(df_raw, "SalePrice")
    x, y = x[N_VALID:], y[N_VALID:]

    # load regression model
    with open(model_path, "rb") as file:
        model = dill.load(file)

    # load bulldozer images
    imgs = []
    for img_file in os.listdir(images_path):
        img = Image.open(os.path.join(images_path, img_file))
        imgs.append(np.array(img))

    return {"X": x, "y": y, "model": model, "imgs": imgs}


def build_webui(config_path: str | Path) -> gr.Blocks:
    """
    A webui app displaying bulldozer estimated vs. real prices.
    """
    with open(config_path) as f:
        config = yaml.safe_load(f)
    res = load_resources(**config)

    def show_bulldozer(index):
        """
        Return image, estimated price, real price and features of a bulldozer.
        """
        if index is None:
            return None, "", "", None
        index = int(index)

        img = res["imgs"][index % len(res["imgs"])]

        row = res["X"].values[index]
        pred_price = int(np.exp(res["model"].predict([row])[0]))
        true_price = int(np.exp(res["y"][index]))

        features = pd.DataFrame({"Feature": res["X"].columns, "Value": [str(v) for v in row]})
        return img, f"{pred_price} Euros", f"{true_price} Euros", features

    with gr.Blocks(title="Choose a bulldozer") as demo:
        gr.Markdown("# Choose a bulldozer")
        index = gr.Dropdown(
            choices=list(range(1, N_VALID + 1)),
            value=None,
            label="Choose a bulldozer index",
        )
        gr.Markdown("## Selected bulldozer")
        image = gr.Image(label="Bulldozer", interactive=False, height=400)
        with gr.Row():
            pred = gr.Textbox(label="Estimated price", interactive=False)
            gold = gr.Textbox(label="Real price", interactive=False)
        gr.Markdown("## Bulldozer features")
        table = gr.Dataframe(interactive=False)

        index.change(show_bulldozer, index, [image, pred, gold, table])
    return demo


def run_webui(config_path: str | Path):
    """
    Launch the bulldozer price webui.
    """
    build_webui(config_path).launch(footer_links=["settings"])
