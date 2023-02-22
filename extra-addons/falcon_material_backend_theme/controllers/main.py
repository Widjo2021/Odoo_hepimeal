# -*- coding: utf-8 -*-
# Part of AppJetty. See LICENSE file for full copyright and licensing details.

import re
import base64
import datetime
import logging
import functools
import werkzeug

import odoo
from odoo import http
from odoo.http import request
from odoo import http as http1
from odoo.modules import get_resource_path
from odoo.addons.web.controllers.main import Home
import io
# from cStringIO import StringIO

class LoginWebsiteBackground(Home):

    @http.route()
    def web_login(self, redirect=None, **kw):

        request.params['LoginBackground'] = True
        return super(LoginWebsiteBackground, self).web_login(redirect=redirect, **kw)

class Backend(odoo.addons.web.controllers.main.Home):
    # ------------------------------------------------------
    # View
    # ------------------------------------------------------

    @http.route('/backend/customize_template_get', type='json', auth='user', website=True)
    def backend_customize_template_get(self, key, full=False, bundles=False):
        """ Get inherit view's informations of the template ``key``. By default, only
        returns ``customize_show`` templates (which can be active or not), if
        ``full=True`` returns inherit view's informations of the template ``key``.
        ``bundles=True`` returns also the asset bundles
        """
        return request.env["ir.ui.view"].customize_template_get(key, full=full, bundles=bundles)

    def get_view_ids(self, xml_ids):
        ids = []
        View = request.env["ir.ui.view"].with_context(active_test=False)
        for xml_id in xml_ids:
            if "." in xml_id:
                xml = xml_id.split(".")
                view_model = request.env.ref(xml_id).id
            else:
                view_model = int(xml_id)
            ids.append(view_model)
        return ids

    @http.route(['/backend/theme_customize_get'], type='json', auth="public", website=True)
    def backend_theme_customize_get(self, xml_ids):
        enable = []
        disable = []
        ids = self.get_view_ids(xml_ids)
        for view in request.env['ir.ui.view'].with_context(active_test=True).sudo().browse(ids):
            if view.active:
                enable.append(view.key)
            else:
                disable.append(view.key)
        return [enable, disable]

    @http.route(['/backend/theme_customize'], type='json', auth="public", website=True)
    def backend_theme_customize(self, enable, disable, get_bundle=False):
        """ enable or Disable lists of ``xml_id`` of the inherit templates
        """
        def set_active(ids, active):
            if ids:
                real_ids = self.get_view_ids(ids)
                request.env['ir.ui.view'].with_context(
                    active_test=True).sudo().browse(real_ids).write({'active': active})
        set_active(disable, False)
        set_active(enable, True)

        if get_bundle:
            context = dict(request.context, active_test=True)
            return {'web.assets_backend':request.env["ir.qweb"]._get_asset_link_urls('web.assets_backend', options=context)}
        return True

    @http.route(['/backend/theme_customize_reload'], type='http', auth="public", website=True)
    def backend_theme_customize_reload(self, href, enable, disable):
        self.backend_theme_customize(enable and enable.split(
            ",") or [], disable and disable.split(",") or [])
        redirect_path = href + \
            ("&theme=true" if "#" in href else "#theme=true")
        return werkzeug.utils.redirect(str(redirect_path))

    @http.route(['/website/multi_render'], type='json', auth="public", website=True)
    def multi_render(self, ids_or_xml_ids, values=None):
        View = request.env['ir.ui.view']
        res = {}
        for id_or_xml_id in ids_or_xml_ids:
            res[id_or_xml_id] = View.render_template(id_or_xml_id, values)
        return res

    @http.route(['/web/binary/login_img'], type='http', auth="public", website=True)
    def login_img(self):
        imgname = 'logo'
        imgext = '.png'
        placeholder = functools.partial(
            get_resource_path, 'web', 'static', 'src', 'img')
        login_img = request.env["ir.config_parameter"].sudo(
        ).get_param("login_img", default=None)
        if not login_img:
            response = http1.send_file(placeholder(imgname + imgext))
            return response

        image_base64 = base64.b64decode(login_img)
        image_data = io.BytesIO(image_base64)

        response = http1.send_file(image_data, filename='logo', mtime=False)
        return response

    @http.route(['/get_apps/menu'], type="json", auth="public", website=True)
    def get_apps_menus(self):
        menu_data = request.env['ir.ui.menu'].load_menus(request.session.debug)
        vals = {'menu_data': menu_data}
        return request.env['ir.ui.view'].render_template('falcon_material_backend_theme.menu_apps', vals)
