import os
# import sys
import socket
import datetime
import time

FILE = os.path.join(os.getcwd(), "network.log")


def ping():
    try:
        socket.setdefaulttimeout(3)

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        host = "8.8.8.8"
        port = 53
        server_address = (host, port)
        s.connect(server_address)
    except OSError as os_err:
        print("[OSError]:", os_err)
        return False

    s.close()
    return True


def calculate_time(start, stop):
    diff = stop - start
    secs = float(str(diff.total_seconds()))
    return str(datetime.timedelta(seconds=secs)).split(".", maxsplit=1)[0]


def first_check():
    if ping():
        live = "\nCONNECTION ACQUIRED\n"
        print(live)

        conn_acq_time = datetime.datetime.now()

        acq_msg = "connection acquired at: " + \
            str(conn_acq_time).split(".", maxsplit=1)[0]
        print(acq_msg)

        with open(FILE, "a", encoding='utf-8') as file:
            file.write(live)
            file.write(acq_msg)
        return True

    not_live = "\nCONNECTION NOT ACQUIRED\n"
    print(not_live)

    with open(FILE, "a", encoding='utf-8') as file:
        file.write(not_live)
    return False


def main():
    monitor_start_time = datetime.datetime.now()
    monitoring_date_time = "monitoring started at: " + \
        str(monitor_start_time).split(".", maxsplit=1)[0]

    if first_check():
        print(monitoring_date_time)
    else:
        while True:
            # infinite loop to see if the connection is acquired
            if not ping():
                # if connection not acquired
                time.sleep(1)
            else:
                # if connection is acquired
                first_check()
                print(monitoring_date_time)
                break

    with open(FILE, "a", encoding='utf-8') as file:
        file.write("\n")
        file.write(monitoring_date_time + "\n")

    while True:
        if ping():
            time.sleep(5)
        else:
            down_time = datetime.datetime.now()
            fail_msg = "disconnected at: " + str(down_time).split(".", maxsplit=1)[0]
            print(fail_msg)

            with open(FILE, "a", encoding='utf-8') as file:
                file.write(fail_msg + "\n")

            while not ping():
                time.sleep(1)

            up_time = datetime.datetime.now()
            uptime_message = "connected again: " + str(up_time).split(".", maxsplit=1)[0]

            down_time = calculate_time(down_time, up_time)
            unavailablity_time = "connection was unavailable for: " + down_time

            print(uptime_message)
            print(unavailablity_time)

            with open(FILE, "a", encoding='utf-8') as file:
                file.write(uptime_message + "\n")
                file.write(unavailablity_time + "\n")


main()
