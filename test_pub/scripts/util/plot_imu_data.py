import csv
import matplotlib.pyplot as plt
from scipy.signal import butter,lfilter,medfilt
from os.path import expanduser

class Plot_csv_data():
    def __init__(self):
            self.imu_data={"gyro_x":[],
                           "gyro_y":[],
                           "gyro_z":[],
                           "accel_x":[],
                           "accel_y":[],
                           "accel_z":[]}
            self.imu_data_filt = {"gyro_x":[],
                                  "gyro_y":[],
                                  "gyro_z":[],
                                  "accel_x":[],
                                  "accel_y":[],
                                  "accel_z":[]}
            self.cutoff = 15    # Hz: Filter cutoff frequency
            self.ts = 200      # Sampling time
            self.order = 2     # Filter order

    def find_filter_params(self):
        nyq = 0.5 * self.fs
        normal_cutoff = self.cutoff / nyq
        self.b, self.a = butter(self.order, normal_cutoff, btype='low', analog=False)

    def butter_lowpass_filter(self,data):
        return lfilter(self.b, self.a, data)

    def import_csv_data(self, root):
        csvFile = csv.reader(open(root, "rb"))
        n_header_lines = 1
        c = 0
        print("Reading data...")
        for row in csvFile:
            # print row
            if c >= n_header_lines and len(row)>=7:
                self.imu_data["gyro_x"].append(float(row[8]))
                # self.imu_data["gyro_y"].append(float(row[8])*-1)
                self.imu_data["gyro_y"].append(float(row[9]))
                self.imu_data["gyro_z"].append(float(row[10]))
                self.imu_data["accel_x"].append(float(row[11]))
                # self.imu_data["accel_y"].append(float(row[12])*-1)
                self.imu_data["accel_y"].append(float(row[12])*-1)
                self.imu_data["accel_z"].append(float(row[13]))
            c += 1
        # for value in self.imu_data["accel_z"]:
        #     print value
        # print("Number of samples: {}".format(len(self.imu_data["gyro_x"])))
        self.fs = len(self.imu_data["gyro_x"])/self.ts      # Sampling frequency
        self.find_filter_params()
        self.imu_data_filt["gyro_x"] = medfilt(self.imu_data["gyro_x"],5)
        self.imu_data_filt["gyro_x"] = self.butter_lowpass_filter(self.imu_data_filt["gyro_x"])
        self.imu_data_filt["gyro_y"] = medfilt(self.imu_data["gyro_y"],5)
        self.imu_data_filt["gyro_y"] = self.butter_lowpass_filter(self.imu_data_filt["gyro_y"])
        self.imu_data_filt["gyro_z"] = medfilt(self.imu_data["gyro_z"],5)
        self.imu_data_filt["gyro_z"] = self.butter_lowpass_filter(self.imu_data_filt["gyro_z"])
        self.imu_data_filt["accel_x"] = medfilt(self.imu_data["accel_x"],5)
        self.imu_data_filt["accel_x"] = self.butter_lowpass_filter(self.imu_data_filt["accel_x"])
        self.imu_data_filt["accel_y"] = medfilt(self.imu_data["accel_y"],5)
        self.imu_data_filt["accel_y"] = self.butter_lowpass_filter(self.imu_data_filt["accel_y"])
        self.imu_data_filt["accel_z"] = medfilt(self.imu_data["accel_z"],5)
        self.imu_data_filt["accel_z"] = self.butter_lowpass_filter(self.imu_data_filt["accel_z"])
        # print("Number of filtered samples: {}".format(len(self.imu_data["gyro_x"])))

    def export_csv_data(self, root):
        f = open(root,'wb')
        f.write('[Datalogging: Item = 0 | Slave index = 0 (Execute 1) | Experiment index = 0 (Read All (Barebone))]\n')
        f.write('Timestamp,Timestamp (ms),accel.x,accel.y,accel.z,gyro.x,gyro.y,gyro.z,strain,analog_0,analog_1,current,enc-disp,enc-cont,enc-comm,VB,VG,Temp,Status1,Status2\n')
        c = 0   # time_stamp
        for row in range(len(self.imu_data["time"])):
            f.write('Mon Sep 26 15:14:38 2016,{},{},{},{},{},{},{},13203,1067,1021,444,0,0,0,199,206,131,2,1\n'.format(c,self.imu_data["accel_x"][c],self.imu_data["accel_y"][c],self.imu_data["accel_z"][c],self.imu_data["gyro_x"][c],self.imu_data["gyro_y"][c],self.imu_data["gyro_z"][c]))
            c += 1
        f.close()

    def plot_filt_vs_orig(self):
        plt.figure(1)
        plt.subplot(121)
        plt.plot(self.imu_data["gyro_y"][3550:3800],'r-')
        plt.title('GYRO Y ORIG')
        plt.subplot(122)
        plt.plot(self.imu_data_filt["gyro_y"][3550:3800],'b-')
        plt.title('GYRO Y FILT')
        plt.show()

    def plot_data(self):
        plt.figure(1)
        plt.subplot(311)
        plt.plot(self.imu_data["gyro_x"][:1000],'r-')
        plt.title('GYRO_X')
        plt.subplot(312)
        plt.plot(self.imu_data["gyro_y"][:1000],'b-')
        plt.title('GYRO_Y')
        plt.subplot(313)
        plt.plot(self.imu_data["gyro_z"][:1000],'y-')
        plt.title('GYRO_Z')
        plt.figure(2)
        plt.subplot(311)
        plt.plot(self.imu_data["accel_x"][:1000],'r-')
        plt.title('ACCEL_X')
        plt.subplot(312)
        plt.plot(self.imu_data["accel_y"][:1000],'b-')
        plt.title('ACCEL_Y')
        plt.subplot(313)
        plt.plot(self.imu_data["accel_z"][:1000],'y-')
        plt.title('ACCEL_Z')
        plt.show()

def main():
    csv_class = Plot_csv_data()
    home_dir = expanduser("~")
    csv_class.import_csv_data(home_dir +  '/catkin_ws/src/agora_exo/exo_control/log/imu_data1.csv')
    csv_class.plot_filt_vs_orig()
    # csv_class.plot_data()
    # csv_class.export_csv_data('/home/miguel/catkin_ws/src/agora_exo/exo_control/log/imu_data1_filt.csv')

if __name__ == '__main__':
    main()
