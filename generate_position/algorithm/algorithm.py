import json
import re
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging

import auditorium
import banquet
import fishbowl
import classroom
import huddleroom
import ushape


class S(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        paths = {
            '/foo': {'status': 200},
            '/bar': {'status': 302},
            '/baz': {'status': 404},
            '/qux': {'status': 500}
        }

        if self.path in paths:
            self.respond(paths[self.path])
        else:
            self.respond({'status': 500})
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))



    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        json_str = post_data.decode('utf-8')  # byte 转 str
        json_str = re.sub('\'', '\"', json_str)  # 单引号转双引号, json.loads 必须使用双引号
        json_dict = json.loads(json_str)  # （注意：key值必须双引号）
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                str(self.path), str(self.headers), post_data.decode('utf-8'))

        res = "You Input: " + post_data.decode('utf-8')
        json_dict_dataForModify=json_dict["newDataForModify"]
        json_dict_lastDataForModify = json_dict["lastDataForModify"]

        if (json_dict_dataForModify["type"] == 'auditorium'):
            auditorium.post(json_dict)
        if (json_dict_dataForModify["type"] == 'banquet'):
            banquet.post(json_dict)
        if (json_dict_dataForModify["type"] == 'classroom'):
            classroom.post(json_dict)
        if (json_dict_dataForModify["type"] == 'fishbowl'):
            fishbowl.post(json_dict)
        if (json_dict_dataForModify["type"] == 'huddle'):
            huddleroom.post(json_dict)
        if (json_dict_dataForModify["type"] == 'ushape'):
            ushape.post(json_dict)

        self.do_HEAD()
        # self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))
        self.wfile.write("{}".format(res).encode('utf-8'))
        # self.wfile.write("POST request for {ASS}".format(data).encode('utf-8'))

    def respond(self, opts):
        response = self.handle_http(opts['status'], self.path)
        self.wfile.write(response)

    def handle_http(self, status_code, path):
        self.send_response(status_code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        content = '''
           <html><head><title>Title goes here.</title></head>
           <body><p>This is a test.</p>
           <p>You accessed path: {}</p>
           </body></html>
           '''.format(path)
        return bytes(content, 'UTF-8')


def position_algorithm(json_dict):
    if "newDataForModify" in json_dict.keys():
        json_dict_dataForModify = json_dict["newDataForModify"]
        json_dict_lastDataForModify = json_dict["lastDataForModify"]
    else:
        json_dict_dataForModify = json_dict

    if (json_dict_dataForModify["type"] == 'auditorium'):
        auditorium.post(json_dict)
    if (json_dict_dataForModify["type"] == 'banquet'):
        banquet.post(json_dict)
    if (json_dict_dataForModify["type"] == 'classroom'):
        classroom.post(json_dict)
    if (json_dict_dataForModify["type"] == 'fishbowl'):
        fishbowl.post(json_dict)
    if (json_dict_dataForModify["type"] == 'huddle'):
        huddleroom.post(json_dict)
    if (json_dict_dataForModify["type"] == 'ushape'):
        ushape.post(json_dict)
    f = open(r"D:\four2\Graduating Design\nlp\generate_position\algorithm\result.json", encoding='utf-8')
    jsonData = ""
    for line in f:
        jsonData += line
    return jsonData

def run(server_class=HTTPServer, handler_class=S, port=8080):
    print("run()")
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print("httpd.server_close()")
    logging.info('Stopping httpd...\n')


if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
    # print(ushape.init(10,-1,-1))

