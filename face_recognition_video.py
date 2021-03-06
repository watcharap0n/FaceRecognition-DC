import numpy as np
import cv2
import dlib
from imutils import face_utils
import pickle


class ModelImage:
    FACE_DESC, FACE_NAME = pickle.load(open('train_datasets.pk', 'rb'))
    detector = dlib.get_frontal_face_detector()
    sp = dlib.shape_predictor('model_image/shape_predictor_68_face_landmarks.dat')
    model = dlib.face_recognition_model_v1('model_image/dlib_face_recognition_resnet_model_v1.dat')


class Recognition(ModelImage):
    def __init__(self, file_name):
        self.file_name = file_name

    def face_recognition_DLIB(self):
        cap = cv2.VideoCapture(self.file_name)
        while True:
            ret, image = cap.read()
            scale = 0.5
            image = cv2.resize(image, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
            gray_scale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            detected = self.detector(gray_scale, 1)
            for d in detected:
                xy = d.left(), d.top()
                wh = d.right(), d.bottom()
                shape = self.sp(gray_scale, d)
                face_desc_first = self.model.compute_face_descriptor(image, shape, 1)
                shape_circle = face_utils.shape_to_np(shape)
                d = []
                for face_desc in self.FACE_DESC:
                    d.append(np.linalg.norm(np.array(face_desc) - np.array(face_desc_first)))
                d = np.array(d)
                idx = np.argmin(d)
                print(d[idx])
                if d[idx] <= 0.39:
                    name = self.FACE_NAME[idx]
                    name = str(name)
                    percent = 1.0 - d[idx]
                    percent = percent * 100
                    cv2.putText(image, f'{name}', (xy[0], xy[1] - 15), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2,
                                cv2.LINE_AA)
                    cv2.putText(image, f'{round(percent, 1)}%', (xy[0] + 40, xy[1] + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                                (0, 255, 0), 2, cv2.LINE_AA)
                    cv2.rectangle(image, xy, wh, (0, 255, 0), 2)
                    for (x, y) in shape_circle:
                        cv2.circle(image, (x, y), 2, (0, 0, 255), -1)
                else:
                    percent = 1.0 - d[idx]
                    percent = percent * 100
                    cv2.putText(image, f'{round(percent, 1)}%', (xy[0], xy[1] - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                                (0, 0, 255), 2,
                                cv2.LINE_AA)
                    cv2.rectangle(image, xy, wh, (0, 0, 255), 2)
                    for (x, y) in shape_circle:
                        cv2.circle(image, (x, y), 2, (0, 0, 255), -1)
                write_image = image[xy[1] - 40:wh[1], xy[0]:wh[0]]
                # cv2.imwrite(filename='cropped.png', img=write_image)
                # cv2.imwrite(filename='preview.png', img=image)
            cv2.imshow('face_recognition', image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


face = Recognition(0)
face.face_recognition_DLIB()
