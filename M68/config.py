from pathlib import Path

def get_config():
    return {
        "batch_size": 2,
        "num_epochs": 20,
        "lr": 10**-4,
        "seq_len": 300,
        "d_model": 512,
        "model_basename": "M68",
        "tokenizer_file": "M68/tokenizer_V2_{0}.json",
        "project_name": "runs/M68"
    }

def get_weights_file_path(config):
    model_folder = "M68/model_folder"
    weights_dir = Path(model_folder)
    weights_dir.mkdir(parents=True, exist_ok=True)
    model_filename = f"{config['model_basename']}.pt"
    return str(weights_dir / model_filename)
