import numpy as np
import random
from collections import deque
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer

---
THOUGHT_LOOPS = 3  


class RLDecisionAgent:
    def __init__(self, actions):
        self.q_table = {}  
        self.actions = actions
        self.alpha = 0.1  
        self.gamma = 0.9  
        self.epsilon = 0.3  

    def get_state_key(self, context_str):
        return hash(context_str.strip().lower())

    def choose_action(self, state):
        if random.random() < self.epsilon:
            return random.choice(self.actions)
        state_key = self.get_state_key(state)
        if state_key in self.q_table:
            return max(self.q_table[state_key], key=self.q_table[state_key].get)
        return random.choice(self.actions)

    def learn(self, state, action, reward):
        state_key = self.get_state_key(state)
        if state_key not in self.q_table:
            self.q_table[state_key] = {a: 0.0 for a in self.actions}
        old_value = self.q_table[state_key][action]
        self.q_table[state_key][action] = old_value + self.alpha * (reward - old_value)


class CognitiveContextEngine:
    def __init__(self, memory_size=5, actions=None):
        self.context_memory = deque(maxlen=memory_size)
        self.current_thought = ""
        self.tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
        self.model = GPT2LMHeadModel.from_pretrained("gpt2")
        self.agent = RLDecisionAgent(actions if actions else ["Explore", "Wait", "Ask", "Think"])

    def update_context(self, new_input: str):
        self.context_memory.append(new_input)
        self.build_thought()

    def score_context(self, context):
       
        return len(context)  

    def process_context(self, context: str):
        inputs = self.tokenizer.encode(context, return_tensors="pt")
        outputs = self.model.generate(inputs, max_length=80, num_return_sequences=1, no_repeat_ngram_size=2)
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True).strip()

    def build_thought(self):
        scored_memory = sorted(list(self.context_memory), key=self.score_context, reverse=True)
        combined_context = " ".join(scored_memory[:3])  # Take top 3 by importance
        thought = combined_context
        for _ in range(THOUGHT_LOOPS):
            thought = self.process_context(thought)
        self.current_thought = thought

    def make_decision(self):
        context_state = " ".join(self.context_memory)
        action = self.agent.choose_action(context_state)
        return action

    def feedback(self, action, reward=1.0):
        state = " ".join(self.context_memory)
        self.agent.learn(state, action, reward)

    def output(self):
        return self.current_thought


class AGISimulation:
    def __init__(self):
        self.agi = CognitiveContextEngine(memory_size=5, actions=["Explore", "Wait", "Ask", "Think", "Act"])

    def run(self, inputs):
        for input_text in inputs:
            print(f"Input: {input_text}")
            self.agi.update_context(input_text)
            thought = self.agi.output()
            decision = self.agi.make_decision()
            print(f"Thought: {thought}")
            print(f"Decision: {decision}\n")
            self.agi.feedback(decision, reward=random.uniform(0, 1))  


if __name__ == "__main__":
    simulation = AGISimulation()
    inputs = [
        "The moon is full tonight and the forest is quiet.",
        "I hear a distant howl. Could it be a wolf?",
        "I must find a place to rest before sunrise.",
    ]
    simulation.run(inputs)

