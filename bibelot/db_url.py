import os
postgres = {
  'user': os.environ['DB_USER'],
  'pw': os.environ['DB_PASS'],
  'db': os.environ['DB_NAME'],
  'host': os.environ['DB_HOST'],
  'port': os.environ['DB_PORT']
}

db_url = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s'%postgres