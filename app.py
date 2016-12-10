import web
import json
from data import data
from web import form
db = web.database(dbn='mysql', db='mydb', user='root',pw='1234')
render = web.template.render('views/', base='base')

urls=(
    '/','index',
    '/mostrar(.*)','mostrar',
    '/buscar(.*)','buscar',
    '/login','login',
    '/principal','principal',
    '/agregar','agregar',
    '/editar/(.+)','editar',
    '/eliminar/(.+)','eliminar',
    '/ver/(.+)','ver'
)
data = data()
data.read()
myFormBuscar = form.Form(
    form.Dropdown('Periodo',data.getPeriodo()),
    form.Dropdown('Entidad',data.getEntidad())
)
myFormLogin= form.Form(
    form.Textbox('Usuario'),
    form.Password('Contrasenia')
)
myFormProductos = form.Form(
    form.Textbox('Nombre'),
    form.Textbox('Cantidad'),
    form.Textbox('Marca'),
    form.Textarea('Precio')
)
class login:
    def GET(self):
        form = myFormLogin()
        return render.login(form)
    def POST(self):
        form = myFormLogin()
        if not form.validates():
            return render.login(form)
        else:
            result = db.select('usuarios')
            dbUser= ""
            dbPassw=""
            for row in result:
                dbUser=row.user
                dbPassw=row.passw
            if dbUser==form.d.Usuario and dbPassw==form.d.Contrasenia:
                raise web.seeother("/principal")
            else:
                return "Usuario Inconrrecto"
class principal:
    def GET(self):
        result= db.select('productos')
        return render.principal(result)

    def POST(self):
        raise web.seeother("/agregar")
class agregar:
    def GET(self):
        form= myFormProductos()
        return render.agregar(form)
    def POST(self):
        form = myFormProductos()
        if not form.validates():
            return render.agregar(form)
        else:
            db.insert('productos',
            Nombre = form.d.Nombre,
            Cantidad = form.d.Cantidad,
            Marca = form.d.Marca,
            Precio = form.d.Precio)
            raise web.seeother("/principal")

class buscar:
    def GET(self,results):
        form = myFormBuscar
        return render.buscar(form, None)
    def POST(self,results):
        form = myFormBuscar
        if not form.validates():
            return render.buscar(form)
        else:
            user_data = web.input()
            periodo = user_data.Periodo
            entidad = user_data.Entidad
            results = data.getDatos(periodo, entidad)
            return render.buscar(form,results)
class editar:
    def GET(self,id):
        form = myFormProductos()
        result = db.select('productos', where = "id=%s" % (id))

        for row in result:
            form['Nombre'].value= row.Nombre
            form['Cantidad'].value = row.Cantidad
            form['Marca'].value = row.Marca
            form['Precio'].value = row.Precio
        return render.editar(form)
    def POST(self,id):
        form = myFormProductos()
        if not form.validates():
            return render.editar(form)
        else:
            db.update('productos',where="id=%s" %(id),
            Nombre = form.d.Nombre,
            Cantidad = form.d.Cantidad,
            Marca = form.d.Marca,
            Precio = form.d.Precio
            )
            raise web.seeother("/principal")
class eliminar:
    def GET(self,id):
        form = myFormProductos()
        result = db.select('productos', where="id=%s" %(id))
        for row in result:
            form['Nombre'].value = row.Nombre
            form['Cantidad'].value = row.Cantidad
            form['Marca'].value = row.Marca
            form['Precio'].value = row.Precio
        return render.eliminar(form)

    def POST(self,id):
        form = myFormProductos()
        if not form.validates():
            return render.eliminar(form)
        else:
            db.delete('productos', where = "id=%s" % (id))
            raise web.seeother("/principal")
class ver:
    def GET(self, id):
        result = db.select('productos', where = "id=%s" % (id))
        return render.ver(result)



class mostrar:
    def GET(self,data):
        data = []
        with open('data/data.json','r') as dat:
            data=json.load(dat)
        return render.mostrar(data['results'])
class index:
    def GET(self):
        return render.index()

if __name__=="__main__":
    app=web.application(urls,globals())
    web.config.debug=True
    app.run()