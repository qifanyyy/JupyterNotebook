import math
from sklearn import neighbors
import os
import os.path
import pickle
from PIL import Image, ImageDraw
import face_recognition
from face_recognition.face_recognition_cli import image_files_in_folder
from fnmatch import fnmatch
from shutil import move, copy2

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'JPG', 'PNG'}

def train(train_directory_path, model_save_path=None, n_neighbors=None, knn_algo='ball_tree'):
    """
    Trains a k-nearest neighbors classifier for face recognition.
    :param train_directory_path: directory that contains a sub-directory for each known person, with its name.
    :param model_save_path: (optional) path to save model on disk
    :param n_neighbors: (optional) number of neighbors to weigh in classification. Chosen automatically if not specified
    :param knn_algo: (optional) underlying data structure to support knn.default is ball_tree
    :return: returns knn classifier that was trained on the given data.
    """
    X = []
    y = []

    # Loop through each person in the training set
    for class_directory_path in os.listdir(train_directory_path):
        if not os.path.isdir(os.path.join(train_directory_path, class_directory_path)):
            continue

        # Loop through each training image for the current person
        for img_path in image_files_in_folder(os.path.join(train_directory_path, class_directory_path)):
            image = face_recognition.load_image_file(img_path)
            face_bounding_boxes = face_recognition.face_locations(image)

            if len(face_bounding_boxes) == 1:
                # Add face encoding for current image to the training set as long as there is only one face in the picture
                X.append(face_recognition.face_encodings(image, known_face_locations=face_bounding_boxes)[0])
                y.append(class_directory_path)

    # Determine how many neighbors to use for weighting in the KNN classifier
    if n_neighbors is None:
        n_neighbors = int(round(math.sqrt(len(X))))

    if len(X) == 0 or len(y) == 0:
        print("Could not detect any faces.")
        quit()

    # Create and train the KNN classifier
    knn_clf = neighbors.KNeighborsClassifier(n_neighbors=n_neighbors, algorithm=knn_algo, weights='distance')
    knn_clf.fit(X, y)

    # Save the trained KNN classifier
    if model_save_path is not None:
        with open(model_save_path, 'wb') as f:
            pickle.dump(knn_clf, f)

    return knn_clf


def predict(predict_directory_path, knn_clf=None, model_path=None, distance_threshold=0.6):
    """
    Recognizes faces in given image using a trained KNN classifier
    :param predict_directory_path: path to image to be recognized
    :param knn_clf: (optional) a knn classifier object. if not specified, model_save_path must be specified.
    :param model_path: (optional) path to a pickled knn classifier. if not specified, model_save_path must be knn_clf.
    :param distance_threshold: (optional) distance threshold for face classification. the larger it is, the more chance
           of mis-classifying an unknown person as a known one.
    :return: a list of names and face locations for the recognized faces in the image: [(name, bounding box), ...].
        For faces of unrecognized persons, the name 'unknown' will be returned.
    """
    if not os.path.isfile(predict_directory_path) or os.path.splitext(predict_directory_path)[1][1:] not in ALLOWED_EXTENSIONS:
        raise Exception("Invalid image path: {}".format(predict_directory_path))

    if knn_clf is None and model_path is None:
        raise Exception("Must supply knn classifier either thourgh knn_clf or model_path")

    # Load a trained KNN model (if one was passed in)
    if knn_clf is None:
        with open(model_path, 'rb') as f:
            knn_clf = pickle.load(f)

    # Load image file and find face locations
    X_img = face_recognition.load_image_file(predict_directory_path)
    X_face_locations = face_recognition.face_locations(X_img)

    # If no faces are found in the image, return an empty result.
    if len(X_face_locations) == 0:
        return []

    # Find encodings for faces in the test iamge
    faces_encodings = face_recognition.face_encodings(X_img, known_face_locations=X_face_locations)

    # Use the KNN model to find the best matches for the test face
    closest_distances = knn_clf.kneighbors(faces_encodings, n_neighbors=1)
    are_matches = [closest_distances[0][i][0] <= distance_threshold for i in range(len(X_face_locations))]

    # Predict classes and remove classifications that aren't within the threshold
    return [(pred, loc) if rec else ("unknown", loc) for pred, loc, rec in zip(knn_clf.predict(faces_encodings), X_face_locations, are_matches)]

def copy_files(name, source_file_path, copy_directory_path):
    copy2_directory_path = os.path.join(copy_directory_path, name)
    if os.path.exists(copy2_directory_path):
        copy2(source_file_path, copy2_directory_path)
    else:
        os.mkdir(copy2_directory_path)
        copy2(source_file_path, copy2_directory_path)


def open_photos(nameInput, retrieve_directory_path):
    retrieve2_directory_path = os.path.join(retrieve_directory_path, nameInput)
    if os.path.exists(retrieve2_directory_path):
        for path, subdirs, files in os.walk(retrieve2_directory_path):
            for name in files:
                photo = Image.open(os.path.join(path, name))
                photo.show()

    else:
        print("Invalid input.")
        quit()


if __name__ == "__main__":

    fileList = []
    pattern = "*.png"
    pattern2 = "*.PNG"
    pattern3 = "*.JPG"
    pattern4 = "*.jpg"
    pattern5 = "*.jpeg"

    # STEP 1: Train the KNN classifier and save it to disk
    # Once the model is trained and saved, you can skip this step next time.
    trainBoolean = input("Do you want to train a model? (Y/N)     ")
    if trainBoolean == "Y":
        train_directory_path = input("Enter the directory path that contains the photos you want to train your model on:     ")
        if os.path.isdir(train_directory_path):
            print("Training KNN classifier...")
            classifier = train(train_directory_path, model_save_path="trained_knn_model.clf")
            print("Training complete!")
        else:
            print("Directory does not exist.")
            quit()
    elif trainBoolean != "N":
        print("Invalid input.")
        quit()


    # STEP 2: Using the trained classifier, make predictions for unknown images
    predictBoolean = input("Do you want to predict the faces in your photos? (Y/N)     ")
    if predictBoolean == "Y":
        predict_directory_path = input("Enter the directory path that contains the photos you want to use your model on:     ")
        copy_directory_path = input("Enter the directory path that you want to copy the photos to:     ")
        if os.path.isdir(predict_directory_path) and os.path.isdir(copy_directory_path):
            for path, subdirs, files in os.walk(predict_directory_path):
                for name in files:
                    fileList.append(os.path.join(path, name))

            for file_path in fileList:
                if fnmatch(file_path, pattern) or fnmatch(file_path, pattern2) or fnmatch(file_path, pattern3) or fnmatch(file_path, pattern4) or fnmatch(file_path, pattern5):

                    print("Looking for faces in {}".format(file_path))

                    # Find all people in the image using a trained classifier model
                    # Note: You can pass in either a classifier file name or a classifier model instance
                    predictions = predict(file_path, model_path="trained_knn_model.clf")

                    # Print results on the console
                    for name, (top, right, bottom, left) in predictions:
                        print("- Found {} at ({}, {})".format(name, left, top))
                        if name != "unknown":
                            copy_files(name, file_path, copy_directory_path)
        elif not(os.path.isdir(predict_directory_path)) and not(os.path.isdir(copy_directory_path)):
            print("Both directories do not exist.")
            quit()
        elif not(os.path.isdir(copy_directory_path)):
            print("The directory you want to copy the photos to does not exist.")
            quit()
        elif not(os.path.isdir(predict_directory_path)):
            print("The directory that contains the photos you want to use the model on does not exist.")
            quit()

    elif predictBoolean != "N":
        print("Invalid input.")
        quit()

    #STEP 3: Based on the user input, you can retrieve the photos you want.
    retrieveBoolean = input("Do you want to retrieve any of the photos you have classified. (Y/N)     ")
    if retrieveBoolean == "Y":
        if predictBoolean == "N":
            retrieve_directory_path = input("Enter the directory path that you want to retrieve the photos from:     ")
        else:
            retrieve_directory_path = copy_directory_path
        nameInput = input("Enter the name of the person whose photos you would like to retrieve:     ")
        open_photos(nameInput,retrieve_directory_path)
    elif retrieveBoolean != "N":
        print("Invalid input.")
        quit()
