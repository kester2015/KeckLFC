try:
    from SC10_COMMAND_LIB import *
    import time
except OSError as ex:
    print("Warning:", ex)


# ------------ Example Device Read&Write -------------- #
def device_read_write_demo(sc10obj):
    print("*** Device Read&Write example")

    baud_rate = [0]    # 0 for 9.6k and 1 for 115k
    baud_rate_list = {0:"9600", 1:"115200"}
    result = sc10obj.get_baud_rate(baud_rate)
    if result < 0:
        print("get_baud_rate failed", result)
    else:
        print("get baud_rate: ", baud_rate_list.get(baud_rate[0]))

    mode = 1
    result = sc10obj.set_mode(mode)  # SC10 mode. 1-manual, 2-auto, 3-single, 4-repeat, 5-external gate
    if result < 0:
        print("set_mode failed", result)
    else:
        print("set_mode to manual")

    mode = [0]
    mode_list = {1: "manual", 2: "auto", 3: "single", 4: "repeat", 5: "external gate"}
    result = sc10obj.get_mode(mode)
    if result < 0:
        print("get_mode failed")
    else:
        print("get_mode:", mode_list.get(mode[0]))

    result = sc10obj.set_open_time(5)
    if result < 0:
        print("set_open_time failed", result)
    else:
        print("set_open_time to 5")

    open_time = [0]
    result = sc10obj.get_open_time(open_time)
    if result < 0:
        print("get_open_time failed")
    else:
        print("get_open_time:", open_time)


def main():
    print("*** SC10 device python example ***")
    sc10obj = SC10()
    try:
        devs = SC10.list_devices()
        print(devs)
        if len(devs) <= 0:
            print('There is no devices connected')
            exit()
        sn = str(input("Please type the device sn to connect: "))
        print("connect ", sn)
        hdl = sc10obj.open(sn, 9600, 3)
        if hdl < 0:
            print("open ", sn, " failed")
            exit()
        if sc10obj.is_open(sn) == 0:
            print("SC10 IsOpen failed")
            sc10obj.close()
            exit()

        device_read_write_demo(sc10obj)
        print("---------------------------Device Read&Write finished-------------------------")
        sc10obj.close()

    except Exception as e:
        print("Warning:", e)
    print("*** End ***")
    input()


main()
