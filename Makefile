RPI_IP_ADDRESS=10.0.0.253
RPI_USERNAME=pi

.PHONY: install-osx
install-osx:
	@bash setup/install_osx.sh

.PHONY: install-raspberry-pi
install-raspberry-pi:
	@bash setup/install_raspberry_pi.sh

.PHONY: run
run:
	@source env/bin/activate && source app/environment.sh && python app/app.py

.PHONY: copy
copy:
	@scp -r app $(RPI_USERNAME)@$(RPI_IP_ADDRESS):/home/$(RPI_USERNAME)/radio_listener/
