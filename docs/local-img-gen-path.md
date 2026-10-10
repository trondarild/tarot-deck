# Local image generation path

Plan for generating card artwork locally on an M1 Pro with 16 GB, at no cost per image. Researched 2026-10-10; check the Hugging Face pages before relying on the details.

## Model

- **Use:** Z-Image-Turbo, 4-bit, run with [mflux](https://github.com/filipstrand/mflux). The pre-quantized repo is `filipstrand/Z-Image-Turbo-mflux-4bit`, from the mflux author. The base model `Tongyi-MAI/Z-Image-Turbo` is reported as Apache 2.0, and produces an image in about 9 steps.
- **Avoid** full-precision downloads (about 31 GB for Z-Image, 34 GB for FLUX.1) and quantizing on this machine: one report saw a memory peak of about 31 GB during conversion.
- **Alternative:** FLUX.2 [klein] 4B, also reported as Apache 2.0. Its 9B sibling and FLUX.2 dev are non-commercial only.

## Before downloading

1. Keep about 15 GB of disk free. Models go to `~/.cache/huggingface/hub`; set `HF_HOME` to move them.
2. On the repo page, confirm the file list, size and licence; neither the size nor the 4-bit copy's licence was confirmed in research.
3. Prefer `.safetensors` files.
4. No Hugging Face login is needed for this repo; gated models such as FLUX.1-dev need a token.

## Steps

```bash
brew install uv
uv tool install --upgrade mflux
uv tool install --upgrade huggingface_hub
hf download filipstrand/Z-Image-Turbo-mflux-4bit
```

Close memory-heavy apps, then generate one test card. Width and height should be multiples of 16; 768 × 1296 is close to the cards' 1:1.7 ratio.

```bash
mflux-generate-z-image-turbo --model filipstrand/Z-Image-Turbo-mflux-4bit \
  --prompt "<card prompt>" --width 768 --height 1296 --steps 9 --seed 1 \
  --output assets/img/zen/maj00.jpg
```

- Check the output flag with `mflux-generate-z-image-turbo --help`.
- If memory runs out, try `--low-ram` or `--mlx-cache-limit-gb`.
- No M1 Pro benchmark was found; expect tens of seconds to a few minutes per image.

## Where the images go

- **Prompts:** in `docs/zen-buddhism-illustration-descriptions.md` and `docs/pessimistic-philosophy-illustration-description.md`. Each is self-contained.
- **Files:** save each image as `assets/img/zen/majNN.jpg` or `assets/img/pessimistic/majNN.jpg`, where `NN` is the two-digit card number. This replaces the placeholder, and the site needs no other change.
- **Restoring:** to regenerate a placeholder, delete the file and run `python3 tools/make_placeholders.py zen pessimistic`.

## Sources

- [mflux](https://github.com/filipstrand/mflux) and its [Z-Image README](https://github.com/filipstrand/mflux/blob/main/src/mflux/models/z_image/README.md)
- [Memory peak when quantizing with mflux-save on a Mac mini M2 Pro](https://zff.dev/CryptoJones/MacminiM2Pro_LocalModelConfig/pulls/2)
- [FLUX.2 klein licensing (VentureBeat)](https://venturebeat.com/technology/black-forest-labs-launches-open-source-flux-2-klein-to-generate-ai-images-in)
