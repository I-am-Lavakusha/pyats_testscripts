from pyats import aetest

class CommonSetup(aetest.CommonSetup):
    @aetest.subsection
    def connect(self, testbed):
        device = testbed.devices['R1']
        device.connect(log_stdout=False)
        self.parent.parameters['device'] = device


class TestVLAN(aetest.Testcase):

    @aetest.test
    def verify_vlan_subinterface(self, device):
        vlan_id = 10
        expected_subintf = f"GigabitEthernet0/0.{vlan_id}"

        output = device.execute('show ip interface brief')
        print(output)

        if expected_subintf in output:
            self.passed(f"VLAN {vlan_id} subinterface exists")
        else:
            self.failed(f"VLAN {vlan_id} subinterface does NOT exist")


class CommonCleanup(aetest.CommonCleanup):
    @aetest.subsection
    def disconnect(self, device):
        device.disconnect()
