import os

def to_hashtag(text):
    words = text.split()
    hashtag = "#" + "".join(word.capitalize() for word in words)
    return hashtag

# Check if input.txt exists
if not os.path.exists("input.txt"):
    with open("input.txt", "w") as file:
        file.write("Enter your text here and rerun the script.")
    print("input.txt was not found, so it has been created. Please enter your text inside and run the script again.")
else:
    # Read from input.txt
    with open("input.txt", "r") as file:
        input_text = file.read().strip()
    
    # Convert to hashtag format
    output_text = to_hashtag(input_text)
    
    # Write to output.txt
    with open("output.txt", "w") as file:
        file.write(output_text)
    
    print("Hashtag generated and saved to output.txt!")
