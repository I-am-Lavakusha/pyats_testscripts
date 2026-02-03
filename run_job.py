from pyats.easypy import run

def main(runtime):
    run(
        testscript='test_ospf.py',
        testbed=runtime.testbed
    )

    run(
        testscript='test_show_version.py',
        testbed=runtime.testbed
    )

    run(
        testscript='test_vlan.py',
        testbed=runtime.testbed
    )
