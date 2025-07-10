# /Users/pouyasamandi/Desktop/Agent_projects/interview_ai/scripts/web_server.py
from flask import Flask, render_template
import threading
import os
import re
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)  # Suppress all but ERROR logs
app = Flask(__name__, template_folder="/Users/pouyasamandi/Desktop/Agent_projects/interview_ai/templates")


def process_latex_content(content):
    """Process content to identify and format LaTeX sections"""
    # Split content by LaTeX code blocks (```latex ... ```)
    latex_pattern = r'```latex\s*\n(.*?)\n```'

    sections = []
    last_end = 0

    for match in re.finditer(latex_pattern, content, re.DOTALL):
        # Add any text before this LaTeX block
        if match.start() > last_end:
            text_before = content[last_end:match.start()].strip()
            if text_before:
                sections.append({
                    'type': 'text',
                    'content': text_before
                })

        # Add the LaTeX block
        latex_content = match.group(1)
        sections.append({
            'type': 'latex',
            'content': latex_content
        })

        last_end = match.end()

    # Add any remaining text after the last LaTeX block
    if last_end < len(content):
        remaining_text = content[last_end:].strip()
        if remaining_text:
            sections.append({
                'type': 'text',
                'content': remaining_text
            })

    # If no LaTeX blocks found, treat entire content as text
    if not sections:
        sections.append({
            'type': 'text',
            'content': content
        })

    return sections


def extract_code_blocks(latex_content):
    """Extract code blocks from LaTeX content"""
    # Pattern to match \begin{verbatim} ... \end{verbatim}
    verbatim_pattern = r'\\begin\{verbatim\}\s*\n(.*?)\n\\end\{verbatim\}'

    # Pattern to match \begin{lstlisting} ... \end{lstlisting}
    lstlisting_pattern = r'\\begin\{lstlisting\}(?:\[[^\]]*\])?\s*\n(.*?)\n\\end\{lstlisting\}'

    code_blocks = []

    for match in re.finditer(verbatim_pattern, latex_content, re.DOTALL):
        code_blocks.append(match.group(1))

    for match in re.finditer(lstlisting_pattern, latex_content, re.DOTALL):
        code_blocks.append(match.group(1))

    return code_blocks


def format_latex_for_display(latex_content):
    """Format LaTeX content for better web display"""
    # Replace LaTeX formatting with HTML equivalents
    formatted = latex_content

    # Handle LaTeX sections (convert to HTML headings)
    formatted = re.sub(r'\\section\{([^}]+)\}', r'<h2>\1</h2>', formatted)
    formatted = re.sub(r'\\subsection\{([^}]+)\}', r'<h3>\1</h3>', formatted)
    formatted = re.sub(r'\\subsubsection\{([^}]+)\}', r'<h4>\1</h4>', formatted)
    formatted = re.sub(r'\\paragraph\{([^}]+)\}', r'<h5>\1</h5>', formatted)
    formatted = re.sub(r'\\subparagraph\{([^}]+)\}', r'<h6>\1</h6>', formatted)

    # Handle textbf (bold)
    formatted = re.sub(r'\\textbf\{([^}]+)\}', r'<strong>\1</strong>', formatted)

    # Handle textit (italic)
    formatted = re.sub(r'\\textit\{([^}]+)\}', r'<em>\1</em>', formatted)

    # Handle underline
    formatted = re.sub(r'\\underline\{([^}]+)\}', r'<u>\1</u>', formatted)

    # Handle LaTeX line breaks
    formatted = re.sub(r'\\\\', '<br>', formatted)
    formatted = re.sub(r'\\newline', '<br>', formatted)

    # Handle verbatim blocks (code)
    formatted = re.sub(
        r'\\begin\{verbatim\}\s*\n(.*?)\n\\end\{verbatim\}',
        r'<pre><code class="language-python">\1</code></pre>',
        formatted,
        flags=re.DOTALL
    )

    # Handle lstlisting blocks (another code environment)
    formatted = re.sub(
        r'\\begin\{lstlisting\}(?:\[[^\]]*\])?\s*\n(.*?)\n\\end\{lstlisting\}',
        r'<pre><code class="language-python">\1</code></pre>',
        formatted,
        flags=re.DOTALL
    )

    # Handle itemize lists
    formatted = re.sub(r'\\begin\{itemize\}', '<ul>', formatted)
    formatted = re.sub(r'\\end\{itemize\}', '</ul>', formatted)

    # Handle enumerate lists
    formatted = re.sub(r'\\begin\{enumerate\}', '<ol>', formatted)
    formatted = re.sub(r'\\end\{enumerate\}', '</ol>', formatted)

    # Handle list items
    formatted = re.sub(r'\\item\s+', '<li>', formatted)

    # Handle description lists
    formatted = re.sub(r'\\begin\{description\}', '<dl>', formatted)
    formatted = re.sub(r'\\end\{description\}', '</dl>', formatted)

    # Handle math expressions (display math)
    formatted = re.sub(r'\\begin\{equation\}(.*?)\\end\{equation\}', r'<div class="math-display">$$\1$$</div>',
                       formatted, flags=re.DOTALL)
    formatted = re.sub(r'\\begin\{align\}(.*?)\\end\{align\}',
                       r'<div class="math-display">$$\\begin{align}\1\\end{align}$$</div>', formatted, flags=re.DOTALL)

    # Handle inline math expressions
    formatted = re.sub(r'\\\((.*?)\\\)', r'<span class="math">\\(\1\\)</span>', formatted)
    formatted = re.sub(r'\$([^$]+)\$', r'<span class="math">$\1$</span>', formatted)

    # Handle common LaTeX commands
    formatted = re.sub(r'\\emph\{([^}]+)\}', r'<em>\1</em>', formatted)
    formatted = re.sub(r'\\texttt\{([^}]+)\}', r'<code>\1</code>', formatted)
    formatted = re.sub(r'\\url\{([^}]+)\}', r'<a href="\1">\1</a>', formatted)
    formatted = re.sub(r'\\href\{([^}]+)\}\{([^}]+)\}', r'<a href="\1">\2</a>', formatted)

    # Handle LaTeX quotes
    formatted = re.sub(r'``([^\']+)\'\'', r'"\1"', formatted)
    formatted = re.sub(r'`([^\']+)\'', r"'\1'", formatted)

    # Clean up extra whitespace and newlines
    formatted = re.sub(r'\n\s*\n', '\n\n', formatted)

    # Convert newlines to HTML line breaks in appropriate contexts
    formatted = re.sub(r'\n', '<br>\n', formatted)
    # Clean up multiple consecutive <br> tags
    formatted = re.sub(r'(<br>\s*){3,}', '<br><br>', formatted)

    return formatted


@app.route('/')
def index():
    try:
        with open("/Users/pouyasamandi/Desktop/Agent_projects/interview_ai/results.txt", "r") as f:
            content = f.read()
    except FileNotFoundError:
        content = "No results yet."

    # Process the content to identify LaTeX sections
    sections = process_latex_content(content)

    # Format each LaTeX section
    for section in sections:
        if section['type'] == 'latex':
            section['formatted'] = format_latex_for_display(section['content'])
            section['code_blocks'] = extract_code_blocks(section['content'])

    return render_template('index.html', sections=sections)


def start_server():
    # Start Flask in a separate thread
    def run():
        app.run(host='0.0.0.0', port=5001, debug=False, use_reloader=False)

    thread = threading.Thread(target=run)
    thread.daemon = True
    thread.start()
    return thread