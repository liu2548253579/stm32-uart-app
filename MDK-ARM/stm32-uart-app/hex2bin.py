#!/usr/bin/env python3
"""
STM32 HEX to BIN converter
This script converts Intel HEX files (.hex) to binary files (.bin) for STM32 microcontrollers.
"""

import sys
import os
import argparse
from intelhex import IntelHex

def hex_to_bin(input_file, output_file=None, start_addr=None, end_addr=None):
    """
    Convert a HEX file to BIN format
    
    Args:
        input_file (str): Path to the input HEX file
        output_file (str, optional): Path to the output BIN file. If None, uses input filename with .bin extension
        start_addr (int, optional): Start address for the binary file. If None, uses the minimum address in the HEX file
        end_addr (int, optional): End address for the binary file. If None, uses the maximum address in the HEX file
        
    Returns:
        tuple: (success, message)
    """
    try:
        # Check if input file exists
        if not os.path.isfile(input_file):
            return False, f"Error: Input file '{input_file}' not found."
        
        # Set default output file if not specified
        if output_file is None:
            output_file = os.path.splitext(input_file)[0] + '.bin'
        
        # Read the HEX file
        ih = IntelHex()
        ih.loadhex(input_file)
        
        # Get address range if not specified
        if start_addr is None:
            start_addr = ih.minaddr()
        if end_addr is None:
            end_addr = ih.maxaddr()
        
        # Write the BIN file
        ih.tobinfile(output_file, start_addr, end_addr)
        
        return True, f"Successfully converted {input_file} to {output_file}"
    
    except Exception as e:
        return False, f"Error during conversion: {str(e)}"

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Convert STM32 HEX files to BIN format')
    parser.add_argument('input', help='Input HEX file')
    parser.add_argument('-o', '--output', help='Output BIN file (default: input filename with .bin extension)')
    parser.add_argument('-s', '--start', type=lambda x: int(x, 0), help='Start address (default: minimum address in HEX file)')
    parser.add_argument('-e', '--end', type=lambda x: int(x, 0), help='End address (default: maximum address in HEX file)')
    args = parser.parse_args()
    
    # Convert the file
    success, message = hex_to_bin(args.input, args.output, args.start, args.end)
    
    # Print result
    print(message)
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
    
    