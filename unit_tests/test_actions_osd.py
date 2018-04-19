from mock import mock
import sys

from test_utils import CharmTestCase

with mock.patch('charmhelpers.contrib.hardening.harden.harden') as mock_dec:
    mock_dec.side_effect = (lambda *dargs, **dkwargs: lambda f:
                            lambda *args, **kwargs: f(*args, **kwargs))
    import show_bcache_devices as bcache_devs


class OpsTestCase2(CharmTestCase):

    def setUp(self):
        super(OpsTestCase2, self).setUp(bcache_devs,['check_output','action_set'])

    def test_show_bcache(self):
        caches = ['sda']
        bcaches = {'bcache0':'sdb','bcache1':'sdc'}
        cmd = "lsblk -l /dev/" + caches[0] + " | tail -n +3 | awk '{print $1}'"
        result = bcache_devs.get_bcaches(caches,bcaches)
        self.check_output.assert_called_with(cmd, shell=True)
