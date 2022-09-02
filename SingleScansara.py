from atcore import *
import numpy as np
import astropy.io.fits as pyfits
import os
import shutil


def create_test(name):
    path = os.getcwd()
    newpath = path + "/"
    if not os.path.exists(newpath + name):
        os.makedirs(newpath + name)
    else:
        while os.path.exists(newpath + name):
            print("File name already exists. Enter another name:")
            name = input()
        os.makedirs(newpath + name)
    newpath = path + "/" + name
    return newpath


def save(image, path, config, directory):
    hdu = pyfits.PrimaryHDU(image)
    hdulist = pyfits.HDUList([hdu])
    for k, v in config.items():
        hdulist[0].header["HIERARCH " + k.upper()] = v
    hdulist.writeto(path, overwrite=True)
    shutil.copy(path, directory)
    if os.path.exists(path):
        os.remove(path)
    else:
        print("The file does not exist")


def parse_arguments():
    # all arguments array
    #arguments = sys.argv[1:]
    argstr = input("Insert data (must include: name, exptime, nrimages):  ")
    arguments = argstr.split()
    try:  # find the index of element "--name"
        name_index = arguments.index('name')
    except:  # hopefuly it exists
        print("Error ", sys.exc_info()[0], "occurred.")
    # the next element of arguments array should be the basename
    name = arguments[name_index + 1]
    try:
        exptime_index = arguments.index('exptime')
    except:
        print("Error ", sys.exc_info()[0], "occurred.")
    exptime = float(arguments[exptime_index + 1])
    try:
        nrimages_index = arguments.index('nrimages')
    except:
        print("Error ", sys.exc_info()[0], "occurred.")
    nrimages = int(arguments[nrimages_index + 1])

    return (name, exptime, nrimages)


def main():

    (name, exptime, nrimages) = parse_arguments()
    location = create_test(name)
    print("I will obtain", nrimages, "images with an exposure time of", float(exptime), "saved as", name)

    print(location)
    for i in range(0,nrimages):

        file_name = "./" + str(i) + ".fits"
        print(file_name)
        print("Single Scan Example")

        print("Intialising SDK3")
        sdk3 = ATCore()  # Initialise SDK3
        deviceCount = sdk3.get_int(sdk3.AT_HNDL_SYSTEM, "DeviceCount");

        print("Found : ", deviceCount, " device(s)");

        if deviceCount > 0:
            try:
                print("  Opening camera ")
                hndl = sdk3.open(0)

                print("    Setting up acuisition")
                sdk3.set_enum_string(hndl, "PixelEncoding", "Mono16")

                imageSizeBytes = sdk3.get_int(hndl, "ImageSizeBytes");
                print("    Queuing Buffer (size", imageSizeBytes, ")");
                buf = np.empty((imageSizeBytes,), dtype='B')
                sdk3.queue_buffer(hndl, buf.ctypes.data, imageSizeBytes);
                buf2 = np.empty((imageSizeBytes,), dtype='B')
                sdk3.queue_buffer(hndl, buf2.ctypes.data, imageSizeBytes);

                sdk3.set_float(hndl, "ExposureTime", exptime)

                print("    Acquiring Frame");
                sdk3.command(hndl, "AcquisitionStart");
                (returnedBuf, returnedSize) = sdk3.wait_buffer(hndl);

                print("    Frame Returned, first 10 pixels");
                pixels = buf.view(dtype='H');
                # for i in range(0, 10):
                #     print("      Pixel ", i, " value ", pixels[i])

                sdk3.command(hndl, "AcquisitionStop");
                print("    Configuring Image")
                config = {}
                config['aoiheight'] = sdk3.get_int(hndl, "AOIHeight")
                config['aoiwidth'] = sdk3.get_int(hndl, "AOIWidth")
                config['aoistride'] = sdk3.get_int(hndl, "AOIStride")
                config['pixelencoding'] = sdk3.get_enum_string(hndl, "PixelEncoding")
                config['temperature'] = sdk3.get_float(hndl, "SensorTemperature")
                    # AT_SetFloat(AT_H Hndl, AT_WC* Feature, double Value);
                config['exposure'] = sdk3.get_float(hndl, "ExposureTime")

                np_arr = buf[0:config['aoiheight'] * config['aoistride']]
                np_d = np_arr.view(dtype='H')
                np_d = np_d.reshape(config['aoiheight'], round(np_d.size / config['aoiheight']))
                formatted_img = np_d[0:config['aoiheight'], 0:config['aoiwidth']]

                print("    Saving to fits file: {0}".format(file_name))
                save(formatted_img, file_name, config, location)            #os.mkdir(os.cwdir+"/test"))

            except ATCoreException as err:
                print("     SDK3 Error {0}".format(err));
            print("  Closing camera");
            sdk3.close(hndl);
        else:
            print("Could not connect to camera");

main()