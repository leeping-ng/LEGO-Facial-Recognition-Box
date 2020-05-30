import os
import face_recognition

def create_embeddings(settings):
    """
    Create embeddings for whitelisted faces.
    
    Takes in:
        - settings: a dictionary of settings specified in settings.yml

    Returns:
        - whitelisted_face_names: a list of whitelisted names
        - whitelisted_face_encodings: a list of encoded face vectors
    """
    whitelisted_face_encodings = []
    whitelisted_face_names = []

    print("[INFO] Creating face embeddings...")

    # only create face embeddings for the people who have been granted access
    whitelisted_people = settings['grant_access']
    for whitelisted_person in whitelisted_people:
        image_path_no_ext = os.path.join(settings['faces_folder'], whitelisted_person)
        # try different file extensions for images
        for ext in ['.jpg', '.png', '.jpeg']:
            try:
                # if the whitelisted name matches the face image name in the folder, embed the image
                image = face_recognition.load_image_file(image_path_no_ext + ext)
                face_encoding = face_recognition.face_encodings(image)[0]
                whitelisted_face_encodings.append(face_encoding)

                # can't use whitelisted_people directly, in case their images are not in the folder
                whitelisted_face_names.append(whitelisted_person)
                break
            except:
                pass

    print("[INFO] Face embeddings created!")
    print('{} will be granted access.'.format(whitelisted_face_names))

    return whitelisted_face_names, whitelisted_face_encodings

        

