from aria2.client import Aria2Client

if __name__ == '__main__':
    # print(len(Aria2Client.get_active_list()))
    # print(len(Aria2Client.get_waiting_list()))
    from datetime import datetime

    fromtimestamp = datetime.fromtimestamp(1683111976)
    print(fromtimestamp.strftime("%y%m%d"))
