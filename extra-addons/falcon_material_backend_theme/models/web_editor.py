
import base64
import os
import re
import uuid

from lxml import etree
from odoo import fields,models,api 


class WebEditor(models.AbstractModel):
    _inherit='web_editor.assets'

    def backend_save_asset(self, url, bundle_xmlid, content, file_type):
        custom_url = self.make_custom_asset_file_url(url, bundle_xmlid)
        datas = base64.b64encode((content or "\n").encode("utf-8"))
        custom_attachment = self._get_custom_attachment(custom_url)
        if custom_attachment:
            custom_attachment.write({"datas": datas})
        else:
            new_attach = {
                'name': url.split("/")[-1],
                'type': "binary",
                'mimetype': (file_type == 'js' and 'text/javascript' or 'text/scss'),
                'datas': datas,
                'url': custom_url,
            }
            new_attach.update(self._save_asset_attachment_hook())
            self.env["ir.attachment"].create(new_attach)
            file_type_info = {
                'tag': 'link' if file_type == 'scss' else 'script',
                'attribute': 'href' if file_type == 'scss' else 'src',
            }

            def views_linking_url(view):
                tree = etree.XML(view.arch)
                return bool(tree.xpath("//%%(tag)s[@%%(attribute)s='%(url)s']" % {
                    'url': url,
                } % file_type_info))

            IrUiView = self.env["ir.ui.view"]
            view_to_xpath = IrUiView.get_related_views(bundle_xmlid, bundles=True).filtered(views_linking_url)
                
            new_view = {
                'name': custom_url,
                'key': 'web_editor.%s_%s' % (file_type, str(uuid.uuid4())[:6]),
                'mode': "extension",
                'inherit_id': view_to_xpath.id,
                'arch': """
                    <data inherit_id="%(inherit_xml_id)s" name="%(name)s">
                        <xpath expr="//%%(tag)s[@%%(attribute)s='%(url_to_replace)s']" position="attributes">
                            <attribute name="%%(attribute)s">%(new_url)s</attribute>
                        </xpath>
                    </data>
                """ % {
                    'inherit_xml_id': view_to_xpath.xml_id,
                    'name': custom_url,
                    'url_to_replace': url,
                    'new_url': custom_url,
                } % file_type_info
            }
            if(self.env['ir.module.module'].sudo().search([('name', '=', 'website'),('state','=','installed')])):
                clr_attachment=IrUiView.create(new_view)
                clr_attachment.website_id=False
            else:
                clr_attachment=IrUiView.create(new_view)

            new_view.update(self._save_asset_view_hook())

        self.env["ir.qweb"].clear_caches()