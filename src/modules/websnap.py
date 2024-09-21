import asyncio
import os
import argparse
from urllib.parse import urlparse
from playwright.async_api import async_playwright
import shutil
import matplotlib.pyplot as plt
from PIL import Image


# Classe's list

# ImageViewer Class
class ImageViewer:
    """Image viewer that allows navigation through a dictionary of images."""
    
    def __init__(self, img_dict):
        """Initialize the ImageViewer with a dictionary of images."""
        self.images = list(img_dict.keys())
        self.img_paths = img_dict
        self.current_index = 0
        self.viewer_open = True  # Flag to track if viewer is open
        
        # Set up the figure and buttons
        self.fig, self.ax = plt.subplots()
        self.btn_prev = plt.Button(plt.axes([0.1, 0.01, 0.3, 0.075]), 'Previous')
        self.btn_next = plt.Button(plt.axes([0.6, 0.01, 0.3, 0.075]), 'Next')
        
        self.btn_prev.on_clicked(self.previous_image)
        self.btn_next.on_clicked(self.next_image)

        # Connect key press events
        self.fig.canvas.mpl_connect('key_press_event', self.on_key_press)
        self.fig.canvas.mpl_connect('close_event', self.on_close)

        self.view_image()
        plt.show()  # Show the window with the image and buttons

    def view_image(self):
        """View the current image based on the current index."""
        title = self.images[self.current_index]
        img_path = self.img_paths[title]

        try:
            img = Image.open(img_path)
            self.ax.clear()
            self.ax.imshow(img)
            self.ax.set_title(title)
            self.ax.axis('off')  # Hide axes
            plt.draw()
        except Exception as e:
            print(f"Error loading image: {e}")

    def next_image(self, event=None):
        """Go to the next image."""
        if self.current_index < len(self.images) - 1:
            self.current_index += 1
            self.view_image()
        else:
            print("You are at the last image.")

    def previous_image(self, event=None):
        """Go to the previous image."""
        if self.current_index > 0:
            self.current_index -= 1
            self.view_image()
        else:
            print("You are at the first image.")

    def on_key_press(self, event):
        """Handle key press events for navigation."""
        if event.key == 'right':
            self.next_image()
        elif event.key == 'left':
            self.previous_image()
        elif event.key == 'q':
            self.on_close

    def on_close(self, event):
        """Handle the close event."""
        self.viewer_open = False  # Set flag to indicate viewer is closed
        plt.close(self.fig)  # Close the figure
# ENDCLASS

# Snap Class
class Snap:
    @staticmethod
    async def take_screenshot(url, filename='screenshot.png', save_dir='./tmp/'):
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.goto(url)

            # Ensure the save directory exists
            os.makedirs(save_dir, exist_ok=True)

            full_path = os.path.join(save_dir, filename)
            await page.screenshot(path=full_path)
            print(f"Screenshot saved to: {full_path}")

            await browser.close()
# ENDCLASS


async def main(websnapargs):
    # websnapargs = argparse.ArgumentParser(description='Take a screenshot of a webpage.')
    # websnapargs.add_argument('--url', type=str, help='The URL of the webpage to screenshot.')
    # websnapargs.add_argument('-o', '--output', type=str, help='Optional output filename for the screenshot (default: <webpage>.png)')
    # websnapargs.add_argument('-f', '--fromfile', type=str, help='Optional file containing a list of URLs to screenshot (one per line).')
    # websnapargs.add_argument('-vi', '--view', action='store_true', help='Optional auto view the images after taken')
    # websnapargs.add_argument('-cf', '--clearafter', action='store_true', help='Clear images after viewing')

    args = websnapargs

    if not args.url and not args.fromfile:
        websnapargs.error('Please include either --url or --fromfile. Neither provided.')

    if args.fromfile:
        with open(args.fromfile, 'r') as file:
            urls = [line.strip() for line in file if line.strip()]
    else:
        urls = [args.url]

    img_dict = {}  # Dictionary to store image paths

    for url in urls:
        purl = urlparse(url)
        print(f"{url=}\n{purl=}")
        hostname = purl.hostname.replace('.', '_')  # Replace dots with underscores for folder name
        webpage = purl.path.strip('/').replace('/', '_') or 'index'  # Strip leading/trailing slashes
        root_path = "tmp"
        save_directory = f'./{root_path}/{hostname}/screenshots/'  # Directory to save the screenshot
        filename = args.output if args.output else f'{webpage}.png'  # Use specified output filename or default

        await Snap.take_screenshot(url, filename, save_directory)

        # Store the image path in the dictionary
        full_image_path = os.path.join(save_directory, filename)
        img_dict[filename] = full_image_path

    # Open the viewer only after all screenshots have been taken
    if args.view and img_dict:
        viewer = ImageViewer(img_dict)  # Assuming ImageViewer handles opening images

        # Clear images after viewing if the flag is set
        if args.clearafter:
            try:
                shutil.rmtree(f'./{root_path}')
                print(f"cleared done!")
            except Exception as e:
                print(f"Error clearing: {e}")

def core(cliargs):
        asyncio.run(main(cliargs))  # Use asyncio.run to run the core async function