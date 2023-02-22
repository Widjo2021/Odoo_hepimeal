{
    'name' : 'Pph 21',
    'author' : 'PrimaVisi GLobalindo',
    'description' : """
        Custome Module PPH 21 Terdiri Dari setting
        1. setting ptkp
        2. setting tunjangan jabatan per karyawan atau global
    """,
    'depends': [
        'hr',
        'hr_contract'
    ],
    'data': [
        'views/ptkp_views.xml',
        'views/inherite_hr_employee_views.xml',
        'views/tarif_pph.xml'
    ],
    'installable': True,
    'application': False,
    'auto_install': False
}
