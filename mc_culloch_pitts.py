# McCulloch-Pitts Neuron (1943)
# Einfaches binäres Schwellenwert-Neuron

import numpy as np

def mcp_neuron(inputs, weights, bias, threshold=0):
    """
    McCulloch-Pitts Neuron
    inputs: Eingabevektor (binär 0 oder 1)
    weights: Gewichtevektor
    bias: Bias (schwellenwertverschiebung)
    threshold: Schwellenwert (standard 0)
    Ausgabe: 1 wenn weighted sum + bias >= threshold, sonst 0
    """
    weighted_sum = np.dot(inputs, weights) + bias
    return 1 if weighted_sum >= threshold else 0

# Beispiel: Umsetzung der AND-Funktion
# AND: x1 AND x2 = 1 nur wenn beide 1 sind
print("AND-Funktion mit McCulloch-Pitts Neuron:")
weights_and = [1, 1]  # Beide Eingaben gleich wichtig
bias_and = -1.5       # Schwellenwert so setzen, dass nur bei (1,1) Ausgabe 1
test_cases = [[0,0], [0,1], [1,0], [1,1]]
for inputs in test_cases:
    out = mcp_neuron(inputs, weights_and, bias_and, threshold=0)
    print(f"AND({inputs[0]}, {inputs[1]}) = {out}")

print("\n" + "="*50 + "\n")

# Beispiel: OR-Funktion
# OR: x1 OR x2 = 1 wenn mindestens eine Eingabe 1 ist
print("OR-Funktion mit McCulloch-Pitts Neuron:")
weights_or = [1, 1]
bias_or = -0.5       # Schwellenwert so setzen, dass bei mindestens einer 1 Ausgabe 1
for inputs in test_cases:
    out = mcp_neuron(inputs, weights_or, bias_or, threshold=0)
    print(f"OR({inputs[0]}, {inputs[1]}) = {out}")

print("\n" + "="*50 + "\n")

# Beispiel: NOT-Funktion (eine Eingabe)
print("NOT-Funktion mit McCulloch-Pitts Neuron:")
weights_not = [-1]   # Negative Gewicht für Negation
bias_not = 0.5
test_cases_not = [[0], [1]]
for inputs in test_cases_not:
    out = mcp_neuron(inputs, weights_not, bias_not, threshold=0)
    print(f"NOT({inputs[0]}) = {out}")

print("\n" + "="*50 + "\n")

# Beispiel: XOR-Problem (zeigt Grenzen des einzelnen MCP-Neurons)
# XOR kann nicht mit einem einzelnen MCP-Neuron gelöst werden
print("XOR-Versuch mit einem MCP-Neuron (wird scheitern):")
# Wir versuchen verschiedene Gewichte und Bias, aber es ist unmöglich
weights_xor = [1, 1]
bias_xor = -0.5  # Dies ist eigentlich OR
for inputs in test_cases:
    out = mcp_neuron(inputs, weights_xor, bias_xor, threshold=0)
    print(f"XOR({inputs[0]}, {inputs[1]}) versucht = {out} (erwartet: {inputs[0] ^ inputs[1]})")

print("\nDies zeigt, dass ein einzelnes MCP-Neuron (wie ein Perzeptron) nicht-linear trennbare Probleme wie XOR nicht lösen kann.")