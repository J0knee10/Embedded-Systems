import sys
import os

# -----------------------------------------------------------------------------
# This is the function from your hex_to_c_array.txt file
# -----------------------------------------------------------------------------
def hex_to_c_array(hex_data, var_name):

  c_str = ''

  # Create header guard
  c_str += '#ifndef ' + var_name.upper() + '_H\n'
  c_str += '#define ' + var_name.upper() + '_H\n\n'

  # Add array length at top of file
  c_str += '\nunsigned int ' + var_name + '_len = ' + str(len(hex_data)) + ';\n'

  # Declare C variable
  c_str += 'unsigned char ' + var_name + '[] = {'
  hex_array = []
  for i, val in enumerate(hex_data) :

    # Construct string from hex
    hex_str = format(val, '#04x')

    # Add formatting so each line stays within 80 characters
    if (i + 1) < len(hex_data):
      hex_str += ','
    if (i + 1) % 12 == 0:
      hex_str += '\n '
    hex_array.append(hex_str)

  # Add closing brace
  c_str += '\n ' + format(' '.join(hex_array)) + '\n};\n\n'

  # Close out header guard
  c_str += '#endif //' + var_name.upper() + '_H'

  return c_str

# -----------------------------------------------------------------------------
# Main script logic to read the model and write the C header file
# -----------------------------------------------------------------------------
def main():
    # Check for correct command-line arguments
    if len(sys.argv) != 3:
        print("Usage: python convert_model.py <path/to/your_model.tflite> <path/to/output_model.h>")
        sys.exit(1)

    tflite_file_path = sys.argv[1]
    output_header_path = sys.argv[2]
    
    # The variable name in the C file is derived from the output filename
    # e.g., "cosine_model.h" becomes "cosine_model"
    # Ensure this matches the expected name in the Arduino sketch (e.g., "cosine_model")
    variable_name = os.path.splitext(os.path.basename(output_header_path))[0]

    print(f"Input TFLite file: {tflite_file_path}")
    print(f"Output C header file: {output_header_path}")
    print(f"C variable name: {variable_name}")

    try:
        # Read the binary content of the TFLite model
        with open(tflite_file_path, 'rb') as f:
            tflite_binary = f.read()
            # tflite_hex = tflite_binary.hex()

        # Call the function to convert the binary data to a C array string
        c_array_str = hex_to_c_array(tflite_binary, variable_name)

        # Write the C array string to the output header file
        with open(output_header_path, 'w') as f:
            f.write(c_array_str)
            
        print(f"\nSuccessfully converted model to {output_header_path}")

    except FileNotFoundError:
        print(f"\nError: Input file not found at {tflite_file_path}")
        sys.exit(1)
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
