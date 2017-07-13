# -*- encoding: utf-8 -*-

from openerp.osv import osv, fields
import openerp.addons.decimal_precision as dp

class account_invoice(osv.osv):
    _inherit = 'account.invoice'

    _columns = {
        'bolson_id': fields.many2one('bolson.bolson', 'Liquidacion'),
    }

    def onchange_bolson(self, cr, uid, ids, bolson_id, context=None):
        val = {}
        if not bolson_id:
            return {'value': val}

        bolson = self.pool.get('bolson.bolson').browse(cr, uid, bolson_id, context=context)
        if bolson.diario.type == 'purchase':
            val = {'journal_id': bolson.diario.id}
            
        return {'value': val}
