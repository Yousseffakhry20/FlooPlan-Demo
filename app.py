from flask import Flask,render_template,request,redirect,jsonify,make_response

import numpy as np
import cv2

from flask import request, redirect
import pytesseract
import nums_from_string




from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import FileField
from flask_uploads import configure_uploads, IMAGES, UploadSet

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'

app= Flask(__name__,template_folder='template')










app.config['SECRET_KEY'] = 'thisisasecret'
app.config['UPLOADED_IMAGES_DEST'] = r'static\Image\Uploads'

images = UploadSet('images', IMAGES)
configure_uploads(app, images)

class MyForm(FlaskForm):
    image = FileField('image')

@app.route('/', methods=['GET', 'POST'])
def upload_image():
    form = MyForm()

    if form.validate_on_submit():
        
        filename = images.save(form.image.data)
        # return f'Filename: { filename }'


        img = cv2.imread(r'D:\HTML\Flask Tutorial\static\Image\Uploads\\'+ filename)

        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

        _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

        # cv2.imshow('',thresh)

        mor_img = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, (100,100), iterations=1)

        contours, hierarchy = cv2.findContours(mor_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) # I addapted this part of the code. This is how my version works (2.4.16), but it could be different for OpenCV 3 

        sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)

        for c in sorted_contours[1:]:
            area = cv2.contourArea(c)
            if area > 6000:
                print (area)
                cv2.drawContours(img, [c], -1, (0,0,200), 3)
                x, y, w, h = cv2.boundingRect(c) # the lines below are for getting the approximate center of the rooms
                cx = x + w / 2
                cy = y + h / 2
                # cv2.putText(img,str(area),(cx,cy), cv2.FONT_HERSHEY_SIMPLEX, .5,(255,0,0),1,cv2.CV_AA)

        # cv2.imshow('',mor_img)
        # cv2.imshow('',img)
        # cv2.waitKey(0)



        text=pytesseract.image_to_string(img,config="--psm 11")


        sentence = text
        print(nums_from_string.get_nums(sentence))
        output=nums_from_string.get_nums(sentence)

        return render_template(r"UploadImage.html", form=form,detected_dimensions='Dimensions are {}'.format(output))
    
    else:
        return render_template(r"UploadImage.html", form=form)




















if __name__ == "__main__":
    app.run(debug=True) 