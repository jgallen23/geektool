#!/usr/bin/env python

from scrapeassist import WebScraper
from optparse import OptionParser

class Bugzilla(object):
    def __init__(self, url):
        self.url = url
        self.scraper = WebScraper()

    def login(self, login, passwd):
        url = self.url + "/index.cgi"
        post_data = {
            'Bugzilla_login': login,
            'Bugzilla_password': passwd,
            'Bugzilla_restrictlogin': "false",
            'GoAheadAndLogIn': 'Login'
        }
        content = self.scraper.get_content(url, post_data)
        if content.find("Invalid Username Or Password") == -1:
            return True
        else:
            raise "Invalid Login or Password"

    def get_bugs(self, search):
        url = "%s/buglist.cgi?cmdtype=runnamed&namedcmd=%s&ctype=csv" % (self.url, search.replace(" ", "%20"))

        csv = self.scraper.get_content(url)
        if csv.find("The search named <em>%s</em>" % (search)) != -1:
            raise "Invalid Search Name"

        bugs = []
        tmp_bugs = csv.split("\n")
        columns = tmp_bugs[0].split(",")
        for b in tmp_bugs[1:]:
            b2 = b.split(",")
            bug = {}
            for i, column in enumerate(columns):
                bug[column.replace("\"", "")] = b2[i].replace("\"", "")
            bugs.append(bug)

        return bugs


def main():
    usage = "usage: %prog -u [url] -l [login] -p [pass] -s [search]"
    parser = OptionParser(usage)
    parser.add_option("-u", "--url", action = "store", type = "string", dest = "url")
    parser.add_option("-l", "--login", action = "store", type = "string", dest = "login")
    parser.add_option("-p", "--pass", action = "store", type = "string", dest = "passwd")
    parser.add_option("-s", "--search", action = "store", type = "string", dest = "search")

    (options, args) = parser.parse_args()

    if options.url and options.search:
        b = Bugzilla(options.url)
        if options.login:
            b.login(options.login, options.passwd)
        bugs = b.get_bugs(options.search)
        print "Bugzilla (%s) - %s" % (options.search, len(bugs))
        for bug in bugs:
            print "%(short_desc)s (%(bug_status)s/%(resolution)s)\n  %(assigned_to)s" % bug

    else:
        parser.print_help()


if __name__ == "__main__": main()
