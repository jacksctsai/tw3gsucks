#!/usr/bin/env python
# Forwarded version from thomasfischer.biz!!!
#
import os, sys, string, time, getopt, socket, select, re, errno, copy, signal        

def queryWhois(query, server='whois.ripe.net'):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while 1:
        try:
            s.connect((server, 43))
        except socket.error, (ecode, reason):
            if ecode==errno.EINPROGRESS:
                continue
            elif ecode==errno.EALREADY:
                continue
            else:
                raise socket.error, (ecode, reason)
            pass
        break                                            

    ret = select.select ([s], [s], [], 30)

    if len(ret[1])== 0 and len(ret[0]) == 0:
        s.close()
        raise TimedOut, "on data"           

    s.setblocking(1)

    s.send("%sn" % query)
    page = ""
    while 1:
        data = s.recv(8196)
        if not data: break
        page = page + data
        pass

    s.close()

    if string.find(page, "IANA-BLK") != -1:
        raise 'no match'

    if string.find(page, "Not allocated by APNIC") != -1:
        raise 'no match'

    return page

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "usage: %s " % sys.argv[0]
        sys.exit(1)
    ip = sys.argv[1]

    #for server in ['whois.arin.net', 'whois.ripe.net', 'whois.apnic.net', 'whois.lacnic.net', 'whois.afrinic.net']:
    for server in ['whois.arin.net']:
        try:
            res = queryWhois(ip, server)
            print '======', server
            print res
            break # we only need the info once
        except:
            pass