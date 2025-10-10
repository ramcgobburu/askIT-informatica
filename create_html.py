#!/usr/bin/env python3
"""
Script to convert the Informatica Agent Tech Blog Markdown to HTML
This HTML can be easily printed to PDF using browser print functionality
"""

import markdown
import os
from pathlib import Path

def create_html():
    """Convert the markdown file to HTML with print-friendly styling."""
    
    # Read the markdown file
    md_file = Path("INFORMATICA_AGENT_TECH_BLOG.md")
    if not md_file.exists():
        print("Error: INFORMATICA_AGENT_TECH_BLOG.md not found")
        return
    
    with open(md_file, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    # Convert markdown to HTML
    html = markdown.markdown(
        markdown_content,
        extensions=[
            'markdown.extensions.tables',
            'markdown.extensions.fenced_code',
            'markdown.extensions.toc',
            'markdown.extensions.codehilite'
        ]
    )
    
    # Add CSS styling for better print appearance
    styled_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Building an Intelligent Informatica Agent</title>
        <style>
            @page {{
                size: A4;
                margin: 0.75in;
            }}
            
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
            }}
            
            h1 {{
                color: #2c3e50;
                border-bottom: 3px solid #3498db;
                padding-bottom: 10px;
                page-break-before: always;
            }}
            
            h1:first-child {{
                page-break-before: avoid;
            }}
            
            h2 {{
                color: #34495e;
                border-bottom: 2px solid #ecf0f1;
                padding-bottom: 5px;
                margin-top: 30px;
            }}
            
            h3 {{
                color: #7f8c8d;
                margin-top: 25px;
            }}
            
            code {{
                background-color: #f8f9fa;
                padding: 2px 4px;
                border-radius: 3px;
                font-family: 'Courier New', monospace;
            }}
            
            pre {{
                background-color: #f8f9fa;
                padding: 15px;
                border-radius: 5px;
                overflow-x: auto;
                border-left: 4px solid #3498db;
                page-break-inside: avoid;
            }}
            
            table {{
                border-collapse: collapse;
                width: 100%;
                margin: 20px 0;
                page-break-inside: avoid;
            }}
            
            th, td {{
                border: 1px solid #ddd;
                padding: 12px;
                text-align: left;
            }}
            
            th {{
                background-color: #3498db;
                color: white;
            }}
            
            tr:nth-child(even) {{
                background-color: #f2f2f2;
            }}
            
            blockquote {{
                border-left: 4px solid #3498db;
                margin: 20px 0;
                padding: 10px 20px;
                background-color: #f8f9fa;
                font-style: italic;
            }}
            
            .toc {{
                background-color: #f8f9fa;
                padding: 20px;
                border-radius: 5px;
                margin: 20px 0;
            }}
            
            .highlight {{
                background-color: #fff3cd;
                padding: 15px;
                border-radius: 5px;
                border-left: 4px solid #ffc107;
                margin: 20px 0;
            }}
            
            /* Print-specific styles */
            @media print {{
                body {{
                    font-size: 12pt;
                }}
                
                h1 {{
                    page-break-before: always;
                }}
                
                h1:first-child {{
                    page-break-before: avoid;
                }}
                
                pre, table {{
                    page-break-inside: avoid;
                }}
                
                .no-print {{
                    display: none;
                }}
            }}
            
            /* Print instructions */
            .print-instructions {{
                background-color: #e3f2fd;
                border: 1px solid #2196f3;
                padding: 15px;
                margin: 20px 0;
                border-radius: 5px;
                text-align: center;
            }}
        </style>
    </head>
    <body>
        <div class="print-instructions no-print">
            <h3>📄 How to Create PDF</h3>
            <p><strong>To convert this HTML to PDF:</strong></p>
            <ol>
                <li>Press <kbd>Ctrl+P</kbd> (Windows/Linux) or <kbd>Cmd+P</kbd> (Mac)</li>
                <li>Select "Save as PDF" as the destination</li>
                <li>Choose "More settings" and set margins to "Minimum"</li>
                <li>Click "Save" to create your PDF</li>
            </ol>
        </div>
        
        {html}
        
        <div class="print-instructions no-print">
            <p><strong>✅ PDF Ready!</strong> Use your browser's print function to save as PDF.</p>
        </div>
    </body>
    </html>
    """
    
    # Write HTML file
    with open('INFORMATICA_AGENT_TECH_BLOG.html', 'w', encoding='utf-8') as f:
        f.write(styled_html)
    
    print("✅ HTML created successfully: INFORMATICA_AGENT_TECH_BLOG.html")
    print("📄 Open the HTML file in your browser and use Ctrl+P (or Cmd+P) to print as PDF")

if __name__ == "__main__":
    create_html()
