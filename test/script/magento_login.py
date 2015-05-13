#! /usr/bin/env python

import json
import re
import requests
import sys


class MagentoInteraction(object):
    def __init__(self, ip, domain="example.com",
                 login_id="wp_user", password=""):
        self.ip = ip
        self.domain = domain
        self.login_id = login_id
        self.password = password
        self.session = requests.Session()
        self.session.headers.update({"Host": self.domain})

    def get_login_page(self):
        url = "http://{}".format(self.ip)
        r = self.session.get(url)
        return r.text

    def magento_post_login(self):
        url = "http://{}/admin".format(self.ip)
        print "url is {}".format(url)
        data = {"login[username]": self.login_id,
                "login[password]": self.password}
        print json.dumps(data, indent=4)
        r = self.session.post(url, data=data, allow_redirects=False, verify=False)
        while r.is_redirect:
            redirect_url = r.headers.get('location')
            patched_url = re.sub(self.domain, self.ip, redirect_url)
            print "redirecting to {}...".format(patched_url)
            r = self.session.get(patched_url, allow_redirects=False, verify=False)
        print "status code is {}".format(r.status_code)
        return r.text

    def login_successful(self):
        content = self.magento_post_login()
        return "Dashboard" in content


if __name__ == "__main__":
    print json.dumps(sys.argv)
    ip = sys.argv[1]
    domain = sys.argv[2]
    login_id = sys.argv[3]
    password = sys.argv[4]
    magento = MagentoInteraction(ip, domain=domain, login_id=login_id, password=password)

    if magento.login_successful():
        print "Magento admin login successful."
        sys.exit(0)
    else:
        print "login failed :("
        sys.exit(1)
