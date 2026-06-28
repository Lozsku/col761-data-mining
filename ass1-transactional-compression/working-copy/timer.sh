start="$(date +%s.%N)"
echo "start: $start"
timeout 3600 bash interface.sh C "test2_copied1.dat" "compressed.dat" > log.out 2> log.err
timeout 600 bash interface.sh D "compressed.dat" "decompressed.dat" > decompression_log.out 2> decompression_log.err
python3 -u check_loss.py "test1_copied.dat" "decompressed.dat" > loss_out.txt 2> loss_err.txt
python3 -u compression_ratio.py "test1_copied.dat" "compressed.dat" > compression_out.txt 2> compression_err.txt
end="$(date +%s.%N)"
echo "end: $end"
echo "time = "
python3 -c "print($end-$start)"
