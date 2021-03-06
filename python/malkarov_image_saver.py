#Импорт библиотек
import time
import numpy as np
import matplotlib.pyplot as plt #Библиотека визуализации графики
import vrep #Библиотека виртуальной среды
import random
from skimage import color, measure, draw #Библиотека анализа изображений

#Вывод информации о запуске программы
print ('Program started')

#Подключение к удалённой сессии
vrep.simxFinish(-1)
clientID = vrep.simxStart('127.0.0.1', 19997, True, True, 5000, 5)
if clientID!=-1:

     #Если подключение произошло успешно...
    print ('Connected to remote API server')
    vrep.simxStartSimulation(clientID,vrep.simx_opmode_oneshot)

    #Подключение камеры
    error, camera_1 = vrep.simxGetObjectHandle(clientID, 'perspective_vision_1', vrep.simx_opmode_oneshot_wait) #Левая камера
    error, camera_2 = vrep.simxGetObjectHandle(clientID, 'perspective_vision_2', vrep.simx_opmode_oneshot_wait) #Правая камера
    
    #Получение изображений с камер
    error, resolution, image_1 = vrep.simxGetVisionSensorImage(clientID, camera_1, 0, vrep.simx_opmode_streaming)
    error, resolution, image_2 = vrep.simxGetVisionSensorImage(clientID, camera_2, 0, vrep.simx_opmode_streaming)

    #Установка задержки 0.1 секунды
    time.sleep(0.1)
    increment = 0
    message = 0

    #Состояние подключения к виртуальной сессии
    error, info = vrep.simxGetInMessageInfo(clientID, vrep.simx_headeroffset_server_state)

    #Пока нет ошибки...
    while (info != 0):

        #Если нет ошибки чтения изображения, приступить к чтению данных с камеры...
        error, resolution, image_1 = vrep.simxGetVisionSensorImage(clientID, camera_1, 0, vrep.simx_opmode_buffer)
        error, resolution, image_2 = vrep.simxGetVisionSensorImage(clientID, camera_2, 0, vrep.simx_opmode_buffer)
        if error == vrep.simx_return_ok:

            #Пока снимков меньше 200...
            if increment <= 200:

                #Получение массива из изображения с первой камеры           
                img_1 = np.array(image_1, dtype = np.uint8)
                img_1.resize([resolution[1], resolution[0],3])
                img_1 = np.flip(img_1, axis=0) #Отразить полученные данные по вертикали

                #Запись в файл текстурированного изображения
                plt.imsave("D:/robot_workspace/photos/textured/fig_{}.png".format(increment), img_1)

                #Получение массива из изображения со второй камеры
                img_2 = np.array(image_2, dtype = np.uint8)
                img_2.resize([resolution[1], resolution[0],3])
                img_2 = np.flip(img_2, axis=0)

                #Запись в файл целевого изображения
                plt.imsave("D:/robot_workspace/photos/discoloured/fig_{}.png".format(increment), img_2)

                increment += 1 #Инкремент числа снимков

                time.sleep(0.25) #Период создания снимков
            else:
                if message == 0:
                    
                    #Остановить сохранение изображений и вывести сообщение
                    print ('Max count of images')
                    message = 1
        else:
            print('Error:', error) #Вывести, если возникла ошибка чтения

        error, info = vrep.simxGetInMessageInfo(clientID, vrep.simx_headeroffset_server_state)

    vrep.simxFinish(clientID)
else:
    print ('Failed connecting to remote API server') #Вывести, если возникла ошибка подключения
print ('Program ended') #Вывести при завершении приложения