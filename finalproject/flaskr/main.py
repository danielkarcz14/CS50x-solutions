import os
import re
import plotly.express as px
import plotly.io as py
import pandas as pd
import requests
import random


email_validate_pattern = r"^\S+@\S+\.\S+$"
password_pattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{8,}$"

news_api_key = ""

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify, send_file
)
from werkzeug.exceptions import abort
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.auth import login_required
from flaskr.db import get_db

from datetime import date, datetime

from fpdf import FPDF



bp = Blueprint('dashboard', __name__)


@bp.route('/')
@login_required
def index():
    db = get_db()
    name = db.execute(
        'SELECT name FROM user WHERE id = ?', (g.user['id'], )
    ).fetchone()
    articles = get_articles()
    return render_template('dashboard/index.html', name=name, articles=articles)

@bp.route('/create', methods=["POST", "GET"])
@login_required
def create_plan():
    if request.method == "POST":
        plan_name = request.form['plan-name']
        month_value = float(request.form['slider-eur-month'])
        time = float(request.form['slider-time'])
        extra_deposit = float(request.form['slider-eur-deposit'])
        interest_rate = float(request.form['slider-percentage-interest'])
        result_value = calculate_result(month_value, time, extra_deposit, interest_rate)
        current_date = date.today().strftime('%Y-%m-%d')


        # print(g.user['id'], plan_name, month_value, time, extra_deposit, interest_rate, result_value, current_date)

        db = get_db()
        error = None

        if not plan_name:
            error = "Plan's name is required"

        users_plans = db.execute(
            'SELECT plans_name FROM savings_plan WHERE user_id = ?', (g.user['id'],)
        ).fetchall()
        for user_plan in users_plans:
            if dict(user_plan)['plans_name'] == plan_name:
                error = f"Plan '{plan_name}' already exists!"

        if error is None:
            db.execute(
                'INSERT INTO savings_plan (user_id, plans_name, monthly_amount, extra_deposit, time_of_saving, total_amount, created_at, interest_rate) VALUES(?, ?, ?, ?, ?, ?, ?, ?)', 
                (g.user['id'], plan_name, month_value, extra_deposit, time, result_value, current_date, interest_rate)
            )
            db.commit()
            return redirect(url_for("dashboard.my_plans"))
        
        flash(error)


    return render_template('dashboard/create.html')




@bp.route('/myplans', methods=['POST', 'GET'])
@login_required
def my_plans():
    db = get_db()
    if request.method == "POST":
        ## download plan 
        if request.is_json:
            create_pdf()

        action = request.form.get('action')  
        current_plan_name = request.form.get('plan-name')
        plan_id = request.form.get('plan-id')
        if not current_plan_name:
            error = f"Must enter plan's name!"
            flash(error)
            return redirect(url_for("dashboard.my_plans"))
        
        if action == "delete":
            try:
                plan = db.execute(
                    'SELECT * FROM savings_plan WHERE user_id = ? AND plans_name = ?', (g.user['id'], current_plan_name,)
                ).fetchone()
                if plan is None:
                    error = f"Plan '{current_plan_name}' doesn't exist!"
                    print(error)
                    flash(error)
                    return redirect(url_for("dashboard.my_plans"))
                else:
                    db.execute(
                        'DELETE FROM savings_plan WHERE user_id = ? AND id = ?', (g.user['id'], plan_id,)
                    )
                    db.commit()
            except db.IntegrityError:
                error = f"Plan '{current_plan_name}' already deleted!"
            else:
                return redirect(url_for("dashboard.my_plans"))
            flash(error)

        if action == "change":
            month_value = request.form['slider-eur-month']
            time = request.form['slider-time']
            extra_deposit = request.form['slider-eur-deposit']
            result_value = request.form['result-value'].replace(' €', '')
            current_date = date.today().strftime('%Y-%m-%d')
            interest_rate = float(request.form['slider-percentage-interest'])
            print(result_value)
           
            db.execute(
                    '''
                    UPDATE savings_plan 
                    SET plans_name = ?, monthly_amount = ?, extra_deposit = ?, time_of_saving = ?, total_amount = ?, created_at = ?, interest_rate = ?
                    WHERE user_id = ? AND id = ?
                    ''', (current_plan_name, month_value, extra_deposit, time, result_value, current_date, interest_rate, g.user['id'], plan_id) 
                ) 
            db.commit()
     
            return redirect(url_for("dashboard.my_plans"))
        

    plans = db.execute('SELECT * FROM savings_plan WHERE user_id = ?', (g.user['id'], )).fetchall()
    return render_template('dashboard/myplans.html', plans=plans)


@bp.route('/settings', methods=['POST', 'GET'])
@login_required
def settings():
    db = get_db()
    users = db.execute('SELECT * FROM user WHERE id = ?', (g.user['id'],)).fetchall()
    pw = db.execute('SELECT password FROM user WHERE id = ?', (g.user['id'],)).fetchone()

    if request.method == 'POST':
        messagess = {
            "firstname":[],
            "lastname": [],
            "email": [],
            "username": [],
            "password": [],
            "new_password": [],
            "new_password_check": [],
            "success": [],
        }
        if request.is_json:
            data = request.get_json()
            first_name = data['firstname']
            if not first_name:
                messagess["firstname"].append('Skap je hrdina!')

            last_name = data['lastname']
            if not last_name:
                messagess["lastname"].append('Last name is required!')

            email = data['email']
            if not email:
                messagess["email"].append('Pičo email skap!')

            if email and not re.match(email_validate_pattern, email):
                messagess["email"].append('This is not valid email address!')

            username = data['username']
            if not username:
                messagess["username"].append('Username name is required!')

            elif len(username) < 5:
                messagess["username"].append('Username must contain atleast 5 characters!')

            password = data['oldpassword']
            if not password:
                messagess["password"].append('You have to enter your password to change data!')
           
            if password and not check_password_hash(pw[0], password):
                messagess["password"].append('Old password is not matching!')


            if update_flag(messagess):
                db.execute(
                        '''
                        UPDATE user
                        SET name = ?, surname = ?, email = ?, username = ?
                        WHERE id = ?
                        ''', (first_name, last_name, email, username, g.user['id'],)
                    )
                db.commit()


                new_password = data['newpassword']
                new_password_check = data['newpasswordcheck']
                if new_password or new_password_check:
                    if not new_password or not new_password_check:
                        messagess["new_password_check"].append('Both new password fields must be filled out!')
                    elif new_password != new_password_check:
                        messagess["new_password_check"].append('New passwords do not match!')
                    elif not re.match(password_pattern, new_password):
                        messagess["new_password_check"].append('New password must meet the criteria!')
                    elif new_password == password or new_password_check == password:
                        messagess["new_password_check"].append('New password must be different than old password!')
                    else:
                        db.execute('''
                            UPDATE user
                            SET password = ?
                            WHERE id = ?
                        ''', (generate_password_hash(new_password), g.user['id']))
                        db.commit()

            if update_flag(messagess):      
                messagess["success"].append('Changed!')
                
            return jsonify({'messagess': messagess})

        else:
            return jsonify({'status': 'error'}), 400

    return render_template('dashboard/settings.html', users=users)


def update_flag(error_list):
    for value in error_list.values():
        if len(value) == 0:
            update = True
        else:
            update = False
            break
    return update


def create_pdf():
    data = request.get_json()
    plan_name = data['plan_name']
    total_amount = float(data['total_amount'])
    monthly_amount = float(data['monthly_amount'])
    interest_rate = float(data['interest_rate'])
    created_at = data['created_at']
    time_of_saving = float(data['time_of_saving'])
    extra_deposit = data['extra_deposit']
    print(plan_name, total_amount, monthly_amount, created_at, time_of_saving, extra_deposit)

    total_amount_data = []
    saved_data = []
    years = []
    for i in range(int(time_of_saving) + 1):
        total_amount_data.append(round(calculate_result(int(monthly_amount), i, int(extra_deposit), interest_rate), 2))
        years.append(i)
        if total_amount_data:
            saved_data.append(round(total_amount_data[i] - total_amount_data[i - 1], 2))


    table_df = {
        "Year": years,
        "Growth": saved_data,
        "Total Amount": total_amount_data
    }
    table_data = pd.DataFrame(table_df)

    data = [table_data.columns.tolist()] + table_data.values.tolist()


    df = pd.DataFrame({'Years': years, 'Total Amount Saved': total_amount_data})
    fig = px.line(df, x='Years', y='Total Amount Saved') 


    fig.update_traces(line=dict(color='#A3E635'), fill='tozeroy', fillcolor='#ECFCCB') 

    fig.update_layout(
    xaxis = dict(
        tickmode = 'linear',
        tick0 = 0,
        dtick = 1,
        showgrid=False
        ),
        plot_bgcolor='#F0F0F0'
    )
    fig.update_yaxes(tickformat=',.0f', tickprefix='€', showgrid=False, range=[extra_deposit, None])


    py.write_image(fig, 'chart.png')
    
    pdf_report = FPDF()

    pdf_report.add_page()
    pdf_report.set_font('Arial', 'B', 25)
    pdf_report.cell(80)
    pdf_report.cell(0, 10, plan_name)
    pdf_report.ln(20)

    pdf_report.set_font('Arial', '', 11)
    pdf_report.cell(0, 5, f'Monthly amount: {monthly_amount} eur')
    pdf_report.ln(6)
    pdf_report.cell(0, 5, f'Time Of Saving: {time_of_saving} years')
    pdf_report.ln(6)
    pdf_report.cell(0, 5, f'Extra Deposit: {extra_deposit} eur')
    pdf_report.ln(8)
    pdf_report.cell(0, 5, f'Interest: {interest_rate}%')
    pdf_report.ln(8)
    pdf_report.set_font('Arial', 'B', 11)
    pdf_report.cell(0, 5, f'Totaly Saved: {total_amount} eur')
    pdf_report.ln(10)

    pdf_report.set_font('Arial', '', 11)

    for header in data[0]:
        pdf_report.cell(40, 10, str(header), 1)
    pdf_report.ln()

    pdf_report.set_font('Arial', '', 12)
    for row in data[1:]:
        for item in row:
            pdf_report.cell(40, 10, str(item), 1)
        pdf_report.ln()
            

    pdf_report.image('chart.png', x=None, y=None, w=pdf_report.w - 20, h=0)
    pdf_report.output('reports/report.pdf', 'F')



def calculate_result(month_value, time, extra_deposit, interest):
    per_annual_interest_rate = interest / 100 + 1
    monthly_interest_rate = pow(per_annual_interest_rate, 1/12) - 1
    months = float(time * 12)

    future_month_value = month_value * ((pow(1 + monthly_interest_rate, months) - 1) / monthly_interest_rate) * (1 + monthly_interest_rate)

    future_value_extra_deposit = extra_deposit * pow(1 + monthly_interest_rate, months)

    total_future_value = future_month_value + future_value_extra_deposit

    return round(total_future_value, 2)

@bp.route('/remove-file')
def remove_file():
    path = 'C:/Users/danie/Desktop/finalproject/reports/report.pdf'
    if os.path.exists(path):
        os.remove(path)
    return "File removed", 200

@bp.route('/download')
def download():
    path = 'C:/Users/danie/Desktop/finalproject/reports/report.pdf'
    return send_file(path, as_attachment=True)


def get_articles():
    topic = ['technology', 'finance']

    url = f"https://newsapi.org/v2/everything?q={random.choice(topic)}&language=en&apiKey={news_api_key}"

    response = requests.get(url)
    if response.status_code == 200:
        results = response.json()

        articles = []

        articles.extend(random.choices(results['articles'], k=3))

        return articles
