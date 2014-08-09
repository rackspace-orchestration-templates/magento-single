Description
===========

This is a Heat template to deploy a single Linux server running Magento
Community Edition.


Requirements
============
* A Heat provider that supports the following:
  * OS::Nova::KeyPair
  * Rackspace::Cloud::Server
  * OS::Heat::RandomString
  * OS::Heat::ChefSolo
* An OpenStack username, password, and tenant id.
* [python-heatclient](https://github.com/openstack/python-heatclient)
`>= v0.2.8`:

```bash
pip install python-heatclient
```

We recommend installing the client within a [Python virtual
environment](http://www.virtualenv.org/).

Parameters
==========
Parameters can be replaced with your own values when standing up a stack. Use
the `-P` flag to specify a custom parameter.

* `server_hostname`: Hostname to use for the server that is built. (Default:
  Magento)
* `username`: Username for the Magento Administrative user account. (Default:
  MagentoAdmin)
* `domain`: Domain to be used with the Magento store (Default: example.com)
* `last_name`: Last name of the Admin user (Default: last)
* `database_name`: Magento database name (Default: magento)
* `first_name`: First name of the Admin user (Default: first)
* `database_user`: Magento Database Username (Default: magentouser)
* `image`: Required: Server image used for all servers that are created as a
  part of this deployment. (Default: Ubuntu 12.04 LTS (Precise Pangolin))
* `install_sample_data`: If selected, this will install Magento sample data.
  This can be useful for development purposes. (Default: False)
* `admin_email`: Email address to associate with the Magento admin account.
  (Default: admin@example.com)
* `chef_version`: Version of chef client to use (Default: 11.14.2)
* `flavor`: Required: Rackspace Cloud Server flavor to use. The size is based
  on the amount of RAM for the provisioned server. (Default: 4 GB Performance)
* `kitchen`: URL for a git repo containing required cookbooks (Default:
  https://github.com/rackspace-orchestration-templates/magento-single)

Outputs
=======
Once a stack comes online, use `heat output-list` to see all available outputs.
Use `heat output-show <OUTPUT NAME>` to get the value of a specific output.

* `private_key`: SSH Private Key
* `admin_user`: Admin User
* `admin_password`: Admin Password
* `server_ip`: Server IP
* `mysql_root_password`: MySQL Root Password
* `admin_url`: Admin URL
* `magento_url`: Store URL

For multi-line values, the response will come in an escaped form. To get rid of
the escapes, use `echo -e '<STRING>' > file.txt`. For vim users, a substitution
can be done within a file using `%s/\\n/\r/g`.

Stack Details
=============
#### Getting Started
If you're new to Magento Community Edition, the [Magento User
Guide](http://www.magentocommerce.com/resources/user-guide-download) will
step you through the process of configuring and managing your store. This
guide is free, but does require you to provide a valid email address to
receive it.

The [Magento Forum](http://www.magentocommerce.com/boards/) provides a place
to get answers to both simple and advanced questions regarding configuration
and management of Magento Community Edition.

#### Logging into Magento
To login, go to the URL listed above in a browser. If your DNS is not
pointing to this installation, you can add a line in your [hosts
file](http://www.rackspace.com/knowledge_center/article/how-do-i-modify-my-hosts-file)
to point your domain to the IP of this Cloud Server. Once you've done this,
restart your browser and navigate to the site. The backend can be accessed by
adding '/admin' to the end of the URL, and you can login with the credentials
provided above.

#### Logging in via SSH
The private key provided in the passwords section can be used to login as
root via SSH. We have an article on how to use these keys with [Mac OS X and
Linux](http://www.rackspace.com/knowledge_center/article/logging-in-with-a-ssh-private-key-on-linuxmac)
as well as [Windows using
PuTTY](http://www.rackspace.com/knowledge_center/article/logging-in-with-a-ssh-private-key-on-windows).

#### Details of Your Setup
This deployment was stood up using
[chef-solo](http://docs.opscode.com/chef_solo.html). Once the deployment is
up, chef will not run again, so it is safe to modify configurations.

A system user named 'magento' has been created.  This user does not have a
password set, so if you wish to use the account, a password will need to be
set.  This account is the system user for PHP-FPM, so deletion of this user
will take eCommerce site down.

[Nginx](http://nginx.org/en/) is used as the web server and listens on port
80 and 443 to handle web traffic. The configuration for your site can be
found in /etc/nginx/sites-enabled. There will be a default site
configuration, and a seperate one for SSL traffic. Magento itself is
installed in /var/www/vhosts. You will find a directory with the name of
website you entered as a part of this deployment. The SSL certificates used
are self signed and were generated when this deployment was created. You can
replace the private key and certificate by overwriting the ones in
/etc/nginx/ssl.

[PHP-FPM](http://php.net/manual/en/install.fpm.php) is used to handle
evaluation of all PHP-based pages. The configuration for this installation is
in /etc/php5/fpm/pools/magento.conf. By default, PHP-FPM is running as the
'magento' user, listens on 127.0.0.1:9001.

Object and session caching are handled by
[Memcached](http://www.memcached.org/).  Memcache helps performance by
storing data in memory for faster responses to clients. These caches help
lessen the number of queries required to the database.  There are two
seperate instances of Memcached running to ensure session and object caching
are handled seperately.  The session cache is listening on 127.0.0.1:11211,
and is set as a 512MB cache.  The object cache is listening on
127.0.0.1:11212, and it is set as a 1.5GB cache.  The configuration files are
memcached_sessions.conf and memcached_backend.conf in /etc.

[MySQL 5.5](http://www.mysql.com/) is installed as the database backend. All
configuration with Magento has been handled as a part of the setup. The MySQL
root password is provided as a part of this deployment.  If you lose or
forget the password, it can also be found in /root/.my.cnf.

MySQL backups are performed nightly by
[Holland](https://github.com/holland-backup/holland).  Backups can be found
in /var/lib/mysqlbackup.

#### Magento Plugins
There are thousands of plugins that have been developed for Magento by the
developer community. [Magento
Connect](http://www.magentocommerce.com/magento-connect/) provides an easy
way to discover popular plugins that other users have found to be helpful.
Not all plugins are free, and we recommend only installing the plugins that
you need.

#### Additional Notes
There is not an automatic way to add additional nodes to this deployment.
This deployment is meant for lower traffic or testing scenarios.

Contributing
============
There are substantial changes still happening within the [OpenStack
Heat](https://wiki.openstack.org/wiki/Heat) project. Template contribution
guidelines will be drafted in the near future.

License
=======
```
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```
