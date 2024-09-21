# Webpage Screenshot Tool
### 
##### from now no need for exit the terminal and open the broswer whice eat the ram just to view
## Overview

This tool allows you to take screenshots of webpages using Playwright. It supports capturing screenshots from a single URL or multiple URLs specified in a file. You can customize the output filename and the directory where screenshots are saved.

## Features

- Capture screenshots of any webpage.
- Specify an output filename.
- Provide a file containing multiple URLs for batch processing.
- Automatically create necessary directories for saving screenshots.

## Installation

Ensure you have Python installed on your system. You can install the required libraries using pip:

### Prerequisites

This project requires Playwright, so please follow these steps:

1. **Clone the repository and install dependencies:**

    ```bash
    git clone http://github.com/ShulkwiSEC/websnap.git
    cd websnap
    python3 -m pip install -r requirements.txt
    ```

2. **Install the necessary browsers:**

    ```bash
    python3 -m playwright install
    ```

Now everything is set up!

## Usage

### Command-Line Arguments

The tool can be run from the command line with the following syntax:

```bash
usage: websnap.py [-h] [--url URL] [-o OUTPUT] [-f FROMFILE] [-vi] [-cf]

Take a screenshot of a webpage.

options:
  -h, --help            show this help message and exit
  --url URL             The URL of the webpage to screenshot.
  -o OUTPUT, --output OUTPUT
                        Optional output filename for the screenshot (default: <webpage>.png)
  -f FROMFILE, --fromfile FROMFILE
                        Optional file containing a list of URLs to screenshot (one per line).
  -vi, --view           Optional auto view the images after taken
  -cf, --clearafter     Clear images after viewing
```

# Example Usage
## Single URL

```bash
$ python websnap.py --url https://www.google.com
```

## Multiple URLs from File
```bash
$ $ python websnap.py -f urls.txt
```


## Requirements

- **Python 3.x**: Ensure you have Python version 3.x installed.
- **Playwright Library**: This tool requires the Playwright library for functionality. You can install it   

using pip:
```bash
pip install playwright
python -m playwright install
```
## Documentation

### Image Viewer

You can use the following dictionary format to reference images in your viewer:

```python
img_dict = {
    'intl_fil_gmail_about_policy.png': r'C:\path\to\image1.png',
    'intl_mr_in_gmail_about.png': r'C:\path\to\image2.png',
}
```


#### View Mode Shortcuts
- Use the "left" arrow key to go to the previous image.
- Use the "right" arrow key to go to the next image.
- Press "q" to exit or close the viewer.


## Conclusion

This Webpage Screenshot Tool provides a simple and efficient way to capture screenshots of webpages using Playwright. Whether you are working with a single URL or batch processing multiple links, this tool streamlines the process and offers flexibility in naming and saving files. We hope you find it useful for your projects!

For any questions or contributions, feel free to open an issue or submit a pull request on the GitHub repository.