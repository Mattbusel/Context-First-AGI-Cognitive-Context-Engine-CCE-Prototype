import numpy as np
import random
from collections import deque
from sklearn.preprocessing import StandardScaler
from transformers import GPT2LMHeadModel, GPT2Tokenizer


class CognitiveContextEngine:
    def __init__(self, memory_size=5):
        self.context_memory = deque(maxlen=memory_size)  
        self.current_thought = ""
        self.scaler = StandardScaler()  
        self.model = GPT2LMHeadModel.from_pretrained("gpt2")  
        self.tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

    def update_context(self, new_input: str):
        """
        Add a new input to the context memory and update the current thought.
        """
        self.context_memory.append(new_input)
        self.build_thought()

    def build_thought(self):
        """
        Build a thought by combining the latest inputs and processing through the cognitive engine.
        This is where reasoning and context-building happens before any output is generated.
        """
       
        context = " ".join(self.context_memory)
        self.current_thought = self.process_context(context)

    def process_context(self, context: str):
        """
        Process the accumulated context to generate a thought using cognitive processes.
        Here, we simulate this with GPT-2's next word prediction as a placeholder for reasoning.
        """
        inputs = self.tokenizer.encode(context, return_tensors="pt")
        outputs = self.model.generate(inputs, max_length=100, num_return_sequences=1, no_repeat_ngram_size=2)
        thought = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return thought.strip()

    def make_decision(self, action_choices: list):
        """
        Make a decision based on the context and current thought.
        In a real AGI system, this would involve deeper reasoning.
        """
        decision = random.choice(action_choices)  
        return decision

    def output(self):
        """
        Return the current thought as the output, simulating AGI's response based on context.
        """
        return self.current_thought


class AGISimulation:
    def __init__(self):
        self.agi = CognitiveContextEngine(memory_size=5)  
        self.action_choices = ["Move Left", "Move Right", "Jump", "Think about options"]
    
    def run(self, inputs):
        """
        Run the AGI system by feeding inputs and making decisions.
        """
        for input_text in inputs:
            self.agi.update_context(input_text)  
            thought = self.agi.output()  
            print(f"Context: {input_text}")
            print(f"Thought: {thought}")
            
           
            decision = self.agi.make_decision(self.action_choices)
            print(f"Decision: {decision}\n")
    

if __name__ == "__main__":
    inputs = [
        "The weather is cloudy and cold.",
        "I need to find a shelter from the storm.",
        "I am feeling hungry and tired."
    ]

    simulation = AGISimulation()
    simulation.run(inputs)
