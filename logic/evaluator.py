from .tokenizer import LiteralToken, OperatorToken, BracketToken, EvaluatedToken
import copy
import sys

class Evaluator:
    def __init__(self):
        self.variables = []
                
    def _xor(self, a: bool, b: bool) -> bool:
        return (a and not b) or (not a and b)
    
    def evaluateMaps(self, tokens: list):
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
            
        results = []
            
        for map in maps:
            newTokens = copy.deepcopy(tokens)
            results.append([map, self.evaluate(newTokens, map)])
            
        return results
    
    def evaluateBracket(self, bracket: BracketToken, map: dict) -> EvaluatedToken:
        for index, token in enumerate(bracket.tokens):
            if isinstance(token, BracketToken):
                bracket.tokens[index] = self.evaluateBracket(token, map)
        
        tokens = bracket.tokens
        value = self.evaluate(tokens, map)
        
        token = EvaluatedToken(not value if bracket.applyNot else value)
        
        return token
    
    def evaluate(self, tokens: list, map: dict) -> bool:
        for index, token in enumerate(tokens):
            if isinstance(token, BracketToken):
                tokens[index] = self.evaluateBracket(token, map)
        
        index = 0
        
        while index < len(tokens):
            currentToken = tokens[index]
            
            if isinstance(currentToken, OperatorToken):
                if index != 0:
                    leftToken = tokens[index - 1]
                    rightToken = tokens[index + 1]
                    
                    if isinstance(leftToken, OperatorToken) or isinstance(rightToken, OperatorToken):
                        print("error: invalid syntax")
                        sys.exit()
                        
                    if isinstance(leftToken, EvaluatedToken):
                        leftEval = leftToken.value
                    else:
                        leftEval = not map[leftToken.expression] if leftToken.applyNot else map[leftToken.expression]
                    
                    if isinstance(rightToken, EvaluatedToken):
                        rightEval = rightToken.value
                    else:
                        rightEval = not map[rightToken.expression] if rightToken.applyNot else map[rightToken.expression]
                        
                    if currentToken.expression == "&":
                        tokens[index] = EvaluatedToken(leftEval and rightEval)
                    elif currentToken.expression == "|":
                        tokens[index] = EvaluatedToken(leftEval or rightEval)
                    elif currentToken.expression == "#":
                        tokens[index] = EvaluatedToken(self._xor(leftEval, rightEval))
                        
                    tokens.pop(index - 1)
                    tokens.pop(index)
                    
                    index = 0
                else:
                    print("error: invalid syntax")
                    sys.exit()
        
            index += 1
            
        return tokens[0].value
        
    def _extract_bracket_literals(self, tokens: list) -> list:
        actualTokens = "".join([token.expression for token in tokens])
        literals = []
        
        for char in actualTokens:
            if char.isalpha() and char not in literals:
                literals.append(char)
                
        return literals
                        
    def generate_values(self, variables: int) -> list:
        return [("0" * (variables - len(bin(a).replace("0b", "")))) + (bin(a).replace("0b", "")) for a in range(pow(2, variables))] 