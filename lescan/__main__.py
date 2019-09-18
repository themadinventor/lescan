import sys
import argparse
import gatt
import lescan


class AnyDeviceManager(gatt.DeviceManager):

    def device_discovered(self, device):
        self.print_device(device)

    def print_device(self, device):
        print('[%s] %s' % (device.mac_address, device.alias()))

        rssi = device._properties.Get('org.bluez.Device1', 'RSSI')
        print('\trssi', rssi)

        try:
            txpwr = device._properties.Get('org.bluez.Device1', 'TxPower')
            print('\ttxpwr', txpwr)
        except Exception:
            pass

        try:
            svcdata = device._properties.Get('org.bluez.Device1',
                                             'ServiceData')
            svcdatas = ''
            for k, v in svcdata.items():
                v = ''.join(['%02x' % b for b in v])
                svcdatas = '%s: %s' % (k, v)
            print('\tservices', svcdatas)
        except Exception:
            pass

        try:
            mfgdata = device._properties.Get('org.bluez.Device1',
                                             'ManufacturerData')
            mfgdatas = ''
            for k, v in mfgdata.items():
                v = ''.join(['%02x' % b for b in v])
                mfgdatas = '%04x: %s' % (k, v)
            print('\tmfgdata', mfgdatas)
        except Exception:
            pass

        print()


class FilteringDeviceManager(AnyDeviceManager):

    def __init__(self, bdaddr=None, mfgid=None, rssi=None, *args, **kwargs):
        self.bdaddr = bdaddr
        self.mfgid = mfgid
        self.rssi = rssi
        super().__init__(*args, **kwargs)

    def device_discovered(self, device):
        if self.bdaddr and self.bdaddr != device.mac_address:
            return

        if self.mfgid:
            found = False
            try:
                mfgdata = device._properties.Get('org.bluez.Device1',
                                                 'ManufacturerData')
                for k, _ in mfgdata.items():
                    if k == self.mfgid:
                        found = True
            except Exception:
                pass

            if not found:
                return

        if self.rssi:
            rssi = device._properties.Get('org.bluez.Device1', 'RSSI')
            if rssi < self.rssi:
                return

        self.print_device(device)


def fuzzy_int(s):
    return int(s, 0)


def main():
    parser = argparse.ArgumentParser(
            description='lescan %s' % lescan.__version__,
            prog='lescan',
            epilog='Website: https://github.com/themadinventor/lescan')

    parser.add_argument(
            '--version', '-v',
            help='Print lescan version',
            action='store_true'
            )

    parser.add_argument(
            '--interface', '-i',
            help='Bluetooth interface',
            default='hci0'
            )

    parser.add_argument(
            '--bdaddr', '-b',
            help='Filter by device BDADDR'
            )

    parser.add_argument(
            '--mfgid', '-M',
            help='Filter by manufacturer data ID',
            type=fuzzy_int,
            )

    parser.add_argument(
            '--rssi', '-r',
            help='Filter by RSSI',
            type=float
            )

    args = parser.parse_args()

    if args.version:
        print('lescan', lescan.__version__)
        sys.exit(0)

    try:
        manager = FilteringDeviceManager(bdaddr=args.bdaddr,
                                         mfgid=args.mfgid,
                                         rssi=args.rssi,
                                         adapter_name=args.interface)
        manager.start_discovery()
        manager.run()
    except KeyboardInterrupt:
        print('Interrupted')


if __name__ == '__main__':
    main()
