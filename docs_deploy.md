# Login to remote server and Manually run
* This will setup all the required server file configs
* and also create proper directory structure.
./0-setup_web_static.sh # Only run once per server.
# archive web resource files in current directory
fab -f 1-pack_web_static.py do_pack
# Upload archive to remote host - clutter is left in /data/
fab -f 2-do_deploy_web_static.py do_deploy:archive_path=versions/web_static_20230409092328.tgz -u 108999f0b0e4 -p 785b0035e30507820c46 --hosts 108999f0b0e4.a73c91be.alx-cod.online
# Test for Success Deploy
curl -Si 0:/current/he