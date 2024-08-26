import logic

generator = logic.TruthTableGenerator()

generated = generator.generate_truth_table("a & b | c # d")

for result in generated:
    print(result, generated[result])