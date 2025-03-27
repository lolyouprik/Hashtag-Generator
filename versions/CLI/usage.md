### Key Features

1. **Core Hashtag Generation**: Transforms text into properly formatted hashtags
2. **Settings Management**: Supports the same customization options as the GUI version
3. **History Tracking**: Maintains a history of generated hashtags
4. **File I/O Support**: Can import from and export to files
5. **Cross-Platform Compatibility**: Works on Windows, macOS, and Linux with OS-specific config paths

### Usage

1. **Basic usage** - Convert text to a hashtag:

   ```bash
   python main.py -t "Hashtag Generator App"
   # Output: #HashtagGeneratorApp
   ```

2. **Import from file**:

   ```bash
   python main.py -i input.txt
   ```

3. **Export to file**:

   ```bash
   python main.py -t "Hashtag Generator App" -o output.txt
   ```

4. **Pipe text from another command**:

   ```bash
   echo "Hashtag Generator App" | python main.py
   ```

5. **Customize settings**:

   ```bash
   python main.py --keep-special --no-capitalize -t "Hello World!"
   ```

6. **View history**:

   ```bash
   python main.py --history
   ```

7. **Clear history**:

   ```bash
   python main.py --clear-history
   ```

8. **View current settings**:

   ```bash
   python main.py --settings
   ```
