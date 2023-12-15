import socket
import ssl

COOKIE_JAR = {}
class URL:
    def __init__(self,url):
        # print(url)
        self.scheme, url = url.split("://", 1)
        assert self.scheme in ["http", "https"]

        if "/" not in url:
            url = url + "/"
        self.host, url = url.split("/", 1)
        self.path = "/" + url

        if self.scheme == "http":
            self.port = 80
        elif self.scheme == "https":
            self.port = 443

        if ":" in self.host:
            self.host, port = self.host.split(":", 1)
            self.port = int(port)

    def request(self,top_level_url,payload=None):
        s = socket.socket(
            family=socket.AF_INET,
            type=socket.SOCK_STREAM,
            proto=socket.IPPROTO_TCP,
        )

        s.connect((self.host,self.port))

        if (self.scheme == "https"):
            s = ssl.wrap_socket(s, keyfile=None, certfile=None, server_side=False, cert_reqs=ssl.CERT_NONE, ssl_version=ssl.PROTOCOL_SSLv23)
        
        
        method = "POST" if payload else "GET"
        body = "{} {} HTTP/1.0\r\n".format(method, self.path)
        body += "Host: {}\r\n".format(self.host)
        if self.host in COOKIE_JAR:
            cookie, params = COOKIE_JAR[self.host]
            allow_cookie = True
            if top_level_url and params.get("samesite", "none") == "lax":
                if method != "GET":
                    allow_cookie = self.host == top_level_url.host
            if allow_cookie:
                body += "Cookie: {}\r\n".format(cookie)
        if payload:
            length = len(payload.encode("utf8"))
            body += "Content-Length: {}\r\n".format(length)
        body += "\r\n" + (payload if payload else "")
        s.send(body.encode("utf8"))

        response = s.makefile("r", encoding="utf8", newline="\r\n")

        statusline = response.readline()
        version, status, explanation = statusline.split(" ", 2)

        response_headers = {}
        
        while True:
            line = response.readline()
            if line == "\r\n": break
            header, value = line.split(":", 1)
            response_headers[header.lower()] = value.strip()

        if "set-cookie" in response_headers:
            cookie = response_headers["set-cookie"]
            params = {}
            if ";" in cookie:
                cookie, rest = cookie.split(";", 1)
                for param in rest.split(";"):
                    if '=' in param:
                        param, value = param.strip().split("=", 1)
                    else:
                        value = "true"
                    params[param.casefold()] = value.casefold()
            COOKIE_JAR[self.host] = (cookie, params)

        body = response.read()
        s.close()
        # print(body)
        return response_headers,body
        
    def resolve(self, url):
        if "://" in url: return URL(url)
        if not url.startswith("/"):
            dir, _ = self.path.rsplit("/", 1)
            while url.startswith("../"):
                _, url = url.split("/", 1)
                if "/" in dir:
                    dir, _ = dir.rsplit("/", 1)
            url = dir + "/" + url
        if url.startswith("//"):
            return URL(self.scheme + ":" + url)
        else:
            return URL(self.scheme + "://" + self.host + \
                       ":" + str(self.port) + url)
    def load(self):
        headers, body = self.request()
        return (headers,body)
    
    def origin(self):
        return self.scheme + "://" + self.host + ":" + str(self.port)
    
    def __repr__(self) -> str:
        port_part = ":" + str(self.port)
        if self.scheme == "https" and self.port == 443:
            port_part = ""
        if self.scheme == "http" and self.port == 80:
            port_part = ""
        return self.scheme + "://" + self.host + port_part + self.path
    
if __name__ == "__main__":
    import sys
    URL(sys.argv[1]).load()
