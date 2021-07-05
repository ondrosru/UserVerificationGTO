import io
import base64
import os
import cv2
import qrcode
import numpy as np
import face_recognition
from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from fastapi.responses import FileResponse
from typing import Any, List



from app.core.config import get_settings
from app.schemas.user import User
from app.db.repositories.user import user_repository
from app.db.repositories.user_photo import user_photo_repository
from app.db.repositories.trial_in_event import trial_in_event_repository
from app.db.repositories.result_on_trial_in_event import result_on_trial_in_event_repository
from app.db.repositories.event_participant import event_participant_repository
from app.api.deps import get_db


router = APIRouter()
settings = get_settings()
BASE_DIR = os.path.abspath(os.getcwd())


@router.get("/event/{event_id}/trial/{trial_id}/search", response_model=List[User])
def search_user(event_id: int, trial_id: int, text: str = '', *, db=Depends(get_db)) -> Any:
    trial_in_event = trial_in_event_repository.get_all_by_event_id_and_trial_id(
        db, event_id=event_id, trial_id=trial_id)
    if not trial_in_event:
        raise HTTPException(404, detail="Trial in current event not found")
    user_ids = set()
    users_in_trial = result_on_trial_in_event_repository.get_all_by_trial_event_id(
        db, trial_event_id=trial_in_event.id)
    for user_in_trial in users_in_trial:
        user_ids.add(user_in_trial.user_id)
    users = user_repository.search_user(db, text)
    result = []
    for user in users:
        if user.id in user_ids:
            result.append(user)
    return result


@router.get("/event/{event_id}/search", response_model=List[User])
def search_user_in_event(event_id: int, text: str = '', *, db=Depends(get_db)) -> Any:
    users_in_event = event_participant_repository.get_by_event_id(
        db, event_id=event_id)
    if users_in_event == []:
        return []
    user_ids = set()
    for user_in_event in users_in_event:
        user_ids.add(user_in_event.user_id)
    users = user_repository.search_user(db, text)
    result = []
    for user in users:
        if user.id in user_ids:
            result.append(user)
    return result


@router.post("/event/{event_id}/trial/{trial_id}/search/by_photo")
def search_user_by_face(event_id: int, trial_id: int, img: UploadFile = File(...),  *, db=Depends(get_db)) -> Any:
    trial_in_event = trial_in_event_repository.get_all_by_event_id_and_trial_id(
        db, event_id=event_id, trial_id=trial_id)
    if not trial_in_event:
        raise HTTPException(404, detail="Trial in current event not found")
    user_ids = set()
    users_in_trial = result_on_trial_in_event_repository.get_all_by_trial_event_id(
        db, trial_event_id=trial_in_event.id)
    for user_in_trial in users_in_trial:
        user_ids.add(user_in_trial.user_id)
    path = os.path.abspath(os.path.join(BASE_DIR, settings.IMG_DIR))
    known_faces_user_id = []
    known_face_encodings_images = []
    for user_id in user_ids:
        user_photo = user_photo_repository.get_user_photo_by_user_id(
            db, user_id)
        if user_photo:
            image_path = os.path.abspath(
                os.path.join(path, user_photo.img_name))
            if (os.path.exists(image_path)):
                image = face_recognition.load_image_file(image_path)
                image_face_encoding = face_recognition.face_encodings(image)[0]
                known_face_encodings_images.append(image_face_encoding)
                known_faces_user_id.append(user_id)
    unknown_image = load_image_into_numpy_array(img.file.read())
    face_locations = face_recognition.face_locations(unknown_image)
    face_encodings = face_recognition.face_encodings(
        unknown_image, face_locations)
    user = None
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(
            known_face_encodings_images, face_encoding)
        face_distances = face_recognition.face_distance(
            known_face_encodings_images, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            user = user_repository.get(
                db, id=known_faces_user_id[best_match_index])

    if not user:
        raise HTTPException(404, detail="User not found.")
    return user


@router.post("/event/{event_id}/search/by_photo")
def search_user_by_face_in_event(event_id: int, img: UploadFile = File(...),  *, db=Depends(get_db)) -> Any:
    users_in_event = event_participant_repository.get_by_event_id(
        db, event_id=event_id)
    if users_in_event == []:
        raise HTTPException(404, detail="No participants found for this event")
    path = os.path.abspath(os.path.join(BASE_DIR, settings.IMG_DIR))
    known_faces_user_id = []
    known_face_encodings_images = []
    for user_in_event in users_in_event:
        user_photo = user_photo_repository.get_user_photo_by_user_id(
            db, user_in_event.user_id)
        if user_photo:
            image_path = os.path.abspath(
                os.path.join(path, user_photo.img_name))
            if (os.path.exists(image_path)):
                image = face_recognition.load_image_file(image_path)
                image_face_encoding = face_recognition.face_encodings(image)[0]
                known_face_encodings_images.append(image_face_encoding)
                known_faces_user_id.append(user_in_event.user_id)
    unknown_image = load_image_into_numpy_array(img.file.read())
    face_locations = face_recognition.face_locations(unknown_image)
    face_encodings = face_recognition.face_encodings(
        unknown_image, face_locations)
    user = None
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(
            known_face_encodings_images, face_encoding)
        face_distances = face_recognition.face_distance(
            known_face_encodings_images, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            user = user_repository.get(
                db, id=known_faces_user_id[best_match_index])

    if not user:
        raise HTTPException(404, detail="User not found.")
    return user


@router.post("/qr")
def get_qr(user_id: int, *, db=Depends(get_db)):
    user = user_repository.get(db, id=user_id)
    if not user:
        raise HTTPException(404, detail="User not found")
    text_for_qr = user.id.__str__() + user.email
    encMessage = rsa.encrypt(text_for_qr.encode(), publicKey)
    print(encMessage)
    qr = qrcode.QRCode()
    qr.add_data(encMessage.decode())
    img = qr.make_image(fill_color="black", back_color="white")
    path = os.path.join(BASE_DIR, "temp.png")
    img.save(path)
    return FileResponse(path)


@router.post("/qr/id/")
def get_qr_id(text: str, *, db=Depends(get_db)):
    decMessage = rsa.decrypt(text.encode(), privateKey).decode()
    return decMessage


def load_image_into_numpy_array(data):
    npimg = np.frombuffer(data, np.uint8)
    frame = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return frame
