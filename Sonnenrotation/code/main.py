# Dieses Programm ist NUR für die Bilder von SDO zugeschnitten.
# https://sdo.gsfc.nasa.gov/data/aiahmi/


# Dieser Fehler tritt auf, wenn die Matplotlib-Bibliothek nicht richtig installiert ist oder wenn einige der benötigten DLLs fehlen.
# Es ist auch möglich, dass das Problem durch die Installation der VC++ 2015-Redistributable-Pakete gelöst werden kann. 
# Du kannst Sie hier herunterladen und installieren: https://www.microsoft.com/en-us/download/details.aspx?id=48145

# Bitte größere Sonneflecken benutzen

import datetime
import re
import cv2
import matplotlib.pyplot as plt

IMAGE_1 = r"E:\Development\Python\Sonnenrotation\data\20130525_010655_1024_HMII.jpg"
IMAGE_2 = r"E:\Development\Python\Sonnenrotation\data\20130527_053655_1024_HMII.jpg"

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






# Lade das Bild
img = cv2.imread(IMAGE_1)

# Konvertiere das Bild in Graustufen
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Verwende einen Canny-Filter, um Kanten zu finden
edges = cv2.Canny(gray, 50, 150)

# Verwende eine Hough-Transformation, um die Konturen des Objekts zu finden
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Wähle die Kontur des Objekts, das du untersuchen möchtest
obj_contour = max(contours, key = cv2.contourArea)

# Berechne die südlichste, nördlichste, westlichste und östlichste Koordinate des Objekts
left = tuple(obj_contour[obj_contour[:, :, 0].argmin()][0])
right = tuple(obj_contour[obj_contour[:, :, 0].argmax()][0])
top = tuple(obj_contour[obj_contour[:, :, 1].argmin()][0])
bottom = tuple(obj_contour[obj_contour[:, :, 1].argmax()][0])

print("Südlichste Koordinate:", bottom)
print("Nördlichste Koordinate:", top)
print("Westlichste Koordinate:", left)
print("Östlichste Koordinate:", right)

#plt.imshow(img)
#plt.show()

# Bild laden
img = cv2.imread(IMAGE_1)

# Rechteck erkennen
ret,thresh = cv2.threshold(gray,127,255,0)

# Mittelpunkt ermitteln
for cnt in contours:
    if cv2.contourArea(cnt) > 200: # nur contours mit einer Fläche größer als 50 betrachten
        M = cv2.moments(cnt)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        # Mittelpunkt zeichnen
        cv2.circle(img, (cX, cY), 5, (255, 0, 0), -1)
print(f"X-Click {cX} Y-Click {cY}")

sun_radius = right[0] - cX
print(f"R: {sun_radius}")



def find_edge(img, point_y):
    edge_x = 0
    edges = cv2.Canny(img, 50, 150)
    while True:
        if edges[edge_x, point_y] > 0:
            break
        else:
            edge_x += 1
    distance = abs(point_y - edge_x)
    return distance



def show_sun(image):
	img = cv2.imread(image)

	# Flächen erkennen
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	ret,thresh = cv2.threshold(gray,127,255,0)
	contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	# Bild anzeigen
	cv2.imshow("Bild", img)

	# Mausklick abfangen
	def on_mouse(event, x, y, flags, param):
		global center_area
		global dist_to_edge

		if event == cv2.EVENT_LBUTTONDOWN:
			# Koordinaten speichern
			coordinates = (x, y)
			print("Klickkoordinaten:", coordinates)
			
			for cnt in contours:
				if cv2.contourArea(cnt) > 10 and cv2.contourArea(cnt) < 300: # nur contours mit einer Fläche größer als 50 betrachten
					if cv2.pointPolygonTest(cnt, (x, y), False) >= 0:
						# Mittelpunkt ermitteln
						M = cv2.moments(cnt)
						c_arae_X = int(M["m10"] / M["m00"])
						c_arae_Y = int(M["m01"] / M["m00"])

						dist_to_edge = find_edge(img, c_arae_Y)
						print("dist_to_edge", dist_to_edge)

						print("Mittelpunkt der Fläche:", (c_arae_X, c_arae_Y))
						center_area = (c_arae_X, c_arae_Y)
			
						
					
			# Fenster schließen
			cv2.destroyAllWindows()

	# Mausklick-Callback registrieren
	cv2.setMouseCallback("Bild", on_mouse)

	# Warten auf Mausklick
	cv2.waitKey(0)

	dist_from_center = cX - center_area[0]
	hoehe = cY - center_area[1]

	return dist_from_center, hoehe, dist_to_edge

dist_to_center1, hoehe, _ = show_sun(IMAGE_1)
# dist_to_center2, _  = show_sun(IMAGE_2)


plt.imshow(img)
plt.show()