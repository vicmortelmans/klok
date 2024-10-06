#!/usr/bin/env python
import sys
import re

def slow_down_abc_tempo(input_stream, factor=5):
    # Read the entire ABC file from stdin
    abc_content = input_stream.read()

    # Find the "Q" field using a regular expression to handle formats like Q:1/4=200
    q_pattern = re.compile(r"(Q:\s*\d+/\d+=)(\d+)", re.IGNORECASE)
    
    # Function to slow down the tempo
    def modify_tempo(match):
        original_q_value = int(match.group(2))
        new_q_value = original_q_value // factor
        return f"{match.group(1)}{new_q_value}"

    # Substitute the Q value with the slowed down tempo
    new_abc_content = re.sub(q_pattern, modify_tempo, abc_content)

    # Output the modified ABC content
    return new_abc_content

if __name__ == "__main__":
    # Read from stdin
    input_stream = sys.stdin
    modified_content = slow_down_abc_tempo(input_stream)

    # Print the modified content to stdout
    sys.stdout.write(modified_content)

