import os
import sys
import json
import argparse
from pathlib import Path


class HashtagGeneratorCLI:
    """Command Line Interface for the Hashtag Generator App"""

    def __init__(self):
        """Initialize the CLI with default settings"""
        self.history = []
        self.settings = {
            "remove_special_chars": False,
            "capitalize_first_letter": True,
            "history_max_items": 10,
        }
        self.config_dir = self._get_config_dir()
        self.load_settings()

    def _get_config_dir(self):
        """Get the appropriate configuration directory based on OS"""
        home = Path.home()
        
        if sys.platform == "win32":
            config_dir = home / "AppData" / "Local" / "HashtagGenerator"
        elif sys.platform == "darwin":
            config_dir = home / "Library" / "Application Support" / "HashtagGenerator"
        else:  # Linux and other Unix-like
            config_dir = home / ".config" / "hashtag-generator"
            
        # Create config directory if it doesn't exist
        config_dir.mkdir(parents=True, exist_ok=True)
        return config_dir

    def load_settings(self):
        """Load settings from config file if it exists"""
        config_file = self.config_dir / "config.json"
        history_file = self.config_dir / "history.json"
        
        if config_file.exists():
            try:
                with open(config_file, "r") as f:
                    self.settings.update(json.load(f))
            except Exception as e:
                print(f"Warning: Could not load settings: {e}", file=sys.stderr)

        if history_file.exists():
            try:
                with open(history_file, "r") as f:
                    self.history = json.load(f)
            except Exception as e:
                print(f"Warning: Could not load history: {e}", file=sys.stderr)

    def save_settings(self):
        """Save settings to config file"""
        config_file = self.config_dir / "config.json"
        history_file = self.config_dir / "history.json"
        
        try:
            with open(config_file, "w") as f:
                json.dump(self.settings, f, indent=2)
                
            with open(history_file, "w") as f:
                json.dump(self.history, f, indent=2)
        except Exception as e:
            print(f"Error: Could not save settings: {e}", file=sys.stderr)

    def generate_hashtag(self, text):
        """Transform input text into a hashtag format"""
        if not text:
            return ""
            
        # Remove special characters if enabled
        if self.settings["remove_special_chars"]:
            # Keep alphanumeric and spaces only
            text = ''.join(c for c in text if c.isalnum() or c.isspace())
        
        # Capitalize first letter of each word if enabled
        if self.settings["capitalize_first_letter"]:
            text = text.title()
        
        # Remove spaces
        hashtag = text.replace(" ", "")
        
        # Add hashtag symbol
        hashtag = f"#{hashtag}"
        
        # Add to history
        if hashtag not in self.history:
            self.history.insert(0, hashtag)
            # Maintain max history size
            self.history = self.history[:self.settings["history_max_items"]]
            self.save_settings()
            
        return hashtag

    def import_from_file(self, filename):
        """Import text from file"""
        try:
            with open(filename, "r") as f:
                return f.read().strip()
        except Exception as e:
            print(f"Error reading file: {e}", file=sys.stderr)
            return None

    def export_to_file(self, hashtag, filename):
        """Export hashtag to file"""
        try:
            with open(filename, "w") as f:
                f.write(hashtag)
            return True
        except Exception as e:
            print(f"Error writing file: {e}", file=sys.stderr)
            return False

    def show_history(self, limit=None):
        """Show hashtag history"""
        if not self.history:
            print("History is empty.")
            return

        print("\nHashtag History:")
        for i, tag in enumerate(self.history[:limit]):
            print(f"{i+1}. {tag}")

    def clear_history(self):
        """Clear hashtag history"""
        self.history = []
        self.save_settings()
        print("History cleared.")

    def update_settings(self, args):
        """Update settings based on command line arguments"""
        if args.no_special is not None:
            self.settings["remove_special_chars"] = args.no_special
            
        if args.capitalize is not None:
            self.settings["capitalize_first_letter"] = args.capitalize
            
        if args.history_size is not None:
            self.settings["history_max_items"] = args.history_size
            
        self.save_settings()
        print("Settings updated.")

    def show_settings(self):
        """Show current settings"""
        print("\nCurrent Settings:")
        print(f"  Remove special characters: {self.settings['remove_special_chars']}")
        print(f"  Capitalize first letter: {self.settings['capitalize_first_letter']}")
        print(f"  Max history items: {self.settings['history_max_items']}")


def main():
    """Main function to handle command line arguments and run the app"""
    parser = argparse.ArgumentParser(
        description="Hashtag Generator - Convert text to hashtags from the command line"
    )
    
    # Input options
    input_group = parser.add_argument_group("Input Options")
    input_group.add_argument("-t", "--text", help="Text to convert to hashtag")
    input_group.add_argument("-i", "--input", help="Input file path")
    
    # Output options
    output_group = parser.add_argument_group("Output Options")
    output_group.add_argument("-o", "--output", help="Output file path")
    
    # Settings options
    settings_group = parser.add_argument_group("Settings")
    settings_group.add_argument("--no-special", dest="no_special", action="store_true",
                               help="Remove special characters", default=None)
    settings_group.add_argument("--keep-special", dest="no_special", action="store_false",
                               help="Keep special characters", default=None)
    settings_group.add_argument("--capitalize", dest="capitalize", action="store_true", 
                               help="Capitalize first letter of each word", default=None)
    settings_group.add_argument("--no-capitalize", dest="capitalize", action="store_false",
                               help="Don't capitalize first letter of each word", default=None)
    settings_group.add_argument("--history-size", type=int, dest="history_size",
                               help="Maximum number of history items to keep")
    
    # History commands
    history_group = parser.add_argument_group("History Commands")
    history_group.add_argument("--history", action="store_true", 
                              help="Show hashtag history")
    history_group.add_argument("--clear-history", action="store_true",
                              help="Clear hashtag history")
    history_group.add_argument("--history-limit", type=int, default=None,
                              help="Number of history items to show")
    
    # Other commands
    parser.add_argument("--settings", action="store_true", 
                       help="Show current settings")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Initialize the Hashtag Generator
    generator = HashtagGeneratorCLI()
    
    # Handle command-specific actions
    if args.settings:
        generator.show_settings()
        return
        
    if args.clear_history:
        generator.clear_history()
        return
        
    if args.history:
        generator.show_history(args.history_limit)
        return
    
    # Handle settings updates
    if any(x is not None for x in [args.no_special, args.capitalize, args.history_size]):
        generator.update_settings(args)
    
    # Process text input
    input_text = None
    
    if args.text:
        input_text = args.text
    elif args.input:
        input_text = generator.import_from_file(args.input)
    else:
        # Check if receiving from pipe
        if not sys.stdin.isatty():
            input_text = sys.stdin.read().strip()
        else:
            # No input provided, show help
            parser.print_help()
            return
    
    if input_text:
        hashtag = generator.generate_hashtag(input_text)
        print(hashtag)
        
        if args.output:
            if generator.export_to_file(hashtag, args.output):
                print(f"Hashtag saved to {args.output}")
            else:
                print(f"Failed to save hashtag to {args.output}")


if __name__ == "__main__":
    main()