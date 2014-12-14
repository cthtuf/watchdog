import sys
from flask import Flask, request
from flask.ext.restful import reqparse, abort, Api, Resource
from grab import Grab

app = Flask(__name__)
api = Api(app)

SITES = {
    1: {'url': 'http://ya.ru'},
}

parser = reqparse.RequestParser() #should be global

def abort_if_site_doesnt_exist(site_id):
    if site_id not in SITES:
        abort(404, message="Site {} doesn't exist".format(site_id))

class SitesList(Resource):
    def get(self):
        '''
        Get list of sites
        '''
        return SITES

    def post(self):
        '''
        Create site record
        '''
        parser.add_argument('url', type=str, required=True, 
            help='URL cannot be blank')
        args = parser.parse_args()
        site_id = len(SITES) + 1
        SITES[site_id] = {'url': args['url']}
        return site_id, 201

class Site(Resource):
    def get(self, site_id):
        '''
        Get site info
        '''
        abort_if_site_doesnt_exist(site_id)
        return SITES[site_id]

    def delete(self, site_id):
        '''
        Delete site
        '''
        abort_if_site_doesnt_exist(site_id)
        try:
            del SITES[site_id]
            return '', 204
        except Exception, e:
            print "Unexpected error:", sys.exc_info()[0]
            return '', 500

    def put(self, site_id):
        '''
        Change site info

        At this moment supports only change url
        '''
        parser.add_argument('url', type=str, required=True, 
            help='URL cannot be blank')
        args = parser.parse_args()
        try:
            SITES[site_id]['url'] = args['url']
            return '', 204
        except Exception, e:
            print "Unexpected error:", sys.exc_info()[0]
            return '', 500

class SiteCheck(Resource):
    def get(self, site_id):
        abort_if_site_doesnt_exist(site_id)
        try:
            g = Grab()
            g.go(SITES[site_id]['url'])
            return g.doc.select('//title').text()
        except Exception, e:
            print "Unexpected error:", sys.exc_info()[0]
            return '', 500

class SiteRules(Resource):
    def get(self, site_id):
        abort_if_site_doesnt_exist(site_id)
        try:
            if 'rules' in SITES[site_id].keys():
                return SITES[site_id]['rules']
            else:
                return {}
        except Exception, e:
            print "Unexpected error:", sys.exc_info()[0]
            return {}, 500        

    def post(self, site_id):
        abort_if_site_doesnt_exist(site_id)
        try:
            if not 'rules' in SITES[site_id]:
                SITES[site_id]['rules'] = {}
            for (k, v) in request.form.iteritems():
                SITES[site_id]['rules'][k] = v.encode('ascii', 'ignore')
            return SITES[site_id]['rules'], 201
        except Exception, e:
            print "Unexpected error:", sys.exc_info()[0]
            return '', 500

    def put(self, site_id):
        abort_if_site_doesnt_exist(site_id)
        try:
            for (k, v) in request.form.iteritems():
                SITES[site_id]['rules'][k] = v.encode('ascii', 'ignore')
            return SITES[site_id]['rules'], 201
        except Exception, e:
            print "Unexpected error:", sys.exc_info()[0]
            return '', 500                            

class SiteRule(Resource):
    def get(self, site_id, rule):
        abort_if_site_doesnt_exist(site_id)
        return SITES[site_id]['rules'][rule], 200

    def delete(self, site_id, rule):
        abort_if_site_doesnt_exist(site_id)
        try:
            del SITES[site_id]['rules'][rule]
            return '', 204
        except Exception, e:
            print "Unexpected error:", sys.exc_info()[0]
            return '', 500            

    
api.add_resource(SitesList, '/sites/')
api.add_resource(Site, '/site/<int:site_id>/')
api.add_resource(SiteRules, '/site/<int:site_id>/rules/')
api.add_resource(SiteRule, '/site/<int:site_id>/rule/<string:rule>/')
api.add_resource(SiteCheck, '/site/<int:site_id>/check/')


if __name__ == '__main__':
    app.run(debug=True)