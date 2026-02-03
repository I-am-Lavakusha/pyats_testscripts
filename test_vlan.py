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

    @aetest.test
    def verify_vlan_exists_in_database(self, device):
        """New: check that VLAN 10 exists in 'show vlan brief'."""
        vlan_id = 10
        output = device.execute('show vlan brief')
        print(output)
        if str(vlan_id) in output:
            self.passed(f"VLAN {vlan_id} exists in VLAN database")
        else:
            self.failed(f"VLAN {vlan_id} does not exist in VLAN database")

    @aetest.test
    def verify_vlan_svi_up(self, device):
        """New: check that SVI Vlan10 (if configured) is up/up."""
        vlan_id = 10
        svi = f"Vlan{vlan_id}"
        output = device.execute(f"show ip interface brief | include {svi}")
        print(output)
        if svi in output and 'up' in output:
            self.passed(f"{svi} interface is up")
        else:
            self.failed(f"{svi} interface is not up or not configured")


class CommonCleanup(aetest.CommonCleanup):

    @aetest.subsection
    def disconnect(self, device):
        device.disconnect()
