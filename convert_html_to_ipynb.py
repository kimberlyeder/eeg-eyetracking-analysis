import nbformat as nbf
from bs4 import BeautifulSoup
import html
import re
import sys

try:
    # Read the HTML file
    print("Reading HTML file...")
    with open('04.03_EEG_Preprocess.html', 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Parse HTML
    print("Parsing HTML...")
    soup = BeautifulSoup(html_content, 'lxml')
except Exception as e:
    print(f"Error reading/parsing file: {e}")
    sys.exit(1)

# Create a new notebook
print("Creating notebook structure...")
nb = nbf.v4.new_notebook()

# Find all cells
cells = soup.find_all('div', class_=re.compile(r'jp-Cell'))
print(f"Found {len(cells)} cells to convert...")

for idx, cell in enumerate(cells):
    try:
        cell_id = cell.get('id', '').replace('cell-id=', '')
        cell_classes = cell.get('class', [])
        
        # Check if it's a markdown cell
        if 'jp-MarkdownCell' in cell_classes:
            # Extract markdown content
            markdown_div = cell.find('div', class_='jp-RenderedMarkdown')
            if markdown_div:
                # Get the HTML content and convert back to markdown-like text
                content = markdown_div.get_text().strip()
                if content:  # Only add non-empty cells
                    nb.cells.append(nbf.v4.new_markdown_cell(content))
                    print(f"  Added markdown cell {idx+1}")
        
        # Check if it's a code cell
        elif 'jp-CodeCell' in cell_classes:
            # Extract code
            code_div = cell.find('div', class_='highlight')
            if code_div:
                pre_tag = code_div.find('pre')
                if pre_tag:
                    # Get text content and unescape HTML entities
                    code = pre_tag.get_text().strip()
                    
                    if not code:  # Skip empty code cells
                        continue
                    
                    # Extract output if exists
                    output_area = cell.find('div', class_='jp-OutputArea')
                    outputs = []
                    
                    if output_area:
                        # Find all output children
                        output_children = output_area.find_all('div', class_='jp-OutputArea-child', recursive=False)
                        
                        for output_child in output_children:
                            # Text output
                            text_output = output_child.find('div', class_='jp-RenderedText')
                            if text_output:
                                output_text = text_output.get_text()
                                outputs.append(nbf.v4.new_output(
                                    output_type='stream',
                                    name='stdout',
                                    text=output_text
                                ))
                            
                            # HTML output
                            html_output = output_child.find('div', class_='jp-RenderedHTMLCommon')
                            if html_output and not text_output:  # Avoid duplicates
                                output_html = str(html_output)
                                outputs.append(nbf.v4.new_output(
                                    output_type='display_data',
                                    data={'text/html': output_html}
                                ))
                            
                            # Image output
                            img_output = output_child.find('img')
                            if img_output:
                                img_src = img_output.get('src', '')
                                if img_src.startswith('data:image'):
                                    # Extract image data
                                    outputs.append(nbf.v4.new_output(
                                        output_type='display_data',
                                        data={'image/png': img_src.split(',')[1] if ',' in img_src else ''}
                                    ))
                    
                    # Create code cell
                    code_cell = nbf.v4.new_code_cell(code)
                    if outputs:
                        code_cell.outputs = outputs
                    nb.cells.append(code_cell)
                    print(f"  Added code cell {idx+1} ({'with outputs' if outputs else 'no outputs'})")
    except Exception as e:
        print(f"  Warning: Error processing cell {idx+1}: {e}")
        continue

# Write the notebook
print("Writing notebook file...")
try:
    with open('04.03_EEG_Preprocess.ipynb', 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
    print(f"✓ Conversion complete! Created notebook with {len(nb.cells)} cells.")
    print("✓ Output file: 04.03_EEG_Preprocess.ipynb")
except Exception as e:
    print(f"Error writing notebook: {e}")
    sys.exit(1)
