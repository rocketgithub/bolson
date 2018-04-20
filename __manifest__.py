# -*- encoding: utf-8 -*-

{
    'name' : 'Bolson',
    'version' : '1.0',
    'category': 'Custom',
    'description': """Manejo de cajas chicas y liquidaciones""",
    'author': 'Rodrigo Fernandez',
    'website': 'http://solucionesprisma.com/',
    'depends' : [ 'l10n_gt_extra' ],
    'data' : [
        'views/report.xml',
        'views/bolson_view.xml',
        'views/invoice_view.xml',
        'views/payment_view.xml',
        'views/reporte_bolson.xml',
        'security/ir.model.access.csv',
        'security/bolson_security.xml',
    ],
    'installable': True,
    'certificate': '',
}
