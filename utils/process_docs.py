import os
import html2text
import argparse

def process_directory(input_dir, output_dir):
    h = html2text.HTML2Text()
    h.ignore_links = True  # You can add more html2text options here if needed

    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.html'):
                # Compute input and output paths
                input_path = os.path.join(root, file)
                rel_path = os.path.relpath(input_path, input_dir)
                output_path = os.path.join(output_dir, rel_path.replace('.html', '.txt'))

                # Ensure output directory exists
                os.makedirs(os.path.dirname(output_path), exist_ok=True)

                # Read HTML file
                with open(input_path, 'r', encoding='utf-8') as infile:
                    html_content = infile.read()

                # Convert HTML to text
                text_content = h.handle(html_content)

                # Save the cleaned text
                with open(output_path, 'w', encoding='utf-8') as outfile:
                    outfile.write(text_content)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process a directory of HTML files to text.')
    parser.add_argument('input_dir', help='The directory containing HTML files')
    parser.add_argument('output_dir', help='The directory to save cleaned text files')

    args = parser.parse_args()

    process_directory(args.input_dir, args.output_dir)
