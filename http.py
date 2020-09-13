import socket


def createTCPSocket():
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def sendRequest():
    return None


class http:
    http_protocol = "HTTP/1.0"

    def __init__(self, print_response_from_http_client):

        # Server to send request to
        self._server = None
        self._path = None
        self._port = None

        self._verbosity = None

        self._request_type = None
        self._request = None
        self._request_headers = {}
        self._request_query_parameters = ""
        self._request_body = ""

        self._response = None
        self._response_headers = None
        self._response_data = None

        self.print_response_from_http_client = print_response_from_http_client

    @property
    def server(self):
        return self._server

    @server.setter
    def set_server(self, server):
        self._server = server

    @property
    def path(self):
        return self._path

    @path.setter
    def set_path(self, path):
        if path == "":
            self._path = "/"
        else:
            self._path = path

    @property
    def port(self):
        return self._port

    @port.setter
    def set_port(self, port):
        self._port = port

    @property
    def verbosity(self):
        return self._verbosity

    @verbosity.setter
    def set_verbosity(self, verbosity):
        self._verbosity = verbosity

    @property
    def request_type(self):
        return self._request_type

    @request_type.setter
    def set_request_type(self, request_type):
        self._request_type = request_type

    @property
    def request(self):
        return self._request

    @request.setter
    def set_request(self, request):
        self._request = request

    @property
    def request_headers(self):
        header = ""
        for key, val in self._request_headers.items():
            header = header + (key + ": " + val + "\n")
        return header

    @request_headers.setter
    def set_request_headers(self, request_headers):
        self._request_headers.update(request_headers)

    @property
    def request_query_parameters(self):
        return self._request_query_parameters

    @request_query_parameters.setter
    def set_request_query_parameters(self, request_query_parameters):
        self._request_query_parameters = request_query_parameters

    @property
    def request_body(self):
        return self._request_body

    @request_body.setter
    def set_request_body(self, request_body):
        self._request_body = request_body

    @property
    def response(self):
        return self._response

    @response.setter
    def set_response(self, response):
        self._response = response

    @property
    def response_headers(self):
        return self._response_headers

    @response_headers.setter
    def set_response_headers(self, response_headers):
        self._response_headers = response_headers

    @property
    def response_data(self):
        return self._response_data

    @response_data.setter
    def set_response_data(self, response_data):
        self._response_data = response_data

    def send_HTTP_request(self):
        self.generate_request()
        tcp_socket = createTCPSocket()
        try:
            tcp_socket.connect((self.server, self.port))
            tcp_socket.sendall(self.request.encode("utf-8"))
            server_response = tcp_socket.recv(2048, socket.MSG_WAITALL)
            self.parse_response(server_response.decode("utf-8"))
            self.displayResults()

        except socket.error as error:
            print("socket connection error: ", error)

    def generate_request(self):
        # GET /status/418 HTTP/1.0
        # Host: httpbin.org
        # HTTP/1.1 418 I'M A TEAPOT
        # Server: nginx
        # Date: Sat, 29 Jul 2017 21:58:24 GMT
        # Content-Length: 135
        # Connection: close
        # Access-Control-Allow-Origin: *
        # x-more-info: http://tools.ietf.org/html/rfc2324
        # Access-Control-Allow-Credentials: true

        if self.request_query_parameters:
            self.set_request_query_parameters = "?" + self.request_query_parameters

        self.set_request = self.request_type.upper() + " " + self.path + \
                           self.request_query_parameters + " " + self.http_protocol + " \n" + \
                           self.request_headers + "\n"

        if self.request_type == "post":
            if self.request_body:
                self.set_request = self.request + self.request_body

    def parse_response(self, response):
        (headers, json_response) = response.split("\r\n\r\n")

        self.set_response = response
        self.set_response_headers = headers
        self.set_response_data = json_response

    def displayResults(self):
        if self._verbosity:
            self.print_response_from_http_client(self.response, self.response_data)
        else:
            self.print_response_from_http_client(self.response_data, self.response_data)
