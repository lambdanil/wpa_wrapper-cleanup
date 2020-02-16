install:
	mkdir -p $(DESTDIR)/usr/share/wpa_wrapper/
	mkdir -p $(DESTDIR)/usr/share/wpa_wrapper/networks/
	mkdir -p $(DESTDIR)/usr/share/wpa_wrapper/conf/
	mkdir -p $(DESTDIR)/usr/bin
	cp -r wpa_wrapper/* $(DESTDIR)/usr/share/wpa_wrapper/
	cp wpa_wrapper/wpa_wrapper $(DESTDIR)/usr/bin/wpa_wrapper
	cp wpa_wrapper/wpa_wrapper-last $(DESTDIR)/usr/bin/wpa_wrapper-last
	chmod +x $(DESTDIR)/usr/bin/wpa_wrapper
	chmod +x $(DESTDIR)/usr/bin/wpa_wrapper-last
remove:
	rm -rf $(DESTDIR)/usr/share/wpa_wrapper
	rm -f $(DESTDIR)/usr/bin/wpa_wrapper
	rm -f $(DESTDIR)/usr/bin/wpa_wrapper-last
