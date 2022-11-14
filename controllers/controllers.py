# -*- coding: utf-8 -*-
# from odoo import http


# class Pirates(http.Controller):
#     @http.route('/pirates/pirates', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pirates/pirates/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('pirates.listing', {
#             'root': '/pirates/pirates',
#             'objects': http.request.env['pirates.pirates'].search([]),
#         })

#     @http.route('/pirates/pirates/objects/<model("pirates.pirates"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pirates.object', {
#             'object': obj
#         })
