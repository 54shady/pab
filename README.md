# Python Android Builder(pab)

## Prepareration(Option)

	python -m pip install --user --upgrade setuptools wheel
	python -m pip install --user --upgrade twine

## Generate package

	python setup.py sdist bdist_wheel

## Upload the packate(register a count first)

    python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

## Install the package from url

    sudo pip install argcomplete
    sudo pip install -i https://test.pypi.org/simple/ python_android_build

## Install and Uninstall from local package

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
