from FitsOperationsSara import *
from IdentifyFilesSara import *
import os
from os import path
import numpy as np
import sys
import subprocess

def create_3d_array(images):      ## creates a stack of images of the same kind and gets their sizes
    list_data = list(images.values())

    x = np.shape(list_data[0])[0]
    y = np.shape(list_data[0])[1]

    for i in range(1,len(list_data)):
        if np.shape(list_data[i]) != (x, y):
            print(np.shape(i), " ; ", x, " ", y)
            print("Error. Files format not compatible.")
            sys.exit("FormatError")

    arr1 = np.ndarray((len(list_data), x, y))

    # in cazul 3d, timpul de executie 113 secunde

    for i in range(len(list_data)):  
        for row in range(0, x):
            for col in range(0, y):
                arr1[i][row][col] = list_data[i][row][col]
    #print("size arr1: ", np.shape(arr1))
    return arr1


def get_stat(images):     #is given a list of image names       ##obtains average and median
    arr1 = create_3d_array(images)
    list_data = list(images.values())
    np.sort(arr1, axis = 0)
    avg = arr1.mean(axis = 0)
    median = arr1[int(len(list_data)/2)]
    #print(median)
    return avg, median


def make_mbias(images):
    return get_stat(images)


def make_mdark(images, mbias):          #the mbias is made by subtracting the mbias from the dark image
    dark_arr = create_3d_array(images)

    if np.shape(dark_arr[0]) != np.shape(mbias):
        print("Error. Mbias and Dark format not compatible.")
        sys.exit("FormatError")

    for i in range(np.shape(dark_arr)[0]):
        dark_arr[i] = np.subtract(dark_arr[i], mbias)
    # for zid in range(np.shape(dark_arr)[0]):
    #     for xid in range(np.shape(dark_arr)[1]):                #find less complex method
    #         for yid in range(np.shape(dark_arr)[2]):
    #             dark_arr[zid][xid][yid] = dark_arr[zid][xid][yid] - mbias[xid][yid]
    (avg, median) = get_stat(images)
    return median


def make_mflat(images, mbias, mdark):           ## for mflat, we need mbias and mdark to include in operations
    flat_arr = create_3d_array(images)

    if np.shape(flat_arr[0]) != np.shape(mbias) or np.shape(flat_arr[0]) != np.shape(mdark):
        print("Error. Flat and MDark or MBias format not compatible.")
        sys.exit("FormatError")

    for i in range(np.shape(flat_arr)[0]):
        flat_arr[i] = np.subtract(flat_arr[i], mbias)
        flat_arr[i] = np.subtract(flat_arr[i], mdark)
    # for zid in range(np.shape(flat_arr)[2]):
    #     for xid in range(np.shape(flat_arr)[0]):                #de cautat met mai putin complexe
    #         for yid in range(np.shape(flat_arr)[1]):
    #             flat_arr[zid][xid][yid] = flat_arr[zid][xid][yid] - mbias[xid][yid] - mdark[xid][yid]
    (not_imp, median) = get_stat(images)
    median = np.array(median)
    avg_pixel = median.mean()
    avg_pixel = float("{:.2f}".format(avg_pixel))
    median_norm = median / avg_pixel
    median_norm = np.matrix.round(median_norm, 2)
    return median, median_norm


def make_science_ready(images, mbias, mdark, mflatn):           # scince ready is the finite product, which includes all
    light_arr = create_3d_array(images)                         # operations done on the previous types of images

    if np.shape(light_arr[0]) != np.shape(mbias) or np.shape(light_arr[0]) != np.shape(mdark):
        print("Error. Light and MBias or MDark format not compatible.")
        sys.exit("FormatError")
    elif np.shape(light_arr[0]) != np.shape(mflatn):
        print("Error. Light and MFlatN format not compatible.")
        sys.exit("FormatError")

    for i in range(np.shape(light_arr)[0]):
        light_arr[i] = np.subtract(light_arr[i], mbias)
        light_arr[i] = np.subtract(light_arr[i], mdark)
        light_arr[i] = np.divide(light_arr[i], mflatn)
        light_arr[i] = np.matrix.round(light_arr[i], 2)
    # for zid in range(np.shape(light_arr)[2]):
    #     for xid in range(np.shape(light_arr)[0]):                
    #         for yid in range(np.shape(light_arr)[1]):
    #             light_arr[zid][xid][yid] = (light_arr[zid][xid][yid] - mbias[xid][yid] - mdark[xid][yid]) / mflatn[xid][yid]
    #             light_arr[zid][xid][yid] = float("{:.2f}".format(light_arr[zid][xid][yid]))
    return light_arr



def main():

    procedure = input("Select procedure: Mass processing or Selective processing (1 or 2): ")           #interogation on whether only one kind of image is processed
    if procedure == "1":                                                                                #or all types
        (dark_list, flat_list, bias_list, light_list, mypath) = get_type()

        saving_path = input("Enter path for saving file: ")
        while path.exists(saving_path):
            saving_path = input("Path already exist. Enter another: ")
        os.makedirs(saving_path)
        os.chdir(saving_path)

        bias_data = image_processing(bias_list, mypath)
        (bias_avg, mbias) = make_mbias(bias_data)
        save_image(mbias, "MasterBias", 0)

        dark_data = image_processing(dark_list, mypath)
        mdark = make_mdark(dark_data, mbias)
        save_image(mdark, "MasterDark", 0)

        flat_data = image_processing(flat_list, mypath)
        mflat, mflat_norm = make_mflat(flat_data,mbias,mdark)
        save_image(mflat_norm, "MasterFlatNorm", 0)

        light_data = image_processing(light_list, mypath)
        final = make_science_ready(light_data,mbias,mdark,mflat_norm)
        # print(final)
        # print(np.shape(final))

        for i in range(np.shape(final)[0]):
            # print(np.shape(final[i]))
            name = save_image(final[i], "ScienceReady",  i)
            #subprocess.call(("/usr/bin/xpaset ds9 fits nume < ", saving_path + "/" + name))
            command = "/usr/bin/xpaset ds9 fits" + "Light" + "<" + saving_path + "/" + name
            os.system(command)

    elif procedure == "2":
        number = int(input("Enter number of images to be processed: "))
        saving_path = input("Enter path which contains images: ")           #for reading and saving, the same path is used
        list_img = list()
        for i in range (number):
            name = input("Enter name of image: ")
            list_img.append(name)
        list_data = image_processing(list_img, saving_path)

    viz = input("Enter name of images you want to open: ")
    viz = viz.split("")
    for i in viz:
        if i.find("Dark") >= 0 or i.find("dark") >= 0:
            command = "/usr/bin/xpaset ds9 fits" + "Light" + "<" + saving_path + "/" + str(i)
        elif i.find("Light") >= 0 or i.find("light") >= 0:
            command = "/usr/bin/xpaset ds9 fits" + "Dark" + "<" + saving_path + "/" + str(i)
        elif i.find("Bias") >= 0 or i.find("bias") >= 0: 
            command = "/usr/bin/xpaset ds9 fits" + "Bias" + "<" + saving_path + "/" + str(i)
        elif i.find("flat") >= 0 or i.find("Flat") >= 0:
            command = "/usr/bin/xpaset ds9 fits" + "Flat" + "<" + saving_path + "/" + str(i)
        os.system(command)

main()
