from .tokenizer import LiteralToken, OperatorToken, BracketToken, EvaluatedToken
import copy
import sys

class Evaluator:
    def __init__(self):
        self.variables = []
                
    def _xor(self, a: bool, b: bool) -> bool:
        return (a and not b) or (not a and b)

    def evaluateBracket(self, token: BracketToken, map: dict):
        for index, tkn in enumerate(token.tokens):
            if isinstance(tkn, BracketToken):
                token.tokens[index] = self.evaluateBracket(tkn, map)
        
        for index, tkn in enumerate(token.tokens):
            if isinstance(tkn, OperatorToken):
                if index != 0:
                    left = token.tokens[index - 1]
                    right = token.tokens[index + 1]
                    
                    if isinstance(left, OperatorToken) or isinstance(right, OperatorToken):
                        print("error: invalid syntax")
                        sys.exit()
                        
                    if isinstance(left, EvaluatedToken):
                        leftEval = left.value
                    else:
                        leftEval =  not map[left.expression] if left.applyNot else map[left.expression]
                        
                    if isinstance(right, EvaluatedToken):
                        rightEval = right.value
                    else:
                        rightEval = not map[right.expression] if right.applyNot else map[right.expression]
                
                if tkn.expression == "&":
                    return EvaluatedToken(not (leftEval and rightEval) if token.applyNot else (leftEval and rightEval))
                elif tkn.expression == "%":
                    return EvaluatedToken(not (leftEval or rightEval) if token.applyNot else (leftEval or rightEval))
                elif tkn.expression == "#":
                    return EvaluatedToken(not self._xor(leftEval, rightEval) if token.applyNot else self._xor(leftEval, rightEval))
                
                token.tokens.pop(index - 1)
                token.tokens.pop(index)
                
    def evaluate(self, tokens: list):
        # Create map for all the variables
        
        for token in tokens:
            if isinstance(token, LiteralToken) and token.expression not in self.variables:
                self.variables.append(token.expression) 
            elif isinstance(token, BracketToken):
                for variable in self._extract_bracket_literals(token.tokens):
                    if variable not in self.variables:
                        self.variables.append(variable)
        
        values = self.generate_values(len(self.variables))
        maps = []
        
        for value in values:
            currMap = {}
            
            for index, digit in enumerate(value):
                currMap[self.variables[index]] = True if digit == "1" else False
                
            maps.append(currMap)
            
        originalTokens = copy.deepcopy(tokens)
        
        results = []
            
        for map in maps:
            tokens = copy.deepcopy(originalTokens)
            
            for index, token in enumerate(tokens):
                if isinstance(token, BracketToken):
                    tokens[index] = self.evaluateBracket(token, map)
            
            for index, token in enumerate(tokens):
                if isinstance(token, OperatorToken):
                    if index != 0:
                        left = tokens[index - 1]
                        right = tokens[index + 1]
                    
                        if isinstance(left, OperatorToken) or isinstance(right, OperatorToken):
                            print("error: invalid syntax")
                            sys.exit()
                            
                        if isinstance(left, EvaluatedToken):
                            leftEval = left.value
                        else:
                            leftEval =  not map[left.expression] if left.applyNot else map[left.expression]
                            
                        if isinstance(right, EvaluatedToken):
                            rightEval = right.value
                        else:
                            rightEval = not map[right.expression] if right.applyNot else map[right.expression]
                
                        if token.expression == "&":
                            tokens[index] = EvaluatedToken(leftEval and rightEval)
                        elif token.expression == "%":
                            tokens[index] = EvaluatedToken(leftEval or rightEval)
                        elif token.expression == "#":
                            tokens[index] =  EvaluatedToken(self._xor(leftEval, rightEval))
                
                        tokens.pop(index - 1)
                        tokens.pop(index)
            
            results.append([map, tokens[0].value])
        
        return results
        
    def _extract_bracket_literals(self, tokens: list) -> list:
        actualTokens = "".join([token.expression for token in tokens])
        literals = []
        
        for char in actualTokens:
            if char.isalpha() and char not in literals:
                literals.append(char)
                
        return literals
                        
    def generate_values(self, variables: int) -> list:
        return [("0" * (variables - len(bin(a).replace("0b", "")))) + (bin(a).replace("0b", "")) for a in range(pow(2, variables))] 