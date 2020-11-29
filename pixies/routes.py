import os
import datetime
from flask import render_template, url_for,flash,redirect,request,json,jsonify,make_response
from pixies import app,db,bcrypt,Cloud,mail
from pixies.forms import RegistrationForm,LoginForm,UpdateCuentaForm,RequestResetForm,ResetPasswordForm
from pixies.models import User,analizis,calcularThreeM,datos_agrupados_porPais,firstTendatos,dataforMap,dataMap,PDF,groupByPais
from flask_login import login_user,current_user,logout_user,login_required
from flask_mail import Message



@app.route('/',methods=['GET','POST'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('analisis'))
    form = LoginForm()
    if form.validate_on_submit():
        usuarios = User.query.filter_by(email=form.email.data).first()
        if usuarios and bcrypt.check_password_hash(usuarios.password,form.password.data):
            login_user(usuarios,remember=form.remember.data)
            return redirect(url_for('analisis'))
        else:  
            flash('Esta meco mijo esa no es carnal!! checa',category='error')    
    return render_template('home.html',form=form)

@app.route('/Registarte',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('analisis'))
    form = RegistrationForm()
    if form.validate_on_submit():
        checkar = User.query.count()
        if checkar < 10:
                has_contrasena = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
                usuario = User(username=form.username.data, email=form.email.data,password=has_contrasena)
                db.session.add(usuario)
                db.session.commit()
                flash('Tu cuenta fue creada exitosamente, ya es posible iniciar sesion', category='success')
                return redirect(url_for('index'))
    return render_template('registerF.html',form=form)



def save_foto(form_picture):
    subir = Cloud.uploader.upload(form_picture,folder='project/',use_filename = True)
    ubicacion = subir.get('secure_url')
    identicacion = (subir.get('public_id'))
    #form_picture.save(subir.get('secure_url'))
    #form_id.save(subir.get('public_id'))
    return ubicacion,identicacion


@app.route('/informacion_usuario',methods=['GET','POST'])
@login_required
def usuario():
    form= UpdateCuentaForm()
    form.public_id.data = current_user.public_id
    
    if form.validate_on_submit():
        if form.foto.data:
           
            ubicacion,identificacion = save_foto(form.foto.data)
            current_user.image_file = ubicacion
            current_user.public_id = identificacion
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Tu cuenta fue actualizada exitosamente','success')
        redirect(url_for('usuario'))
    elif request.method == 'GET':
        form.username.data =  current_user.username
        form.email.data = current_user.email

    #image_file = url_for('static',filename='profile_img/'+ current_user.image_file)
    image_file = current_user.image_file
    return render_template('user_info.html',
                           image_file = image_file,form=form)

@app.route('/logout')
def salir_sesion():
    logout_user()
    return redirect(url_for('index'))

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                    sender='victor.sistemasnav@gmail.com',
                    recipients=[user.email])
    msg.body=f'''Porfavor borra la password, para ello visita la pagina:
{url_for('reset_token',token=token , _external=True)}

Si no lo solicitastes porfavor ignore esto carnal!!
    '''
    mail.send(msg)               

@app.route('/reset_password',methods=['GET','POST'])
def reset_password():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An Email Has been sent with instructions to reset your password, check spam folder', category='alert')
        return redirect(url_for('index'))
    return render_template('reset_request.html',form=form)

@app.route('/reset_password/<token>',methods=['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('that is invalid or expired token','warning')
        return redirect(url_for('reset_password'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        has_contrasena = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = has_contrasena
        db.session.commit()
        flash('Tu password fue actualizada, ya es posible iniciar sesion', category='success')
        return redirect(url_for('index'))
    return render_template('reset_token.html',form=form) 

#ruta para la pagina donde muestra los datos importantes
@app.route('/analis_tablas_mssql_and_posgresql',methods=['GET','POST'])
@login_required   
def analisis():
    return render_template("an_tables.html", estadi =  calcularThreeM(),grupo_mayor=datos_agrupados_porPais(1),
                                    grupo_menor=datos_agrupados_porPais(2),grupo_moda=datos_agrupados_porPais(3))


#Ruta donde muestra los datos de ambas base  de datos
@app.route('/json/en_mi_casa')
def showdd():
    db = analizis.query.all()
    if db:
        datos = [{"ID":a.id_analisis,"firstName":a.name,"email":a.email,"address":a.address,"zip":a.zip,"phone":a.phone,"ciudad":a.ciudad,"country":a.pais} for a in db]
        return jsonify({"data":datos})
    else:
        datos = [{"ID":"no hay datos","firstName":"no hay datos","email":"no hay datos","address":"no hay datos","zip":"no hay datos","phone":"no hay datos","ciudad":"no hay datos","country":"no hay datos"}]
        return jsonify({"data":datos})

#son los datos agrupaso en json
@app.route('/paisAgrupado')
def paisG():
    datito = groupByPais()
    return jsonify({"data":datito})

@app.route('/downlods')
def pdfDownload():
    #Fechas
    fecha = datetime.datetime.now()
    fechita = str(fecha.day) + '/'+ fecha.strftime("%A")+'/'+str(fecha.year)
    #datos del usarios
    usernombre = current_user.username
    emailus = current_user.email
    #datos de los paises
    numClients =  firstTendatos()
     #datos
    estadi =  calcularThreeM()

    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.print_chapter(estadi,fechita,usernombre,emailus,numClients)
    response = make_response(pdf.output(dest='S').encode('latin-1'))
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=output.pdf'
    return response


   #####Datos para suministarr la Mapita de la dora exploradora

#son los datos sin nombre variable en json en forma [{}]
@app.route('/pasitas')
def pmapa():
    da =dataforMap()
    return jsonify(da) 

#son los datos con nombre variable en json en forma [{}]
@app.route('/pasitas/mapi')
def mapita():
    das =dataMap()
    return jsonify(das)

#son los datos todos los paises del munod en codigo EU como ejemplo
@app.route('/codex')
def codeguito():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT,'static/data','names.json')
    dato = json.load(open(json_url))
    return dato

@app.route('/ncodes')
def codegui():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT,'static/data','reeves.json')
    dato = json.load(open(json_url))
    return jsonify(dato)

@app.route('/continents')
def continentss():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT,'static/data','continent.json')
    dato = json.load(open(json_url))
    return jsonify(dato)
#33333333333333333333333333333333333333333333333333333333333333 


