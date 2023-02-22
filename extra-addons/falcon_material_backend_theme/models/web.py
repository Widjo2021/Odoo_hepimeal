# -*- coding: utf-8 -*-
# Part of AppJetty. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class CustomResConfiguration(models.TransientModel):
    """ Inherit the base settings to add favicon. """
    _inherit = 'res.config.settings'

    is_login_background= fields.Boolean("Do you want to set login page background?")
    is_back_img_color= fields.Selection([
        ('image', 'Image'),
        ('color', 'Color'),
    ], string="Background options",
        help="Background image or color")
    login_img = fields.Binary(
        'Background image',  readonly=False, attachment=True,help="Please set image for background")
    login_color = fields.Char(
        'Background color',  readonly=False,help="Please set Hex color for background")

    @api.model
    def get_values(self):
        # def get_default_alias_domain(self, fields):
        res = super(CustomResConfiguration, self).get_values()
        is_login_background = self.env["ir.config_parameter"].get_param(
            "is_login_background", default=None)
        is_back_img_color =self.env["ir.config_parameter"].get_param(
            "is_back_img_color", default=None)
        login_img =self.env["ir.config_parameter"].get_param(
            "login_img", default=None)
        login_color=self.env["ir.config_parameter"].get_param(
            "login_color", default=None)
        res.update(
            is_login_background=is_login_background or False,
            is_back_img_color=is_back_img_color or False,
            login_img=login_img or False,
            login_color=login_color or False,
        )
        return res

    def set_values(self):
        super(CustomResConfiguration, self).set_values()
        for record in self:
            self.env['ir.config_parameter'].set_param(
                "is_login_background", record.is_login_background or '')
            self.env['ir.config_parameter'].set_param(
                "is_back_img_color", record.is_back_img_color or '')
            self.env['ir.config_parameter'].set_param(
                "login_img", record.login_img or '')
            self.env['ir.config_parameter'].set_param(
                "login_color", record.login_color or '')

