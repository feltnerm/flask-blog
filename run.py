#!/usr/bin/env python

import sys
import argparse

from experientiarum import generate_app

def process_args(argv):
    

    if not argv:
        argv = sys.argv[1:]

    ap = argparse.ArgumentParser(description='Run experientiarum server')
    
    
    ap.add_argument('-s','--server-type', default='dev')
                    
    
    args = ap.parse_args(argv)
    
    return args
    

def main(argv=None):
    ''' Main function in which we run the Flask application 
    which also invokes the blueprints of all other active
    applications. 
    
    @todo: dev/prod command line arguments and config importing
    '''
    
    run_settings = process_args(argv)
    if run_settings.server_type.startswith('d'):
        app = generate_app('config.DevConfig')
        
    elif run_settings.server_type.startswith('t'):
        app = generate_app('config.TestConfig')
    
    else run_settings.server_type.startswith('d'):
        app = generate_app('config.ProdConfig')
        
    app.run()

    return 0
if __name__ == '__main__':
    status = main()
    sys.exit(status)