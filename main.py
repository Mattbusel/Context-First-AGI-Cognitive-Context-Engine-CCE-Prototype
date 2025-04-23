from agi_core.cognitive_engine import AGISimulation

if __name__ == "__main__":
    simulation = AGISimulation()
    inputs = [
        "The moon is full tonight and the forest is quiet.",
        "I hear a distant howl. Could it be a wolf?",
        "I must find a place to rest before sunrise.",
    ]
    simulation.run(inputs)
