import os

def generate_html(folder_path):
    # Create a list to store the image paths
    image_paths = []

    # Walk through the folder and its subfolders
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            # Check if the file is a PNG image
            if file.lower().endswith('.png'):
                # Get the full path of the image
                image_path = os.path.join(root, file)
                # Add the image path to the list
                image_paths.append(image_path)

    # Open the HTML file for writing
    with open('index.html', 'w') as f:
        # Write the HTML header
        f.write('<!DOCTYPE html>\n')
        f.write('<html lang="en">\n')
        f.write('<head>\n')
        f.write('<meta charset="UTF-8">\n')
        f.write('<meta name="viewport" content="width=device-width, initial-scale=1.0">\n')
        f.write('<title>Image Gallery</title>\n')
        f.write('<link rel="stylesheet" href="styles.css">\n')
        f.write('</head>\n')
        f.write('<body>\n')

        
        f.write('<input type="text" id="searchInput" placeholder="Enter search term...">\n')
        f.write('<button onclick="searchImages()">Search</button>\n')

        # Write the image tags
        f.write('<div id="imageContainer">\n')
        for image_path in image_paths:
            f.write(f'<img src="{image_path}" alt="{image_path}" title="{image_path}">\n')
            f.write(f'<div class="top-left">{image_path}</div>\n')
        #f.write('<\div>\n')

        f.write('<script src="script.js"></script>\n')

        # Write the HTML footer
        f.write('</body>\n')
        f.write('</html>\n')

# Example usage
folder_path = '../plots'
generate_html(folder_path)
