import re

def main():
    # Prompt the user for an HTML string and print the parsed short link or None
    print(parse(input("HTML: ")))

def parse(s):
    # Define a regex pattern to target YouTube embed URLs inside iframe tags
    # - '<iframe[^>]*': matches the opening iframe tag and any attributes before 'src'
    # - 'src="https?://': matches the src attribute starting with either http:// or https://
    # - '(?:www\.)?': a non-capturing group that optionally matches 'www.'
    # - 'youtube\.com/embed/': matches the literal base path for embedded YouTube videos
    # - '([a-zA-Z0-9_-]+)': a capturing group that isolates the unique 11-character video ID
    pattern = r'<iframe[^>]*src="https?://(?:www\.)?youtube\.com/embed/([a-zA-Z0-9_-]+)"'
    
    # Search the input string 's' for the pattern, ignoring case sensitivity (re.I)
    match = re.search(pattern, s, re.I)

    # If a match is found structurally
    if match:
        # Extract the video ID from the first capturing group and format it into a short URL
        return f"https://youtu.be/{match.group(1)}"
    
    # Return None if the input HTML doesn't match the required YouTube iframe structure
    return None

if __name__ == "__main__":
    main()
