import doit,os

from doit.action import CmdAction
from doit.tools import result_dep

DOIT_CONFIG = {'default_tasks': []}

SERVICE_NAME="spike1"

def _generate_env():
    """ 
        See https://github.com/pydoit/doit/issues/171 for CmdAction anvironment usage
        To get it working right, you need to copy the current environment or nothing will work right
    """
    S=doit.get_initial_workdir() +"/config/sonarqube"    
    my_env=os.environ.copy()
    my_env['PING_HOST']= '127.0.0.1'
    my_env['S']=S
    return my_env

# Bug executed every time
def task_make_grafana_preconf_volume():
    GRAFANA_BUILD=doit.get_initial_workdir()+"/config/grafana_build"
    return {
        'actions': [
            "docker volume create %s_grafana-storage" % (SERVICE_NAME),
            # id is 104,group is 107
            "docker run --rm -v %s_grafana-storage:/data -v %s:/to_copy alpine cp /to_copy/grafana.db /data/grafana.db"  % (SERVICE_NAME, GRAFANA_BUILD),
            "docker run --rm -v %s_grafana-storage:/data -v %s:/to_copy alpine chown 104:107  /data/grafana.db"  % (SERVICE_NAME, GRAFANA_BUILD),
            "docker run --rm -v %s_grafana-storage:/data -v %s:/to_copy alpine ls -l /data/grafana.db"  % (SERVICE_NAME, GRAFANA_BUILD),

        ], 
        'verbosity': 2
    }

def task_make_pinger_image():
    #print(my_env)   
    return {
        'task_dep': ['make_grafana_preconf_volume'],
        'targets':  [ 'images/pinger.tar'    ],
        'file_dep': [ 'slow_ping/Dockerfile' ],
        # %(dependencies)s -o %(targets)s
        'actions':[
            CmdAction(
                        'docker-compose -f slow-pinger-deploy.yml build', 
                        env=_generate_env()),
           'docker save -o images/pinger.tar slow-ping:latest',
        ],
        'verbosity': 2
    }

def task_run_service():
    return {
        #'uptodate': [result_dep('make_pinger_image')],
        #'uptodate': [False ],
        'file_dep':  [ 'images/pinger.tar',  'slow-pinger-deploy.yml' ],
        'actions':[
            CmdAction('env',env=_generate_env()),
            CmdAction('docker stack up --compose-file slow-pinger-deploy.yml '+SERVICE_NAME,
            env=_generate_env()),
	        'docker stack services '+SERVICE_NAME,
	        'docker service ps '+SERVICE_NAME+'_influxdb'
        ],
        'verbosity': 2
    }

def task_all():
    """
    Build the complete service stack
    """
    return {'actions': None,
            'task_dep': ['make_pinger_image', 'run_service', 'status']}

# run with --continue to overcome error on status launch
def task_status():
    return {
        'uptodate': [False ],
        'actions':[
            'docker stack services %s ' % (SERVICE_NAME),
            #'docker service ps %s_slow_ping' % (SERVICE_NAME),
            #'docker service ps %s_influxdb'  % (SERVICE_NAME),            
        ],
        'verbosity': 2
    }

def task_clean_all():
    """ Remove example stack completly """
    return {        
        'actions':[
            'echo Removing %s_* services' % (SERVICE_NAME),
            'docker stack rm %s' % (SERVICE_NAME),
	        'rm -f images/pinger.tar',
	        'sleep 2',
	        'docker stack services %s' % (SERVICE_NAME)
        ],
        'verbosity': 2
        
    }
def task_clean_volume_too():
    """
    !DANGEROUS! Remove persistent volumes.
    Use after clean_all
    """
    return {
        'actions':[
            "docker volume rm -f %s_grafana-storage %s_influxdb" %(SERVICE_NAME, SERVICE_NAME)
        ]
    }