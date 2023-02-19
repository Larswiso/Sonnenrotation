# Autor Lars Wisotzky
# Dieses Programm ist NUR für die Bilder von SDO zugeschnitten.
# https://sdo.gsfc.nasa.gov/data/aiahmi/


import datetime
import math
import re

import cv2
import matplotlib.pyplot as plt
import numpy as np
import openpyxl
import pandas as pd
from sympy import sign

IMAGE_1 = r".\Sonnenrotation\data\20130525_010655_1024_HMII.jpg"
IMAGE_2 = r".\Sonnenrotation\data\20130527_053655_1024_HMII.jpg"

match1 = re.search(r"(\d{4})(\d{2})(\d{2})_(\d{2})(\d{2})(\d{2})", IMAGE_1)
match2 = re.search(r"(\d{4})(\d{2})(\d{2})_(\d{2})(\d{2})(\d{2})", IMAGE_2)

if match1 and match2:
    year1, month1, day1, hour1, minute1, second1 = match1.groups()
    date_time1 = datetime.datetime(int(year1), int(month1), int(day1), int(hour1), int(minute1), int(second1))
    
    year2, month2, day2, hour2, minute2, second2 = match2.groups()
    date_time2 = datetime.datetime(int(year2), int(month2), int(day2), int(hour2), int(minute2), int(second2))
    
    time_difference = (date_time2 - date_time1).total_seconds() / 86400
    print("Zeitdifferenz in Tagen: {:.2f}".format(time_difference))
else:
    print("Keine Zeit gefunden.")

# Berechne die südlichste, nördlichste, westlichste und östlichste Koordinate des Objekts
img = cv2.imread(IMAGE_1)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 50, 150)
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
obj_contour = max(contours, key = cv2.contourArea)

left = tuple(obj_contour[obj_contour[:, :, 0].argmin()][0])
right = tuple(obj_contour[obj_contour[:, :, 0].argmax()][0])
top = tuple(obj_contour[obj_contour[:, :, 1].argmin()][0])
bottom = tuple(obj_contour[obj_contour[:, :, 1].argmax()][0])


# Mittelpunkt der Sonne
for cnt in contours:
    if cv2.contourArea(cnt) > 200: # nur contours mit einer Fläche größer als 50 betrachten
        M = cv2.moments(cnt)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])

# Radius der Sonne
sun_radius = right[0] - cX

# berechnet distanz vom rand zum mittelpunkt auf einer höhe
def find_edge(img, point_y):
    edge_x = 0
    edges = cv2.Canny(img, 50, 150)
    while True:
        if edges[edge_x, point_y] > 0:
            break
        else:
            edge_x += 1
    distance = cX - edge_x
    return distance
import cv2

def show_sun(image, first_img=False):
    img = cv2.imread(image)

    # Flächen erkennen
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 127, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    def on_mouse(event, x, y, flags, param):
        global center_area
        global dist_to_edge

        if event == cv2.EVENT_LBUTTONDOWN:
            for cnt in contours:
                if cv2.contourArea(cnt) > 10 and cv2.contourArea(cnt) < 300: # nur contours mit einer Fläche größer als 50 betrachten
                    if cv2.pointPolygonTest(cnt, (x, y), False) >= 0:
                        # Mittelpunkt ermitteln
                        M = cv2.moments(cnt)
                        c_arae_X = int(M["m10"] / M["m00"])
                        c_arae_Y = int(M["m01"] / M["m00"])

                        dist_to_edge = find_edge(img, c_arae_Y) # auf der Höhe des Sonnenflecks
                        center_area = (c_arae_X, c_arae_Y)

            cv2.destroyAllWindows()

    if first_img:
        cv2.putText(img, "Waehle einen Sonnenfleck aus.", (100, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    else:
        cv2.line(img, (0, center_area[1]), (1024, center_area[1]), (0, 0, 255), thickness=2)
        cv2.putText(img, "Waehle gleichen rotierten Sonnenfleck aus.", (100, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    cv2.imshow("Sonnenflecken", img)
    cv2.setMouseCallback("Sonnenflecken", on_mouse)
    cv2.waitKey(0)

    dist_from_center = cX - center_area[0] # SYM_r1,2
    hoehe = cY - center_area[1] # SYM_H

    return dist_from_center, hoehe, dist_to_edge

r1, hoehe, rho = show_sun(IMAGE_1, first_img=True)
r2, _, _  = show_sun(IMAGE_2)

latitude = abs(round(math.degrees(np.arcsin(hoehe/sun_radius)),2))

sin_01 =  math.degrees(np.arcsin(r1/rho))
sin_02 =  math.degrees(np.arcsin(r2/rho))

if sign(sin_01) == sign(sin_02):
    alpha = sin_02 - sin_01
else:
    alpha = abs(sin_01) + abs(sin_02)

alpha = abs(alpha)
circulation_time= round((360/alpha)*time_difference, 2)

print("Radius der Sonne: {}px".format(sun_radius))
print("Radius der Sonne auf Höhe der Sonnenflecken: {}px".format(rho))
print("Distanz vom Sonnenfleck zur Vertikalen (Sonnenmitte) - Höhe: {}px".format(hoehe))
print("Distanz vom 1. Sonnenfleck zur Senkrechten (Sonnenmitte) - r1: {}px".format(r1))
print("Distanz vom 2. Sonnenfleck zur Senkrechten (Sonnenmitte) - r2: {}px".format(r2))
print("Sonnenrotation: {} Tage am Bereitengrad: {}°".format(circulation_time, latitude))




# Name der Excel-Datei festlegen
filename = "Sonnenrotation\output\sonnenrotations_daten.xlsx"

# Überprüfen, ob die Datei bereits existiert oder nicht
try:
    workbook = openpyxl.load_workbook(filename)
    worksheet = workbook.active
except FileNotFoundError:
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.append(["Zeitdifferenz", "Rho", "Höhe", "Pos. von Mittelachse (r1)", "Pos. von Mittelachse (r2)", "Breitengrad", "Sonnenrotation"])

worksheet.append([time_difference, rho, hoehe, r1, r2, latitude, circulation_time])

# Excel-Datei speichern
workbook.save(filename)
print("Die Excel-Datei wurde erfolgreich gespeichert.")


# Lade die Daten aus der Excel-Tabelle
df = pd.read_excel(filename)
x = df['Breitengrad']
y = df['Sonnenrotation']

# Erstelle das Liniendiagramm
plt.plot(x, y, marker='o')
plt.xlabel("Breitengrad")
plt.ylabel("Rotationsperiode in Tagen")
plt.title("Differentielle Rotation der Sonne" +"\n" +f"Insgesamt: {len(x)} Sonnenflecken")
plt.axis([0, 90, 24, 36])     
plt.grid(True)  

plt.savefig('Sonnenrotation\output\diagramm.png')
plt.show()