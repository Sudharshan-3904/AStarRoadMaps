from transformers import AutoTokenizer, AutoModel
from transformers.onnx import export
from pathlib import Path

model_id = "TheBloke/LLaMA-2-7B-fp16"  # Or the original HF model
output_path = Path("onnx-model")

# Export model to ONNX
export.preprocessor_export(
    model_id,
    output_path
)
# Qwen/Qwen3-Embedding-0.6B