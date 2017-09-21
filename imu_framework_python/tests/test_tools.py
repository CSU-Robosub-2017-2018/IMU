import csv
import numpy as np
import matplotlib.pyplot as plt

from imu_framework.imu_tools import imu_tools


class testing():
    testing = imu_tools(1000)

    '''
    i =0   this makes csv file
    while i <= 5:
        tup = (1,2,3,4,5,6,7,8,9)

        testing.print2CvFile(9,tup,'billy_phillips_2_14_2017','test',i)
        i+=1


    with open('Billy_Phillips_2_15_2017_still_test_data.csv', 'rb') as this:
        reader = csv.reader(this, delimiter=' ', quotechar='|')
        for row in reader:
            list = list(', '.join(row))


    somthing = 0
    i = 0
    with open('Billy_Phillips_2_15_2017_still_test_data.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            list = (row['X Acc'], row['Y Acc'], row['Z Acc'],
                             row['X Gyro'], row['Y Gyro'], row['Z Gyro'],
                             row['X Mag'], row['Y Mag'], row['Z Mag'])
            print (list)
            your_list = map(tuple, reader)

    print (your_list)



    datafile = open('Billy_Phillips_2_15_2017_still_test_data.csv', 'r')
    datareader = csv.reader(datafile, delimiter=';')
    data = []
    for row in datareader:
        data.append(row)
    tupleData = tuple(data)
    '''

    data = testing.csvData2NpArray('test_files/data/csv/Billy_Phillips_2_15_2017ttttt_test_data.csv', 0)
    i = 0
    while i <= len(data) - 1:
        testing.fifoMemoryUpdate(data[i])
        testing.livePlot(testing.lowPassFilter(150000))
        # plt.plot(testing.lowPassFilter(150000))
        # plt.pause(0.00000000000000001)
        # plt.clf()
        i += 1



    '''
    i = 0
    while i<=len(filtered)-1:

        if i == 0:
            with open('dattta.csv', "w") as csvfile:
                fieldnames = ['filtered']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerow({'filtered': filtered[i]})
            print('looooook heeeer,     ', filtered[3])

        if i != 0:
            with open('dattta.csv', "a") as csvfile:
                fieldnames = ['filtered']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writerow({'filtered': filtered[i],})
            print('looooook heeeer,     ', filtered[3])
        i+=1
    '''

    # plt.plot(data)
    # plt.plot(testing.lowPassFilter(10))
    # plt.show()

    # print('fequency shit')
    # print(np.fft.fftfreq(len(data1),0.0000025))


    #data1 = testing.csvData2NpArray('Billy_Phillips_upDown_2_15_2017_test_data.csv', 0)
    #
    # W = np.fft.fftfreq(data1.size, 0.0000025)
    # f_signal = np.fft.fft(data1)
    # cut_f_signal = f_signal.copy()
    # cut_f_signal[(np.abs(W) > 100000)] = 0
    # cut_signal = np.fft.ifft(cut_f_signal)
    #
    # plt.plot(data1, 'r')
    # plt.plot(cut_signal)
    # plt.show()
    #
    # # plt.plot(W, f_signal, 'r')
    # # plt.plot(W, cut_f_signal, 'b')
    # # plt.show()


