import json

import falcon

from app import extension
from app import models


@falcon.before(extension.before_resource)
@falcon.after(extension.after_resource)
class BookResource(object):

    def on_get(self, req, resp, isbn):
        book = self._match(req, resp, isbn)
        if book:
            print("isbn {0} に対する get だよ~ん".format(isbn))  # 実際の処理は割愛
            resp.body = json.dumps(book)
            resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        pass  # todo: 要実装

    def on_put(self, req, resp, isbn):
        book = self._match(req, resp, isbn)
        if book:
            print(json.loads(req.stream.read().decode('utf-8')))
            print("isbn {0} に対する put だよ~ん".format(isbn))  # 実際の処理は割愛
            resp.status = falcon.HTTP_200

    def on_delete(self, req, resp, isbn):
        book = self._match(req, resp, isbn)
        if book:
            print("isbn {0} に対する delete だよ~ん".format(isbn))  # 実際の処理は割愛
            resp.status = falcon.HTTP_200

    def _match(self, req, resp, isbn):
        if isbn:
            book = models.BookModel().find(isbn)
            if book:
                return book
            else:
                resp.body = "isbn {0} is invalid".format(isbn)
                resp.status = falcon.HTTP_404
                return None
        else:
            resp.body = "isbn is required"
            resp.status = falcon.HTTP_400
            return None


app = falcon.API(middleware=extension.ExtensionComponent())
app.add_route("/books/{isbn}", BookResource())

# if __name__ == "__main__":
#     from wsgiref import simple_server
#
#     httpd = simple_server.make_server("127.0.0.1", 8000, app)
#     httpd.serve_forever()

