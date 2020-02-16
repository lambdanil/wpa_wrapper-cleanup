D="$DESTDIR"
istall:
	mkdir -p "$D"/usr/share/wpa_wrapper/
	mkdir -p "$D"/usr/share/wpa_wrapper/networks/
	mkdir -p "$D"/usr/share/wpa_wrapper/conf/
	cp -r wpa_wrapper/* $D/usr/share/wpa_wrapper/
	cp wpa_wrapper/wpa_wrapper "$D"/usr/bin
	cp wpa_wrapper/wpa_wrapper-last "$D"/usr/bin
	chmod +x "$D"/usr/bin/wpa_wrapper
	chmod +x "$D"/usr/bin/wpa_wrapper-last
remove:
	rm -rf "$D"/usr/share/wpa_wrapper
	rm -f "$D"/usr/bin/wpa_wrapper
	rm -f "$D"/usr/bin/wpa_wrapper-last
