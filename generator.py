import torch

def generate_images(pipe, prompt, width, height, num_images, seed, output_dir):
    generator = torch.Generator("cuda" if torch.cuda.is_available() else "cpu").manual_seed(seed)
    images = []
    for i in range(num_images):
        image = pipe(
            prompt,
            width=width,
            height=height,
            generator=generator,
            num_inference_steps=20,
            guidance_scale=7.0
        ).images[0]
        filename = f"{output_dir}/{prompt.replace(' ', '_')}_{seed}_{i+1}.png"
        image.save(filename)
        images.append(filename)
    return images