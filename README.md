# Sun-rotation
Calculate the differential rotation of the sun using two images and a few mouse clicks.

## Differential sun rotation
The sun rotates around its own axis. Since it is a ball of gas, it rotates
not uniform, but much faster at the equator than at the
Poland. This is called differential sun rotation.
## Setup
1. Open cmd in Sun-rotation folder and type **pip install -r requirements.txt**
2. Since this program is ONLY tailored for the images from SDO, the images must also be downloaded from there. [To SDO](https://sdo.gsfc.nasa.gov/data/aiahmi/)
3. Save the images in the folder **Images**.
4. Enter the file path of the related images in the first two variables. (1st time and 2nd time)
## How it use
1. run the program 
- e.g. with cmd: Open cmd in Sun-rotation folder and type **python sun_rotation.py**
2. the first window will open: Select a sunspot and close the window.
3. the second window will open: Click on the left edge of the sun and at the height of the yellow line. Then close the window.
4. The last window will open: Select the same but rotated sunspot from the first window and close window.
5. in the terminal: Enter the time of the first image **[YEAR MONTH DAY HOUR MINUTE SECOND]**.
6. in the terminal: Enter the time of the second image **[YEAR MONTH DAY HOUR MINUTE SECOND]**.
7. sun rotation is displayed in the terminal.
8. the acquired data will be saved in an Excel spreadsheet.
9. the collected data is also saved in a text document. This is important for the chart.
