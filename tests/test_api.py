# -*- coding: utf-8 -*-

from acore_soap_remote import api


def test():
    _ = api


if __name__ == "__main__":
    from acore_soap_remote.tests import run_cov_test

    run_cov_test(__file__, "acore_soap_remote.api", preview=False)
