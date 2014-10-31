reset
MYINSTALLPATH=./cmake_build
rm -rf $MYINSTALLPATH
mkdir $MYINSTALLPATH

cd $MYINSTALLPATH
cmake -DCMAKE_INSTALL_PREFIX=. ../brainvisa-cmake
make install
./bin/bv_maker sources
./bin/bv_env /home/jl237561/tmp/brainvisa-cmake-test/cmake_build/bin/bv_maker configure
./bin/bv_maker build
cd ..

