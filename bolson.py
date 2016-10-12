# -*- encoding: utf-8 -*-

from openerp.osv import osv, fields
import logging

class bolson_bolson(osv.osv):
    _name = 'bolson.bolson'
    _description = 'Bolson de facturas y cheques'

    def conciliar(self, cr, uid, ids, context={}):

        for obj in self.browse(cr, uid, ids, context):

            lineas = []

            total = 0
            for f in obj.facturas:
                for l in f.move_id.line_ids:
                    if l.account_id.reconcile:
                        if not l.reconciled:
                            total += l.credit - l.debit
                            lineas.append(l)
                        else:
                            raise osv.except_osv('Error!', 'La factura %s ya esta conciliada' % (f.number))

            for c in obj.cheques:
                for l in c.move_line_ids:
                    if l.account_id.reconcile:
                        if not l.reconciled :
                            total -= l.debit - l.credit
                            lineas.append(l)
                        else:
                            raise osv.except_osv('Error!', 'El cheque %s ya esta conciliado' % (c.number))

            if round(total) != 0 and not obj.cuenta_desajuste:
                raise osv.except_osv('Error!', 'El total de las facturas no es igual al total de los cheques y los extractos')

            pares = []
            nuevas_lineas = []
            for linea in lineas:
                nuevas_lineas.append((0, 0, {
                    'name': linea.name,
                    'debit': linea.credit,
                    'credit': linea.debit,
                    'account_id': linea.account_id.id,
                    'partner_id': linea.partner_id.id,
                    'journal_id': obj.diario.id,
                    'date_maturity': obj.fecha,
                }))

            if total != 0:
                nuevas_lineas.append((0, 0, {
                    'name': 'Diferencial en ' + obj.name,
                    'debit': -1 * total if total < 0 else 0,
                    'credit': total if total > 0 else 0,
                    'account_id': obj.facturas[0].account_id.id,
                    'date_maturity': obj.fecha,
                }))

            move_id = self.pool.get('account.move').create(cr, uid, {
                'line_ids': nuevas_lineas,
                'ref': obj.name,
                'date': obj.fecha,
                'journal_id': obj.diario.id,
            }, context=context);

            move = self.pool.get('account.move').browse(cr, uid, move_id, context=context)
            indice = 0
            invertidas = move.line_ids[::-1]
            for linea in lineas:
                self.pool.get('account.move.line').reconcile(cr, uid, [linea.id, invertidas[indice].id], context=context)
                indice += 1

            self.pool.get('account.move').post(cr, uid, [move_id], context=context)
            self.write(cr, uid, obj.id, {'asiento': move_id})

        return True

    def cancelar(self, cr, uid, ids, context={}):

        for obj in self.browse(cr, uid, ids, context):
            for l in obj.asiento.line_ids:
                if l.reconciled:
                    self.pool.get('account.move.line').remove_move_reconcile(cr, uid, [l.id], context=context)
            self.pool.get('account.move').button_cancel(cr, uid, [obj.asiento.id], context=context)
            self.pool.get('account.move').unlink(cr, uid, [obj.asiento.id], context=context)

        return True

    _columns = {
        'fecha': fields.date('Fecha', required=True),
        'name': fields.char('Descripcion', size=40, required=True),
        'facturas': fields.one2many('account.invoice', 'bolson_id', 'Facturas'),
        'cheques': fields.one2many('account.payment', 'bolson_id', 'Cheques'),
        'company_id': fields.many2one('res.company', 'Company', required=True),
        'diario': fields.many2one('account.journal', 'Diario', required=True),
        'asiento': fields.many2one('account.move', 'Asiento'),
        'cuenta_desajuste': fields.many2one('account.account', 'Cuenta de desajuste'),
    }
    _defaults = {
        'company_id': lambda self,cr,uid,c: self.pool.get('res.company')._company_default_get(cr, uid, 'account.invoice', context=c),
    }
    _order = 'fecha desc'
