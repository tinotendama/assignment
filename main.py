

import cv2
import streamlit as st
import sys
import numpy as np
import tensorflow as tf
import os
from tensorflow.keras import layers
from tensorflow.keras import Model
from os import getcwd
from keras.models import load_model

model = tf.keras.applications.inception_v3.InceptionV3(
    include_top=True,
    weights='imagenet',
    input_tensor=None,
    input_shape=None,
    pooling=None,
    classes=1000,
    classifier_activation='softmax'
)

model.save('Model.h5')

model= load_model('Model.h5',compile=(False))

#Testining the model on a single frame
#Preprocessg

test = tf.io.read_file('/content/drive/MyDrive/frame/ants.jpg')
test= tf.io.decode_image(test,channels=3)
test= tf.image.resize(test,[299,299])
test = tf.expand_dims(test, axis=0)
test = tf.keras.applications.inception_v3.preprocess_input(test)

#Predicting and Decoding the Predictions
predictions = tf.keras.applications.inception_v3.decode_predictions(model.predict(test), top=1)

for (i, (imagenetID, label, prob)) in enumerate(predictions[0]):
    print("{}. {}: {:.2f}%".format(i+1, label, prob*100))

vid_cap = cv2.VideoCapture('muna.mp4')
success, image=vid_cap.read()
count = 0
while success:
    cv2.imwrite('frame%d.jpg'%count, image)
success, image=vid_cap.read()
print('read a new frame: ', success)
count+=1


def predict(frame, model):
    # Pre-process the image for model prediction
    img = cv2.resize(frame, (299, 299))
    img = img.astype(np.float32)
    img = np.expand_dims(img, axis=0)

    img /= 255.0

    # Predict with the Inceptionv3 model
    prediction = model.predict(img)

    # Convert the prediction into text
    pred_text = tf.keras.applications.inception_v3.decode_predictions(prediction, top=1)
    for (i, (imagenetID, label, prob)) in enumerate(pred_text[0]):
        label  = ("{}: {:.2f}%".format(label, prob * 100))

    st.markdown(label)

def predict2(frame, model):
    # Pre-process the image for model prediction
    img = cv2.resize(frame, (290, 290))
    img = img.astype(np.float32)
    img = np.expand_dims(img, axis=0)

    img /= 255.0

    # Predict with the Inceptionv3 model
    prediction = model.predict(img)

    # Convert the prediction into text
    pred_text = tf.keras.applications.inception_v3.decode_predictions(prediction, top=1)
    for (i, (imagenetID, label, prob)) in enumerate(pred_text[0]):
        pred_class = label
       

    return pred_class


def object_detection(search_key,frame, model):
    label = predict2(frame,model)
    label = label.lower()
    if label.find(search_key) > -1:
        st.image(frame, caption=label)

        return sys.exit()
    else:
        pass
        #st.text('Not Found')
        #return sys.exit()
        

# Main App
def main():
    """Visualization"""
    st.title("Object Detection ")
    st.text("Built with Streamlit and Inceptionv3")

    activities = ["Detect Objects", "About"]
    choice = st.sidebar.selectbox("Choose Activity", activities)
    
    if choice == "Detect Objects":
        st.subheader("Upload the video to detect")

        video_file = st.file_uploader("upload the video...", type=["mp4", "avi"])

        if video_file is not None:
            path = video_file.name
            with open(path,mode='wb') as f: 
                f.write(video_file.read())         
                st.success("Saved Video")
                video_file = open(path, "rb").read()
                st.video(video_file)
            cap = cv2.VideoCapture(path)
            frame_width = int(cap.get(3))
            frame_height = int(cap.get(4))

            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            output = cv2.VideoWriter('output.mp4', fourcc, 20.0, (frame_width, frame_height))
            
            if st.button("Detect Objects"):
                
                # Start the video prediction loop
                while cap.isOpened():
                    ret, frame = cap.read()
    
                    if not ret:
                        break
    
                    
                    # Perform object detection
                    predict(frame, model)
    
                    # Display the resulting frame
                    #st.image(frame, caption='Video Stream', use_column_width=True)
    
                cap.release()
                output.release()
                cv2.destroyAllWindows()
                
            key = st.text_input('Search key')
            key = key.lower()
            
            if key is not None:
            
                if st.button("Search for the object"):
                    
                    
                    # Start the video prediction loop
                    while cap.isOpened():
                        ret, frame = cap.read()
        
                        if not ret:
                            break
        
                        # Perform object detection
                        object_detection(key,frame, model)
                        
        
                        # Display the resulting frame
                        #st.image(frame, caption='Video Stream', use_column_width=True)
        
                    cap.release()
                    output.release()
                    cv2.destroyAllWindows()

    elif choice == "About":
        st.subheader("By")
        st.text("TINOTENDA AND RAYMOND")


if __name__ == '__main__':
    main()

   

