# Before running the code, make sure to install:
# https://www.anaconda.com/docs/getting-started/miniconda/install
# You can check the available versions of PyTorch and other components here:
# https://pytorch.org/get-started/locally/
# https://pytorch.org/get-started/previous-versions/


import secrets
import string
import torch
# Uncomment the following line if you are using Hugging Face Inference API
#from huggingface_hub import InferenceClient
from diffusers import FluxPipeline
from transformers import pipeline, AutoTokenizer
import logging


logging.getLogger("transformers").setLevel(logging.ERROR)

def generate_random_string(length=64):
    alphabet = string.digits
    random_string = ''.join(secrets.choice(alphabet) for i in range(length))
    return random_string

random_seed = generate_random_string()
seed_value = abs(hash(random_seed)) % (2**32)
torch.manual_seed(seed_value)

model_id = "meta-llama/Llama-3.2-1B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_id)
text_pipe = pipeline(
    "text-generation",
    model=model_id,
    tokenizer=tokenizer,
    torch_dtype=torch.float16,
    device="cuda"
)

#-------------------
# max 2 token special random output
message = (
    f"Answer with max two words only: Think of a name for an item that can be sold. "
    f"The name must be a real word (noun or adjective with noun) and cannot include any non-alphabetic characters. "
    f"Provide only the name without any explanation or examples."
)

outputs = text_pipe(
    message,
    max_new_tokens=2,
    temperature=0.7,
    top_p=1.0,
    top_k=100000
)
#-------------------

#-------------------
# normal output
# message = (
#     f"I'm new to AI. "
#     f"Can you tell me what I can draw?"
# )

# outputs = text_pipe(
#     message,
#     max_new_tokens=64,
#     temperature=0.7,
#     top_p=1.0,
#     top_k=100000
# )
#-------------------

response_text = outputs[0]["generated_text"].strip()
response_text = " ".join(response_text.split()[len(message.split()):]).strip()
#-------------------
# for max 2 token special random output
response_text = ''.join(char for char in response_text if char not in string.digits and char not in string.punctuation)
#-------------------
print("GENERATED ITEM ============> < " + response_text + " >")


# $env:PYTORCH_CUDA_ALLOC_CONF="expandable_segments:True"
# in PowerShell (for other shells check how to set PYTORCH_CUDA_ALLOC_CONF="expandable_segments:True" variable) if failing with CUDA out of memory error


#-------------------
# Uncomment the following lines if you are using Hugging Face Inference API
#image_client = InferenceClient("black-forest-labs/FLUX.1-schnell", token="Your HF API token")
#image = image_client.text_to_image(response_text)
#-------------------
# Uncomment the following lines if you are using model locally
image_pipe = FluxPipeline.from_pretrained("black-forest-labs/FLUX.1-schnell", torch_dtype=torch.bfloat16)
image_pipe.enable_sequential_cpu_offload()
image = image_pipe(
    response_text,
    guidance_scale=0.0,
    output_type="pil",
    num_inference_steps=4,
    max_sequence_length=256,
    generator=torch.Generator("cpu").manual_seed(0)
).images[0]
#-------------------
image.show()

