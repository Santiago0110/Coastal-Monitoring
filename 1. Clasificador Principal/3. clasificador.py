# -*- coding: utf-8 -*-
"""
Created on Sun Sep 15 17:36:20 2019
@author: Santiago Lasso
"""
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
"""---------------------------------------------------------------------------- 
Leer archivo de datos
----------------------------------------------------------------------------""" 
import pandas as pd
data = pd.read_csv("1.1 dataset.csv", sep=';')
data["Zona"]= pd.factorize(data["Zona"])[0]
"""---------------------------------------------------------------------------- 
Lee CSV y crea un imagen de los valores RGB de cada punto del CSV 
----------------------------------------------------------------------------"""
def frame_to_img(csv):
    size = csv.shape[0]
    raiz = np.sqrt(size)
    r = int(np.ceil(raiz))
    new_img = np.zeros((r,r,3),'uint8')
    i=0
    while i<(r*2):
        for j in range(r):
            for k in range(r):
                if(i<size):
                    new_img[j,k,0] = data["r"][i]
                    new_img[j,k,1] = data["g"][i]
                    new_img[j,k,2] = data["b"][i]
                i+=1
    plt.imshow(new_img)
    img_final = Image.fromarray(new_img)
    img_final.save('Imágenes Presentación/dataframe_img.jpg')
"""---------------------------------------------------------------------------- 
Separación de datos: X y Y
----------------------------------------------------------------------------"""
# Extrae DATOS (RGB) desde comienzo de la columna hasta columna -1
X = data[data.columns[3:-1]] 
# Extrae CLASE (ZONA) a la que pertenecen los datos
Y = data[data.columns[-1]]   

#Mostrar X e Y: 4 primeras filas
print(X[:4])
print(Y[:4])

#Hace un random de los índices de los datos
index = np.random.permutation(len(Y))

#DataFrame to Array
X=X.as_matrix()
Y=Y.as_matrix()

#Separación de datos 70/30
split = 0.3
X_train = X[index[int(split*len(Y)):]]
Y_train = Y[index[int(split*len(Y)):]]
X_test = X[index[0:int(split*len(Y))],:]
Y_test = Y[index[0:int(split*len(Y))]]
"""---------------------------------------------------------------------------- 
Función que genera la matriz de confusión
----------------------------------------------------------------------------""" 
import itertools 

def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype('float')/cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
"""---------------------------------------------------------------------------- 
Entrenamiento
----------------------------------------------------------------------------"""
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

#n_estimators = number of trees in the random forest
model=RandomForestClassifier(max_depth=10, n_estimators=30, max_features=3)
model.fit(X_train,Y_train)

#Predecir valores
score_train = model.score(X_train,Y_train)
score_test = model.score(X_test,Y_test)

#Porcentaje de eficiencia de datos entrenados
print(score_train)
#Porcentaje de eficiencia de datos validados
print(score_test)
#Porcentaje de importancia por RGB
print(model.feature_importances_)
"""---------------------------------------------------------------------------- 
Salida del modelo junto con la matriz de confusión
----------------------------------------------------------------------------"""
from sklearn.metrics import confusion_matrix

#Predicción con datos del 30% X_test
predicted = model.predict(X_test)
#Cambiar tipo de dato
A = predicted.astype(int)
accuracy = accuracy_score(Y_test, A) 
print(accuracy)
cm = confusion_matrix(Y_test, A)
plot_confusion_matrix(cm, [0,1,2,3,4])
"""---------------------------------------------------------------------------- 
Guardar modelo
----------------------------------------------------------------------------"""
from sklearn.externals import joblib 
joblib.dump(model, '3.1 modelo.pkl') 