# from PIL import Image
# import os, glob
# import numpy as np
# from sklearn.model_selection import train_test_split
# import cv2

# # 분류 대상 카테고리 선택하기 --- (※1)
# caltech_dir = "./image/101_ObjectCategories"
# categories = [ 'Heart', 'Oblong', 'Oval', 'Round', 'Square' ]
# nb_classes = len(categories)

# # 이미지 크기 지정 --- (※2)
# image_w = 64 
# image_h = 64
# pixels = image_w * image_h * 3

# # 이미지 데이터 읽어 들이기 --- (※3)
# X = []
# Y = []
# for idx, cat in enumerate(categories):
#     # 레이블 지정 --- (※4)
#     # One Hot Encoding (비트를 이용하여 labeling)
#     label = [0 for i in range(nb_classes)]
#     label[idx] = 1

# # 이미지 --- (※5)
#     IMAGE_DIR = './imageSet/processed_training_set/'+cat+'/'
#     files = glob.glob(IMAGE_DIR+"/*.jpg")
#     for i, f in enumerate(files):
#         img = Image.open(f) # --- (※6)
#         img = img.convert("RGB")
#         img = img.resize((image_w, image_h))
#         data = np.asarray(img)
#         X.append(data)
#         Y.append(label)
#         # if i % 10 == 0:
#         #     print(i, "\n", data)
# X = np.array(X)
# print(X)
# print(X.shape)
# Y = np.array(Y)
# # 학습 전용 데이터와 테스트 전용 데이터 구분 --- (※7)
# X_train, X_test, y_train, y_test = train_test_split(X, Y)
# # xy = (X_train, X_test, y_train, y_test)
# # np.save("./imageSet/5obj.npy", xy)
# # print("ok,", len(Y))


from keras.models import Sequential
from keras.layers import Convolution2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
import numpy as np
import tensorflow as tf

# 카테고리 지정하기
categories = [ 'Heart', 'Oblong', 'Oval', 'Round', 'Square' ]
nb_classes = len(categories)
# 이미지 크기 지정하기
image_w = 64 
image_h = 64

# 데이터 불러오기 --- (※1)
(X_train, X_test, y_train, y_test) = np.load("./imageSet/5obj.npy", allow_pickle=True)
# 데이터 정규화하기
X_train = X_train.astype("float") / 256
X_test  = X_test.astype("float")  / 256
print('X_train shape:', X_train.shape)

# 모델 구축하기 --- (※2)
model = Sequential()
model.add(Convolution2D(32, 3, 3, 
    padding='same',
    input_shape=X_train.shape[1:]))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Convolution2D(32, 3, 3, padding='same'))
model.add(Activation('relu'))
model.add(Convolution2D(32, 3, 3))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Flatten()) # --- (※3) 
model.add(Dense(512))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(nb_classes))
model.add(Activation('softmax'))

model.compile(loss='binary_crossentropy',
    optimizer='rmsprop',
    metrics=['accuracy'])

# 모델 훈련하기 --- (※4)
model.fit(X_train, y_train, batch_size=32, epochs=50)
    
# 모델 평가하기--- (※5)
score = model.evaluate(X_test, y_test)
print('loss=', score[0])
print('accuracy=', score[1])