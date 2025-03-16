# Run this script to check if PyTorch is installed and if CUDA is available 
# before running the main.py script.


import torch


print(torch.__version__) # Shows the torch version
print(torch.version.cuda)  # Shows the CUDA version PyTorch was built with
print(torch.cuda.is_available())  # Should return True if CUDA is working

