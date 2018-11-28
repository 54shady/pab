# Python Android Builder(pab)

## Generate package

	python setup.py sdist

## Install and Uninstall

Install using package

	sudo pip install dist/python_android_build-1.0.0.tar.gz

without super user permission:

	pip install --user dist/python_android_build-1.0.0.tar.gz

Install from source

	sudo pip install -e .

Maybe export local path is necessary(Gentoo)

	export PATH=$PATH:~/.local/bin

Uninstall

	sudo pip uninstall python_android_build
	or
	sudo -H pip uninstall python_android_build
