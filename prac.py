import tkinter as tk

# Function to eliminate useless symbols in the CFG
def eliminate_useless_symbols(cfg_input_text):
    productions = {}
    non_terminals = set()
    terminals = set()

    # Split input text into lines and process each line
    lines = cfg_input_text.split('\n')
    for line in lines:
        line = line.strip()
        if line:
            parts = line.split('->')
            lhs = parts[0].strip()
            rhs = parts[1].strip()

            non_terminals.add(lhs)
            symbols = rhs.split('|')
            productions[lhs] = symbols
            for symbol in symbols:
                for char in symbol:
                    if not char.isupper() and char != 'ε':
                        terminals.add(char)

    # Find reachable symbols
    reachable = set()
    reachable.add('S')  # Starting symbol, change to your specific starting symbol

    while True:
        updated = False
        for non_terminal in productions:
            for symbols in productions[non_terminal]:
                if all((s in reachable or not s.isupper() or s == 'ε') for s in symbols):
                    if non_terminal not in reachable:
                        updated = True
                        reachable.add(non_terminal)

        if not updated:
            break

    # Find non-reachable non-terminals
    non_reachable = non_terminals - reachable

    # Remove non-reachable non-terminals from productions' right-hand side
    for non_terminal in non_reachable:
        productions.pop(non_terminal, None)
        for key, values in productions.items():
            productions[key] = [s for s in values if not any(c in s for c in non_reachable)]

    # Clean empty productions and terminals
    productions = {key: [p for p in prod if p] for key, prod in productions.items()}
    terminals.discard('')  # Remove empty string if it exists

    # Construct the updated CFG text without useless symbols
    updated_cfg = []
    for nt in productions:
        symbols = '|'.join(productions[nt])
        updated_cfg.append(f"{nt} -> {symbols}")

    return '\n'.join(updated_cfg)

# Function to process the CFG input
def process_cfg():
    input_text = input_textbox.get("1.0", "end-1c")  # Get text from input textbox
    result = eliminate_useless_symbols(input_text)
    output_textbox.delete(1.0, "end")  # Clear previous content in output textbox
    output_textbox.insert("end", result)  # Display the result in output textbox

# Create the main application window
app = tk.Tk()
app.title("CFG Useless Symbols Eliminator")

# Input Textbox
input_label = tk.Label(app, text="Enter CFG:")
input_label.pack()

input_textbox = tk.Text(app, height=10, width=40)
input_textbox.pack()

# Output Textbox
output_label = tk.Label(app, text="Output:")
output_label.pack()

output_textbox = tk.Text(app, height=10, width=40)
output_textbox.pack()

# Process Button
process_button = tk.Button(app, text="Process CFG", command=process_cfg)
process_button.pack()

# Start the GUI application
app.mainloop()
