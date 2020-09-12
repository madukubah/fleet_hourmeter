 # -*- coding: utf-8 -*-
from odoo import api, fields, models, _

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