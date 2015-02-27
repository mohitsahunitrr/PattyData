#!/usr/bin/env python
##############################################################################
# Description:      Script to remove a raw data item and the related POTree/OSG
#
# Authors:          Oscar Martinez, NLeSC, o.rubi@esciencecenter.nl
#                   Elena Ranguelova, NLeSc
# Created:          16.02.2015
# Last modified:    27.02.2015
#
# Changes:
#
# Notes:            * User gives an ID from raw_data_item_id
#                   * The absPath of the raw data item is retrieved
#                   * The absPath of related (OSG/POTree) data item are retrieved
#                   * All the previous data is deleted
##############################################################################
import argparse
import utils, time


logger = None
connection = None
cursor = None

def argument_parser():
    description = "Removes a Raw data item and the related converted data from the file structure."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-i', '--itemid', help='Raw data item id (with ? the available raw data items are listed)',
                        action='store', required=True)
    parser.add_argument('-d','--dbname',default=utils.DEFAULT_DB, help='PostgreSQL DB name ' + utils.DEFAULT_DB + ']',type=str , required=False)
    parser.add_argument('-u','--dbuser',default=utils.USERNAME,help='DB user [default ' + utils.USERNAME + ']',type=str, required=False)
    parser.add_argument('-p','--dbpass',default='',help='DB pass',type=str, required=False)
    parser.add_argument('-t','--dbhost',default='',help='DB host',type=str, required=False)
    parser.add_argument('-r','--dbport',default='',help='DB port',type=str, required=False)
    parser.add_argument('-l', '--log', help='Log level',
                        choices=['debug', 'info', 'warning', 'error',
                                 'critical'],
                        default=utils.DEFAULT_LOG_LEVEL)

    return parser 
 
def apply_argument_parser(options=None):
    """ Apply the argument parser. """
    parser = argument_parser()
    if options is not None:
        args = parser.parse_args(options)
    else:
        args = parser.parse_args() 
            
    return args
    
#def remove_data(opts):
#    """
#    Removes the data from the file structure.
#    """
#    logger.info('Removing data.')
#   # logger.info("Finished copying data to " + TARGETDIR)


def fetch_abs_path(siteId):
    """ get the absolute data item path given the site ID"""
    abs_path = ""
    
    fetch_abs_path_statement = 'select abs_path from raw_data_item natural join item where item_id = %s'
    abs_path,num = utils.fetchDataFromDB(cursor, fetch_abs_path_statement, [siteId,],[], False)
        
    
    return abs_path
    
def fetch_potree_abs_paths(siteId):
    """ get the absolute data item paths for the potree converted data given the site ID"""
    abs_paths = ""
    
    fetch_potree_abs_path_statement = 'select abs_path from potree_data_item_pc natural join raw_data_item_pc natural join item where item_id = %s'
    abs_paths,num = utils.fetchDataFromDB(cursor, fetch_potree_abs_path_statement, [siteId,],[], False)
        
    
    return abs_paths, num   
    
def fetch_osg_abs_paths_pc(siteId):
    """ get the absolute data item paths for the osg PC data given the site ID"""
    abs_paths = ""
    
    fetch_osg_abs_path_statement = 'select abs_path from osg_data_item natural join osg_data_item_pc_site natural join  raw_data_item_pc natural join item where item_id = %s'
    abs_paths,num = utils.fetchDataFromDB(cursor, fetch_osg_abs_path_statement, [siteId,],[], False)
        
    
    return abs_paths, num       
#------------------------------------------------------------------------------        
def run(args): 
    
    # set logging level
    global logger
    global connection
    global cursor
    
    logger = utils.start_logging(filename=utils.LOG_FILENAME, level=args.log)
    logger.info('#######################################')
    logger.info('Starting script RemoveRawDataItem.py')
    logger.info('#######################################')

 # start timer
    t0 = utils.getCurrentTime()
    
    # connect to the DB
    connection, cursor = utils.connectToDB(args.dbname, args.dbuser, args.dbpass, args.dbhost, args.dbport) 

    # fetch the abs_path
    abs_path = fetch_abs_path(args.itemid)        
    msg = 'Abs path fetched: %s', abs_path
    print msg
    logger.info(msg)
    
    # fetch the potree abs_paths
    abs_potree_paths, num = fetch_potree_abs_paths(args.itemid)        
    msg = '%s abs potree paths fetched %s' %(num, abs_potree_paths)
    print msg
    logger.info(msg)
    
    # fetch the OSG abs_paths
    abs_osg_pc_paths, num = fetch_osg_abs_paths_pc(args.itemid)        
    msg = '%s abs OSG paths for PC fetched: %s' %(num, abs_osg_pc_paths)
    print msg
    logger.info(msg)    
    # copy the data to the target directory
    #remove_data(opts)

    # measure elapsed time
    elapsed_time = time.time() - t0    
    msg = 'Finished. Total elapsed time: %.02f seconds. See %s' % (elapsed_time, utils.LOG_FILENAME)
    print(msg)
    logger.info(msg)

    return


    
if __name__ == '__main__':
    run( apply_argument_parser() )
