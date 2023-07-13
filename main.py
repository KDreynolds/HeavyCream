import os
from pathlib import Path

# Function to generate CSS
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
    return css_content

# Function to generate HTML
def generate_html():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>My HTMX App</title>
        <link rel="stylesheet" type="text/css" href="styles.css">
    </head>
    <body>
        <div class="App">
            <header class="App-header">
                <img src="logo.png" class="App-logo" alt="logo" />
                <p>
                    Edit <code>main.html</code> and save to reload.
                </p>
                <a class="App-link" href="https://htmx.org" target="_blank" rel="noopener noreferrer">
                    HeavyCream Docs
                </a>
                <br>
                <br>
                <a class="App-link" href="https://htmx.org" target="_blank" rel="noopener noreferrer">
                    Learn HTMX
                </a>
            </header>
        </div>
        <br>

        <button hx-get="/get_example">GET example</button><br>
        <br>
        <button hx-post="/post_example">POST example</button>

        <!-- Don't forget to include htmx library -->
        <script src="https://unpkg.com/htmx.org@1.6.1"></script>
    </body>
    </html>
    """
    return html_content

# Function to generate backend code
def generate_backend(backend_type):
    if backend_type == "flask":
        backend_code = """
from flask import Flask, request, render_template
app = Flask(__name__)

@app.route('/get_example', methods=['GET'])
def get_example():
    return "GET request received"

@app.route('/post_example', methods=['POST'])
def post_example():
    return "POST request received"

@app.route('/static/<path:filename>')
def staticfiles(filename):
    return app.send_static_file(filename)

if __name__ == '__main__':
    app.run(debug=True)
"""
    elif backend_type == "gin":
        backend_code = """
package main

import (
	"github.com/gin-gonic/gin"
)

func main() {
	r := gin.Default()

	r.GET("/get_example", func(c *gin.Context) {
		c.String(200, "GET request received")
	})
	
	r.POST("/post_example", func(c *gin.Context) {
		c.String(200, "POST request received")
	})

	r.Run() // listen and serve on 0.0.0.0:8080
}
"""
    elif backend_type == "slim":
        backend_code = """
<?php
use Psr\Http\Message\ResponseInterface as Response;
use Psr\Http\Message\ServerRequestInterface as Request;
use Slim\Factory\AppFactory;

require __DIR__ . '/../vendor/autoload.php';

$app = AppFactory::create();

$app->get('/get_example', function (Request $request, Response $response, $args) {
    $response->getBody()->write("GET request received");
    return $response;
});

$app->post('/post_example', function (Request $request, Response $response, $args) {
    $response->getBody()->write("POST request received");
    return $response;
});

$app->run();
"""
    else:
        raise ValueError(f"Unsupported backend type: {backend_type}")

    return backend_code

# Main script
def main():
    backend_type = input("Enter the backend you want to use (flask/gin/slim): ")

    # Generate the content
    html_content = generate_html()
    css_content = generate_css()
    backend_code = generate_backend(backend_type)

    # Write the content to files
    Path("index.html").write_text(html_content)
    Path("styles.css").write_text(css_content)

    if backend_type == "flask":
        Path("app.py").write_text(backend_code)
    elif backend_type == "gin":
        Path("app.go").write_text(backend_code)
    elif backend_type == "slim":
        Path("index.php").write_text(backend_code)

    print(f"Boilerplate for {backend_type} backend has been created.")

if __name__ == "__main__":
    main()
