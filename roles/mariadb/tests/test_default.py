import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    '.molecule/ansible_inventory').get_hosts('all')


def test_hosts_file(File):
    f = File('/etc/hosts')

    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'


def test_openstack_config(File):
    f = File('/etc/mysql/mariadb.conf.d/99-openstack.cnf')

    assert f.exists
    lines = [
        '[mysqld]',
        'bind-address = 127.0.0.1',
        'port = 3306',
        'datadir = /var/lib/mysql',
        'default-storage-engine = innodb',
        'innodb_file_per_table',
        'max_connections = 4096',
        'collation-server = utf8_general_ci',
        'character-set-server = utf8'
    ]
    for line in lines:
        assert f.contains(line)


def test_mariadb_server(Service):
    s = Service('mysql')

    assert s.is_enabled
    assert s.is_running
