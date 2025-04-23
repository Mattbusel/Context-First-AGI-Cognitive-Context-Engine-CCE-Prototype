from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

class TransformerEngine:
    def __init__(self, model_name="gpt2", device=None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name).to(self.device)
        self.model.eval()

    def generate_response(self, context, max_length=150):
        inputs = self.tokenizer(context, return_tensors="pt").to(self.device)
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_length=max_length,
                temperature=0.7,
                top_p=0.95,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

    def tokenize_input(self, text):
        return self.tokenizer.encode(text, return_tensors="pt").to(self.device)

    def get_hidden_states(self, text):
        tokens = self.tokenize_input(text)
        with torch.no_grad():
            outputs = self.model

