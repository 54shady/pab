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

## Usage

### Compile uboot

For RK3399 sapphire-excavator board

	pbl --udefconfig evb-rk3399_defconfig -u

For firefly-rk3399 board(default config)

	pbl -u
	or using config
	pbl --udefconfig firefly-rk3399_defconfig -u

### Flash uboot

	upgrade_tool di -uboot uboot.img && upgrade_tool rd

### Compile kernel

For RK3399 sapphire-excavator board

	pbl --ktarget rk3399-sapphire-excavator-linux.img -k

For firefly-rk3399 board(default config)

	pbl -k
	or using config
	pbl --ktarget rk3399-firefly-linux.img -k

### Flash kernel

	upgrade_tool di -b boot.img && upgrade_tool rd
