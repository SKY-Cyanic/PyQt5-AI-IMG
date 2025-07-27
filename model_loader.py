from PyQt5.QtCore import QThread, pyqtSignal
import torch
from diffusers import StableDiffusionPipeline, StableDiffusionImg2ImgPipeline

class ModelLoader(QThread):
    finished = pyqtSignal(object, object)

    def run(self):
        model_id = "runwayml/stable-diffusion-v1-5"
        dtype = torch.float16 if torch.cuda.is_available() else torch.float32
        device = "cuda" if torch.cuda.is_available() else "cpu"

        pipe_txt2img = StableDiffusionPipeline.from_pretrained(
            model_id,
            torch_dtype=dtype,
            safety_checker=None,
            low_cpu_mem_usage=True
        ).to(device)

        pipe_img2img = StableDiffusionImg2ImgPipeline.from_pretrained(
            model_id,
            torch_dtype=dtype,
            safety_checker=None,
            low_cpu_mem_usage=True
        ).to(device)

        if torch.cuda.is_available():
            pipe_txt2img.unet.to(memory_format=torch.channels_last)
            pipe_img2img.unet.to(memory_format=torch.channels_last)
            torch.backends.cudnn.benchmark = True

        self.finished.emit(pipe_txt2img, pipe_img2img)