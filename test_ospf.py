from pyats import aetest


class CommonSetup(aetest.CommonSetup):
    @aetest.subsection
    def connect(self, testbed):
        device = testbed.devices['R1']
        device.connect(log_stdout=False)
        self.parent.parameters['device'] = device


class TestOSPF(aetest.Testcase):

    @aetest.test
    def check_ospf_process(self, device):
        output = device.execute('show ip ospf')
        print(output)

        if 'Routing Process "ospf' in output:
            self.passed("OSPF process is running")
        else:
            self.failed("OSPF process is NOT running")

    @aetest.test
    def check_ospf_neighbors(self, device):
        output = device.execute('show ip ospf neighbor')
        print(output)

        if 'FULL' in output:
            self.passed("OSPF neighbors are in FULL state")
        else:
            self.failed("No OSPF neighbors in FULL state")

    @aetest.test
    def check_ospf_routes(self, device):
        output = device.execute('show ip route ospf')
        print(output)

        if 'O' in output:
            self.passed("OSPF routes are present in routing table")
        else:
            self.failed("No OSPF routes found")


class CommonCleanup(aetest.CommonCleanup):
    @aetest.subsection
    def disconnect(self, device):
        device.disconnect()
