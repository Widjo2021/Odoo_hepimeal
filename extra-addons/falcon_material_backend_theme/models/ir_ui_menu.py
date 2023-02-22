# -*- coding: utf-8 -*-
# Part of AppJetty. See LICENSE file for full copyright and licensing details.
import base64
import operator
from odoo.tools.translate import _
from odoo import api, fields, models, tools

MENU_ITEM_SEPARATOR = "/"


class IrView(models.Model):
    _name = "ir.ui.view"
    _inherit = ["ir.ui.view"]
    customize_show = fields.Boolean("Customize Show")
    iswebsite = fields.Boolean("Website Used", default=True)

    def write(self, vals):
        '''COW for ir.ui.view. This way editing websites does not impact other
        websites. Also this way newly created websites will only
        contain the default views.
         '''
        for view in self.with_context(active_test=False):
            if view.key in [ 
                'falcon_material_backend_theme.option_layout_small', 
                'falcon_material_backend_theme.option_font_style_open_sans', 
                'falcon_material_backend_theme.option_font_style_josefin_slab', 
                'falcon_material_backend_theme.option_font_style_vollkorn', 
                'falcon_material_backend_theme.option_font_style_ubuntu', 
                'falcon_material_backend_theme.option_font_style_roboto', 
                'falcon_material_backend_theme.option_font_style_dancing_script', 
                'falcon_material_backend_theme.option_button_style_1', 
                'falcon_material_backend_theme.option_button_style_2', 
                'falcon_material_backend_theme.option_button_style_3', 
                'falcon_material_backend_theme.option_button_style_4', 
                'falcon_material_backend_theme.option_button_style_5', 
                'falcon_material_backend_theme.option_button_style_6',
                'falcon_material_backend_theme.option_mode_style_night',
                'falcon_material_backend_theme.option_separator_style_1',
                'falcon_material_backend_theme.option_separator_style_2',
                'falcon_material_backend_theme.option_separator_style_3',
                'falcon_material_backend_theme.option_separator_style_4',
                'falcon_material_backend_theme.option_separator_style_5',
                'falcon_material_backend_theme.option_separator_style_6',
                'falcon_material_backend_theme.sidebar_nav_hover_style_1',
                'falcon_material_backend_theme.sidebar_nav_hover_style_2',
                'falcon_material_backend_theme.sidebar_nav_hover_style_3',
                'falcon_material_backend_theme.sidebar_nav_hover_style_4',
                'falcon_material_backend_theme.option_font_style_7',
                'falcon_material_backend_theme.option_font_style_8',
                'falcon_material_backend_theme.option_font_style_9',
                'falcon_material_backend_theme.option_font_style_10',
                'falcon_material_backend_theme.option_font_style_11',
                'falcon_material_backend_theme.option_font_style_12'

            ]:
                website_specific_view = view.search([
                    ('key', '=', view.key),
                ], limit=1)
                if website_specific_view:
                    super(IrView, website_specific_view).write(vals)
                    continue

        super(IrView, self).write(vals)

        return True


class IrUiMenu(models.Model):
    _inherit = 'ir.ui.menu'

    menu_icon_type= fields.Selection([('icon','Icon'),('image','Image')],string='Menu Items icon',help='Select icon/image for menu items',default='icon')
    menu_icon_image = fields.Binary(
        'icon image', attachment=True, help="Please set image for menu icon")
    menu_icon_class = fields.Char("Icon Class")
    # customize_show = fields.Boolean("Customize Show")

    @api.model
    @tools.ormcache_context('self._uid', 'debug', keys=('lang',))
    def load_menus(self, debug):
        """ Loads all menu items (all applications and their sub-menus).

        :return: the menu root
        :rtype: dict('children': menu_nodes)
        """
        fields = ['name', 'sequence', 'parent_id', 'action',
                  'web_icon', 'web_icon_data', 'menu_icon_class','menu_icon_type','menu_icon_image']
        menu_root_ids = self.get_user_roots()
        menu_roots = menu_root_ids.read(fields) if menu_root_ids else []
        menu_root = {
            'id': False,
            'name': 'root',
            'parent_id': [-1, ''],
            'children': menu_roots,
            'all_menu_ids': menu_root_ids.ids,
        }
        if not menu_roots:
            return menu_root

        # menus are loaded fully unlike a regular tree view, cause there are a
        # limited number of items (752 when all 6.1 addons are installed)
        menus = self.search([('id', 'child_of', menu_root_ids.ids)])
        menu_items = menus.read(fields)

        # adds roots at the end of the sequence, so that they will overwrite
        # equivalent menu items from full menu read when put into id:item
        # mapping, resulting in children being correctly set on the roots.
        menu_items.extend(menu_roots)
        menu_root['all_menu_ids'] = menus.ids

        # make a tree using parent_id
        menu_items_map = {
            menu_item["id"]: menu_item for menu_item in menu_items}
        for menu_item in menu_items:
            parent = menu_item['parent_id'] and menu_item['parent_id'][0]
            if parent in menu_items_map:
                menu_items_map[parent].setdefault(
                    'children', []).append(menu_item)

        # sort by sequence a tree using parent_id
        for menu_item in menu_items:
            menu_item.setdefault('children', []).sort(
                key=operator.itemgetter('sequence'))

        return menu_root