def compare_text_files(file1_path, file2_path):
    # Read the contents of the first file
    with open(file1_path, 'r') as file1:
        file1_content = file1.read()

    # Read the contents of the second file
    with open(file2_path, 'r') as file2:
        file2_content = file2.read()

    # Compare the contents of the two files
    if file1_content == file2_content:
        print("The contents of the two files are the same.")
    else:
        print("The contents of the two files are different.")

# Paths to the text files
file1_path = "gspan.txt"
file2_path = "gspan2.txt"

# Call the function to compare the text files
compare_text_files(file1_path, file2_path)
