import sys
import re
from typing import TextIO, Optional, Tuple
from rich.syntax import Syntax
from rich.console import Console
from pygments.styles import get_all_styles

block_pattern = r"```(\w+)?[\n\r]([\s\S]*?)```"

def print_text_highlighted(code, language):
    syntax = Syntax(code, language, theme='material', line_numbers=False)
    console = Console(record=True)
    console.print(syntax)

class SimpleTokenizer:
    def __init__(self, stream: TextIO):
        self.stream = stream
        self.current_char = ''
        self.temp_buffer = ''
        self.end_of_stream = False

    def _advance(self) -> Optional[str]:
        """Advance to the next character in the stream."""
        self.current_char = self.stream.read(1)
        if self.current_char == '':
            self.end_of_stream = True
        return self.current_char

    def _consume_until(self, delimiter: str) -> str:
        """Consume characters until the delimiter is reached."""
        buffer = ""
        while not self.end_of_stream:
            if buffer.endswith(delimiter):
                break
            buffer += self._advance()
            
        return buffer

    def get_next_token(self) -> Optional[Tuple[str, str]]:
        """Generate tokens based on the current position in the data."""
        if self.end_of_stream:
            return None

        self.temp_buffer += self._advance()

        while not self.end_of_stream and self.current_char == '`':
            self.temp_buffer += self._advance()

        # BLOCK
        if self.temp_buffer.startswith("```"):
            block = self.temp_buffer
            block += self._consume_until("```")
            self.temp_buffer = ""
            return ("BLOCK", block)

        # QUOTE
        if self.temp_buffer.startswith("`"):
            block = self.temp_buffer
            block += self._consume_until("`")
            self.temp_buffer = ""
            return ("QUOTE", block)

        if self.temp_buffer:
            text = self.temp_buffer
            self.temp_buffer = ""
            return ("TEXT", text)
        
        return None

    def tokenize(self):
        """Tokenize the entire input and return a list of tokens."""
        tokens = []
        while not self.end_of_stream:
            token = self.get_next_token()
            if token:
                if token[0] != "TEXT":
                  print(token[0])
                  print(token[1], "\n\n")
                  
                tokens.append(token)
            self._advance()  # Move to the next character
        return tokens

def process_input_stream():
    language = ""
    tokenizer = SimpleTokenizer(sys.stdin)
    console = Console()

    while True:
        token = tokenizer.get_next_token()
        if token:
            [token_type, token_value] = token
            if token_type == "TEXT":
                sys.stdout.write(token_value)
            
            if token_type == "QUOTE":
                console.print(token_value, style="blue")

            if token_type == "BLOCK":
                match = re.search(block_pattern, token_value)
                language = match.group(1)
                code = match.group(2)
                if language:
                    console.print("```" + language, style="magenta")
                    print_text_highlighted(code, language)
                    console.print("```\n", style="magenta")
                else:
                    print("```\n" + code + "```")
        else:
            break

if __name__ == "__main__":
    process_input_stream()