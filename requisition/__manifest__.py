{
    'name': 'Purchase Requisiton',
    'description': 'Requisiton For Purchase Order',
    'author': 'Mehedi Hasan',
    'depends': ['base', 'purchase'],
    'application': True,
    'data': [
        'security/requisition_security.xml',
        'security/ir.model.access.csv',
        'views/purchase_with_requisition.xml',
        'views/requisition_view.xml',
        'views/requisition_menu.xml'
    ],
}
