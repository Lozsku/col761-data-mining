cd $PBS_O_WORKDIR
module load compiler/gcc/9.1.0
bash interface.sh C D_test3.dat D_test_big_final.dat
bash interface.sh D D_test_big_final.dat D_test_big_decomp.dat
