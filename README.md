# Python Android Builder(pab)

## Generate package

	python setup.py sdist

## Install and Uninstall

Install

	sudo pip install dist/python_android_build-1.0.0.tar.gz

	without super user permission:
	pip install --user dist/python_android_build-1.0.0.tar.gz

Maybe export local path is necessary(Gentoo)

	export PATH=$PATH:~/.local/bin

Add your user name to the usb group(Gentoo)

	sudo usermod -aG usb your_user_name

Install from source

	sudo pip install -e .

Uninstall

	sudo pip uninstall python_android_build
	or
	sudo -H pip uninstall python_android_build
