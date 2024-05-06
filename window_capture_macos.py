from array import array
from Quartz import CGWindowListCopyWindowInfo, kCGWindowListOptionOnScreenOnly, kCGNullWindowID, CGWindowListCreateImageFromArray, CGRectNull, kCGWindowImageDefault
from Quartz.CoreGraphics import CGImageGetWidth, CGImageGetHeight, CGImageGetDataProvider, CGDataProviderCopyData
from PIL import Image, ImageGrab
import numpy as np
import os

class WindowCaptureMacos:
    w=0
    h=0
    window_id = None
    def __init__(self):
         # Get a list of all windows
        window_list = CGWindowListCopyWindowInfo(kCGWindowListOptionOnScreenOnly, kCGNullWindowID)

        # Find the window belonging to the specific process
        for window in window_list:
            if window['kCGWindowOwnerName'] == "Albion Online Client":
                # Get the window's position and size
                window_id = window['kCGWindowNumber']
                window_bounds = window['kCGWindowBounds']
                x = window_bounds['X']
                y = window_bounds['Y']
                h = window_bounds['Height']
                w = window_bounds['Width']
                self.window_id = window_id
                break
    
    def get_screenshot(self):
        window_array = array('i', [self.window_id])
        print(window_array)
        # Capture the screenshot
        image = CGWindowListCreateImageFromArray(CGRectNull, window_array, kCGWindowImageDefault)
        print(image)
        width = CGImageGetWidth(image)
        height = CGImageGetHeight(image)
        print(width, height)
        data_provider = CGImageGetDataProvider(image)
        data = CGDataProviderCopyData(data_provider)
    
    
        os.system('screencapture -x -l -x %s' % (self.window_id))
        
        # pil_image = Image.frombytes("RGBA", (width, height), bytes(data))
        pil_image = ImageGrab.grabclipboard()
        # Save the PIL Image
        # pil_image.save("screenshot.png")
        
        # Convert the data to a numpy ndarray
        img = np.array(pil_image)
        # img.shape = (height, width, 4)

        # Remove the alpha channel
        img = img[..., :3]
        
        # convert to BGR
        img = img[:, :, ::-1]
        
        # Ensure the array is C-contiguous for some cv2 functions
        img = np.ascontiguousarray(img)
        return img
        