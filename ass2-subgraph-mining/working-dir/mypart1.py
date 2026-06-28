import os
import time
import matplotlib.pyplot as plt

def run_fsg(Threshold_list):
    fsg_runtimes = []
    for Threshold in Threshold_list:
        command = "./fsg -s " + str(Threshold) + " " + "fsgfile.txt"
        start_time = time.time()
        os.system(command)
        end_time = time.time()
        fsg_runtimes.append(end_time - start_time)
    return fsg_runtimes

def run_gaston(Threshold_list, gaston_graphs_file):
    gaston_runtimes = []
    for Threshold in Threshold_list:
        count = get_graph_count(gaston_graphs_file)
        Thresholdnum = float(Threshold * count / 100)
        command = "./gaston " + str(Thresholdnum) + " gastonfile.txt gaston-output.txt"
        start_time = time.time()
        os.system(command)
        end_time = time.time()
        gaston_runtimes.append(end_time - start_time)
    return gaston_runtimes

def run_gspan(Threshold_list):
    gspan_runtimes = []
    for Threshold in Threshold_list:
        Thresholdnum = float(Threshold / 100)
        start_time = time.time()
        command = "./gSpan-64 -f gspanfile.txt -s " + str(Thresholdnum) + " -o"
        os.system(command)
        end_time = time.time()
        gspan_runtimes.append(end_time - start_time)
    return gspan_runtimes

def get_graph_count(file_path):
    with open(file_path, "r") as file:
        for line in file:
            count = int(line)
            return count

def plot_runtimes(Threshold_list, fsg_runtimes, gspan_runtimes, gaston_runtimes):
    plt.plot(Threshold_list, fsg_runtimes, label="FSG")
    plt.plot(Threshold_list, gspan_runtimes, label="GSPAN")
    plt.plot(Threshold_list, gaston_runtimes, label="GASTON")
    plt.xlabel("Threshold")
    plt.ylabel("Runtimes")
    plt.title("Runtime vs Threshold for various algorithms")
    plt.legend()
    plt.savefig('runtime1.png')

def main():
    Threshold_list = [5, 10, 25, 50, 95]
    fsg_runtimes = run_fsg(Threshold_list)
    gspan_runtimes = run_gspan(Threshold_list)
    gaston_runtimes = run_gaston(Threshold_list, "gastonfile1.txt")
    print(fsg_runtimes)
    print(gspan_runtimes)
    print(gaston_runtimes)
    plot_runtimes(Threshold_list, fsg_runtimes, gspan_runtimes, gaston_runtimes)

if __name__ == "__main__":
    main()
