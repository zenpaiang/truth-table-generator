# truth table generator

a truth table generator i wrote when learning about boolean logic in my computer science class

# bad code

this code has not been 100% tested so if you come across any wrong results or errors please open a pull request.

# usage and examples

### basic logic gates

`AND` (`&`) gate: `a & b`  
`OR` (`|`) gate: `a | b`  
`XOR` (`#`) gate: `a # b`  

### negation

negations are done with the `~` character, so `~(a & b)` would be a `NAND` gate.

`NOT` gate: `~a`

`NAND` gate: `~(a & b)`  
`NOR` gate: `~(a | b)`  
`XNOR` gate: `~(a # b)`  

# parsing method

the evaluator (`logic/evaluator.py`) parses from a left to right basis. here's an example:  

`a, b, c, d = true`

`a & b | c # d`    

1. evaluate `a & b` -> `true`
2. evaluate `true | c` -> `true`
3. evaluate `true # d` -> `false`

final result = `false`