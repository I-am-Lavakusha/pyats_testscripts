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

    @aetest.test
    def check_ospf_router_id_present(self, device):
        """New: verify OSPF router-id line exists."""
        output = device.execute('show ip ospf | include Router ID')
        print(output)
        if 'Router ID' in output:
            self.passed("OSPF router-id is present")
        else:
            self.failed("OSPF router-id is not shown in output")

    @aetest.test
    def check_ospf_interface_brief(self, device):
        """New: basic sanity on OSPF interfaces."""
        output = device.execute('show ip ospf interface brief')
        print(output)
        if 'Interface' in output and 'Nbr' in output:
            self.passed("OSPF interface brief output looks correct")
        else:
            self.failed("OSPF interface brief output does not look expected")

class CommonCleanup(aetest.CommonCleanup):
    @aetest.subsection
    def disconnect(self, device):
        device.disconnect()
