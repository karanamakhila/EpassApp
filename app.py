import requests
from flask import Flask, render_template, request
from twilio.rest import Client
import requests_cache
account_sid = "ACd9ac5b46d541f9ae1c48142b2defe14d"
auth_token = "9c5088ae16bdde3723430604a902f300"
client = Client(account_sid, auth_token)
app = Flask(__name__,template_folder='template')
@app.route('/')
def registration_form():
    return render_template('test_page.html')
@app.route('/login_page', methods=['POST','GET'])
def login_reg_details():
    first_name = request.form['fname']
    last_name = request.form['lname']
    email_id = request.form['email']
    source_st = request.form['source-state']
    source_dt = request.form['source-dt']
    dest_st = request.form['dest-st']
    dest_dt = request.form['dest-dt']
    pno = request.form['pno']
    date = request.form['trip']
    full_name = first_name+" "+last_name
    r = requests.get('https://api.covid19india.org/v4/data.json')
    json_data = r.json()
    cnt = json_data[dest_st]['districts'][dest_dt]['total']['confirmed']
    pop = json_data[dest_st]['districts'][dest_dt]['meta']['population']
    print(cnt)
    print(pop)
    travel_pass = ((cnt/pop)*100)
    if(travel_pass<= 30) and request.method == 'POST':
        status = 'CONFIRMED'
        message=client.messages.create(from_='whatsapp:+14155238886',
                               body='Hello '+full_name+' '+'Your Travel From '+' '+source_dt+' To '+dest_dt+' is '+ status+' '+' '+date+',',
                               to='whatsapp:+917386196723')
        return render_template('user_registration_dtls.html', var=full_name , var1=email_id,
                                var3=source_st,var4=source_dt,var5=dest_st,var6=dest_dt,
                               var7=pno,var8=date,var9=status) #var2=id_proof,
    else:
        status='Not Confirmed'
        message=client.messages.create(from_='whatsapp:+14155238886',
                               body='Hello '+ full_name +' ' +'Your',
                               to='whatsapp:+917386196723')
        return render_template('user_registration_dtls.html', var=full_name, var1=email_id,
                                var3=source_st, var4=source_dt, var5=dest_st, var6=dest_dt,
                               var7=pno, var8=date, var9=status,) #var2=id_proof,
if __name__ == '__main__':
    app.run(debug=True,port=5000,host="localhost")