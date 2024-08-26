from .evaluator import Evaluator
from .tokenizer import Tokenizer

class TruthTableGenerator:
    def generate_truth_table(self, expression: str):
        tokenizer = Tokenizer()
        tokens = tokenizer.tokenize(expression)

        evaluator = Evaluator()
        evaluated = evaluator.evaluateMaps(tokens)
        
        rs = {}

        for map, result in evaluated:
            binary = "".join(["1" if value else "0" for value in map.values()])
            proper = "1" if result else "0"
            rs[binary] = proper
        return rs