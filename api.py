import sys
from flask import Flask, request
from flask.ext.restful import reqparse, abort, Api, Resource
from grab import Grab

app = Flask(__name__)
api = Api(app)

SITES = {
    1: {'url': 'http://ya.ru'},
}

CONDITIONS = {
    1: "Exists",
    2: "Not exists",
    3: "Has value",
    4: "Hasn't value",
    5: "Contains",
    6: "Doesn't contains",
}

PARAMETERS = [
    {
        'id' : 1,
        'name' : 'favicon',
        'conditions' : [1,2],
        'tag' : 'link',
        'attr' : { 
            'rel' : ['shortcut icon', 'icon'], #shortcut icon in ico, icon in gif\png
            'type' : ['image/png', 'image/gif', 'image/ico', 'image/x-icon', 'image/vnd.microsoft.icon'],
            'href' : 

        }
    },
    {
        'id' : 2,
        'name' : 'meta-keywords',
        'conditions' : [1,2,3,4,5,6],  
    },
    {
        'id' : 3,
        'name' : 'meta-description',
        'conditions' : [1,2,3,4,5,6],
    },
    {
        'id' : 4,
        'name' : 'meta-copyright',
        'conditions' : [1,2,3,4,5,6],
    },
    {
        'id' : 5,
        'name' : 'meta-author',
        'conditions' : [1,2,3,4,5,6],
    },
    {
        'id' : 6,
        'name' : 'meta-robots',
        'conditions' : [1,2,3,4,5,6],
        'available' : ['follow', 'unfollow', 'index', 'noindex'],
    },
    {
        'id' : 7,
        'name' : 'title',
        'conditions' : [1,2,3,4,5,6],
    },
    {
        'id' : 8,
        'name' : 'rel-author',
        'conditions' : [1,2,3,4,5,6],
    },
    {
        'id' : 9,
        'name' : 'rel-publisher',
        'conditions' : [1,2,3,4,5,6],
    },
    {
        'id' : 10,
        'name' : 'og-title',
        'conditions' : [1,2,3,4,5,6],
    },
    {
        'id' : 11,
        'name' : 'og-type',
        'conditions' : [1,2,3,4,5,6],
    },
    {
        'id' : 12,
        'name' : 'og-image',
        'conditions' : [1,2,3,4,5,6],
    },
    {
        'id' : 14,
        'name' : 'og-url',
        'conditions' : [1,2,3,4,5,6],
    },
    {
        'id' : 15,
        'name' : 'og-description',
        'conditions' : [1,2,3,4,5,6],
    },
    {
        'id' : 16,
        'name' : 'twitter-card',
        'conditions' : [1,2,3,4,5,6],
    },
    {
        'id' : 17,
        'name' : 'twitter-url',
        'conditions' : [1,2,3,4,5,6],
    },
    {
        'id' : 18,
        'name' : 'twitter-title',
        'conditions' : [1,2,3,4,5,6],
    },
    {
        'id' : 19,
        'name' : 'twitter-description',
        'conditions' : [1,2,3,4,5,6],
    },
    {
        'id' : 20,
        'name' : 'twitter-image',
        'conditions' : [1,2,3,4,5,6],
    },
    {
        'id' : 21,
        'name' : 'html-lang',
        'conditions' : [1,2,3,4,5,6],
    },
    {
        'id' : 22,
        'name' : 'meta-google',
        'conditions' : [1,2,3,4,5,6],
        'available' : ['notranslate'],
    },
]

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