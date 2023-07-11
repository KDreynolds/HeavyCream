from bs4 import BeautifulSoup

def generate_css():
    css_content = """
    body {
        background-color: linen;
    }

    button {
        background-color: blue;
        color: white;
        border: none;
        padding: 15px 32px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
    }
    """
    with open("styles.css", "w") as f:
        f.write(css_content)

class HTMXBackendCreator:
    def __init__(self, backend_type, html=None):
        self.backend_type = backend_type
        self.html = html or self.generate_html()  # Use provided HTML or generate a generic one

        self.backend_generators = {
            'flask': FlaskGenerator,
            'gin': GinGenerator,
            'php-slim': SlimPHPGenerator,
        }

        if backend_type not in self.backend_generators:
            raise ValueError(f"Unsupported backend type: {backend_type}")

        self.generator = self.backend_generators[backend_type](self.html)

    def generate_backend(self):
        return self.generator.generate()

    def generate_html(self):
        # Create a generic HTML with HTMX elements for the chosen backend type
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <link rel="stylesheet" type="text/css" href="styles.css">
        </head>
        <body>

        <button hx-get="/get_example">GET example</button>
        <button hx-post="/post_example">POST example</button>

        </body>
        </html>
        """
        return html_content




class BackendGenerator:
    def __init__(self, html):
        self.soup = BeautifulSoup(html, 'html.parser')

    def find_htmx_elements(self):
        return self.soup.find_all(lambda tag: any(tag.get(attr) for attr in ['hx-get', 'hx-post', 'hx-put', 'hx-delete']))

class FlaskGenerator(BackendGenerator):
    def generate(self):
        flask_app_code = """
from flask import Flask, request, render_template
app = Flask(__name__)

"""

        for tag in self.find_htmx_elements():
            url = tag.get('hx-get') or tag.get('hx-post') or tag.get('hx-put') or tag.get('hx-delete')
            method = 'GET' if tag.get('hx-get') else 'POST' if tag.get('hx-post') else 'PUT' if tag.get('hx-put') else 'DELETE'

            flask_app_code += f"""
@app.route('{url}', methods=['{method}'])
def handle_request():
    if request.method == 'POST':
        # Handle POST request here
        return "POST request received"
    elif request.method == 'GET':
        # Handle GET request here
        return "GET request received"
    elif request.method == 'PUT':
        # Handle PUT request here
        return "PUT request received"
    elif request.method == 'DELETE':
        # Handle DELETE request here
        return "DELETE request received"
    else:
        return "Unknown request method"
"""

        flask_app_code += """
@app.route('/static/<path:filename>')
def staticfiles(filename):
    return app.send_static_file(filename)

if __name__ == '__main__':
    app.run(debug=True)
"""

        return flask_app_code

class GinGenerator(BackendGenerator):
    def generate(self):
        gin_app_code = """
package main

import (
	"github.com/gin-gonic/gin"
)

func main() {
	r := gin.Default()

"""

        for tag in self.find_htmx_elements():
            url = tag.get('hx-get') or tag.get('hx-post') or tag.get('hx-put') or tag.get('hx-delete')
            method = 'GET' if tag.get('hx-get') else 'POST' if tag.get('hx-post') else 'PUT' if tag.get('hx-put') else 'DELETE'
            
            handler = f'''
	c.String(200, "{method} request received")
'''

            gin_app_code += f"""
	r.{method}("{url}", func(c *gin.Context) {{{handler}}})
"""

        gin_app_code += """
	r.Run() // listen and serve on 0.0.0.0:8080
}
"""

        return gin_app_code

class SlimPHPGenerator(BackendGenerator):
    def generate(self):
        php_code = """
<?php
require 'vendor/autoload.php';

$app = new \Slim\App;

"""

        for tag in self.find_htmx_elements():
            url = tag.get('hx-get') or tag.get('hx-post') or tag.get('hx-put') or tag.get('hx-delete')
            method = 'GET' if tag.get('hx-get') else 'POST' if tag.get('hx-post') else 'PUT' if tag.get('hx-put') else 'DELETE'

            handler = f'''
    return $response->withStatus(200)->write('{method} request received');
'''

            php_code += f"""
$app->{method.lower()}('{url}', function ($request, $response, $args) {{{handler}}});
"""

        php_code += """
$app->run();
?>

"""

        return php_code

generate_css()  # Call this function to create the CSS file

# Generate Flask backend from custom HTML
creator = HTMXBackendCreator('flask', html)
print(creator.generate_backend())

# Generate Flask backend from a generic HTML
creator = HTMXBackendCreator('flask')
print(creator.generate_backend())

# Generate Gin backend from custom HTML
creator = HTMXBackendCreator('gin', html)
print(creator.generate_backend())

# Generate SlimPHP backend from custom HTML
creator = HTMXBackendCreator('php-slim', html)
print(creator.generate_backend())