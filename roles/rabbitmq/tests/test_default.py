import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    '.molecule/ansible_inventory').get_hosts('all')


def test_hosts_file(File):
    f = File('/etc/hosts')

    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'


def test_package(Package):
    p = Package('rabbitmq-server')

    assert p.is_installed


def test_rabbitmq(Service):
    s = Service('rabbitmq-server')

    assert s.is_enabled
    assert s.is_running


def test_conf(Sudo, Command):
    with Sudo():
        vhosts = Command('rabbitmqctl list_vhosts | grep /openstack')
        users = Command('rabbitmqctl list_users | grep openstack')

        assert vhosts.rc == 0
        assert users.rc == 0
