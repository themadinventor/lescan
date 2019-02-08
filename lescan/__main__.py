import gatt

class AnyDeviceManager(gatt.DeviceManager):

    def device_discovered(self, device):
        print('[%s] %s' % (device.mac_address, device.alias()))

        rssi = device._properties.Get('org.bluez.Device1', 'RSSI')
        print('\trssi', rssi)

        try:
            txpwr = device._properties.Get('org.bluez.Device1', 'TxPower')
            print('\ttxpwr', txpwr)
        except Exception as e:
            pass

        try:
            svcdata = device._properties.Get('org.bluez.Device1',
                    'ServiceData')
            svcdatas = ''
            for k, v in svcdata.items():
                v = ''.join(['%02x' % b for b in v])
                svcdatas = '%s: %s' % (k, v)
            print('\tservices', svcdatas)
        except:
            pass

        try:
            mfgdata = device._properties.Get('org.bluez.Device1',
                    'ManufacturerData')
            mfgdatas = ''
            for k, v in mfgdata.items():
                v = ''.join(['%02x' % b for b in v])
                mfgdatas = '%04x: %s' % (k, v)
            print('\tmfgdata', mfgdatas)
        except:
            pass

        print()


def main():
    manager = AnyDeviceManager(adapter_name='hci0')
    manager.start_discovery()
    manager.run()


if __name__ == '__main__':
    main()
