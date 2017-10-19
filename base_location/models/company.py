# -*- coding: utf-8 -*-
# Copyright 2016 Nicolas Bessi, Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class ResCompany(models.Model):
    _inherit = 'res.company'

    city_id = fields.Many2one(
        'res.city',
        compute='_compute_address',
        inverse='_inverse_city_id',
        string="City"
    )

    zip_id = fields.Many2one(
        'res.better.zip',
        string='ZIP Location',
        compute='_compute_address',
        inverse='_inverse_zip_id',
        help='Use the city name or the zip code to search the location',
    )

    def _get_company_address_fields(self, partner):
        res = super(ResCompany, self)._get_company_address_fields(partner)
        res['city_id'] = partner.city_id
        res['zip_id'] = partner.zip_id
        return res

    def _inverse_city_id(self):
        for company in self:
            company.partner_id.city_id = company.city_id

    def _inverse_zip_id(self):
        for company in self:
            company.partner_id.zip_id = company.zip_id

    @api.onchange('zip_id')
    def on_change_city(self):
        if self.zip_id:
            self.zip = self.zip_id.name
            self.city_id = self.zip_id.city_id
            self.city = self.zip_id.city
            self.country_id = self.zip_id.country_id
            if self.country_id.enforce_cities:
                self.state_id = self.city_id.state_id
            else:
                self.state_id = self.zip_id.state_id

