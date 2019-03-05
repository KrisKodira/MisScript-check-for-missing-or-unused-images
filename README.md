# Check for missing or unused images in website
A Python script that makes it simple to check a website for missing images or unused images

# What is MisScript?
MisScript is a Python Script that you can run on your web server to check if any .html, .php, .js or .css files contain dead links to images or if there are any images on the server that are not used by any files.

# Requirements
- Python 3  
- You need to install **Python Requests** to be able to check dead image links that aren't directly on the server.  
Install it with pip like this:  
    `pip install requests`

# Installation & Usage
The easiest way to use MisScript is to download it and place inside the folder of the file or directory you want to check.  
Then follow these steps:  
1. Open your terminal in the directory you want to check
2. Type `python3 check-image.py` in your terminal
3. Then you will be asked if you want to check only one file or a whole directory
    * **If you choose dir:**
    * You will be asked if you want to check the current directory or some other directory
    * Then you can choose to exclude some folders from being checked. Keep in mind that folders should be excluded if you generate the image url for example with php or javascript while the site is running. You can exclude both the image folder or the folder with the css/js/php and html files.
    
    * **If you choose file**
    * You will get your results immediatly
4. You will get a result with the amount of missing and unused images and the space that is used by all the images that aren't linked (If you want an accurate number of unused images you need to exclude the folders that generate images themselves)
5. Now you will be able to list all the missing or unused images in the terminal or skip to the next step
6. Here you can choose if you want to save all the paths to the unused and missing images to a .txt file (The .txt file will generate a file in the directory you're checking)
7. Now you can choose to move all the unused images into a folder (Be careful with this since I haven't tested this enough. I would recommend creating the file from the previous step and then deleting the images by hand.)
8. That's it!

# Disclaimer
- Don't use the **moving**-feature (step 7.) on sensitive data since it may break your website
- Use this script at your own risk
- I am not responsible for anything that happens with your data
