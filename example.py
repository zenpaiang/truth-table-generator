import logic

generator = logic.TruthTableGenerator()

generated = generator.generate_truth_table("a & b")

for result in generated:
    print(result, generated[result])