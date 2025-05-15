tokens=[{'A':1},{'B':2},{"C":3},{"D":4},{'E':5},{'F':6},{"G":7},{"H":8},{'I':9},{'J':10},{"K":11},{"L":12},{'M':13},{'N':14},{"O":15},{"P":16},{'Q':17},{'R':18},{"S":19},{"T":20},{'U':21},{'V':22},
        {"W":23},{"X":24},{"Y":25},{"Z":26}]

# Step 1: Convert token list to a lookup dictionary
token_dict = {list(d.keys())[0]: list(d.values())[0] for d in tokens}

# Step 2: Tokenize the text
text = "I AM A GOOD GUY"
output_tokens = []

for char in text:
    if char == " ":
        continue  # skip spaces
    token_id = token_dict.get(char.upper())
    if token_id:
        output_tokens.append(token_id)

print(output_tokens)
