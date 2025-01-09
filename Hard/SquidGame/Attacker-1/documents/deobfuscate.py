import re

def decode_chr(match):
    """Decode ChrW() expressions like ChrW(6 + 4) to readable characters."""
    expression = match.group(1)  # Extract the inner content of ChrW(...)
    try:
        # Evaluate the arithmetic inside ChrW
        result = eval(expression.strip())
        # Convert to character only if it's in the printable ASCII range
        if 32 <= result <= 126:
            decoded_char = chr(result)
            print(f"Decoding: {match.group(0)} -> {decoded_char}")  # Debug output
            return decoded_char
        else:
            # If not printable, retain the original expression
            print(f"Non-printable: {match.group(0)} retained.")
            return match.group(0)
    except Exception as e:
        print(f"Error decoding {match.group(0)}: {e}")
        return match.group(0)  # If decoding fails, return the original match

def deobfuscate_vba(input_text):
    """Deobfuscate the entire VBA code."""
    # Match all ChrW(...) expressions
    pattern = r'ChrW\(([^\)]+)\)'  # Regex to match content inside ChrW(...)
    decoded_text = re.sub(pattern, decode_chr, input_text)
    return decoded_text

def main():
    # Read the input text file
    with open("input.txt", "r") as file:
        input_text = file.read()
    
    # Deobfuscate the VBA code
    deobfuscated_text = deobfuscate_vba(input_text)
    
    # Save the output to a new file
    with open("deobfuscated_output.txt", "w") as output_file:
        output_file.write(deobfuscated_text)

    print("Deobfuscation completed. Check 'deobfuscated_output.txt' for results.")

if __name__ == "__main__":
    main()

