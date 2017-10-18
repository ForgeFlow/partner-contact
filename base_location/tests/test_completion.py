# -*- coding: utf-8 -*-
# Copyright 2015 Yannick Vaucher, Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestCompletion(TransactionCase):

    def test_onchange_better_zip_state_id(self):
        """ Test onchange on res.better.zip """
        usa_MA = self.env.ref('base.state_us_34')
        self.better_zip1.state_id = usa_MA
        self.better_zip1._onchange_state_id()
        self.assertEqual(self.better_zip1.country_id, usa_MA.country_id)

    def test_onchange_better_zip_city_id(self):
        self.better_zip2.city_id = self.city_madrid
        self.better_zip2._onchange_city_id()
        self.assertEqual(self.better_zip2.city, self.city_madrid.name)

    def test_onchange_better_zip_country_id(self):
        self.better_zip1.country_id = self.env.ref('base.es')
        self.better_zip1._onchange_country_id()
        self.assertFalse(self.better_zip1.state_id)

    def test_onchange_partner_city_completion(self):
        self.partner1.zip_id = self.better_zip1
        self.partner1.onchange_zip_id()
        self.assertEqual(self.partner1.zip, self.better_zip1.name)
        self.assertEqual(self.partner1.city, self.better_zip1.city)
        self.assertEqual(self.partner1.state_id, self.better_zip1.state_id)
        self.assertEqual(self.partner1.country_id, self.better_zip1.country_id)

    def test_onchange_company_city_completion(self):
        self.company.better_zip_id = self.better_zip1
        self.company.on_change_city()
        self.assertEqual(self.company.zip, self.better_zip1.name)
        self.assertEqual(self.company.city, self.better_zip1.city)
        self.assertEqual(self.company.state_id, self.better_zip1.state_id)
        self.assertEqual(self.company.country_id, self.better_zip1.country_id)

    def test_onchange_company_city_id_completion(self):
        self.company.better_zip_id = self.better_zip2
        self.company.on_change_city()
        self.assertEqual(self.company.zip, self.better_zip2.name)
        self.assertEqual(self.company.city, self.better_zip2.city)
        self.assertEqual(self.company.state_id, self.better_zip2.state_id)
        self.assertEqual(self.company.country_id, self.better_zip2.country_id)

    def setUp(self):
        super(TestCompletion, self).setUp()
        state_vd = self.env['res.country.state'].create({
            'name': 'Vaud',
            'code': 'VD',
            'country_id': self.ref('base.ch'),
        })
        self.env['res.country'].browse(self.ref('base.es')).write({
            'enforce_cities': True
        })
        self.company = self.env.ref('base.main_company')
        self.better_zip1 = self.env['res.better.zip'].create({
            'name': 1000,
            'city': 'Lausanne',
            'state_id': state_vd.id,
            'country_id': self.ref('base.ch'),
        })
        self.partner1 = self.env['res.partner'].create({
            'name': 'Camptocamp',
        })
        self.state_bcn = self.env['res.country.state'].create({
            'name': 'Barcelona',
            'code': '08',
            'country_id': self.ref('base.es'),
        })
        self.state_madrid = self.env['res.country.state'].create({
            'name': 'Madrid',
            'code': '28',
            'country_id': self.ref('base.es'),
        })
        self.city_bcn = self.env['res.city'].create({
            'name': 'Barcelona',
            'state_id': self.state_bcn.id,
            'country_id': self.ref('base.es'),
        })
        self.city_madrid = self.env['res.city'].create({
            'name': 'Madrid',
            'state_id': self.state_madrid.id,
            'country_id': self.ref('base.es'),
        })
        self.better_zip2 = self.env['res.better.zip'].create({
            'city_id': self.city_bcn.id,
            'city': self.city_bcn.name,
            'state_id': self.state_bcn.id,
            'country_id': self.ref('base.es'),
        })
