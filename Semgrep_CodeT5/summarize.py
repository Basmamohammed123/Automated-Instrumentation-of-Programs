import re
from transformers import AutoModel, AutoTokenizer

# Specify the checkpoint and device
checkpoint = "Salesforce/codet5p-220m-bimodal"
device = "cpu"  # Change to "cuda" if GPU is available

# Load the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(checkpoint, trust_remote_code=True)
model = AutoModel.from_pretrained(checkpoint, trust_remote_code=True).to(device)

# Input and output file paths
file_path = "functions.py"
output_file = "output.py"


# Function to extract individual functions from the code
def split_into_functions(code):
    """
    Splits a Python script into individual functions.
    """
    pattern = re.compile(r"(def .+?:\n(?: {4}.+\n?)*)")
    return pattern.findall(code)


# Function to add summary after the function header
def add_summary_to_function(function_code, summary):
    """
    Inserts the summary below the function header.
    """
    lines = function_code.splitlines()
    result = []
    for i, line in enumerate(lines):
        if i == 0:  # Function header
            result.append(line)
            result.append(f'    """ {summary} """')  # Add summary
        else:
            result.append(line)
    return "\n".join(result)


# Read the input file
with open(file_path, "r") as file:
    code = file.read()

# Split the code into individual functions
functions = split_into_functions(code)

# Annotate each function with a summary
annotated_functions = []
for func in functions:
    # Tokenize the function code
    input_ids = tokenizer(func, return_tensors="pt").input_ids.to(device)
    
    # Generate summary
    generated_ids = model.generate(input_ids, max_length=200)
    summary = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
    
    # Add the summary to the function
    annotated_function = add_summary_to_function(func, summary)
    annotated_functions.append(annotated_function)

# Combine the annotated functions back into a single code block
annotated_code = "\n\n".join(annotated_functions)

# Write the annotated code to the output file
with open(output_file, "w") as file:
    file.write(annotated_code)
