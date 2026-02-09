import modal

app = modal.App("flux-default-web")

image = modal.Image.debian_slim(python_version="3.10").pip_install(
    "diffusers",
    "transformers",
    "torch",
    "gradio",
    "sentencepiece",
)

@app.cls(image=image, gpu="A100")
class Model:
    @modal.enter()
    def load(self):
        import torch
        from diffusers import DiffusionPipeline

        self.pipe = DiffusionPipeline.from_pretrained(
            "black-forest-labs/FLUX.1-dev",
            torch_dtype=torch.bfloat16,
        ).to("cuda")

    @modal.method()
    def generate(self, prompt):
        return self.pipe(prompt, num_inference_steps=25).images[0]


@app.function(image=image)
@modal.asgi_app()
def fastapi_app():
    import gradio as gr
    from fastapi import FastAPI
    from gradio.routes import mount_gradio_app

    web_app = FastAPI()

    def go(text):
        return Model().generate.remote(text)

    with gr.Blocks() as demo:
        inp = gr.Textbox(label="Prompt")
        out = gr.Image()
        gr.Button("Generate").click(go, inp, out)

    return mount_gradio_app(web_app, demo, path="/")