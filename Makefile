install:
	mkdir -p /usr/share/wpa_wrapper/
	mkdir -p /usr/share/wpa_wrapper/networks/
	mkdir -p /usr/share/wpa_wrapper/conf/
	cp -r wpa_wrapper/* /usr/share/wpa_wrapper/
	cp wpa_wrapper/wpa_wrapper /usr/bin
	cp wpa_wrapper/wpa_wrapper-last /usr/bin
	chmod +x /usr/bin/wpa_wrapper
	chmod +x /usr/bin/wpa_wrapper-last
remove:
	rm -rf /usr/share/wpa_wrapper
	rm -f /usr/bin/wpa_wrapper
	rm -f /usr/bin/wpa_wrapper-last
