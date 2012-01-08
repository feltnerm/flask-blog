#!/usr/bin/env python

import sys
import argparse

from experientiarum import app

def process_settings(args):
    
    server_type = ''

def process_args(argv):
    

    if not argv:
        argv = sys.argv[1:]

    ap = argparse.ArgumentParser(description='Run experientiarum server')
    
    
    ap.add_argument('-d','--development', help='Run development server'
                    , default = True, action='store_true')
    
    ap.add_argument('-p','--production', help='Run production server'
                    , default = False, action='store_true')
    
    args = ap.parse_args(argv)
    
    return args
    

def main(argv=None):
    ''' Main function in which we run the Flask application 
    which also invokes the blueprints of all other active
    applications. 
    
    @todo: dev/prod command line arguments and config importing
    '''
    

    app.run()

    return 0
if __name__ == '__main__':
    status = main()
    sys.exit(status)