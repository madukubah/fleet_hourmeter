 # -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class FleetVehicle(models.Model):
	_inherit = 'fleet.vehicle'
	hourmeter_count = fields.Integer(compute="_compute_count_all", string='Hourmeter')

	@api.multi
	def hourmeter_return_action_to_open(self):
		""" This opens the xml view specified in xml_id for the current vehicle """
		self.ensure_one()
		xml_id = self.env.context.get('xml_id')
		if xml_id:
			res = self.env['ir.actions.act_window'].for_xml_id('fleet_hourmeter', xml_id)
			res.update(
				context=dict(self.env.context, default_vehicle_id=self.id, group_by=False),
				domain=[('vehicle_id', '=', self.id)]
			)
			return res
		return False
	
	@api.multi
	def _compute_count_all(self):
		super(FleetVehicle, self )._compute_count_all()
		VehicleHourmeter = self.env['fleet.vehicle.hourmeter']
		for record in self:
			hourmeters = VehicleHourmeter.search([('vehicle_id', '=', record.id)])
			record.hourmeter_count = sum([ hourmeter.value for hourmeter in hourmeters ])

class FleetVehicleHourmeter(models.Model):
	_name = "fleet.vehicle.hourmeter"

	name = fields.Char(compute='_compute_vehicle_log_name', store=True)
	date = fields.Date(default=fields.Date.context_today)
	start = fields.Float('Start Hour')
	end = fields.Float('End Hour')
	value = fields.Float('Hourmeter Value', group_operator="max", compute="_compute_value" )
	vehicle_id = fields.Many2one('fleet.vehicle', 'Vehicle', required=True)

	@api.depends('vehicle_id', 'date')
	def _compute_vehicle_log_name(self):
		for record in self:
			name = record.vehicle_id.name
			if not name:
				name = record.date
			elif record.date:
				name += ' / ' + record.date
			self.name = name

	@api.depends('start', 'end')
	def _compute_value(self):
		for record in self:
			record.value = record.end - record.start