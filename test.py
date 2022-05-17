from flask import Flask,render_template,request,redirect,send_file,url_for
import subprocess
import os
from os import path
import cv2
from werkzeug.utils import send_file
from PIL import Image,ImageChops

app=Flask("__name__")
d = "static/img/test.jpg"

'''cmd="python b2w.py"
p=subprocess.Popen(cmd,shell=True)
out=p.communicate()'''
def is_greyscale(im):
    """
    Check if image is monochrome (1 channel or 3 identical channels)
    """
    if im.mode not in ("L", "RGB"):
        raise ValueError("Unsuported image mode")

    if im.mode == "RGB":
        rgb = im.split()
        if ImageChops.difference(rgb[0],rgb[1]).getextrema()[1]!=0: 
            return False
        if ImageChops.difference(rgb[0],rgb[2]).getextrema()[1]!=0: 
            return False
    return True

@app.route('/')
def  hello_world():   
    return render_template('index.html',d=d,path=path)

app.config["IMAGE_UPLOADS"]="D:/HCI Jcomp/static/img"
@app.route("/uploadImage",methods=["GET","POST"])
def upload_image():
    if request.method=="POST":
        if request.files:
            image=request.files["image"]
            image.save(os.path.join(app.config["IMAGE_UPLOADS"],"upload.jpg"))
            im= Image.open("./static/img/upload.jpg")
            if is_greyscale(im):
                im.save("./static/img/test.jpg")
                return redirect(request.url)
                
            else:
                msg="Please Enter a valid Black and White Image"
                
                return render_template("index.html",d=d,path=path,msg=msg)
            

    return render_template('index.html',d=d,path=path)

@app.route("/colorize")
def colorize():
    '''cmd="python b2w.py"
    p=subprocess.Popen(cmd,shell=True)
    out=p.communicate()'''
    exec(open("b2w.py").read())
    
    return render_template('index.html',d=d,path=path)
@app.route("/download")
def download_file():
    down="./static/img/out.jpg"
    return send_file(down,as_attachment=True,environ=request.environ)
'''@app.route('/imgcheck')
def imgcheck():
    msg=""'''

if __name__=="__main__":
    
    app.run(debug=True)


