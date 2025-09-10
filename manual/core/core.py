import asyncio
import pyautogui
import cv2
import numpy as np
from PIL import Image
import time
import os

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0 

def form():
    """
    Returns screenshot for form detection from current directory
    """
    try:
        current_dir = os.getcwd()
        form_files = ['public.key']
        
        for filename in form_files:
            filepath = os.path.join(current_dir, filename)
            if os.path.exists(filepath):
                image = Image.open(filepath)
                # print(f"Form template loaded: {filename}")
                return image
        
        # If no specific form file found, look for any image file
        for file in os.listdir(current_dir):
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                filepath = os.path.join(current_dir, file)
                image = Image.open(filepath)
                # print(f"Using first available image for form: {file}")
                return image
        
        # print("No form screenshot found in current directory")
        return None
        
    except Exception as e:
        # print(f"Error loading form screenshot: {e}")
        return None

async def start():
    """
    Main function for automatic form detection and confirmation
    """
    # print("Starting automatic form search...")
    
    # Load form template once at startup
    # print("Loading form template...")
    form_template = form()
    
    if form_template is None:
        # print("ERROR: No form template found! Put form.png in current directory")
        return
    
    # print("Form template loaded successfully!")
    
    while True:
        try:
            # Stage 1: Form search using loaded template
            form_found, form_location = await find_form_on_screen(form_template)
            
            if form_found:
                # print(f"Form found at position: {form_location}")
                
                # Stage 2: Calculate confirmation button position
                button_location = calculate_confirm_button_position(form_location)
                
                # print(f"Confirmation button position calculated: {button_location}")
                
                # Моментальный клик на рассчитанную позицию
                await instant_click(button_location)
                
                # print("Form successfully confirmed!")
                
                # Pause after click to avoid repeated clicks
                await asyncio.sleep(1)
            
            # Wait 0.5 seconds before next check
            await asyncio.sleep(0.5)
            
        except Exception as e:
            print(f"Error in search loop: {e}")
            await asyncio.sleep(0.5)

async def find_form_on_screen(form_template):
    """
    First stage: search for form on screen using loaded template
    Returns (form found, coordinates as (x, y, width, height))
    """
    try:
        # Take current screenshot
        current_screenshot = pyautogui.screenshot()
        
        # Search using template matching
        form_found = search_form_by_template(current_screenshot, form_template)
        
        if form_found:
            return True, form_found
        
        return False, None
        
    except Exception as e:
        print(f"Error searching for form: {e}")
        return False, None

def calculate_confirm_button_position(form_location):
    try:
        x, y, w, h = form_location
        
        button_x = x + int(w * 0.85) 
        button_y = y + int(h * 0.85)
        
        return (button_x, button_y)
        
    except Exception as e:
        print(f"Error calculating button position: {e}")
        return None

async def instant_click(location):
    try:
        x, y = location
        
        pyautogui.click(x, y)
        
        # print(f"Instant click executed at coordinates: ({x}, {y})")
        
    except Exception as e:
        ...
        # print(f"Error during instant click: {e}")

def search_form_by_template(screenshot, form_template):
    """
    Search form by template image
    Returns (x, y, width, height) of found form
    """
    try:
        # Convert form template to OpenCV format
        template_cv = cv2.cvtColor(np.array(form_template), cv2.COLOR_RGB2BGR)
        template_gray = cv2.cvtColor(template_cv, cv2.COLOR_BGR2GRAY)
        
        # Convert screenshot to OpenCV format
        screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        screenshot_gray = cv2.cvtColor(screenshot_cv, cv2.COLOR_BGR2GRAY)
        
        # Template matching
        result = cv2.matchTemplate(screenshot_gray, template_gray, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        if max_val >= 0.8:  # Confidence threshold
            h, w = template_gray.shape
            # print(f"Form template matched with confidence: {max_val:.2f}")
            return (max_loc[0], max_loc[1], w, h)
        else:
            ...
            # print(f"Form template match too low: {max_val:.2f}")
        
        return None
        
    except Exception as e:
        print(f"Error in template search: {e}")
        return None

# Example usage
if __name__ == "__main__":
    # Run the main function
    asyncio.run(start())