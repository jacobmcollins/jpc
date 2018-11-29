from client.JPCClient import JPCClient
import argparse
import os
import sys

path = os.path.dirname(__file__)
sys.path.append(path)


def handle_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("ip", type=str, help="server ip address")
    return parser.parse_args()


if __name__ == '__main__':
    try:
        args = handle_args()
        client = JPCClient(args.ip)
        client.run()
    except KeyboardInterrupt:
        print('keyboard interrupt')
    except Exception as e:
        print(e)
    finally:
        sys.exit()