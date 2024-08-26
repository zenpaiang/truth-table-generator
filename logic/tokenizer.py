import sys

class TokenType:
    BRACKET = 0
    OPERATOR = 1
    LITERAL = 2
        
class LiteralToken:
    def __init__(self, expression: str, applyNot: bool):
        self.actual = ("~" if applyNot else "") + expression
        self.expression = expression
        self.applyNot = applyNot
        
    def __str__(self):
        return f"LiteralToken(expression={self.expression}, actual={self.actual}, applyNot={self.applyNot})"
        
class OperatorToken:
    def __init__(self, expression: str):
        self.expression = expression
        
    def __str__(self):
        return f"OperatorToken(expression={self.expression})"
        
class BracketToken:
    def __init__(self, expression: str, applyNot: bool):
        self.expression = expression
        self.actual = ("~" if applyNot else "") + f"({expression}"
        self.tokens: list[LiteralToken | OperatorToken] = []
        self.applyNot = applyNot
        
        bracketDepth = 0
        charBuffer = ""
        tokenBuffer = []
        applyNot = False
        
        if expression.count("(") != expression.count(")"):
            print("error: unmatched brackets")
            sys.exit()
            
        counter = 0
        
        for index, char in enumerate(expression):
            if bracketDepth == 0:
                if char in "&|#":
                    tokenBuffer.append(
                        OperatorToken(
                            expression=char
                        )
                    )
                    
                    charBuffer = ""
                elif char in "abcdefghijklmnopqrstuvwxyz":
                    tokenBuffer.append(
                        LiteralToken(
                            expression=char,
                            applyNot=index != 0 and expression[index - 1] == "~"
                        )
                    )
                    charBuffer = ""
                elif char in " ~()":
                    pass
                else:
                    print("error: invalid syntax")
                    sys.exit()
                    
            if bracketDepth > 0 and not char == ")":
                charBuffer += char
            if char == "(":
                if counter != 0 and expression[counter - 1] == "~":
                    applyNot = True
                    
                bracketDepth += 1
            if char == ")" and bracketDepth > 1:
                charBuffer += char
                bracketDepth -= 1
            elif char == ")" and bracketDepth == 1:
                bracketDepth -= 1
                tokenBuffer.append(
                    BracketToken(
                        expression=charBuffer, 
                        applyNot=applyNot
                    )
                )
                
                charBuffer = ""
                
            counter += 1
            
        if bracketDepth:
            print("error: unmatched brackets")
            sys.exit()
            
        self.tokens = tokenBuffer     
        
    def __str__(self):
        tokenstrs = []
        
        for token in self.tokens:
            if isinstance(token, LiteralToken):
                display = f"LiteralToken(expression={token.expression}, actual={token.actual}, applyNot={token.actual})"
            elif isinstance(token, OperatorToken):
                display = f"OperatorToken(expression={token.expression})"
            elif isinstance(token, EvaluatedToken):
                display = f"EvaluatedToken(value={token.value})"
        
            tokenstrs.append(display)
            
        tkns = ", ".join(tokenstrs)
        
        return f"BracketToken(expression={self.expression}, actual={self.actual}), tokens=[{tkns}], applyNot={self.applyNot})"
    
class EvaluatedToken:
    def __init__(self, value: bool):
        self.value = value
        
    def __str__(self) -> str:
        return f"EvaluatedToken(value={self.value})"
        
class Tokenizer:
    def tokenize(self, expression: str):
        bracketDepth = 0
        charBuffer = ""
        tokenBuffer = []
        applyNot = False
        
        if expression.count("(") != expression.count(")"):
            print("error: unmatched brackets")
            sys.exit()
            
        counter = 0
        
        for index, char in enumerate(expression):
            if not bracketDepth:
                if char in "&|#":
                    tokenBuffer.append(
                        OperatorToken(
                            expression=char
                        )
                    )
                    
                    charBuffer = ""
                elif char in "abcdefghijklmnopqrstuvwxyz":         
                    tokenBuffer.append(
                        LiteralToken(
                            expression=char,
                            applyNot=index != 0 and expression[index - 1] == "~"
                        )
                    )
                    charBuffer = ""
                elif char in " ~()":
                    pass
                else:
                    print("error: invalid syntax")
                    sys.exit()
                    
            if bracketDepth > 0 and not char == ")":
                charBuffer += char
            if char == "(":
                if counter != 0 and expression[counter - 1] == "~":
                    applyNot = True
                    
                bracketDepth += 1
            if char == ")" and bracketDepth > 1:
                charBuffer += char
                bracketDepth -= 1
            elif char == ")" and bracketDepth == 1:
                bracketDepth -= 1
                tokenBuffer.append(
                    BracketToken(
                        expression=charBuffer, 
                        applyNot=applyNot
                    )
                )
                charBuffer = ""
                
            counter += 1
            
        if bracketDepth:
            print("error: unmatched brackets")
            sys.exit()
            
        return tokenBuffer