from IdentifyFilesSara import *
from astropy.io import fits
import numpy as np
import os
from datetime import datetime

###/home/astro/PycharmProjects/SARA/operations_on_fits


def addition(d):   #d = lista cu array-urile fiecarei imagini
    result = 0
    for i in d.values():
    #for i in d:
        result = result + i
    return result


def substraction(d1, d2):    #2 elem din arrayul de date
    return d1 - d2


def multiplication(data, sc):       #sc = scalarul
    return data * sc


def division(img, imp):        #img = first image, imp = scalar or second image
    return img / imp


def get_average(d):
    return addition(d) / len(d)


# def get_median(d):     #d = table of data
#     for i in d:
#         cube.append(i)
global default_value
def image_processing(list_images, path):          #for getting table of data
    images_data = dict()
    for i in list_images:
        hdul = fits.open(path + "/" + i)
        images_data[i] = hdul[0].data
        #default_value = hdul[0].data
    return images_data


def save_image(results, name, counter):                   #for saving new images
    new_hdu = fits.PrimaryHDU(np.shape(results))
    hdulist = fits.HDUList([new_hdu])
    new_hdu.data = results
    today = datetime.today()
    date = today.strftime("%Y-%m-%d")
    hdulist[0].header["DATE"] = date
    hdulist[0].header["NAME"] = "SR" + str(counter)
    file_name = name + "_" + str(counter)+".fits"
    hdulist.writeto(file_name)
    return file_name


global new_name


def execute_instruction(images_data):
    new_hdu = fits.PrimaryHDU(np.shape(images_data[0]))
    hdulist = fits.HDUList([new_hdu])
    instruction = input("Enter operation name (addition, substraction, multiplication, division): ")
    if instruction == "addition":
        # result = addition(list_data)
        result = addition(images_data)
        new_hdu.data = result
        counter = 0
        # for i in list_images:
        for i in images_data.keys():
            hdulist[0].header["IMAGE" + str(counter)] = i
            counter = counter + 1
        new_name = "images_addition"

    elif instruction == "substraction":
        clarif1 = input("Enter name of first image: ")
        clarif2 = input("Enter name of second image: ")
        try:
            # img1_index = list_images.index(clarif1)
            # data1 = list_data[img1_index]
            data1 = images_data[clarif1]
        except:
            "Error. No file with this name."
        try:
            # img2_index = list_images.index(clarif2)
            # data2 = list_data[img2_index]
            data2 = images_data[clarif2]
        except:
            "Error. No file with this name."
        result = substraction(data1, data2)
        new_hdu.data = result
        hdulist[0].header["IMAGE1"] = clarif1
        hdulist[0].header["IMAGE2"] = clarif2
        new_name = clarif1 + "_modified"

    elif instruction == "multiplication":
        clarif = input("Enter image name: ")
        scalar = input("Enter number: ")
        scalar = float(scalar)
        try:
            data = images_data[clarif]
        except:
            print("No file with this name.")
        result = multiplication(data, scalar)
        new_hdu.data = result
        new_name = clarif + "_modified"

    elif instruction == "division":
        clarif1 = input("Enter name of first image: ")
        try:
            # img1_index = list_images.index(clarif1)
            # data1 = list_data[img1_index]
            data1 = images_data[clarif1]
        except:
            "Error. No file with this name."
        clarif2 = input("With scalar? ")
        if clarif2 == "da":
            scalar = input("Enter number: ")
            scalar = float(scalar)
            # result = division(list_data, scalar)
            result = division(data1, scalar)
            new_hdu.data = result
        else:
            clarif2 = input("Enter name of second image: ")
            try:
                # img2_index = list_images.index(clarif2)
                # data2 = list_data[img1_index]
                data2 = images_data[clarif2]
            except:
                "Error. No file with this name."
            result = division(data1, data2)
            new_hdu.data = result
            hdulist[0].header["IMAGE2"] = clarif2
        hdulist[0].header["IMAGE1"] = clarif1
        new_name = clarif1 + "_modified"
    else:
        print("Error", instruction, "not available")
        return 0

    today = datetime.today()
    date = today.strftime("%Y-%m-%d")
    hdulist[0].header["DATE"] = date
    hdulist[0].header["NAME"] = "SR" + str(counter)
    hdulist.writeto(new_name + "_" + str(counter) + ".fits")




