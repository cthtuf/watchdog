from flask import Flask, request
from flask.ext.restful import reqparse, abort, Api, Resource
from grab import Grab

app = Flask(__name__)
api = Api(app)

SITES = {
    '1': {'url': 'http://ya.ru'},
    '2': {'url': 'http://google.com'},
    '3': {'url': 'http://cthtuf.name'},
}


def abort_if_site_doesnt_exist(site_id):
    if site_id not in SITES:
        abort(404, message="Site {} doesn't exist".format(site_id))

parser = reqparse.RequestParser()
parser.add_argument('url', type=str)


# Todo
#   show a single todo item and lets you delete them
class Site(Resource):
    def get(self, site_id):
        abort_if_site_doesnt_exist(site_id)
        return SITES[site_id]

    def delete(self, site_id):
        abort_if_site_doesnt_exist(site_id)
        del SITES[site_id]
        return '', 204

    def put(self, site_id):
        args = parser.parse_args()
        site = {'url': args['url']}
        SITES[site_id] = site
        return site, 201


# TodoList
#   shows a list of all todos, and lets you POST to add new tasks
class SitesList(Resource):
    def get(self):
        return SITES

    def post(self):
        args = parser.parse_args()
        site_id = '%d' % (len(SITES) + 1)
        SITES[site_id] = {'url': args['url']}
        return SITES[site_id], 201

class SiteCheck(Resource):
    def get(self, site_id):
        abort_if_site_doesnt_exist(site_id)
        g = Grab()
        g.go(SITES[site_id]['url'])
        return g.doc.select('//title').text()

class SiteRules(Resource):
    def get(self, site_id):
        abort_if_site_doesnt_exist(site_id)
        try:
            return SITES[site_id]['rules']
        except Exception, e:
            return {}        

    def post(self, site_id):
        abort_if_site_doesnt_exist(site_id)
        SITES[site_id]['rules']=request.form
        return '', 201

class SiteRule(Resource):
    def get():
        pass

    def delete():
        pass

    def put():
        pass
##
## Actually setup the Api resource routing here
##
api.add_resource(SitesList, '/sites/')
api.add_resource(Site, '/site/<string:site_id>')
api.add_resource(SiteRules, '/site/<string:site_id>/rules/')
api.add_resource(SiteRule, '/site/<string:site_id>/rule/<string:rule_id>')
api.add_resource(SiteCheck, '/site/<string:site_id>/check/')


if __name__ == '__main__':
    app.run(debug=True)