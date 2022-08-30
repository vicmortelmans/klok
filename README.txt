Bediening van een oude klok die nu bestuurd wordt door een Raspberry Pi met 3 stappenmotors.

calibration.txt = time of last calibration
offset.txt = number of minutes the hands have been adjusted since last calibration
correction.txt = correction factor to normal speed; SHOULD BE IN THE NEIGHBOURHOOD OF 1.0

Ze heeft nu ook een web-interface. De files zitten in een tar.
Om de tar te actualiseren:

tar cvf web.tar --exclude=".*" -T web.list --absolute-names

Om de tar uit te pakken (opgelet: overschrijft systeembestanden!!)

tar --absolute names -xvf web.tar
