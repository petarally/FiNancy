from datetime import datetime
import matplotlib
import matplotlib.pyplot as plt
from sqlalchemy import func
from io import BytesIO
import base64
from models import db, Payment
from decimal import Decimal

matplotlib.use('Agg') 

def generate_graph(chart_type, x_labels, y_data, title, x_title):
    if chart_type == 'bar':
        plt.bar(x_labels, y_data)
    elif chart_type == 'pie':
        plt.pie(y_data, labels=x_labels, autopct='%1.1f%%')
    plt.xlabel(x_title)
    plt.ylabel('troškovi')
    plt.title(title)
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return image_base64

def generiraj_graf_prema_mjesecima(chart_type):
    results = db.session.query(func.strftime('%m', Payment.date).label('month'),
                               func.sum(Payment.amount).label('total_amount')).\
        group_by(func.strftime('%m', Payment.date)).all()
    labels = [datetime.strptime(r.month, '%m').strftime('%B') for r in results]
    data = [r.total_amount for r in results]
    title = 'Mjesečni prikaz troškova'
    return generate_graph(chart_type, labels, data, title, 'mjeseci')

def generiraj_graf_prema_godinama(chart_type):
    results = db.session.query(func.strftime('%Y', Payment.date).label('year'),
                               func.sum(Payment.amount).label('total_amount')).\
        group_by(func.strftime('%Y', Payment.date)).all()
    labels = [r.year for r in results]
    data = [r.total_amount for r in results]
    title = 'Godišnji prikaz troškova'
    return generate_graph(chart_type, labels, data, title, 'godine')

def generiraj_graf_ukupan_prema_firmama(chart_type):
    results = db.session.query(Payment.company_name, func.sum(Payment.amount).label('total_amount')).\
        group_by(Payment.company_name).all()
    labels = [r.company_name for r in results]
    data = [r.total_amount for r in results]
    title = 'Prikaz troškova prema firmama'
    return generate_graph(chart_type, labels, data, title, 'firme')

def izvedi_statistiku(tvrtka):
    rezultati = {}
    ukupan_iznos = db.session.query(func.sum(Payment.amount)).filter(Payment.company_name == tvrtka).scalar()
    rezultati['ukupan_iznos'] = round(ukupan_iznos, 2) if ukupan_iznos else 0
    prosjecan_iznos = db.session.query(func.avg(Payment.amount)).filter(Payment.company_name == tvrtka).scalar()
    rezultati['prosjecan_iznos'] = round(prosjecan_iznos, 2) if prosjecan_iznos else 0
    minimalni_iznos = db.session.query(func.min(Payment.amount)).filter(Payment.company_name == tvrtka).scalar()
    rezultati['minimalni_iznos'] = round(minimalni_iznos, 2) if minimalni_iznos else 0
    maksimalni_iznos = db.session.query(func.max(Payment.amount)).filter(Payment.company_name == tvrtka).scalar()
    rezultati['maksimalni_iznos'] = round(maksimalni_iznos, 2) if maksimalni_iznos else 0
    return rezultati

def graf_promjene(tvrtka):
    results = db.session.query(func.strftime('%m', Payment.date).label('month'),
                               func.sum(Payment.amount).label('total_amount')).\
        filter(Payment.company_name == tvrtka).\
        group_by(func.strftime('%m', Payment.date)).all()
    months = [int(r.month) for r in results]
    data = [r.total_amount for r in results]
    price_diff = [0] + [data[i] - data[i-1] for i in range(1, len(data))]
    month_labels = [datetime.strptime(str(m), '%m').strftime('%B') for m in months]
    chart_type = 'bar'
    x_labels = month_labels
    y_data = price_diff
    title = f'Kretanje mjesečnih troškova prema: {tvrtka}'
    fig, ax = plt.subplots()
    ax.bar(x_labels, y_data, color='blue')
    max_abs_value = max(max(y_data), abs(min(y_data)))
    ax.axhline(0, color='black', linewidth=0.8)
    ax.set_ylim(-max_abs_value * Decimal('1.1'), max_abs_value * Decimal('1.1'))
    for i, v in enumerate(y_data):
        ax.text(i, v, f'{v}', ha='center', va='bottom')
    return generate_graph(chart_type, x_labels, y_data, title, 'promjene')

def dohvati_plative_zapise(iznos):
    platiti = []
    unpaid_payments = Payment.query.filter_by(payment_number=0).all()
    for payment in unpaid_payments:
        if payment.amount <= iznos:
            platiti.append(payment)
    return platiti