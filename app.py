import tableauserverclient as tsc 
import json 

with open('./config.json') as f:
    cfg = json.load(f)['server']
    conn = json.load(f)['conn']

auth = tsc.TableauAuth(cfg['user'], cfg['password'], cfg['site'])
tableau = tsc.Server(cfg['url'], use_server_version=True)

with tableau.auth.sign_in(auth):
    for ds in tsc.Pager(tableau.datasources):

        tsc.datasources.populate_connections(ds)

        # Check connections for user@server_host combo to determine if update is needed
        for c in ds.connections if (
            ds.server_address == conn['host'] and ds.username == conn['user']
            ):

            c.username = conn['user']
            c.password = conn['password']

            tsc.datasources.update_connection(ds, c)
            