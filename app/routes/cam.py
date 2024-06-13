
from flask import Blueprint, session, redirect, render_template
import cv2
import os


camera = cv2.VideoCapture(0)
    
    
CAM = Blueprint('cam', __name__)

@CAM.route('/cam')
def spotify():
    if 'user' not in session:
        session['redirect'] = 'cam'
        return redirect("/login")
    success, frame = camera.read()
    if success:
        # Enregistrer l'image capturée
        img_path = 'app/static/captured_image.jpg'
        cv2.imwrite(img_path, frame)
        return render_template('cam.html', img_path=img_path)
    
    