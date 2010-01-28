#!/usr/bin/env python
import re
import urllib
import urllib2
import httplib
import cookielib

class RedirectHandler(urllib2.HTTPRedirectHandler):
    def http_error_302(self,req,fp,code,msg,headers):
        result = urllib2.HTTPRedirectHandler.http_error_302(
            self, req, fp, code, msg, headers)
        result.status = code
        return result

class ScraperBase(object):
    def __init__(self):
        self.content = ""

    def get_content(self):
        raise "Must override"

    def scrape(self):
        raise "Must override"

    def interactive(self):
        namespace = locals().copy()
        namespace["scraper"] = self
        namespace["s"] = self
        import IPython
        IPython.Shell.IPShell(argv = [], user_ns=namespace).mainloop(sys_exit=1)

class WebScraper(ScraperBase):
    def __init__(self, url = None, debug = False):
        ScraperBase.__init__(self)
        self.url = url
        self.user_agent = "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.12) Gecko/20080207 Ubuntu/7.10 (gutsy) Firefox/2.0.0.12"
        self.cookie_jar = cookielib.CookieJar()
        debug_level = 1 if debug else 0
        httplib.HTTPConnection.debuglevel = debug_level
        handler = urllib2.HTTPHandler(debuglevel=debug_level)
        self.opener = urllib2.build_opener(RedirectHandler(),handler,urllib2.HTTPCookieProcessor(self.cookie_jar))

    def get_content(self, url = None, post_data = None):
        if post_data:
            post_data = urllib.urlencode(post_data)
        if not url:
            url = self.url
        req = urllib2.Request(url, post_data)
        req.add_header("User-Agent", self.user_agent)
        res = self.opener.open(req)
        html = res.read()
        return html

    def scrape(self, regex, url = None, post_data = None):
        if not self.content and not url:
            url = self.url
        if url:
            self.content = self.get_content(url, post_data)

        matches = re.compile(regex, re.S).findall(self.content)
        return matches

class FileScraper(ScraperBase):
    def __init__(self, file_path):
        if not os.path.exists(file_path):
            raise "File not found"
        self.file_path = file_path

    def get_content(self):
        f = open(self.file_path, 'r')
        contents = f.read()
        f.close()
        return contents

    def scrape(self, regex):
        if not self.content:
            self.content = self.get_content()
        matches = re.compile(regex, re.S).findall(self.content)
        return matches

def main():
    from optparse import OptionParser
    usage = "usage: %prog [options]"
    parser = OptionParser(usage)
    parser.add_option("-u", "--url", action = "store", type = "string", dest = "url")
    parser.add_option("-f", "--file", action = "store", type = "string", dest = "file")
    parser.add_option("-d", "--debug", action = "store_true", default = False, dest = "debug")


    (options, args) = parser.parse_args()

    scraper = None
    if options.url:
        scraper = WebScraper(url = options.url, debug = options.debug)
    elif options.file:
        scraper = FileScraper(options.file)

    if scraper:
        scraper.interactive()
    else:
        parser.print_help()

if __name__ == "__main__": main()
