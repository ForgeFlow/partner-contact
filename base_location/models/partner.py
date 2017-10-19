# -*- coding: utf-8 -*-
# Copyright 2016 Nicolas Bessi, Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'
    zip_id = fields.Many2one('res.better.zip', 'ZIP Location')

    @api.onchange('city_id')
    def _onchange_city_id(self):
        if not self.zip_id:
            super(ResPartner, self)._onchange_city_id()
        if self.zip_id and self.city_id != self.zip_id.city_id:
            self.zip_id = False
            self.zip = False
            self.city = False
        if self.city_id:
            return {
                'domain': {
                    'zip_id': [('city_id', '=', self.city_id.id)]
                },
            }
        return {'domain': {'zip_id': []}}

    @api.onchange('state_id')
    def _onchange_state_id(self):
        if self.zip_id and self.state_id != self.zip_id.state_id:
            self.zip_id = False
            self.zip = False
            self.city = False
        if self.state_id:
            return {
                'domain': {
                    'zip_id': [('state_id', '=', self.state_id.id)]
                },
            }
        return {'domain': {'zip_id': []}}

    @api.onchange('country_id')
    def _onchange_country_id(self):
        if self.zip_id and self.zip_id.country_id != self.country_id:
            self.zip_id = False
        res = super(ResPartner, self)._onchange_country_id()
        res['domain']['zip_id'] = []
        if self.country_id and self.country_id.enforce_cities:
            res['domain']['zip_id'] = [('country_id', '=', self.country_id.id)]
        return res

    @api.onchange('zip_id')
    def onchange_zip_id(self):
        if self.zip_id:
            self.country_id = self.zip_id.country_id
            self.state_id = False
            if self.country_id.enforce_cities:
                self.city_id = self.zip_id.city_id
            self.zip = self.zip_id.name
            self.state_id = self.zip_id.state_id
            self.city = self.zip_id.city
