set -e

# make android or make something else
# make [otapackage]
# $1 envsetup.sh
# $2 combo
# $3 numbers of running jonbs
# $4 [otapackage, systemimage, bootimage,etc]
source $1 $2
make -j$3
