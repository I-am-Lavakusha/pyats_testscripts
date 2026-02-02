from pyats.easypy import run

def main(runtime):
    run(
        testscript='test_ospf.py',
        testbed=runtime.testbed
    )

