web: gunicorn variant-kb.wsgi --log-file -
config:set DATABASE_URL='mysql://root:password@localhost:3306/variant_db'
addons:create cleardb:ignite
addons:create cleardb:ignite --fork=`heroku config:get DATABASE_URL`