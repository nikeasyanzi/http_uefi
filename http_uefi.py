#! /usr/bin/env python3
import cgi
import json
import os
import subprocess
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from subprocess import PIPE, Popen
from urllib.parse import urlparse

SOURCE_PATH = os.path.abspath("./")
UPLOAD_DIRECTORY = r"{}\uploads".format(SOURCE_PATH)
TEST_LOG_DIRECTORY = r"{}\logs".format(SOURCE_PATH)

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

if not os.path.exists(TEST_LOG_DIRECTORY):
    os.makedirs(TEST_LOG_DIRECTORY)


def post_route(operation, message):
    """
    handle post requests file uploading
    """

    def readlog(path):
        content=""

        try:
            with open(path) as f:
                content = f.readlines()
        except FileNotFoundError:
                content = "File {} not found. Aborting".format(path)
        #print(content)
        res = {"message": content}
        return res
    def listdir(path):
        try:
            content=os.listdir(path)
        except Exception as e:
            content="{} at Path {}".format(e,path)
        res = {"message": content}
        return res

    post_operations = {
        'readlog': readlog,
        'listdir': listdir,
    }

    try:
        print(operation,message)
        path=message["path"]
        res=post_operations[operation](path)
        return res

    except KeyError as error:
        res="The operation {} is not supported".format(operation)

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            html = """
                <html>
                    <body>
                        <h2>Upload a file</h2>
                        <form enctype="multipart/form-data" method="post">
                            <input type="file" name="file" />
                            <input type="submit" value="Upload" />
                        </form>
                    </body>
                </html>
            """
            self.wfile.write(html.encode("utf-8"))
        elif "/run/" in self.path:
            file = urlparse(self.path)

            print(file.path)
            filename = os.path.basename(file.path)
            file_path = os.path.join(UPLOAD_DIRECTORY, filename)
            print("{}:{}".format(filename, file_path))
            print("isfile:", os.path.isfile(file_path))
            print("exist:", os.path.exists(file_path))
            # TODO error handling if !os.path.isfile(file_path):

            cmd = file_path
            if file_path.endswith(".py"):
                cmd = "python {}".format(file_path)
            print("cmd:{}\n".format(cmd))

            try:
                result=0
                # Open the file and read its content.
                result = os.system(cmd)
                response = {"returncode": result}
            except Exception as e:
                response = {"error": str(e)}
            # print(execution_response)

            self.send_response(400)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
        elif "/byehttpuefi" in self.path:
            content = "Bye HTTP UEFI!!"
            self.send_response(400)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            response = {"message": content}
            self.wfile.write(json.dumps(response).encode())
            exit(0)

        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        ctype, pdict = cgi.parse_header(self.headers["Content-Type"])
        if self.path == "/" and ctype == "multipart/form-data":
                form = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={"REQUEST_METHOD": "POST"},
                )
                if "file" in form:
                    field_item = form["file"]
                    if field_item.file:
                        filename = os.path.basename(field_item.filename)
                        file_path = os.path.join(UPLOAD_DIRECTORY, filename)
                        with open(file_path, "wb") as f:
                            f.write(field_item.file.read())
                        self.send_response(201)
                        self.send_header("Content-type", "application/json")
                        self.end_headers()
                        response = {
                            "message": "File uploaded successfully",
                            "filename": filename,
                        }
                        self.wfile.write(json.dumps(response).encode())

        elif ctype == 'application/json':
            # read the message and convert it into a python dictionary
            length = int(self.headers.get('content-length'))
            message = json.loads(self.rfile.read(length))
        
            operation=self.path[1:]
            message=post_route(operation,message)
            
            # send the message back
            self.send_response(400)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(message).encode(encoding='utf_8'))
        else:
            self.send_response(400)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            response = {"message": "invalid Post"}
            self.wfile.write(json.dumps(message).encode(encoding='utf_8'))

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8080):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Welcome to http over UEFI, default is 8080")
    print(f"Starting httpd server on port {port}")
    print(f"Please note https IS NOT SUPPORTED, and connect with http://xxx.xxx.xxx.xxx:{port}")
    httpd.serve_forever()

if __name__ == "__main__":
    import json

    run()
