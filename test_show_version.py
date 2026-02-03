from pyats import aetest
from pyats.topology import loader
from packaging import version


class CommonSetup(aetest.CommonSetup):

    @aetest.subsection
    def connect_to_device(self, testbed):
        device = testbed.devices['R1']
        device.connect(log_stdout=False)
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

    @aetest.test
    def check_uptime_present(self, device):
        """New: verify uptime field exists in parsed output."""
        parsed = device.parse('show version')
        uptime = parsed.get('version', {}).get('uptime', "")
        print(f"\nReported uptime: {uptime}")
        if uptime:
            self.passed("Uptime field is present in 'show version' output")
        else:
            self.failed("Uptime field is missing in 'show version' parsed data")

    @aetest.test
    def check_model_present(self, device):
        """New: verify platform/model field exists."""
        parsed = device.parse('show version')
        model = parsed.get('version', {}).get('platform', "")
        print(f"\nPlatform / Model: {model}")
        if model:
            self.passed("Platform/model information is present")
        else:
            self.failed("Platform/model information is missing")


class CommonCleanup(aetest.CommonCleanup):

    @aetest.subsection
    def disconnect(self, device):
        device.disconnect()
