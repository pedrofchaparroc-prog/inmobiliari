from flask import Blueprint, render_template, request, jsonify

main = Blueprint('main', __name__)

# Datos muy básicos en memoria: editar aquí si quieres cambiar ejemplos
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


@main.route('/')
def index():
    # Pasa la lista de apartamentos a la plantilla
    return render_template('index.html', apartments=APARTMENTS)


def find_apartment(number):
    for a in APARTMENTS:
        if a.get('number') == number:
            return a
    return None


@main.route('/toggle_status', methods=['POST'])
def toggle_status():
    """Endpoint simple para cambiar el estado (disponible<->ocupado).

    Recibe JSON: {"number": "101"}
    Devuelve JSON: {"status": "ocupado"}
    """
    data = request.get_json(silent=True) or {}
    number = data.get('number')
    if not number:
        return jsonify({'error': 'number required'}), 400
    apt = find_apartment(number)
    if not apt:
        return jsonify({'error': 'not found'}), 404
    apt['status'] = 'ocupado' if apt.get('status') == 'disponible' else 'disponible'
    return jsonify({'status': apt['status']})


@main.route('/apt/<number>')
def apt_detail(number):
    apt = find_apartment(number)
    if not apt:
        return jsonify({'error': 'not found'}), 404
    return jsonify(apt)
