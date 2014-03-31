__author__ = 'ruiayLinSunny'
from mylibs.mytools import *
import pxssh , string


#uniform output
def printinfo (a , b):
    print '     >> ',str(a).ljust(25) , '  :     ',b

#check infos for install
def beforCheck(hostname , port):
    #check port useful
    portcheck = check_port_in_use(hostname,port)

    #check host if it alive
    hostcheck = ping_host(hostname,5)
    if portcheck :
        printinfo('port %s'%(port) ,'OK' )
    else :
        printinfo('port %s'%(port) ,'ERROR' )
    if hostcheck :
        printinfo('ping %s '%(hostname) ,'OK' )
    else :
        printinfo('ping %s '%(hostname) ,'ERROR' )


def gen_config(port,pools,basedir,logdir=''):
    if logdir == '':
        logdir = '/data/mysql{0}/log'.format(port)
    config_template='''
[mysql]
port={0}
prompt=\\u@\\d \\r:\\m:\\s>
default-character-set=gbk
[mysqld]
default-storage-engine=INNODB
#dirs
basedir={1}
tmpdir=/data/mysql{2}/tmp
socket=/data/mysql{3}/run/mysql.sock
slave_load_tmpdir=/data/mysql{4}/tmp
log-error=/data/mysql{5}/log/alert.log
slow_query_log_file=/data/mysql{6}/log/slow.log
relay_log_info_file={7}/binlog/relay-log.info
master-info-file={8}/binlog/master.info
log-bin={9}/binlog/binlog
relay-log={10}/binlog/relaylog
datadir=/data/mysql{11}/data
innodb_log_group_home_dir={12}/iblog
innodb_data_home_dir={13}/iblog
#innodb
innodb_log_files_in_group=4
innodb_log_file_size=200M
innodb_buffer_pool_size={14}g
innodb_open_files=655350
innodb_flush_log_at_trx_commit=2
innodb_max_dirty_pages_pct=50
innodb_io_capacity=200
innodb_read_io_threads=4
innodb_write_io_threads=16
innodb_file_per_table=1
innodb_thread_concurrency=16
innodb_change_buffering=inserts
innodb_adaptive_flushing=1
innodb_fast_checksum=1
innodb_adaptive_flushing_method=keep_average
innodb_stats_on_metadata=0
innodb_additional_mem_pool_size=20M
innodb_flush_method=O_DIRECT
innodb_log_buffer_size=10M
transaction-isolation=READ-COMMITTED
query_cache_type=0
log_slow_verbosity=full
thread_stack=262144
table_definition_cache=2048
table_cache=2048
thread_cache_size=256
sync_binlog=1000
max_binlog_size =500M
binlog_cache_size=5M
binlog-format=ROW
expire_logs_days=7
log-slave-updates
long_query_time=1
slow_query_log=1
skip-slave-start
#timeout
connect_timeout=30
delayed_insert_timeout =300
innodb_lock_wait_timeout=50
innodb_rollback_on_timeout=OFF
net_read_timeout=30
net_write_timeout=60
slave_net_timeout=30
port={15}
skip-name-resolve
max_connect_errors=1500
connect_timeout=30
max_allowed_packet=24M
max_connections=15100
max_user_connections=15000
#myisam
concurrent_insert=2
key_buffer=8M
sort_buffer_size=4M
join_buffer_size=4M
read_buffer_size=4M
myisam_sort_buffer_size=20M
#common
character-set-server=gbk
lower_case_table_names=1
skip-external-locking
open_files_limit=65535
read_rnd_buffer_size=5M
safe-user-create
local-infile=0
[mysqld_safe]
pid-file=/data/mysql{16}/run/mysqld.pid
[client]
port={17}
socket=/data/mysql{18}/run/mysql.sock
'''
    return  config_template.format(port,basedir,port,port,port,port,port,logdir,logdir,logdir,logdir,port,
                                   logdir,logdir,pools,port,port,port,port);


def hostinfomation(hostname,user):
    """ print  the configure information """
    try:
        sshs = pxssh.pxssh(timeout=string.atoi("5"));
        sshs.login (hostname, user,original_prompt=r"[#$]" ,auto_prompt_reset=True,login_timeout=5);
        sshs.sendline ('free -g ')  # run a command
        sshs.prompt()               # match the prompt
        print sshs.before           # print everything before the prompt.
        sshs.sendline ('df -vh ')
        sshs.prompt()
        print sshs.before
        sshs.sendline ('')
        sshs.prompt()
        print sshs.before
        sshs.logout()
    except pxssh.ExceptionPxssh , e:
        print "pxssh failed on login."
        print str(e)


