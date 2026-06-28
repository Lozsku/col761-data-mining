if [ $1 == "C" ] 
then
   ./fptree $2 $3 

elif [ $1 == "D" ] 
then
    ./decomp $2 $3
else
 echo "Argument not found"
 
fi
