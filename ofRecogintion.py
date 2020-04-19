import cv2
import pickle


class face:

    def geometry2(self,x, y, w, h, frame):  # vẽ khung xung quanh mặt
        drawBoxColor = [255, 255, 255]
        cv2.line(frame, (x, y), (x + (int(w / 5)), y), drawBoxColor, 1)
        cv2.line(frame, (x + (int(w / 5) * 4), y), (x + w, y), drawBoxColor, 1)
        cv2.line(frame, (x, y), (x, y + (int(h / 5))), drawBoxColor, 1)
        cv2.line(frame, (x + w, y), (x + w, y + int((h / 5))), drawBoxColor, 1)
        cv2.line(frame, (x, (y + int((h / 5 * 4)))), (x, y + h), drawBoxColor, 1)
        cv2.line(frame, (x, (y + h)), (x + int((w / 5)), y + h), drawBoxColor, 1)
        cv2.line(frame, (x + (int((w / 5) * 4)), y + h), (x + w, y + h), drawBoxColor, 1)
        cv2.line(frame, (x + w, (y + int((h / 5 * 4)))), (x + w, y + h), drawBoxColor, 1)
        return frame

    def recognize(self,x, y, w, h, labels, recognizer, gray, frame):

        roi_gray = gray[y:y + h, x:x + w]  # (ycord_start, ycord_end)
        roi_color = frame[y:y + h, x:x + w]

        id_, conf = recognizer.predict(roi_gray)
        if conf >= 45 and conf <= 85:
            # print(5:id_)
            print(labels[id_])
            font = cv2.FONT_HERSHEY_SIMPLEX
            name = labels[id_]
            color = (0, 200, 255)
            stroke = 1
            cv2.putText(frame, name, (x, y), font, 1, color, stroke, cv2.LINE_AA)

        color = (0, 200, 255)  # BGR 0-255
        stroke = 1
        end_cord_x = x + w
        end_cord_y = y + h
        face.geometry2(self, x, y, w, h, frame)
        return frame

    def recognizeface(self,lables, face_cascade, recognizer, detector, frame):

        ob = []
        center_face = [0, 0]
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # -- phat hien mat nguoi --#
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
        for (x, y, w, h) in faces:
            # print(x, y, w, h)
            distance_face = int(w + 3)
            distance_face2 = int(h + 3)
            # print(distance_face)
            # # end_cord_x = x + w
            # # end_cord_y = y + h
            center_face[0] = int(x + (w / 2))
            center_face[1] = int(y + (h / 2))

            # add vị trí khuôn mặt và trạng thái đếm
            if len(ob) == 0:
                # print('*')
                ob.append(center_face[0])
                ob.append(center_face[1])

            else:
                count = 0
                flat = 0
                while count < int(len(ob) / 2):
                    distance = abs(center_face[0] - ob[(count * 2)])
                    distance2 = abs(center_face[1] - ob[((count * 2) + 1)])
                    # print(distance,distance_face)
                    if distance <= distance_face:
                        if distance2 <= distance_face2:
                            flat = 1
                            cv2.line(frame, (center_face[0], center_face[1]), (ob[(count * 2)], ob[((count * 2) + 1)]),
                                     [0, 0, 255], 1)
                            break
                    count = count + 1
                if flat == 0:
                    # print('#')
                    ob.append(center_face[0])
                    ob.append(center_face[1])
            # print('het face')
            frame = face.recognize(self,x, y, w, h, lables, recognizer, gray, frame)

        return frame
