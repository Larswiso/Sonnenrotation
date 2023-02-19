# Sonnenrotation
Berechnen Sie die differentielle Drehung der Sonne mit zwei Bildern und ein paar Mausklicks.

## Differentielle Sonnenrotation
Die Sonne dreht sich um ihre eigene Achse. Da sie ein Gasball ist, dreht sie sich
nicht gleichmäßig, sondern am Äquator viel schneller als an den
Polen. Dies wird als differentielle Sonnenrotation bezeichnet.
## Installation
Öffnen Sie cmd im Ordner Sonnenrotation und geben Sie **pip install -r requirements.txt** ein.

## Vorbereitung
1. Da dieses Programm NUR für die Bilder von SDO zugeschnitten ist, müssen die Bilder auch von dort heruntergeladen werden. [Zu SDO](https://sdo.gsfc.nasa.gov/data/aiahmi/)
2. Speichern Sie die Bilder im Ordner **data**.
3. **Wichtig** Der Name der Bilder sollte nicht verändert werden. Richtig: 20130525_010655_1024_HMII.jpg
3. Geben Sie den Dateipfad der entsprechenden 2 Bilder, die Sie analysieren wollen, in die ersten beiden Variablen ein. (IMAGE_1, IMAGE_2)
4. **Wichtig** Ersetzen nur den dick makierten Teil des Dateipfads: ".\Sonnenrotation\data\ **20130525_010655_1024_HMII.jpg**"
4. Speichern Sie Python-Datei.

## Ausführung
1. Starten Sie das Programm 
- z.B. mit CMD: Öffnen Sie CMD im Ordner Sonnenrotation und geben Sie **python code/main.py** ein
2. Das erste Fenster wird geöffnet: Wählen Sie einen Sonnenfleck aus.
3. Das zweite Fenster wird geöffnet: Wählen Sie den gleichen, aber rotierten Sonnenfleck aus dem ersten Fenster.
4. Die Sonnenrotation wird auf dem Terminal angezeigt.
5. Die erfassten Daten werden in einem Excel-Datei im Ordner **output** gespeichert.
6. Abschließend wird die Sonnenrotaion an den Breitengrad in einen Diagramm veranschaulicht.
7. Das Diagramm wird im Ordner **output** gespeichert.
