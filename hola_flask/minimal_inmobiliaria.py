"""
Minimal Inmobiliaria (un solo archivo).
- Todo en memoria: edita la lista `APARTMENTS` para cambiar datos.
- Ejecutar: `python minimal_inmobiliaria.py` y abrir http://127.0.0.1:5000
"""
from flask import Flask

app = Flask(__name__)

# Datos inventados (editar directamente aquí)
APARTMENTS = [
    {
        'number': '101',
        'address': 'Cl 10 #5-20',
        'rent': 850.0,
        'status': 'ocupado',
        'owner': {'name': 'Ana Torres', 'id': 'DNI-1001'},
        'tenant': {'name': 'Jorge Díaz', 'id': 'CC-2001'},
        'documents': ['contrato_101.pdf'],
        'contract_number': 'C-5001',
        'financial': {'rent': 850.0, 'incomes': [50.0], 'expenses': [120.0]},
        'damages': [{'date': '2025-03-10', 'desc': 'Grieta en pared del baño', 'cost': 250.0}],
    },
    {
        'number': '102',
        'address': 'Cl 10 #5-22',
        'rent': 1200.0,
        'status': 'disponible',
        'owner': {'name': 'Carlos Rojas', 'id': 'DNI-1002'},
        'tenant': None,
        'documents': ['titulo_102.pdf'],
        'contract_number': None,
        'financial': {'rent': 1200.0, 'incomes': [], 'expenses': [300.0]},
        'damages': [],
    },
    {
        'number': '201',
        'address': 'Cr 3 #10-5',
        'rent': 950.0,
        'status': 'ocupado',
        'owner': {'name': 'María Pérez', 'id': 'DNI-1003'},
        'tenant': {'name': 'Lucía Fernández', 'id': 'CC-2002'},
        'documents': ['contrato_201.pdf', 'inventario_201.xlsx'],
        'contract_number': 'C-5002',
        'financial': {'rent': 950.0, 'incomes': [], 'expenses': []},
        'damages': [],
    },
    {
        'number': '202',
        'address': 'Cr 3 #10-7',
        'rent': 700.0,
        'status': 'disponible',
        'owner': {'name': 'Luis Gómez', 'id': 'DNI-1004'},
        'tenant': None,
        'documents': [],
        'contract_number': None,
        'financial': {'rent': 700.0, 'incomes': [], 'expenses': []},
        'damages': [],
    },
    {
        'number': '301',
        'address': 'Av 5 #2-10',
        'rent': 1500.0,
        'status': 'ocupado',
        'owner': {'name': 'Sofía Martínez', 'id': 'DNI-1005'},
        'tenant': {'name': 'Marcos Ruiz', 'id': 'CC-2003'},
        'documents': ['titulo_301.pdf'],
        'contract_number': 'C-5010',
        'financial': {'rent': 1500.0, 'incomes': [100.0], 'expenses': [50.0]},
        'damages': [{'date': '2025-06-01', 'desc': 'Mancha techo cocina', 'cost': 80.0}],
    },
]


def fmt_money(v):
    return f"${v:,.2f}" if v is not None else "—"


@app.route('/')
def index():
    # Construye HTML simple y editable
    parts = [
        '<!doctype html>',
        '<html lang="es"><head><meta charset="utf-8"><title>Inmobiliaria - Demo</title>'
        '<style>body{font-family:Segoe UI,Arial;margin:20px} .apt{border:1px solid #ccc;padding:10px;margin:10px 0}'
        'h2{margin:0 0 8px 0}</style></head><body>',
        '<h1>Listado de Apartamentos (demo)</h1>',
        '<p>Editar la lista <code>APARTMENTS</code> al inicio del archivo para cambiar datos.</p>',
    ]

    for a in APARTMENTS:
        parts.append('<div class="apt">')
        parts.append(f"<h2>Apto {a['number']} — {a['address']}</h2>")
        parts.append(f"<b>Arriendo:</b> {fmt_money(a['rent'])} &nbsp; <b>Estado:</b> {a['status']}<br>")
        owner = a.get('owner') or {}
        parts.append(f"<b>Dueño:</b> {owner.get('name','—')} (ID: {owner.get('id','—')})<br>")
        tenant = a.get('tenant')
        if tenant:
            parts.append(f"<b>Inquilino:</b> {tenant.get('name')} (ID: {tenant.get('id')})<br>")
        else:
            parts.append(f"<b>Inquilino:</b> —<br>")
        docs = ', '.join(a.get('documents', [])) or '—'
        parts.append(f"<b>Documentos:</b> {docs}<br>")
        parts.append(f"<b>Nº Contrato:</b> {a.get('contract_number') or '—'}<br>")
        # Finanzas
        fin = a.get('financial', {})
        incomes = sum(fin.get('incomes', []))
        expenses = sum(fin.get('expenses', []))
        rent = fin.get('rent', a.get('rent', 0))
        net = rent + incomes - expenses
        parts.append(f"<b>Reporte financiero:</b> Rent {fmt_money(rent)}, Ingresos {fmt_money(incomes)}, Gastos {fmt_money(expenses)}, Neto {fmt_money(net)}<br>")
        # Daños
        damages = a.get('damages', [])
        if damages:
            parts.append('<b>Reporte de daños:</b><ul>')
            for d in damages:
                parts.append(f"<li>{d.get('date')} — {d.get('desc')} (costo: {fmt_money(d.get('cost',0))})</li>")
            parts.append('</ul>')
        else:
            parts.append('<b>Reporte de daños:</b> —')

        parts.append('</div>')

    parts.append('</body></html>')
    return '\n'.join(parts)


if __name__ == '__main__':
    app.run(debug=True)
