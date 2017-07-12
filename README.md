# Project
This is a project repository incuding simple flask API  for accepting data – images 
in various formats via POST on http://localhost:5000/images/upload. API accept image, 
figure out wheter image is in SVG format and corvert it to PNG format and then 
return. If image is in any other format just simply return without any changes.

Repository including two type of app file. ( app.py and app2.py)
app.py – accepting  multiple images and after converting display them on website.
app2.py – accepting only one image and after converting save it to disk.

After installing requirements.txt you can simpy run API with python3 app.py/app2.py
