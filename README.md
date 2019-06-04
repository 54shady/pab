# Python Builder For Linux(pbl)

## Generate package

	python setup.py sdist

## Upload package to repo and install

### generate package

	python -m pip install --user --upgrade setuptools wheel
	python setup.py sdist bdist_wheel
	python -m pip install --user --upgrade twine

### uploade the package

	python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

### Install from repo

	sudo pip install argcomplete
	sudo pip install -i https://test.pypi.org/simple/ PythonBuildForLinux

## Install and Uninstall

Install using package

	sudo pip install dist/PythonBuildForLinux-1.0.0.tar.gz

without super user permission:

	pip install --user dist/PythonBuildForLinux-1.0.0.tar.gz

Install from source

	sudo pip install -e .

Maybe export local path is necessary(Gentoo)

	export PATH=$PATH:~/.local/bin

Uninstall

	sudo pip uninstall PythonBuildForLinux
	or
	sudo -H pip uninstall PythonBuildForLinux
