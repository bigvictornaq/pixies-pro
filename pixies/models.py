import statistics
from fpdf import FPDF
from itsdangerous import TimedJSONWebSignatureSerializer as seralizer
from pixies import db,login_manager,app
from sqlalchemy import text
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model,UserMixin):
    #__bind_key__ = 'anali'
    id = db.Column(db.Integer,primary_key=True)
    username= db.Column(db.String(20),unique=True,nullable=False)
    email= db.Column(db.String(120),unique=True,nullable=False)
    image_file = db.Column(db.String(150),nullable=False,default='https://res.cloudinary.com/pixies/image/upload/v1602729197/project/df_xbqa96.jpg')
    public_id = db.Column(db.String(120),default='project/df_xbqa96')
    password = db.Column(db.String(60),nullable=False)
    
    def get_reset_token(self,expires_sec=1800):
        s = seralizer(app.config['SECRET_KEY'],expires_sec)
        return s.dumps({'user_id':self.id}).decode('utf-8')
        
    @staticmethod
    def verify_reset_token(token):
         s = seralizer(app.config['SECRET_KEY'])
         try:
             user_id = s.loads(token)['user_id']
         except:
            return None
         return User.query.get(user_id)   


    def __repr__(self):
        return f"User( '{self.username}','{self.email}','{self.image_file}')"

class analizis(db.Model):
    __tablename__ = 'analisis'
    id_analisis = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50),nullable=False)
    email  = db.Column(db.String(50),nullable=False)
    address = db.Column(db.String(50),nullable=False)
    zip = db.Column(db.String(50),nullable=False)
    phone = db.Column(db.String(50),nullable=False)
    ciudad =db.Column(db.String(50),nullable=False)
    pais   =db.Column(db.String(50),nullable=False)
    def __init__(self, name, email, address,zip,phone,ciudad,pais):
        self.name = name
        self.email = email
        self.address = address
        self.zips = zip
        self.phone = phone
        self.ciudad = ciudad
        self.pais = pais
    def __repr__(self):
        return '<id_analisis{}>'.format(self.id_analisis)

#contiene los datos solamente de los clientes
def bd_dvrental():
    try:
        queri = text("with t1 as (Select *, first_name || ' ' || last_name AS full_name from customer) select full_name as Name, email as Email, address as Address,postal_code as zip, phone as Phone, city as Ciudad, country as Pais from t1  Join address  using (address_id)    join city   using (city_id) join country using (country_id)  join payment  using(customer_id)  group by 1,2,3,4,5,6,7")
        data_todo = db.get_engine().execute(queri)
        return data_todo
    except IndentationError:
        db.session.rollback()
        return None


#se aagrupan los datos por pais
def groupByPais():
    querie = text("SELECT pais, COUNT('ID_Cliente') as cliente FROM public.analisis GROUP BY pais ORDER BY cliente DESC;")
    
    data_USA2 = db.get_engine().execute(querie)
    #anali
    if data_USA2:
        datos = [{"Pais":a[0],"NumeroClientes":a[1]} for a in data_USA2]
        return datos
    else:
        no_data = [{"Pais":"NO HAY DATOS","NumeroClientes":"NO HAY DATOS"}]
        return no_data


#se calcula estadistica de media,moda y mediana
def calcularThreeM():
    querie = text("SELECT pais, COUNT('ID_Cliente') as cliente FROM public.analisis GROUP BY pais ORDER BY cliente DESC;")
    data = db.get_engine().execute(querie)

    
    sumisa = []
    for t in data:
        sumisa.append(t[1])
    if not sumisa:
      #  definitive_master()
        return next(calcularThreeM())

    sd = statistics.mean(sumisa)
    mean = round(sd,2)
    print("Media del: " , mean)
    mediana = statistics.median(sumisa)
    print("Mediana: ",mediana)
    modas = statistics.mode(sumisa)
    print("Moda",modas)
    estadistica = [mean,mediana,modas]
    return estadistica
          

#se aagrupan los datos por pais por comando
def group_low():
    querie = text("SELECT pais, COUNT(pais) as clientes FROM public.analisis GROUP BY pais  having count(pais) < 175 ORDER BY clientes DESC;")
    datos_byP = db.get_engine().execute(querie)
    return datos_byP
def groupgre():
    querie = text("SELECT pais, COUNT(pais) as clientes FROM public.analisis GROUP BY pais  having count(pais) > 175  ORDER BY clientes DESC;")
    datos_byP = db.get_engine().execute(querie)
    return datos_byP
def groupmoda():
    querie = text("SELECT pais, COUNT(pais) as clientes FROM public.analisis GROUP BY pais having count(pais) = 1 ORDER BY clientes DESC;")
    datos_byP = db.get_engine().execute(querie)
    return datos_byP
#metodo para obtner los datos
def datos_agrupados_porPais(grupo):
    switch = {
        1: groupgre,
        2: group_low,
        3: groupmoda
    }
    func = switch.get(grupo,"Nelseon")
    return func()                       

#Uso de dataframes con pandas
def create_dataframe_an():
    engine_an = db.get_engine()
    datafm = pd.read_sql_table('analisis',con=engine_an)
    return datafm

   #DATOS PARA EL MAPA DE LA DORA EXXPLORRADORA
def dataforMap():
    querie = text("SELECT pais, COUNT('ID_Cliente') as cliente FROM public.analisis GROUP BY pais ORDER BY cliente DESC;")
    data = db.get_engine().execute(querie)
    resultado = [{sa[0]:sa[1]} for sa in data]
    return resultado

#datos del mapa
def dataMap():
    querie = text("SELECT pais, COUNT('ID_Cliente') as cliente FROM public.analisis GROUP BY pais ORDER BY cliente DESC;")
    data = db.get_engine().execute(querie)
    resultado = [{"Pais":sa[0],"NumeroClientes":sa[1]} for sa in data]
    return resultado

#Vamos a crear Datos 
def insert_Alld():
    q = text("COPY public.klyients( nombre, email, address, zips, phone, ciudad, country) FROM 'D:\Development\Python\Catweb\msnas.csv' DELIMITER ',' CSV HEADER;commit;")
    doll = db.get_engine().execute(q)

def firstTendatos():
    query = text("SELECT country, COUNT('ID_Cliente') as cliente FROM public.klyients GROUP BY country ORDER BY cliente DESC FETCH FIRST 10 ROWS ONLY;")
    paisbyCl = db.get_engine().execute(query)
    return paisbyCl


#Creacion del template PDF
class PDF(FPDF):
    #Encabezado del pdf
    def header(self):
        # Logo
        self.image('pixies_web\static\profile_img\lgogo.png', 165, 8, 33)
        # Arial bold 15
        self.set_font('Arial', 'B', 25)
        # Se mueve a la derecha
        self.cell(80)
        # Titulo
        self.cell(30, 49, 'Reporte de Analisis de datos', 0, 0, 'C')
        # Line break
        self.ln(20)

    def chapter_body(self,estadistica,date,user,email,num_clients):
        self.ln(10)
        # Times 12
        self.set_font('Times', '', 12)
        self.cell(0,8,"Nombre del Proyecto: Generacion de PDF template con informacion con base de datos",1,1)
        self.set_font('Times', '', 12)
        self.cell(0,8,"Nombre de Reporte: ",1,1)
        self.set_font('Times', '', 12)
        self.cell(150,-8,f"Fecha: {date}",0,0,"R")
        self.ln(2)
        self.set_font('Times', '', 12)
        self.cell(0,8,f"{user}",0,0)
        # Linea horizontal
        self.line(10,68,200,68)
        
        self.ln(8)
        self.set_font('Times', 'I', 12)
        self.cell(0,8,"Nombre Usario quien realizo la consulta",0,0)
        self.ln(10)
        self.set_font('Times', '', 12)
        self.cell(0,8,f"{email}",0,0)
        # Linea horizontal
        self.line(10,85,200,85)
        self.ln(8)
        self.set_font('Times', 'I', 12)
        self.cell(0,8,"Correo Electronico del Usario ",0,0)
        self.ln(8)
        self.set_font('Times','B',14)
        self.cell(78,50,"Proposito De la Investigacion datos",1,2)
        self.set_xy(88,92)
        self.set_font('Times', '', 12)
        texto = '''
 Nosotros previamente seleccionamos las tablas de cliente
 de ambas bases datos, con el objetivo buscar una
 estrategia para las diferentes áreas,en donde no tenga un
 gran impacto,por ejemplo,como los países con menos
 clientes de 20 o menos. Además de buscar un patrón en
 esos países no compiten con los países con mayores
 clientes. Dar unasoluciónpara fortalecer las áreas con
 menores clientes.
        '''
        self.multi_cell(112,5,texto,1,2,"L")
        self.ln()
        self.set_font('Times','B',14)
        self.cell(0,8,"Fase 2 Preprocesamiento",0,0)
        self.ln()
        self.set_font('Times','',12) 
        self.cell(0,8,"Conceptos",0,0)
        self.ln(-1)
        text2 = '''
Para poder comenzar a trabajar en la segunda fase se investigó sobre la media, mediana y moda, las cuales son la herramientanecesaria para poder observar que parte es en la que más me conviene trabajar
        '''
        self.set_font('Times','',12) 
        self.multi_cell(0,5,text2,0,0)
        self.ln()
        self.set_font('Times','',12)
        self.cell(0,8,f"Mediana: {estadistica[1]}",0,0)
        self.ln()
        self.set_font('Times','',12)
        self.cell(0,8,f"Media: {estadistica[0]}",0,0)
        self.ln()
        self.set_font('Times','',12)
        self.cell(0,8,f"Moda: {estadistica[2]}",0,0)
        self.ln(17)
        self.ln(5)
        #tratar de hacer una tabla
        self.set_font('Times','',12)
        th = self.font_size
        num=0
        for row in num_clients:
            num = num + 8
            self.set_xy(120,170 + num)
            for dats in row:              
                self.cell(40,8,str(dats),1)
            self.ln()    
        #alternative
        self.ln(-5)    
    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')
    def print_chapter(self,estadistica,date,user,email,num_clients):
        self.add_page()
        self.chapter_body(estadistica,date,user,email,num_clients)
