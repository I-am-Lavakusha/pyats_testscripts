from pyats import aetest
from pyats.topology import loader
from packaging import version


class CommonSetup(aetest.CommonSetup):
    @aetest.subsection
    def connect_to_device(self, testbed):
        device = testbed.devices['R1']
        device.connect(log_stdout=False)

        # Save device for testcases
        self.parent.parameters['device'] = device


class TestIOSVersion(aetest.Testcase):

    @aetest.test
    def check_ios_version(self, device):
        parsed = device.parse('show version')
        ios_version = parsed['version']['version']

        print(f"\nDetected IOS Version: {ios_version}")

        if version.parse(ios_version) >= version.parse("17.9"):
            self.passed(f"IOS version {ios_version} is compliant")
        else:
            self.failed(f"IOS version {ios_version} is NOT compliant")


class CommonCleanup(aetest.CommonCleanup):
    @aetest.subsection
    def disconnect(self, device):
        device.disconnect()
