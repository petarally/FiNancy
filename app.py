from flask import Flask, request, render_template, redirect, url_for
from sqlalchemy import func
from datetime import datetime
from decimal import Decimal
from models import db, Payment
import base64
from utils import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///payments.sqlite3'
app.config['SECRET_KEY'] = 'random string'

db.init_app(app)

@app.route('/')
def index():
    payments = Payment.query.all()
    total_amount = db.session.query(func.sum(Payment.amount)).filter(Payment.payment_number != 0).scalar() or 0
    total_amount_to_pay = db.session.query(func.sum(Payment.amount)).filter(Payment.payment_number == 0).scalar() or 0
    return render_template('index.html', payments=payments, formatted_date=Payment.formatted_date, total_amount=total_amount, total_amount_to_pay=total_amount_to_pay)

@app.route('/grafovi', methods=['GET', 'POST'])
def grafovi():
    if request.method == 'POST':
        graph_type = request.form['graph_type']
        chart_type = request.form['chart_type']
        if graph_type == 'month':
            month_graph = generiraj_graf_prema_mjesecima(chart_type)
            return render_template('grafovi.html', graph_type=graph_type, chart_type=chart_type, month_graph=month_graph)
        elif graph_type == 'year':
            year_graph = generiraj_graf_prema_godinama(chart_type) 
            return render_template('grafovi.html', graph_type=graph_type, chart_type=chart_type, year_graph=year_graph)
        elif graph_type == 'total':
            total_graph = generiraj_graf_ukupan_prema_firmama(chart_type) 
            return render_template('grafovi.html', graph_type=graph_type, chart_type=chart_type, total_graph=total_graph)
    return render_template('grafovi.html')

@app.route('/statistika', methods=['GET', 'POST'])
def statistika():
    tvrtke = Payment.query.with_entities(Payment.company_name).distinct().all()
    if request.method == 'POST':
        odabrana_tvrtka = request.form['tvrtka']
        rezultati = izvedi_statistiku(odabrana_tvrtka)
        graf_mjesecni = graf_promjene(odabrana_tvrtka)
        return render_template('statistika.html', tvrtke=tvrtke, odabrana_tvrtka=odabrana_tvrtka, rezultati=rezultati, graf_mjesecni=graf_mjesecni)
    return render_template('statistika.html', tvrtke=tvrtke)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        company_name = request.form['company_name']
        amount = Decimal(request.form['amount'])
        payment_number = request.form['payment_number']
        manual_date = request.form.get('manual_date_checkbox') is not None
        if manual_date:
            date = datetime.now()
        else:
            date_str = request.form.get('date', '')
            date = datetime.strptime(date_str, '%d.%m.%Y') if date_str else None
        payment = Payment(company_name=company_name, amount=amount, payment_number=payment_number, manual_date=manual_date, date=date)
        db.session.add(payment)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:payment_id>', methods=['GET', 'POST'])
def edit(payment_id):
    payment = Payment.query.get(payment_id)
    if request.method == 'POST':
        original_date = payment.date
        payment.company_name = request.form['company_name']
        payment.amount = Decimal(request.form['amount'])
        payment.payment_number = request.form['payment_number']
        date_str = request.form.get('date', '')
        date = datetime.now() if not date_str else datetime.strptime(date_str, '%d.%m.%Y %H:%M')
        if date != original_date:  
            payment.edit_date = datetime.now()  
        else:
            payment.edit_date = None  
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', payment=payment)

@app.route('/delete/<int:payment_id>', methods=['POST'])
def delete(payment_id):
    payment = Payment.query.get(payment_id)
    db.session.delete(payment)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_query = request.form['search_query']
        payments = Payment.query.filter(Payment.company_name.like(f'%{search_query}%') | Payment.payment_number.like(f'%{search_query}%')).all()
        return render_template('search.html', payments=payments, search_query=search_query)
    return render_template('search.html')

@app.route('/kalkulator', methods=['GET', 'POST'])
def kalkulator():
    if request.method == 'POST':
        uplata_iznos = Decimal(request.form['uplata_iznos'])
        unpaid_payments = Payment.query.filter_by(payment_number=0).all()
        unpaid_payments.sort(key=lambda payment: payment.amount)
        platiti = []
        preostali_iznos = uplata_iznos
        for payment in unpaid_payments:
            if preostali_iznos >= payment.amount:
                platiti.append(payment)
                preostali_iznos -= Decimal(payment.amount)
                uplata_broj = request.form.get('uplataBroj' + str(payment.id))
                if uplata_broj:
                    payment.payment_number = uplata_broj
                    db.session.commit()
        unpaid_payments = Payment.query.filter_by(payment_number=0).all()
        unpaid_payments.sort(key=lambda payment: payment.amount)
        ukupan_iznos = sum(payment.amount for payment in unpaid_payments)
        return render_template('kalkulator.html', unpaid_payments=unpaid_payments, platiti=platiti, uplata_iznos=uplata_iznos, total_amount_to_pay=ukupan_iznos, preostali_iznos=preostali_iznos)
    unpaid_payments = Payment.query.filter_by(payment_number=0).all()
    ukupan_iznos = sum(payment.amount for payment in unpaid_payments)
    return render_template('kalkulator.html', unpaid_payments=unpaid_payments, total_amount_to_pay=ukupan_iznos)


@app.route('/update_payment_number/<int:payment_id>', methods=['POST'])
def update_payment_number(payment_id):
    payment = Payment.query.get(payment_id)
    uplata_broj = request.form.get('uplataBroj' + str(payment_id))
    if uplata_broj:
        payment.payment_number = uplata_broj
        db.session.commit()
    return redirect(url_for('kalkulator'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=8080)
