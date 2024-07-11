from flask import Blueprint, session, redirect, render_template
import cv2
import app.routes.api as api


CAM = Blueprint('cam', __name__)


@CAM.route('/cam')
def camera():
    if api.checks(["login", "module-camera"]):
        return api.checks(["login", "module-camera"])

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
