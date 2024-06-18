from flask import Blueprint, session, redirect, render_template
import cv2
import os


CAM = Blueprint('cam', __name__)


@CAM.route('/cam')
def camera():
    if "user" not in session:
        session["redirect"] = "cam"
        return redirect("/login")

    # Assurez-vous que la caméra est correctement initialisée
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return redirect("/cam")

    success, frame = cap.read()
    cap.release()  # Libérez la caméra après utilisation

    if success:
        # Enregistrer l'image capturée
        img_path = "app/static/captured_image.jpg"
        cv2.imwrite(img_path, frame)
        return render_template("cam.html")
    else:
        return redirect("/cam")
