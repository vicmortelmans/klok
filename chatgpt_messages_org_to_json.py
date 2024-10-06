#!/usr/bin/env python
import sys
import json

def org_to_json():
    quotes = []
    lines = sys.stdin.read().splitlines()

    in_quote_block = False
    quote_role = ""
    quote_content = []

    for line in lines:
        line = line.strip()

        if line.startswith("#+begin_quote"):
            # Extract the role (after #+begin_quote)
            quote_role = line[len("#+begin_quote"):].strip()
            in_quote_block = True
            quote_content = []
        elif line.startswith("#+end_quote") and in_quote_block:
            # End of the quote block, add the block to the list
            quotes.append({
                "role": quote_role,
                "content": "\n".join(quote_content).strip()
            })
            in_quote_block = False
        elif in_quote_block:
            # Add content to the current quote block
            quote_content.append(line)

    # Output the result as JSON to stdout
    json.dump(quotes, sys.stdout, indent=4)

# Example usage:
if __name__ == "__main__":
    org_to_json()

