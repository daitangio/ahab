import doit,os

from doit.action import CmdAction
from doit.tools import result_dep

DOIT_CONFIG = {'default_tasks': []}

SERVICE_NAME="pinger2"

def task_usage():
    def usage():
        print("Ahab builder v1.0 run doit help for full task list")
    return { 'actions': [usage], 'verbosity': 2}

def _generate_env():
    """ 
        See https://github.com/pydoit/doit/issues/171 for CmdAction
    """
    S=doit.get_initial_workdir() +"/config/sonarqube"    
    my_env=os.environ.copy()
    my_env['PING_HOST']= '127.0.0.1'
    my_env['S']=S
    return my_env

def task_make_pinger_image():
    #print(my_env)   
    return {

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
            CmdAction('docker stack up --compose-file slow-pinger-deploy.yml '+SERVICE_NAME,
            env=_generate_env()),
	        'docker stack services '+SERVICE_NAME,
	        'docker service ps '+SERVICE_NAME+'_influxdb'
        ],
        'verbosity': 2
    }

def task_all():
    return {'actions': None,
            'task_dep': ['make_pinger_image', 'run_service', 'status']}

def task_status():
    return {
        'uptodate': [False ],
        'actions':[
            'docker service ps %s_slow_ping' % (SERVICE_NAME),
            'docker service ps %s_influxdb'  % (SERVICE_NAME),            
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