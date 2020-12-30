Bediening van een oude klok die nu bestuurd wordt door een Raspberry Pi met 3 stappenmotors.
Ze heeft nu ook een web-interface. De files zitten in een tar.
Om de tar te actualiseren:

tar cvf web.tar --exclude=".*" -T web.list --absolute-names
