from extra.config_manager import ConfigManager
from extra.diacritizer import Diacritizer, CBHGDiacritizer
import torch


def myDiacritize(original: str) -> str:
    config = ConfigManager(
        config_path='extra/log_dir/CA_MSA.base.cbhg/config.yml', model_kind='cbhg')
    diacritizer = CBHGDiacritizer(
        config_path='extra/log_dir/CA_MSA.base.cbhg/config.yml', model_kind='cbhg', load_model=True)
    model, _ = config.load_model()
    adz = Diacritizer(config_path='extra/log_dir/CA_MSA.base.cbhg/config.yml',
                      model_kind='cbhg', load_model=True)
    tensor = torch.LongTensor(
        [adz.diacritize_text(original), adz.diacritize_text(original)])
    out = model(src=tensor)['diacritics']
    softMax = torch.nn.Softmax(2)
    predictions = torch.max(out, 2).indices
    for src, prediction in zip(tensor, predictions):
        sentence = diacritizer.text_encoder.combine_text_and_haraqat(
            list(src.detach().cpu().numpy()),
            list(prediction.detach().cpu().numpy()),
        )
    return sentence
