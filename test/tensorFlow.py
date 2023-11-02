import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import tensorflow as tf

print ("Leyendo CSV")
temperature_df = pd.read_csv("celsius_a_fahrenheit.csv")
 
# Visualización
sns.scatterplot(temperature_df)
#plt.show()

#Cargando Set de Datos
print ("Seleccionando las columnas")
X_train = temperature_df['Celsius']
y_train = temperature_df['Fahrenheit']

#Creando el Modelo
print ("Creando el modelo")
model = tf.keras.Sequential()
model.add(tf.keras.layers.Dense(units=1, input_shape=[1]))

#Compilado
print ("Compilando el modelo")
model.compile(optimizer=tf.keras.optimizers.Adam(1), loss='mean_squared_error')

#Entrenando el modelo
print ("Entrenando el modelo")
epochs_hist = model.fit(X_train, y_train, epochs = 100)

#Evaluando modelo
print ("Evaluando el modelo entrenado")
print ("Keys:")
print(epochs_hist.history.keys())
	
#Grafico
plt.plot(epochs_hist.history['loss'])
plt.title('Progreso de Pérdida durante Entrenamiento del Modelo')
plt.xlabel('Epoch')
plt.ylabel('Training Loss')
plt.legend('Training Loss')
#plt.show()

Temp_C = 218
Temp_F = model.predict([Temp_C])
print("Temperatura de Prediccion: " + str(Temp_F))

Temp_F = 9/5 * Temp_C + 32
print("Temperatura de Ecuacion: " + str(Temp_F))
